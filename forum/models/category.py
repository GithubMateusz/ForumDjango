from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from authorization.models import CustomUser


class Category(MPTTModel):

    parent = TreeForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='',
        related_name='children'
    )
    name = models.CharField(
        max_length=150,
        verbose_name='category'
    )
    slug = models.SlugField(
        max_length=150
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='author'
    )
    description = models.CharField(
        max_length=250,
        verbose_name='description'
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        unique_together = ('parent', 'slug')

    def __unicode__(self):
        return '%s%s' % ('--' * self.level, self.name)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'category', args=(self.parent.slug, self.slug,))

    def validate_unique(self, exclude=None):
        if Category.objects.exclude(id=self.id)\
                .filter(parent__isnull=True, slug=self.slug).exists():
            raise ValidationError('The category with this slug is exit.')
        super().validate_unique(exclude)

    def count_topics(self):
        return self.topics.count()

    def count_answers(self):
        answers = 0
        for topic in self.topics.all():
            answers = answers + topic.count_answers()
        return answers
