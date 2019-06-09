from django.contrib import admin

from authorization import models


admin.site.register(models.CustomUser)
