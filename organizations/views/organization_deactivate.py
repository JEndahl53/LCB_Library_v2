# organizations/views/organization_deactivate.py

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404

from organizations.models import Organization
from organizations.views._auth import is_staff_user


@login_required
@user_passes_test(is_staff_user)
def organization_deactivate(request, pk):
    org = get_object_or_404(Organization, pk=pk)

    if request.method == 'POST':
        org.is_active = False
        org.save(update_fields=['is_active'])
        messages.success(request, f'Organization "{org.name}" deactivated.')
        return redirect('organizations:organization_list')

    return render(request, 'organizations/organization_confirm_deactivate.html', {'org': org})
