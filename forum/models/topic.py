
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from authorization.models import CustomUser
from .category import Category


class TopicManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-latest_answer_date')


class Topic(models.Model):
    objects = TopicManager
    STATUS_CHOICES = (
        ('active', 'aktywny'),
        ('blocked', 'zablokowany'),
        ('reported', 'zgłoszony'),
        ('hidden', 'ukryty'),
    )
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 verbose_name='kategoria',
                                 related_name='topics')
    name = models.CharField(max_length=150,
                            verbose_name='nazwa tematu',
                            null=False)
    slug = models.SlugField(max_length=150)
    author = models.ForeignKey(CustomUser,
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True,
                               verbose_name='autor')
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='utworzony')
    latest_answer_date = models.DateTimeField(null=True,
                                             blank=True)
    latest_answer_author = models.ForeignKey(CustomUser,
                                            on_delete=models.SET_NULL,
                                            null=True,
                                            blank=True,
                                            related_name='reply_author')

    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='active')

    class Meta:
        verbose_name = 'temat'
        verbose_name_plural = 'tematy'
        unique_together = (("category", "slug"),)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('topic',
                       args=(
                           self.category.parent.slug,
                           self.category.slug,
                           self.slug,
                       ))

    def count_answers(self):
        return self.answers.count() - 1

    def update_latest_answer(self):
        try:
            answer = self.answers.last()
            self.latest_answer_date = answer.created
            self.latest_answer_author = answer.author
            self.save()
        except IndexError:
            pass
