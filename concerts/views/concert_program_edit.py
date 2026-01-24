# concerts/views/concert_program_edit.py

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from concerts.forms import ConcertProgramForm
from concerts.models import Concert


@staff_member_required
def concert_program_edit(request, pk):
    concert = get_object_or_404(Concert, pk=pk)

    if request.method == 'POST':
        form = ConcertProgramForm(request.POST)
        if form.is_valid():
            program_item = form.save(commit=False)
            program_item.concert = concert
            program_item.save()
            if request.headers.get("HX-Request"):
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
            return redirect('concerts:concert_program_edit', pk=concert.pk)
        if request.headers.get("HX-Request"):
            program_items = concert.program_items.select_related("music").order_by("program_order")
            return render(
                request,
                "concerts/_concert_program_modal.html",
                {
                    "concert": concert,
                    "program_items": program_items,
                    "form": form,
                    "next_order": program_items.count() + 1,
                    "is_modal": True,
                },
                status=400,
            )
    else:
        form = ConcertProgramForm()

    program_items = concert.program_items.select_related("music").order_by("program_order")

    if request.headers.get("HX-Request"):
        return render(
            request,
            "concerts/_concert_program_modal.html",
            {
                "concert": concert,
                "program_items": program_items,
                "form": form,
                "next_order": program_items.count() + 1,
                "is_modal": True,
            },
        )

    return render(
        request,
        'concerts/concert_program_edit.html',
        {
            "concert": concert,
            "program_items": program_items,
            "form": form,
            "next_order": program_items.count() + 1,
            "is_modal": False,
        },
    )
