# concerts/views/concert_program_reorder.py

from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from concerts.forms import ConcertProgramForm
from concerts.models import Concert, ConcertProgram


@staff_member_required
def concert_program_reorder(request, pk):
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")

    concert = get_object_or_404(Concert, pk=pk)
    order = request.POST.get("order", "").strip()
    if not order:
        return HttpResponseBadRequest("order required")

    ids = [int(item_id) for item_id in order.split(",") if item_id.strip().isdigit()]
    program_items = list(
        ConcertProgram.objects.filter(concert=concert, pk__in=ids)
    )
    item_map = {item.pk: item for item in program_items}

    with transaction.atomic():
        for index, item_id in enumerate(ids, start=1):
            item = item_map.get(item_id)
            if item:
                item.program_order = index
                item.save(update_fields=["program_order"])

    updated_items = concert.program_items.select_related("music").order_by("program_order")
    modal_html = render_to_string(
        "concerts/_concert_program_modal.html",
        {
            "concert": concert,
            "program_items": updated_items,
            "form": ConcertProgramForm(),
            "next_order": updated_items.count() + 1,
            "is_modal": True,
        },
        request=request,
    )
    panel_html = render_to_string(
        "concerts/_concert_edit_program_panel.html",
        {"concert": concert, "swap_oob": True},
        request=request,
    )
    return HttpResponse(modal_html + panel_html)
