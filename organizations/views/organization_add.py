# organizations/views/organization_add.py

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect

from organizations.forms import OrganizationForm
from organizations.views._auth import is_staff_user


@login_required
@user_passes_test(is_staff_user)
def organization_add(request):
    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            org = form.save()
            messages.success(request, f'Organization "{org.name}" added.')
            if next_url:
                return redirect(next_url)
            return redirect(org.get_absolute_url())
    else:
        form = OrganizationForm()

    return render(
        request,
        'organizations/organization_form.html',
        {
            'form': form,
            'mode': 'add',
            'next': next_url,
        }
    )
