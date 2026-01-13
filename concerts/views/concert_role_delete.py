# concerts/views/concert_role_delete.py

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, get_object_or_404
from concerts.models import ConcertRole


@staff_member_required
def concert_role_delete(request, concert_pk, role_pk):
    role = get_object_or_404(ConcertRole, pk=role_pk, concert_id=concert_pk)

    if request.method == "POST":
        role.delete()

    return redirect("concerts:concert_roles_edit", pk=concert_pk)
