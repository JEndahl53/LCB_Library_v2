# concerts/views/concert_roles_edit.py

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from concerts.models import Concert
from concerts.forms import ConcertRoleForm


@staff_member_required
def concert_roles_edit(request, pk):
    concert = get_object_or_404(Concert, pk=pk)

    if request.method == 'POST':
        form = ConcertRoleForm(request.POST)
        if form.is_valid():
            role = form.save(commit=False)
            role.concert = concert
            role.save()
            return redirect('concerts:concert_roles_edit', pk=concert.pk)
    else:
        form = ConcertRoleForm()

    roles = (
        concert.roles
        .select_related("person", "role_type")
        .order_by("role_type__display_order", "person__last_name")
    )

    return render(
        request,
        'concerts/concert_roles_edit.html',
        {
            "concert": concert,
            "roles": roles,
            "form": form,
        },
    )
