# people/views/person_hx.py
# This file is an HTMX view for handling HTMX requests related to people

from django.shortcuts import render
from django.db.models import Q

from people.models import Person


def person_hx_search(request):
    """
    HTMX view for searching people.
    """
    query = request.GET.get("q", "").strip()

    people = (
        Person.objects.filter(
            Q(last_name__icontains=query) |
            Q(first_name__icontains=query) |
            Q(display_name__icontains=query)
        ).order_by("last_name", "first_name")[:20]
        if query else []
    )

    return render(
        request,
        "people/_person_search_results.html",
        {"people": people},
    )
