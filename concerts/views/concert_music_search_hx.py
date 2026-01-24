# concerts/views/concert_music_search_hx.py

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from music.models import Music


@staff_member_required
def concert_music_search_hx(request, pk: int):
    query = request.GET.get("q", "").strip()
    music_list = []
    if query:
        music_list = list(
            Music.objects.filter(is_active=True, title__icontains=query)
            .prefetch_related("roles__person", "roles__role_type")
            .order_by("title")[:20]
        )
        for music in music_list:
            composer_names = []
            arranger_names = []
            for role in music.roles.all():
                role_name = role.role_type.name.lower()
                person_name = str(role.person)
                if role_name == "composer":
                    composer_names.append(person_name)
                elif role_name == "arranger":
                    arranger_names.append(person_name)
            music.composer_names = ", ".join(
                sorted(set(composer_names), key=str.casefold)
            )
            music.arranger_names = ", ".join(
                sorted(set(arranger_names), key=str.casefold)
            )

    return render(
        request,
        "concerts/_concert_music_search_results.html",
        {
            "music_list": music_list,
        },
    )
