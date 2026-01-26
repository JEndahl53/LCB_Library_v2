# organizations/services/organization_queryset.py

from django.db.models import QuerySet, Q
from organizations.models import Organization


def get_organization_list_queryset(
    *,
    active: str = "active",
    role: int | None = None,
    needs_review: str = "all",
    search: str | None = None,
) -> QuerySet:
    """
    Canonical queryset builder for staff Organization list views.

    Parameters:
      active:
        - "active" (default)
        - "inactive"
        - "all"

      role:
        - ID of an OrganizationRoleType to filter by.

      search:
        - Search string for organization name.

    Returns:
      A filtered and ordered Organization queryset.
    """
    qs = Organization.objects.all()

    # Active / inactive filter
    if active == "active":
        qs = qs.filter(is_active=True)
    elif active == "inactive":
        qs = qs.filter(is_active=False)

    # Role filter
    if role is not None:
        qs = qs.filter(roles__role_type_id=role, roles__is_active=True).distinct()

    # Needs review filter
    if needs_review == "needs_review":
        qs = qs.filter(needs_review=True)

    # Search filter
    if search:
        qs = qs.filter(name__icontains=search)

    # Ordering
    qs = qs.order_by("name")

    # Prefetch roles and their types for efficient list display
    qs = qs.prefetch_related("roles__role_type")

    return qs
