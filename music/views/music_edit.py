# music/views/music_edit.py

from django.shortcuts import render, redirect, get_object_or_404

from music.forms import MusicForm
from music.models import Music


def music_edit(request, pk):
    music = get_object_or_404(Music, pk=pk)

    if request.method == "POST":
        form = MusicForm(request.POST, instance=music)
        if form.is_valid():
            music = form.save()
            return redirect("music:music_detail", pk=music.pk)
    else:
        form = MusicForm(instance=music)

    return render(
        request,
        "music/music_form.html",
        {
            "form": form,
            "music": music,
            "is_create": False,
        },
    )
