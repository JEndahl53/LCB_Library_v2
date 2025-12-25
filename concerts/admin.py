from django.contrib import admin

# Register your models here.

from .models import Concert, ConcertRole
from people.models import PersonRoleType


class ConcertRoleInline(admin.TabularInline):
    model = ConcertRole
    extra = 1
#    autocomplete_fields = ['person']
    ordering = ["display_order"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "role_type":
            kwargs["queryset"] = PersonRoleType.objects.filter(is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Concert)
class ConcertAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'venue')
    search_fields = ('title', )
    list_filter = ('venue', 'date')

    inlines = [ConcertRoleInline]
