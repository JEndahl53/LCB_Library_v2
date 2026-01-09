# organizations/views/organization_role_add.py

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect

from organizations.models import Organization, OrganizationRole
from organizations.forms import OrganizationRoleForm
from organizations.views._auth import is_staff_user


@login_required
@user_passes_test(is_staff_user)
def organization_role_add(request, org_pk):
    org = get_object_or_404(Organization, pk=org_pk)

    if request.method == 'POST':
        form = OrganizationRoleForm(request.POST)
        if form.is_valid():
            role = form.save(commit=False)
            role.organization = org
            role.save()
            messages.success(request, f'Role "{role.role_type.name}" added to {org.name}.')
            return redirect(org.get_absolute_url())
    else:
        form = OrganizationRoleForm()

    return render(
        request,
        'organizations/organization_role_form.html',
        {
            'form': form,
            'org': org,
            'mode': 'add'
        }
    )
