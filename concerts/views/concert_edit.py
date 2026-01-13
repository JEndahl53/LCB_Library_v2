# concerts/views/concert_edit.py

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from concerts.forms import ConcertForm
from concerts.models import Concert


@staff_member_required
def concert_edit(request, pk):
    concert = get_object_or_404(Concert, pk=pk)

    if request.method == "POST":
        form = ConcertForm(request.POST, instance=concert)
        if form.is_valid():
            concert = form.save()
            return redirect("concerts:concert_detail", pk=concert.pk)
    else:
        form = ConcertForm(instance=concert)

    return render(
        request,
        "concerts/concert_edit.html",
        {
            "form": form,
            "concert": concert,
        },
    )
