# venues/views/venue_list.py

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from venues.models import Venue


@staff_member_required
def venue_list(request):
    venues = Venue.objects.all()
    return render(
        request,
        "venues/venue_list.html",
        {"venues": venues},
    )
