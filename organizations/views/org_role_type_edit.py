# organizations/views/org_role_type_edit.py

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from organizations.forms import OrganizationRoleTypeForm
from organizations.models import OrganizationRoleType
from organizations.views._auth import is_staff_user


@login_required
@user_passes_test(is_staff_user)
def org_role_type_edit(request, pk):
    role_type = get_object_or_404(OrganizationRoleType, pk=pk)

    if request.method == "POST":
        form = OrganizationRoleTypeForm(request.POST, instance=role_type)
        if form.is_valid():
            form.save()
            return redirect("organizations:org_role_type_list")
    else:
        form = OrganizationRoleTypeForm(instance=role_type)

    return render(
        request,
        "organizations/org_role_type_edit.html",
        {
            "form": form,
            "role_type": role_type,
        },
    )
