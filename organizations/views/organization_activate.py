# organizations/views/organization_activate.py

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect

from organizations.models import Organization
from organizations.views._auth import is_staff_user


@login_required
@user_passes_test(is_staff_user)
def organization_activate(request, pk):
    org = get_object_or_404(Organization, pk=pk)

    org.is_active = True
    org.save(update_fields=['is_active'])
    messages.success(request, f'Organization "{org.name}" reactivated.')

    return redirect(org.get_absolute_url())
