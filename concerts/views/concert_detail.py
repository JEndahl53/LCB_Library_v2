# concerts/views/concert_detail.py

from django.shortcuts import render, get_object_or_404
from concerts.models import Concert


def concert_detail(request, pk):
    """Public-facing concert detail view"""
    concert = get_object_or_404(Concert, pk=pk)

    return render(
        request,
        "concerts/concert_detail.html",
        {"concert": concert},
    )
