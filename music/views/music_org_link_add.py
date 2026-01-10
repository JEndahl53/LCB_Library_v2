# music/views/music_org_link_add.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from music.models import Music
from music.forms import MusicOrganizationLinkForm


@require_http_methods(["GET", "POST"])
def music_org_link_add(request, music_pk):
    music = get_object_or_404(Music, pk=music_pk)

    if request.method == "POST":
        form = MusicOrganizationLinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.music = music
            link.save()
            return redirect("music:music_detail", pk=music_pk)
    else:
        form = MusicOrganizationLinkForm()

    return render(
        request,
        "music/music_org_link_form.html",
        {
            "music": music,
            "form": form,
        },
    )
