from django.contrib import admin

# Register your models here.

from .models import Concert, ConcertRole
from people.models import ConcertRoleType


class ConcertRoleInline(admin.TabularInline):
    model = ConcertRole
    extra = 1
#    autocomplete_fields = ['person']
    ordering = ["display_order"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "role_type":
            kwargs["queryset"] = ConcertRoleType.objects.filter(is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# todo edit these lines once we have the venues back into the project. Other fields require tuples
@admin.register(Concert)
class ConcertAdmin(admin.ModelAdmin):
#    list_display = ('title', 'date', 'venue')
    list_display = ('title', 'date', )
    search_fields = ('title', )
#    list_filter = ('venue', 'date')
    list_filter = ('date', )

    inlines = [ConcertRoleInline]