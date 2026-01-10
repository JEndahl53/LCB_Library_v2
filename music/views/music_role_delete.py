# music/views/music_role_delete.py

from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST

from music.models import Music, MusicRole


@require_POST
def music_role_delete(request, music_pk, role_pk):
    music = get_object_or_404(Music, pk=music_pk)
    role = get_object_or_404(MusicRole, pk=role_pk, music=music)

    role.delete()
    return redirect('music:music_detail', pk=music.pk)