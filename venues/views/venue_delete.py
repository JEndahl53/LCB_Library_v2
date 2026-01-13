# venues/views/venue_delete.py

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from venues.models import Venue


@staff_member_required
def venue_delete(request, pk):
    venue = get_object_or_404(Venue, pk=pk)

    if request.method == "POST":
        venue.delete()
        return redirect("venues:venue_list")

    return render(
        request,
        "venues/venue_confirm_delete.html",
        {"venue": venue},
    )
