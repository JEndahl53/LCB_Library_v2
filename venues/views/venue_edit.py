# venues/views/venue_edit.py

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from venues.forms import VenueForm
from venues.models import Venue


@staff_member_required
def venue_edit(request, pk):
    venue = get_object_or_404(Venue, pk=pk)

    if request.method == "POST":
        form = VenueForm(request.POST, instance=venue)
        if form.is_valid():
            form.save()
            return redirect("venues:venue_list")
    else:
        form = VenueForm(instance=venue)

    return render(
        request,
        "venues/venue_form.html",
        {
            "form": form,
            "venue": venue,
            "mode": "edit",
        },
    )
