# people/services/person_queryset.py

from django.db.models import QuerySet, Q
from people.models import Person


def get_person_list_queryset(
    *,
    active: str = "active",
    person_type: str = "both",
    needs_review: str = "all",
    search: str | None = None,
    role: int | None = None,  # int because PersonRoleType.id is an integer, not a str
):
    """
    Canonical queryset builder for staff Person list views.

    Parameters:
      active:
        - "active" (default)
        - "inactive"
        - "all"

      person_type:
        - "individual"
        - "ensemble"
        - "both" (default)

      needs_review:
        - "all" (default)
        - "needs_review"

      Guarantees:
        - Correct filtering
        - Stable ordering (last_name, first_name)
        - Required prefetching for derived role computation
    """

    qs = Person.objects.all()

    # Active / inactive filter
    if active == "active":
        qs = qs.filter(is_active=True)
    elif active == "inactive":
        qs = qs.filter(is_active=False)
    # else: "all" -> no filter

    # Person type filter
    if person_type == "individual":
        qs = qs.filter(person_type=Person.INDIVIDUAL)
    elif person_type == "ensemble":
        qs = qs.filter(person_type=Person.ENSEMBLE)
    # else: "both" -> no filter

    # Needs review filter
    if needs_review == "needs_review":
        qs = qs.filter(needs_review=True)

    # Role filter
    if role is not None:
        qs = qs.filter(
            Q(music_roles__role_type_id=role, music_roles__is_active=True) |
            Q(concert_roles__role_type_id=role, concert_roles__is_active=True)
        ).distinct()

    # Live search filter
    if search:
        qs = qs.filter(
            Q(last_name__icontains=search) |
            Q(first_name__icontains=search) |
            Q(display_name__icontains=search)
        )

    # Ordering (always applied last for clarity)
    qs = qs.order_by("last_name", "first_name")

    # Required prefetches for derived roles
    qs = qs.prefetch_related(
        "music_roles__role_type",
        "music_roles__music",
        "concert_roles__role_type",
    )

    return qs
