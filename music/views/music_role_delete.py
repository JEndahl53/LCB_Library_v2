# music/views/music_role_delete.py


from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string

from music.models import Music, MusicRole
from music.forms import MusicRoleForm
from people.forms.person_form import PersonQuickAddForm


@staff_member_required
def music_role_delete(request, music_pk, role_pk):
    role = get_object_or_404(
        MusicRole,
        id=role_pk,
        music_id=music_pk,
    )

    if request.method == "POST":
        role.delete()

    if request.headers.get("HX-Request"):
        music = get_object_or_404(Music, pk=music_pk)
        roles = (
            music.roles.select_related("person", "role_type")
            .order_by("role_type__display_order", "person__last_name")
        )
        panel_html = render_to_string(
            "music/_music_edit_roles_panel.html",
            {"music": music, "swap_oob": True},
            request=request,
        )
        modal_html = render_to_string(
            "music/_music_roles_modal.html",
            {
                "music": music,
                "roles": roles,
                "form": MusicRoleForm(),
                "person_quick_form": PersonQuickAddForm(),
                "is_modal": True,
            },
            request=request,
        )
        return HttpResponse(modal_html + panel_html)

    return redirect('music:music_roles_edit', pk=music_pk)
