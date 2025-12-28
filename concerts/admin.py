from django.contrib import admin

# Register your models here.

from .models import Concert, ConcertRole, ConcertProgram
from people.models import PersonRoleType


class ConcertProgramInline(admin.TabularInline):
    model = ConcertProgram
    extra = 0
    ordering = ["program_order"]
    autocomplete_fields = ["music"]


class ConcertRoleInline(admin.TabularInline):
    model = ConcertRole
    extra = 1
#    autocomplete_fields = ['person']
    ordering = ["display_order"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "role_type":
            kwargs['queryset'] = PersonRoleType.objects.filter(
                is_active=True,
                scope__in=[
                    PersonRoleType.RoleScope.CONCERT,
                    PersonRoleType.RoleScope.BOTH,
                ],
            ).order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Concert)
class ConcertAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'venue')
    search_fields = ('title', )
    list_filter = ('venue', 'date')
    ordering = ('-date',)

    inlines = [ConcertRoleInline, ConcertProgramInline]
