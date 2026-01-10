# music/views/music_role_add.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from music.models import Music
from music.forms import MusicRoleForm


@require_http_methods(["GET", "POST"])
def music_role_add(request, music_pk):
    music = get_object_or_404(Music, pk=music_pk)

    if request.method == "POST":
        form = MusicRoleForm(request.POST)
        if form.is_valid():
            role = form.save(commit=False)
            role.music = music
            role.save()
            return redirect("music:music_detail", pk=music.pk)
    else:
        form = MusicRoleForm()

    return render(
        request,
        "music/music_role_form.html",
        {
            "music": music,
            "form": form,
        },
    )
