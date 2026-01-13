# venues/views/venue_add.py

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from venues.forms import VenueForm


@staff_member_required
def venue_add(request):
    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == "POST":
        form = VenueForm(request.POST)
        if form.is_valid():
            venue = form.save()
            if next_url:
                return redirect(next_url)
            return redirect("venues:venue_list")
    else:
        form = VenueForm()

    return render(
        request,
        "venues/venue_form.html",
        {
            "form": form,
            "mode": "add",
            "next": next_url,
        },
    )
