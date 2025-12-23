from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Person)
admin.site.register(models.ConcertRoleType)
# admin.site.register(models.ConcertRole)
