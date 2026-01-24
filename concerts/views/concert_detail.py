# concerts/views/concert_detail.py

from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404

from concerts.models import Concert, ConcertProgram


def concert_detail(request, pk):
    """Public-facing concert detail view"""
    concert = get_object_or_404(
        Concert.objects.select_related("venue").prefetch_related(
            "roles__person",
            "roles__role_type",
            Prefetch(
                "program_items",
                queryset=ConcertProgram.objects.select_related("music").prefetch_related(
                    "recordings",
                    "music__roles__person",
                    "music__roles__role_type",
                ),
            ),
        ),
        pk=pk,
    )

    roles = list(concert.roles.all())
    conductors = []
    guests = []
    for role in roles:
        role_name = role.role_type.name.lower()
        if "conductor" in role_name:
            conductors.append(role)
        elif any(term in role_name for term in ("soloist", "guest", "ensemble")):
            guests.append(role)

    program_items = []
    for item in concert.program_items.all():
        composer_names = []
        arranger_names = []
        for role in item.music.roles.all():
            role_name = role.role_type.name.lower()
            person_name = str(role.person)
            if role_name == "composer":
                composer_names.append(person_name)
            elif role_name == "arranger":
                arranger_names.append(person_name)
        item.composer_names = ", ".join(sorted(set(composer_names), key=str.casefold))
        item.arranger_names = ", ".join(sorted(set(arranger_names), key=str.casefold))
        item.has_recordings = item.recordings.exists()
        program_items.append(item)

    return render(
        request,
        "concerts/concert_detail.html",
        {
            "concert": concert,
            "conductors": conductors,
            "guests": guests,
            "program_items": program_items,
        },
    )
