# concerts/views/concert_delete.py

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from concerts.models import Concert


@staff_member_required
def concert_delete(request, pk):
    concert = get_object_or_404(Concert, pk=pk)

    if request.method == "POST":
        concert.delete()
        return redirect("concerts:concert_list")

    return render(
        request,
        "concerts/concert_confirm_delete.html",
        {"concert": concert},
    )
