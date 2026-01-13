# concerts/views/concert_list.py

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from concerts.models import Concert


@staff_member_required
def concert_list(request):
    concerts = Concert.objects.select_related('venue').order_by('-date')
    return render(
        request,
        "concerts/concert_list.html",
        {"concerts": concerts},
    )
