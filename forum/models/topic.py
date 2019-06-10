
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from authorization.models import CustomUser
from .category import Category


class Topic(models.Model):
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
                                 related_name='topic')
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
    updated = models.DateTimeField(auto_now=True)
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

