# people/views/person_reactivate.py

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404

from people.models import Person


def is_staff_user(user):
    return user.is_authenticated and user.is_staff


@login_required
@user_passes_test(is_staff_user)
def person_reactivate(request, pk):
    person = get_object_or_404(Person, pk=pk)

    if request.method == 'POST':
        person.is_active = True
        person.save(update_fields=['is_active'])

        messages.success(
            request,
            f"{person.display_name or person.last_name} has been reactivated."

            )
        return redirect('person_detail', pk=person.pk)

    return render(
        request,
        'people/person_confirm_reactivate.html',
        {'person': person}
        )
