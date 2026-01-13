# genres/views/genre_edit.py

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from genres.forms import GenreForm
from genres.models import Genre


@staff_member_required
def genre_edit(request, pk):
    genre = get_object_or_404(Genre, pk=pk)

    if request.method == "POST":
        form = GenreForm(request.POST, instance=genre)
        if form.is_valid():
            form.save()
            return redirect("genres:genre_list")
    else:
        form = GenreForm(instance=genre)

    return render(
        request,
        "genres/genre_edit.html",
        {
            "form": form,
            "genre": genre,
        },
    )
