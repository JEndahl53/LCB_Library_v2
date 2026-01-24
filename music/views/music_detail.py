# music/views/music_detail.py

from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404

from music.models import Music
from concerts.models import ConcertProgram


def music_detail(request, pk):
    music = get_object_or_404(
        Music.objects.prefetch_related(
            "genres",
            "roles__person",
            "roles__role_type",
            "organization_links__organization",
            "organization_links__role_type",
            Prefetch(
                "program_appearances",
                queryset=ConcertProgram.objects.select_related("concert").order_by(
                    "concert__date"
                ),
            ),
        ),
        pk=pk,
    )

    composer_people = []
    arranger_people = []

    for role in music.roles.all():
        role_name = role.role_type.name.lower()
        if role_name == "composer":
            composer_people.append(role.person)
        elif role_name == "arranger":
            arranger_people.append(role.person)

    composer_people = sorted(
        {person.pk: person for person in composer_people}.values(),
        key=lambda person: (person.last_name or "", person.first_name or "", str(person)),
    )
    arranger_people = sorted(
        {person.pk: person for person in arranger_people}.values(),
        key=lambda person: (person.last_name or "", person.first_name or "", str(person)),
    )

    publisher_links = []
    ownership_links = []
    for link in music.organization_links.all():
        role_code = (link.role_type.code or "").upper()
        role_name = (link.role_type.name or "").lower()
        if role_code == "PUBLISHER" or role_name == "publisher":
            publisher_links.append(link)
        else:
            ownership_links.append(link)

    context = {
        "music": music,
        "composer_people": composer_people,
        "arranger_people": arranger_people,
        "publisher_links": publisher_links,
        "ownership_links": ownership_links,
    }

    return render(request, "music/music_detail.html", context)
