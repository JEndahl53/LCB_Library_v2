# music/services/music_queryset.py

from django.db.models import Q

from music.models import Music
from people.models import PersonRoleType


def get_music_list_queryset(
    *,
    q: str | None = None,
    genre_id: int | None = None,
    score_missing: bool | None = None,
    needs_review: bool | None = None,
    include_inactive: bool = False,
):

    qs = Music.objects.all()

    if not include_inactive:
        qs = qs.filter(is_active=True)

    if needs_review is not None:
        qs = qs.filter(needs_review=needs_review)

    if score_missing:
        qs = qs.filter(score_missing=score_missing)

    if genre_id:
        qs = qs.filter(genres__id=genre_id)

    if q:
        qs = qs.filter(
            Q(title__icontains=q)
            |
            Q(
                roles__role_type__scope__in=["music", "both"],
                roles__person__display_name__icontains=q,
            )
            |
            Q(
                roles__role_type__scope__in=["music", "both"],
                roles__person__first_name__icontains=q,
            )
            |
            Q(
                roles__role_type__scope__in=["music", "both"],
                roles__person__last_name__icontains=q,
            )
        )

    return qs.distinct().prefetch_related(
        "genres",
        "roles__person",
        'roles__role_type',
    )