# organizations/views/org_role_type_delete.py

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from organizations.models import OrganizationRoleType
from organizations.views._auth import is_staff_user


@login_required
@user_passes_test(is_staff_user)
def org_role_type_delete(request, pk):
    role_type = get_object_or_404(OrganizationRoleType, pk=pk)

    if request.method == "POST":
        role_type.delete()
        return redirect("organizations:org_role_type_list")

    return render(
        request,
        "organizations/org_role_type_confirm_delete.html",
        {"role_type": role_type},
    )
