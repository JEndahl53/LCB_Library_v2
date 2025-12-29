# people/views/person_edit.py

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from people.models import Person
from people.forms.person_form import PersonForm


def is_staff_user(user):
    return user.is_authenticated and user.is_staff


@login_required
@user_passes_test(is_staff_user)
def person_edit(request, pk):
    person = get_object_or_404(Person, pk=pk)

    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f"{person.display_name or person.last_name} was successfully updated.",
            )
            return redirect('person_detail', pk=person.pk)
    else:
        form = PersonForm(instance=person)

    return render(request, 'people/person_form.html', {
        'form': form,
        'page_title': 'Edit Person',
        'submit_label': 'Save Changes',
    })