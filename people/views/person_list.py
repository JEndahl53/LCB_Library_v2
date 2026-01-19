# people/views/person_list.py

# from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.shortcuts import render

from people.services.person_queryset import get_person_list_queryset
from people.services.derived_roles import get_derived_roles_for_people
from people.models import PersonRoleType


# def is_staff_user(user):
#     return user.is_authenticated and user.is_staff
#
#
# @login_required
# @user_passes_test(is_staff_user)
def person_list(request):
    """
    Staff-only Person list view.
    """
    # --- Read filters from query string ---
    active = request.GET.get("active", "active")
    person_type = request.GET.get("type", "both")
    needs_review = request.GET.get("needs_review", "all")
    role = request.GET.get("role")
    role_id = int(role) if role else None
    search = request.GET.get("q")

    # --- Build base queryset (already tested) ---
    qs = get_person_list_queryset(
        active=active,
        person_type=person_type,
        needs_review=needs_review,
        role=role_id,
        search=search,
    )

    # --- Pagination ---
    paginator = Paginator(qs, 25)  # 25 rows per page (adjust later)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    # --- Derived roles (bulk, using page objects only) ---
    derived_roles = get_derived_roles_for_people(page_obj.object_list)

    # --- Populate role_types for the template pulldown ---
    role_types = PersonRoleType.objects.filter(is_active=True).order_by("name")

    context = {
        "page_obj": page_obj,
        "people": page_obj.object_list,
        "derived_roles": derived_roles,
        "role_types": role_types,
        "filters": {
            "active": active,
            "type": person_type,
            "needs_review": needs_review,
            "role": role_id,
        },
    }

    if request.headers.get("HX-Request"):
        return render(request, "people/_person_table.html", context)

    return render(request, "people/person_list.html", context)
