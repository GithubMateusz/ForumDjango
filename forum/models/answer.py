from django.db import models

from authorization.models import CustomUser
from .topic import Topic


class Answer(models.Model):
    STATUS_CHOICES = (
        ('active', 'active'),
        ('reported', 'reported'),
        ('hidden', 'hidden'),
        ('delete', 'delete')
    )
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        verbose_name='topic',
        related_name='answers'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='author'
    )
    body = models.TextField(
        null=False,
        verbose_name='text'
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )

    class Meta:
        verbose_name = 'answer'
        verbose_name_plural = 'answers'

    def __str__(self):
        return str(self.topic)

    def save(self, **kwargs):
        super().save(**kwargs)
        self.topic.update_latest_answer()

    def delete(self):
        super().delete()
        self.topic.update_latest_answer()

