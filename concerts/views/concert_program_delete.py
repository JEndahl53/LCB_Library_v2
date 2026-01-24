# concerts/views/concert_program_delete.py

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string

from concerts.forms import ConcertProgramForm
from concerts.models import Concert, ConcertProgram


@staff_member_required
def concert_program_delete(request, concert_pk, program_pk):
    program_item = get_object_or_404(ConcertProgram, pk=program_pk, concert_id=concert_pk)

    if request.method == "POST":
        program_item.delete()

    if request.headers.get("HX-Request"):
        concert = get_object_or_404(Concert, pk=concert_pk)
        program_items = concert.program_items.select_related("music").order_by("program_order")
        panel_html = render_to_string(
            "concerts/_concert_edit_program_panel.html",
            {"concert": concert, "swap_oob": True},
            request=request,
        )
        modal_html = render_to_string(
            "concerts/_concert_program_modal.html",
            {
                "concert": concert,
                "program_items": program_items,
                "form": ConcertProgramForm(),
                "next_order": program_items.count() + 1,
                "is_modal": True,
            },
            request=request,
        )
        return HttpResponse(modal_html + panel_html)

    return redirect("concerts:concert_program_edit", pk=concert_pk)
