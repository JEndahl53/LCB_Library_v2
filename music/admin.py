# music/admin.py
from django.contrib import admin
from .models import Music, MusicRole
from people.models import PersonRoleType


# Register your models here.


class MusicRoleInline(admin.TabularInline):
    model = MusicRole
    extra = 1
    autocomplete_fields = ['person']
    ordering = ['display_order']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'role_type':
            kwargs['queryset'] = PersonRoleType.objects.filter(is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ('title', )
    search_fields = ('title', )
    inlines = [MusicRoleInline]
