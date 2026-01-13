# concerts/views/concert_program_edit.py

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from concerts.models import Concert
from concerts.forms import ConcertProgramForm


@staff_member_required
def concert_program_edit(request, pk):
    concert = get_object_or_404(Concert, pk=pk)

    if request.method == 'POST':
        form = ConcertProgramForm(request.POST)
        if form.is_valid():
            program_item = form.save(commit=False)
            program_item.concert = concert
            program_item.save()
            return redirect('concerts:concert_program_edit', pk=concert.pk)
    else:
        form = ConcertProgramForm()

    program_items = concert.program_items.select_related("music").order_by("program_order")

    return render(
        request,
        'concerts/concert_program_edit.html',
        {
            "concert": concert,
            "program_items": program_items,
            "form": form,
        },
    )
