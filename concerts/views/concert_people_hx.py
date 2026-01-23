# concert/views/concert_people_hx.py

from __future__ import annotations

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404

from concerts.models import Concert, ConcertRole
from people.models import Person, PersonRoleType


def _concert_role_types_qs():
    return (
        PersonRoleType.objects.filter(
            is_active=True,
            scope__in=[
                PersonRoleType.RoleScope.CONCERT,
                PersonRoleType.RoleScope.BOTH
            ]
        )
        .order_by("display_order", "name")
    )


def _ensure_concert_scoped(role_type: PersonRoleType):
    if role_type.scope not in (PersonRoleType.RoleScope.CONCERT, PersonRoleType.RoleScope.BOTH):
        return HttpResponseBadRequest("role_type must be concert-scoped")
    return None


def _historical_people_for_role_type(role_type: PersonRoleType):
    # People who have historically held this role in any concert
    return(
        Person.objects.filter(
            is_active=True,
            concert_roles__role_type=role_type,
        )
        .distinct()
        .order_by("last_name", "first_name", "display_name")
    )


@staff_member_required
def concert_people_panel_hx(request, pk: int):
    concert= get_object_or_404(Concert, pk=pk)

    role_types = list(_concert_role_types_qs())

    return render(
        request,
        "concerts/_concert_people_panel.html",
        {
            "concert": concert,
            "role_types": role_types,
        },
    )


@staff_member_required
def concert_people_role_section_hx(request, pk: int, role_type_id: int):
    concert = get_object_or_404(Concert, pk=pk)
    role_type = get_object_or_404(PersonRoleType, pk=role_type_id, is_active=True)

    bad = _ensure_concert_scoped(role_type)
    if bad:
        return bad

    roles = (
        concert.roles.filter(role_type=role_type)
        .select_related("person", "role_type")
        .order_by("display_order", "person__last_name")
    )

    historical_people = _historical_people_for_role_type(role_type)[:200]

    return render(
        request,
        "concerts/_concert_people_role_section.html",
        {
            "concert": concert,
            role_type: role_type,
            "roles": roles,
            "historical_people": historical_people,
        },
    )


@staff_member_required
def concert_people_search_hx(request, pk: int, role_type_id: int):
    concert = get_object_or_404(Concert, pk=pk)
    role_type = get_object_or_404(PersonRoleType, pk=role_type_id, is_active=True)

    bad = _ensure_concert_scoped(role_type)
    if bad:
        return bad

    query = request.GET.get("q", "").strip()
    people = []
    if query:
        people = (
            Person.objects.filter(
                is_active=True,
            )
            .filter(
                Q(last_name__icontains=query)
                | Q(first_name__icontains=query)
                | Q(display_name__icontains=query)
            )
            .order_by("last_name", "first_name", "display_name")[:20]
        )

    return render(
        request,
        "concerts/_concert_people_search_results.html",
        {
            "concert": concert,
            "role_type": role_type,
            "people": people,
        },
    )

@staff_member_required
def concert_people_add_hx(request, pk: int, role_type_id: int):
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")

    concert = get_object_or_404(Concert, pk=pk)
    role_type = get_object_or_404(PersonRoleType, pk=role_type_id, is_active=True)

    bad = _ensure_concert_scoped(role_type)
    if bad:
        return bad

    person_id = request.POST.get("person_id")
    if not person_id:
        return HttpResponseBadRequest("person_id required")

    person = get_object_or_404(Person, pk=person_id, is_active=True)

    ConcertRole.objects.get_or_create(
        concert=concert,
        person=person,
        role_type=role_type,
        defaults={"display_order": 0, "is_active": True},
    )

    return concert_people_role_section_hx(request, pk=pk, role_type_id=role_type_id)


@staff_member_required
def concert_people_remove_hx(request, pk: int, role_type_id: int):
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")

    concert = get_object_or_404(Concert, pk=pk)
    role_type = get_object_or_404(PersonRoleType, pk=role_type_id, is_active=True)

    bad = _ensure_concert_scoped(role_type)
    if bad:
        return bad

    role_id = request.POST.get("role_id")
    if not role_id:
        return HttpResponseBadRequest("role_id required")

    role = get_object_or_404(ConcertRole, pk=role_id, concert=concert, role_type=role_type)
    role.delete()

    return concert_people_role_section_hx(request, pk=pk, role_type_id=role_type_id)
