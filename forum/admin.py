from django.contrib import admin
from django.db.models import ObjectDoesNotExist

from . import models


class CategoryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/category_list.html'
    list_display = ('__unicode__', 'position', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['position']
    exclude = ('position',)

    def down_to(self, request, queryset):
        for object_queryset in queryset:
            try:
                object_below = self.model.objects.get(position=object_queryset.position + 1)
                object_below.position = object_queryset.position
                object_below.save()
            except ObjectDoesNotExist:
                pass
            finally:
                object_queryset.position = object_queryset.position + 1
                object_queryset.save()

    def up_to(self, request, queryset):
        for object_queryset in queryset.reverse():
            if object_queryset.position > 1:
                try:
                    object_below = self.model.objects.get(position=object_queryset.position - 1)
                    object_below.position = object_queryset.position
                    object_below.save()
                except ObjectDoesNotExist:
                    pass
                finally:
                    object_queryset.position = object_queryset.position - 1
                    object_queryset.save()
            else:
                pass


class ReplyInLine(admin.TabularInline):
    model = models.Reply
    verbose_name = 'tekst'
    verbose_name_plural = 'tekst'
    max_num = 1
    can_delete = False
    null = False


class TopicAdmin(admin.ModelAdmin):
    inlines = [
        ReplyInLine,
    ]
    list_display = ('name', 'category',  'slug',
                    'author', 'created', 'status')
    list_filter = ('created', 'author')
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'created'
    ordering = ['status', 'created']


class ReplyAdmin(admin.ModelAdmin):
    list_display = ('topic', 'body', 'author', 'created', 'status')
    list_filter = ('created', 'author')
    raw_id_fields = ('author',)
    date_hierarchy = 'created'
    ordering = ['status', 'created']


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Topic, TopicAdmin)
admin.site.register(models.Reply, ReplyAdmin)
