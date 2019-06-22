from django.contrib import admin
from django.utils.html import format_html
from mptt.admin import DraggableMPTTAdmin

from .forms import AdminTopicForm
from . import models


class CategoryAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 30
    list_display = ('tree_actions', 'indent_level_category', 'slug', 'description')
    list_display_links = ('indent_level_category',)
    prepopulated_fields = {'slug': ('name',)}

    def indent_level_category(self, instance):
        return format_html(
            '<div style="text-indent:{}px">{}</div>',
            instance._mpttfield('level') * self.mptt_level_indent,
            instance.name,
        )

    indent_level_category.short_description = 'category'


class AnswerInLine(admin.TabularInline):
    model = models.Answer
    verbose_name = 'text'
    verbose_name_plural = 'text'
    max_num = 1
    can_delete = False
    null = False


class TopicAdmin(admin.ModelAdmin):
    form = AdminTopicForm
    inlines = [
        AnswerInLine,
    ]
    list_display = ('name', 'category',  'slug',
                    'author', 'created', 'status')
    list_filter = ('created', 'author')
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'created'
    ordering = ('status', 'created')


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('topic', 'body', 'author', 'created', 'status')
    list_filter = ('created', 'author')
    raw_id_fields = ('author',)
    date_hierarchy = 'created'
    ordering = ('status', 'created')


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Topic, TopicAdmin)
admin.site.register(models.Answer, AnswerAdmin)
