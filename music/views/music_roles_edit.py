# music/views/music_roles_edit.py

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from music.models import Music
from music.forms import MusicRoleForm
from people.forms.person_form import PersonQuickAddForm


@staff_member_required
def music_roles_edit(request, pk):
    music = get_object_or_404(Music, pk=pk)

    if request.method == 'POST':
        form = MusicRoleForm(request.POST)
        if form.is_valid():
            role = form.save(commit=False)
            role.music = music
            role.save()
            if request.headers.get("HX-Request"):
                roles = (
                    music.roles
                    .select_related("person", "role_type")
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
            return redirect('music:music_roles_edit', pk=music.pk)
        if request.headers.get("HX-Request"):
            roles = (
                music.roles
                .select_related("person", "role_type")
                .order_by("role_type__display_order", "person__last_name")
            )
            return render(
                request,
                "music/_music_roles_modal.html",
                {
                    "music": music,
                    "roles": roles,
                    "form": form,
                    "person_quick_form": PersonQuickAddForm(),
                    "is_modal": True,
                },
                status=400,
            )
    else:
        form = MusicRoleForm()

    roles = (
        music.roles
        .select_related("person", "role_type")
        .order_by("role_type__display_order", "person__last_name")
    )

    if request.headers.get("HX-Request"):
        return render(
            request,
            "music/_music_roles_modal.html",
            {
                "music": music,
                "roles": roles,
                "form": form,
                "person_quick_form": PersonQuickAddForm(),
                "is_modal": True,
            },
        )

    return render(
        request,
        'music/music_roles_edit.html',
        {
            "music": music,
            "roles": roles,
            "form": form,
            "person_quick_form": PersonQuickAddForm(),
            "is_modal": False,
        },
    )
