# genres/views/genre_list.py

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from genres.models import Genre

@staff_member_required
def genre_list(request):
    genres = Genre.objects.all()
    return render(
        request,
        "genres/genre_list.html",
        {"genres": genres},
    )