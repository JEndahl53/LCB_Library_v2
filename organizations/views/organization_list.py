# organizations/views/organization_list.py

from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.shortcuts import render

from organizations.models import OrganizationRoleType
from organizations.views._auth import is_staff_user
from organizations.services.organization_queryset import get_organization_list_queryset


@login_required
@user_passes_test(is_staff_user)
def organization_list(request):
    active = request.GET.get('active', 'active')  # active|inactive|all
    role = request.GET.get('role')
    role_id = int(role) if role and role.isdigit() else None
    search = (request.GET.get("q") or "").strip()

    qs = get_organization_list_queryset(
        active=active,
        role=role_id,
        search=search,
    )

    paginator = Paginator(qs, 25)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    role_types = OrganizationRoleType.objects.filter(is_active=True).order_by('name')

    context = {
        'page_obj': page_obj,
        'organizations': page_obj.object_list,
        'role_types': role_types,
        'filters': {
            'active': active,
            'q': search,
            'role': role_id,
        },
    }

    if request.headers.get("HX-Request"):
        return render(request, "organizations/_organization_table.html", context)

    return render(request, 'organizations/organization_list.html', context)