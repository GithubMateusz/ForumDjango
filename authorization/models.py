from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    GENDER_CHOICES = (
        ('men', 'mężczyzna'),
        ('women', 'kobieta'),
    )
    email = models.EmailField(unique=True)
    age = models.IntegerField(verbose_name='wiek', null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES,
                              verbose_name='płeć', null=True)
    avatar = models.ImageField(upload_to='user_avatar', width_field=120,
                               height_field=150, null=True)
    signature = models.CharField(max_length=250, verbose_name='podpis', null=True)

    def __str__(self):
        return self.username
