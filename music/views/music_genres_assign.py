# music/views/music_genres_assign.py
# this view allows us to assign genres to a piece

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404

from music.forms import MusicGenresAssignForm
from music.models import Music

@staff_member_required
def music_genres_assign(request, pk):
    music = get_object_or_404(Music, pk=pk)

    if request.method == "POST":
        form = MusicGenresAssignForm(request.POST, instance=music)
        if form.is_valid():
            form.save()
            return redirect("music:music_edit", pk=music.pk)
    else:
        form = MusicGenresAssignForm(instance=music)

    return render(
        request,
        "music/music_genres_assign.html",
        {
            "music": music,
            "form": form,
        },
    )
