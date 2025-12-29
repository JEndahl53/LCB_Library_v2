# people/views/person_delete.py

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404

from people.models import Person


def is_staff_user(user):
    return user.is_authenticated and user.is_staff


@login_required
@user_passes_test(is_staff_user)
def person_delete(request, pk):
    person = get_object_or_404(Person, pk=pk)

    if request.method == 'POST':
        person.is_active = False
        person.save(update_fields=['is_active'])

        messages.success(
            request,
            f"{person.display_name or person.last_name} has been deactivated."

            )
        return redirect('person_list')

    return render(
        request,
        'people/person_confirm_delete.html',
        {'person': person}
    )