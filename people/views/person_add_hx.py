# people/views/person_add_hx.py

from __future__ import annotations

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string

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

            panel_html = render_to_string(
                "concerts/_concert_edit_people_panel.html",
                {"concert": concert, "swap_oob": True},
                request=request,
            )
            roles = (
                concert.roles
                .select_related("person", "role_type")
                .order_by("role_type__display_order", "display_order", "person__last_name")
            )
            roles_by_type = {}
            for role in roles:
                roles_by_type.setdefault(role.role_type, []).append(role)
            modal_html = render_to_string(
                "concerts/_concert_people_modal.html",
                {
                    "concert": concert,
                    "role_types": (
                        PersonRoleType.objects.filter(
                            is_active=True,
                            scope__in=[PersonRoleType.RoleScope.CONCERT, PersonRoleType.RoleScope.BOTH],
                        )
                        .order_by("display_order", "name")
                    ),
                    "roles_by_type": roles_by_type,
                    "close_person_modal": True,
                },
                request=request,
            )
            return HttpResponse(modal_html + panel_html)
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
