from django.db import models

from authorization.models import CustomUser
from .topic import Topic


class Reply(models.Model):
    STATUS_CHOICES = (
        ('active', 'aktywny'),
        ('reported', 'zgłoszony'),
        ('hidden', 'ukryty'),
        ('delete', 'usunięty'),
    )
    topic = models.ForeignKey(Topic,
                              on_delete=models.CASCADE,
                              verbose_name='temat',
                              related_name='reply'
                              )
    author = models.ForeignKey(CustomUser,
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True,
                               verbose_name='autor')
    body = models.TextField(verbose_name='tekst',
                            null=False)
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='utworzony')
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='active')

    class Meta:
        verbose_name = 'odpowiedź'
        verbose_name_plural = 'odpowiedzi'

    def __str__(self):
        return str(self.topic)




