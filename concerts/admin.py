from django.contrib import admin

# Register your models here.

from .models import Concert, ConcertRole, ConcertProgram, ConcertAudio
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


class ConcertAudioInline(admin.TabularInline):
    model = ConcertAudio
    extra = 0


@admin.register(ConcertAudio)
class ConcertProgramAdmin(admin.ModelAdmin):
    list_display = ["get_concert_date", "get_program_order"]

    def get_concert_date(self, obj):
        return obj.porgram_entry.concert.date
    get_concert_date.short_description = "Concert Date"

    def get_program_order(self, obj):
        return obj.program_entry.program_order
    get_program_order.short_description = "Program Order"
