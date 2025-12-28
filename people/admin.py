from django.contrib import admin
from . import models


class ConcertRoleFilter(admin.SimpleListFilter):
    title = 'Concert role'
    parameter_name = 'concert_role'

    def lookups(self, request, model_admin):
        from people.models import PersonRoleType
        qs = PersonRoleType.objects.filter(
                is_active=True,
                scope__in=["concert", "both"]
            ).order_by('name')
        return [(rt.pk, rt.name) for rt in qs]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
                concert_roles__role_type_id=self.value()
            ).distinct()
        return queryset


class MusicRoleFilter(admin.SimpleListFilter):
    title = 'Music role'
    parameter_name = 'music_role'

    def lookups(self, request, model_admin):
        from people.models import PersonRoleType
        qs = PersonRoleType.objects.filter(
                is_active=True,
                scope__in=["music", "both"]
            ).order_by('name')

        return [(rt.pk, rt.name) for rt in qs]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
                music_roles__role_type_id=self.value()
            ).distinct()
        return queryset


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = [
        'first_name',
        'last_name',
        'display_name',
    ]

    list_filter = [
        # Generic person roles
        'person_type',

        # Concert-specific roles
        ConcertRoleFilter,

        # Music-specific roles
        MusicRoleFilter,
    ]

    distinct = True


admin.site.register(models.PersonRoleType)
