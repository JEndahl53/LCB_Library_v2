# genres/views/genre_delete.py

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from genres.models import Genre


@staff_member_required
def genre_delete(request, pk):
    genre = get_object_or_404(Genre, pk=pk)

    if request.method == "POST":
        genre.delete()
        return redirect("genres:genre_list")

    return render(
        request,
        "genre_delete.confirm_html",
        {"genre": genre},
    )
