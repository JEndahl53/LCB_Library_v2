# organizations/views/org_role_type_list.py

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from organizations.models import OrganizationRoleType
from organizations.views._auth import is_staff_user


@login_required
@user_passes_test(is_staff_user)
def org_role_type_list(request):
    role_types = OrganizationRoleType.objects.all()
    return render(
        request,
        "organizations/org_role_type_list.html",
        {"role_types": role_types},
    )
