# people/views/person_add_hx.py

from __future__ import annotations

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render

from concerts.models import ConcertRole, Concert
from people.forms.person_form import PersonQuickAddForm
from people.models import PersonRoleType, Person


def _ensure_concert_scoped(role_type: PersonRoleType):
    if role_type.scope not in (PersonRoleType.RoleScope.CONCERT, PersonRoleType.RoleScope.BOTH):
        return HttpResponseBadRequest("role_type must be concert-scoped")
    return None


def _historical_people_for_role_type(role_type: PersonRoleType):
    return (
        Person.objects.filter(is_active=True, concert_roles__role_type=role_type)
        .distinct()
        .order_by("last_name", "first_name", "display_name")
    )


@staff_member_required
def person_add_hx(request):
    """
    HTMX view for inline person creation from Concert edit.
    Expects hidden fields: concert_id, role_type_id
    """
    concert_id = request.GET.get("concert_id") or request.POST.get("concert_id")
    role_type_id = request.GET.get("role_type_id") or request.POST.get("role_type_id")

    if not concert_id or not role_type_id:
        return HttpResponseBadRequest("concert_id or role_type_id required")

    concert = get_object_or_404(Concert, pk=concert_id)
    role_type = get_object_or_404(PersonRoleType, pk=role_type_id, is_active=True)

    bad = _ensure_concert_scoped(role_type)
    if bad:
        return bad

    if request.method == "POST":
        form = PersonQuickAddForm(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            person.needs_review = True
            person.is_active = True
            person.save()

            ConcertRole.objects.get_or_create(
                concert = concert,
                person = person,
                role_type = role_type,
                defaults={"display_order": 0, "is_active": True},
            )

            # Return the refreshed role section so the modal can close and the list updates.
            roles = (
                concert.roles.filter(role_type=role_type)
                .select_related("person", "role_type")
                .order_by("display_order", "person__last_name", "person__first_name")
            )
            historical_people = _historical_people_for_role_type(role_type)[:200]

            return render(
                request,
                "concerts/_concert_people_role_section.html",
                {
                    "concert": concert,
                    "role_type": role_type,
                    "roles": roles,
                    "historical_people": historical_people,
                    "close_modal": True,
                },
            )
    else:
        form = PersonQuickAddForm()

    return render(
        request,
        "people/_person_form_inline.html",
        {
            "form": form,
            "concert": concert,
            "role_type": role_type,
        },
    )
