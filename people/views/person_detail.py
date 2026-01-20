# people/views/person_detail.py

# from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404
from people.models import Person


# def is_staff_user(user):
#     return user.is_authenticated and user.is_staff
#
#
# @login_required
# @user_passes_test(is_staff_user)
def person_detail(request, pk):
    person = get_object_or_404(Person, pk=pk)

    music_roles = (
        person.music_roles
        .select_related('role_type', 'music')
        .filter(is_active=True)
        .order_by('role_type__name', 'display_order')
    )

    concert_roles = (
        person.concert_roles
        .select_related('role_type', 'concert')
        .filter(is_active=True)
        .order_by('role_type__name', 'display_order')
    )

    context = {
        'person': person,
        'music_roles': music_roles,
        'concert_roles': concert_roles,
    }

    return render(request, 'people/person_detail.html', context)
