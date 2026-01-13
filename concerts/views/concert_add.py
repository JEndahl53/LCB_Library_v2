# concerts/views/concert_add.py

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from concerts.forms import ConcertForm


@staff_member_required
def concert_add(request):
    if request.method == "POST":
        form = ConcertForm(request.POST)
        if form.is_valid():
            concert = form.save()
            return redirect("concerts:concert_edit", pk=concert.pk)
    else:
        form = ConcertForm()

    return render(
        request,
        "concerts/concert_add.html",
        {"form": form},
    )
