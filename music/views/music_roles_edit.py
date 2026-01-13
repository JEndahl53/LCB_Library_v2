# music/views/music_roles_edit.py

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404

from music.models import Music
from music.forms import MusicRoleForm


@staff_member_required
def music_roles_edit(request, pk):
    music = get_object_or_404(Music, pk=pk)

    if request.method == 'POST':
        form = MusicRoleForm(request.POST)
        if form.is_valid():
            role = form.save(commit=False)
            role.music = music
            role.save()
            return redirect('music:music_roles_edit', pk=music.pk)
    else:
        form = MusicRoleForm()

    roles = (
        music.roles
        .select_related("person", "role_type")
        .order_by("role_type__display_order", "person__last_name")
    )

    return render(
        request,
        'music/music_roles_edit.html',
        {
            "music": music,
            "roles": roles,
            "form": form,
        },
    )
