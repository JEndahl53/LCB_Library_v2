from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name', 'display_name']


admin.site.register(models.PersonRoleType)
