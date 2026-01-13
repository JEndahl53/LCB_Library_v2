# organizations/views/org_role_type_add.py

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from organizations.forms import OrganizationRoleTypeForm
from organizations.views._auth import is_staff_user


@login_required
@user_passes_test(is_staff_user)
def org_role_type_add(request):
    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == "POST":
        form = OrganizationRoleTypeForm(request.POST)
        if form.is_valid():
            form.save()
            if next_url:
                return redirect(next_url)
            return redirect("organizations:org_role_type_list")
    else:
        form = OrganizationRoleTypeForm()

    return render(
        request,
        "organizations/org_role_type_add.html",
        {
            "form": form,
            "next": next_url,
        },
    )
