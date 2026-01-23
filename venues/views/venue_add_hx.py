# venues/views/venue_add_hx.py
# This is an HTMX partial that collects venue name during inline concert creation

from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from venues.forms import VenueQuickAddForm
from concerts.forms import ConcertForm

@staff_member_required
def venue_add_hx(request):
    """
    HTMX view for in-line venue creation
    """
    if request.method == 'POST':
        form = VenueQuickAddForm(request.POST)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.needs_review = True
            venue.save()
            # Prepare the updated dropdown from the main ConcertForm with the new venue selected
            concert_form = ConcertForm(initial={"venue": venue})
            return render(
                request,
                "venues/_venue_select_updated.html",
                {"venue_field": concert_form["venue"]}
            )
        # If form is invalid, we fall through to render the form with errors
    else:
        form = VenueQuickAddForm()

    return render(request, "venues/_venue_form_inline.html", {"form": form})