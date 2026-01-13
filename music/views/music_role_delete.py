# music/views/music_role_delete.py


from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, get_object_or_404

from music.models import Music, MusicRole


@staff_member_required
def music_role_delete(request, music_pk, role_pk):
    role = get_object_or_404(
        MusicRole,
        id=role_pk,
        music_id=music_pk,
    )

    if request.method == "POST":
        role.delete()

    return redirect('music:music_roles_edit', pk=music_pk)