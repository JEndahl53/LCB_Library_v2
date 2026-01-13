# concerts/views/concert_program_delete.py

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, get_object_or_404
from concerts.models import ConcertProgram


@staff_member_required
def concert_program_delete(request, concert_pk, program_pk):
    program_item = get_object_or_404(ConcertProgram, pk=program_pk, concert_id=concert_pk)

    if request.method == "POST":
        program_item.delete()

    return redirect("concerts:concert_program_edit", pk=concert_pk)
