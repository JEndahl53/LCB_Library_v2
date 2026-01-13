# music/views/music_edit.py

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404

from music.forms import MusicForm
from music.models import Music


@staff_member_required
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
        "music/music_edit.html",
        {
            "form": form,
            "music": music,
        },
    )
