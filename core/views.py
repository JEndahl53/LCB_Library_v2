# core/views.py
# This is the main landing page view for the application

from django.shortcuts import render

from concerts.models import Concert, ConcertRole
from genres.models import Genre
from music.models import Music, MusicRole
from organizations.models import Organization
from people.models import Person, PersonRoleType
from venues.models import Venue

def home(request):
    # Adjust these codes if your PersonRoleType.code values differ.
    guest_role_codes = ["GUEST"]
    composer_role_codes = ["COMPOSER"]
    arranger_role_codes = ["ARRANGER"]

    context = {
        "pieces_count": Music.objects.count(),
        "concerts_count": Concert.objects.count(),
        "venues_count": Venue.objects.count(),
        "people_count": Person.objects.count(),
        "genres_count": Genre.objects.count(),
        "organizations_count": Organization.objects.count(),
        "person_role_types_count": PersonRoleType.objects.count(),
        "guest_count": (
            ConcertRole.objects.filter(role_type__code__in=guest_role_codes)
            .values("person_id")
            .distinct()
            .count()
        ),
        "composer_count": (
            MusicRole.objects.filter(role_type__code__in=composer_role_codes)
            .values("person_id")
            .distinct()
            .count()
        ),
        "arranger_count": (
            MusicRole.objects.filter(role_type__code__in=arranger_role_codes)
            .values("person_id")
            .distinct()
            .count()
        ),
    }

    return render(request, "core/home.html", context)
