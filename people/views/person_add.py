# people/views/person_add.py

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect

from people.forms.person_form import PersonForm


def is_staff_user(user):
    return user.is_authenticated and user.is_staff


@login_required
@user_passes_test(is_staff_user)
def person_add(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save()
            messages.success(
                request,
                f"{person.display_name or person.last_name} was added successfully."
            )

            return redirect('people:person_detail', pk=person.pk)
    else:
        form = PersonForm()

    return render(
        request,
        'people/person_form.html',
        {
            'form': form,
            'page_title': 'Add person',
            'submit_label': 'Create a person',
        }
    )