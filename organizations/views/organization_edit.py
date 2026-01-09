# organizations/views/organization_edit.py

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect

from organizations.models import Organization
from organizations.forms import OrganizationForm
from organizations.views._auth import is_staff_user


@login_required
@user_passes_test(is_staff_user)
def organization_edit(request, pk):
    org = get_object_or_404(Organization, pk=pk)

    if request.method == 'POST':
        form = OrganizationForm(request.POST, instance=org)
        if form.is_valid():
            org = form.save()
            messages.success(request, f'Organization "{org.name}" updated.')
            return redirect(org.get_absolute_url())
    else:
        form = OrganizationForm(instance=org)

    return render(
        request,
        'organizations/organization_form.html',
        {
            'form': form,
            'org': org,
            'mode': 'edit'
        }
    )
