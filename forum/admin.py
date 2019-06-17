from django.contrib import admin, messages
from django.db.models import ObjectDoesNotExist

from . import models


class CategoryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/category_list.html'
    list_display = ('__unicode__', 'position', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['position']
    exclude = ('position',)
    actions = ['up_to', 'down_to']

    def up_to(self, request, queryset):
        for object_queryset in queryset.reverse():
            try:
                object_above = self.model.objects.get(
                    parent=object_queryset.parent,
                    position=object_queryset.position - 1)
                object_above.position = object_queryset.position
                object_above.save()
                object_queryset.position = object_queryset.position - 1
                object_queryset.save()

                self.message_user(
                    request,
                    "Pozycja kategorii {0} została zmieniona na {1}."
                    .format(object_queryset, object_queryset.position))
            except ObjectDoesNotExist:
                messages.error(
                    request,
                    'Nie można zmienić pozycji kategorii {0} na wyższą.'
                    .format(object_queryset))

    def down_to(self, request, queryset):
        for object_queryset in queryset:
            try:
                object_below = self.model.objects.get(
                    parent=object_queryset.parent,
                    position=object_queryset.position + 1)
                object_below.position = object_queryset.position
                object_below.save()
                object_queryset.position = object_queryset.position + 1
                object_queryset.save()

                self.message_user(
                    request,
                    "Pozycja kategorii {0} została zmieniona na {1}."
                    .format(object_queryset, object_queryset.position))
            except ObjectDoesNotExist:
                messages.error(
                    request,
                    'Nie można zmienić pozycji kategorii {0} na niższą.'
                    .format(object_queryset))

    up_to.short_description = "Przenieś wyżej"
    down_to.short_description = "Przenieś niżej"


class AnswerInLine(admin.TabularInline):
    model = models.Answer
    verbose_name = 'tekst'
    verbose_name_plural = 'tekst'
    max_num = 1
    can_delete = False
    null = False


class TopicAdmin(admin.ModelAdmin):
    inlines = [
        AnswerInLine,
    ]
    list_display = ('name', 'category',  'slug',
                    'author', 'created', 'status')
    list_filter = ('created', 'author')
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'created'
    ordering = ['status', 'created']


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('topic', 'body', 'author', 'created', 'status')
    list_filter = ('created', 'author')
    raw_id_fields = ('author',)
    date_hierarchy = 'created'
    ordering = ['status', 'created']


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Topic, TopicAdmin)
admin.site.register(models.Answer, AnswerAdmin)
