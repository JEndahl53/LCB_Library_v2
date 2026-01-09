# organizations/views/organization_role_deactivate.py

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect

from organizations.models import OrganizationRole
from organizations.views._auth import is_staff_user


@login_required
@user_passes_test(is_staff_user)
def organization_role_deactivate(request, pk):
    role = get_object_or_404(OrganizationRole, pk=pk)
    org = role.organization

    role.is_active = False
    role.save(update_fields=['is_active'])
    messages.success(request, f'Role "{role.role_type.name}" deactivated for {org.name}.')

    return redirect(org.get_absolute_url())
