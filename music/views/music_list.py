# music/views/music_list.py

from urllib.parse import urlencode

from django.core.paginator import Paginator
from django.db.models import Case, OuterRef, Subquery, Value, When
from django.db.models.functions import Coalesce
from django.shortcuts import render

from genres.models import Genre
from music.models import MusicRole
from music.services.music_queryset import get_music_list_queryset


def music_list(request):
    q = request.GET.get("q")
    genre_id = request.GET.get("genre")
    score_missing = request.GET.get("score_missing")
    needs_review = request.GET.get("needs_review")
    view_mode = request.GET.get("view", "basic")
    sort = request.GET.get("sort", "title")
    sort_dir = request.GET.get("dir", "asc")

    if view_mode not in {"basic", "full"}:
        view_mode = "basic"

    if sort_dir not in {"asc", "desc"}:
        sort_dir = "asc"

    def parse_bool(value):
        if value == "1":
            return True
        if value == "0":
            return False
        return None

    # Safely convert genre_id to int to avoid ValueError
    try:
        selected_genre_id = int(genre_id) if genre_id else None
    except ValueError:
        selected_genre_id = None

    music_qs = get_music_list_queryset(
        q=q or None,
        genre_id=selected_genre_id,
        score_missing=parse_bool(score_missing),
        needs_review=parse_bool(needs_review),
    )

    composer_last_name = Subquery(
        MusicRole.objects.filter(
            music=OuterRef("pk"),
            role_type__name__iexact="composer",
        )
        .order_by("person__last_name", "person__first_name")
        .values("person__last_name")[:1]
    )

    arranger_last_name = Subquery(
        MusicRole.objects.filter(
            music=OuterRef("pk"),
            role_type__name__iexact="arranger",
        )
        .order_by("person__last_name", "person__first_name")
        .values("person__last_name")[:1]
    )

    genre_name = Subquery(
        Genre.objects.filter(music=OuterRef("pk"))
        .order_by("name")
        .values("name")[:1]
    )

    music_qs = music_qs.annotate(
        location_drawer_sort=Coalesce("location_drawer", Value(9999)),
        location_number_sort=Coalesce("location_number", Value(9999)),
        composer_last_name=Coalesce(composer_last_name, Value("")),
        arranger_last_name=Coalesce(arranger_last_name, Value("")),
        genre_name=Coalesce(genre_name, Value("")),
        status_sort=Case(
            When(is_active=False, then=Value(2)),
            default=Value(1),
        ),
        flags_sort=Case(
            When(needs_review=True, score_missing=True, then=Value(3)),
            When(needs_review=True, then=Value(2)),
            When(score_missing=True, then=Value(1)),
            default=Value(0),
        ),
    )

    sort_fields = {
        "location": ["location_drawer_sort", "location_number_sort", "title"],
        "title": ["title"],
        "composers": ["composer_last_name", "title"],
        "arrangers": ["arranger_last_name", "title"],
        "duration": ["duration", "title"],
        "genres": ["genre_name", "title"],
        "status": ["status_sort", "title"],
        "flags": ["flags_sort", "title"],
    }

    if sort not in sort_fields:
        sort = "title"

    order_fields = sort_fields[sort]
    if sort_dir == "desc":
        order_fields = [f"-{field}" for field in order_fields]

    music_qs = music_qs.order_by(*order_fields)

    # Implement pagination (e.g., 25 items per page)
    paginator = Paginator(music_qs, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    for music in page_obj.object_list:
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

    base_params = {
        "q": q or "",
        "genre": selected_genre_id or "",
        "score_missing": score_missing or "",
        "needs_review": needs_review or "",
        "view": view_mode,
    }
    list_params = {
        **base_params,
        "sort": sort,
        "dir": sort_dir,
    }

    filter_query = urlencode(base_params)
    list_query = urlencode(list_params)

    sort_state = {
        key: {
            "active": key == sort,
            "dir": sort_dir,
            "next_dir": "desc" if key == sort and sort_dir == "asc" else "asc",
        }
        for key in sort_fields
    }

    context = {
        "page_obj": page_obj,
        "music_list": page_obj.object_list,
        "genres": Genre.objects.filter(is_active=True),
        "q": q,
        "selected_genre": selected_genre_id,
        "score_missing": score_missing,
        "needs_review": needs_review,
        "view_mode": view_mode,
        "sort": sort,
        "sort_dir": sort_dir,
        "sort_state": sort_state,
        "filter_query": filter_query,
        "list_query": list_query,
        "sort_query_prefix": f"{filter_query}&" if filter_query else "",
        "page_query_prefix": f"{list_query}&" if list_query else "",
    }

    # Future-proofing for HTMX: return a partial template if requested
    if request.headers.get("HX-Request"):
        return render(request, "music/_music_list_table.html", context)

    return render(request, 'music/music_list.html', context)
