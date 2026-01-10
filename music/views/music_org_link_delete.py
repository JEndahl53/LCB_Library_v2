# music/views/music_org_link_delete.py

from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST

from music.models import Music, MusicOrganizationLink


@require_POST
def music_org_link_delete(request, music_pk, link_pk):
    music = get_object_or_404(Music, pk=music_pk)
    link = get_object_or_404(
        MusicOrganizationLink,
        pk=link_pk,
        music=music,
    )

    link.delete()
    return redirect("music:music_detail", pk=music_pk)
