from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Max
from django.urls import reverse

from authorization.models import CustomUser


class CategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('position', 'name')


class Category(models.Model):
    objects = CategoryManager()
    parent = models.ForeignKey('self',
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True,
                               verbose_name='kategoria główna',
                               related_name='children'
                               )
    name = models.CharField(max_length=150,
                            verbose_name='kategoria')
    slug = models.SlugField(max_length=150)
    author = models.ForeignKey(CustomUser,
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True,
                               verbose_name='autor')
    description = models.CharField(max_length=250,
                                   verbose_name='opis')
    position = models.IntegerField(null=True,
                                   blank=True,
                                   default=0,
                                   verbose_name='pozycja')
    _level = 0
    _original_position = None
    _original_parent = None

    class Meta:
        verbose_name = 'kategoria'
        verbose_name_plural = 'kategorie'
        unique_together = ('parent', 'slug')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_parent = self.parent
        self._original_position = self.position

    def __str__(self):
        return self.name

    def __unicode__(self):
        self.get_level(self)
        return '%s%s' % ('--' * self._level, self.name)

    def validate_unique(self, exclude=None):
        if Category.objects.exclude(id=self.id) \
                .filter(parent__isnull=True, slug=self.slug).exists():
            raise ValidationError('Kategoria z takim slugiem już istnieje.')
        super().validate_unique(exclude)

    def save(self, *args, **kwargs):
        try:
            if not self.pk:
                self.new_position()
            elif self.parent != self._original_parent:
                self.new_position()
                self.change_position_objects_in_old_category()
        except TypeError:
            self.position = 1
        finally:
            self._original_parent = self.parent
            self._original_position = self.position
        super().save(*args, **kwargs)

    def delete(self):
        self.change_position_objects_in_old_category()
        super().delete()

    def new_position(self):
        object_with_max_position = Category.objects. \
            filter(parent=self.parent).aggregate(Max('position'))
        self.position = object_with_max_position['position__max'] + 1

    def change_position_objects_in_old_category(self):
        if self._original_parent:
            objects_from_the_old_category = Category.objects.filter(
                parent=self._original_parent,
                position__gte=self._original_position)
        else:
            objects_from_the_old_category = Category.objects.filter(
                parent__is_null=True,
                position__gte=self._original_position)

        for object_old_category in objects_from_the_old_category:
            object_old_category.position = object_old_category.position - 1
            object_old_category.save()

    def get_level(self, category):
        if category.parent:
            self._level = self._level + 1
            self.get_level(category.parent)
        else:
            return self._level

    def get_absolute_url(self):
        return reverse('category',
                       args=(self.parent.slug,
                             self.slug,))

    def count_topics(self):
        return self.topics.count()

    def count_answers(self):
        answers = 0
        for topic in self.topics.all():
            answers = answers + topic.count_answers()
        return answers
