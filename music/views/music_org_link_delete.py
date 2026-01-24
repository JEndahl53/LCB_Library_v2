# music/views/music_org_link_delete.py

from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from music.models import Music, MusicOrganizationLink
from music.forms import MusicOrganizationLinkForm
from organizations.forms import OrganizationQuickAddForm


@require_POST
def music_org_link_delete(request, music_pk, link_pk):
    music = get_object_or_404(Music, pk=music_pk)
    link = get_object_or_404(
        MusicOrganizationLink,
        pk=link_pk,
        music=music,
    )

    link.delete()

    if request.headers.get("HX-Request"):
        panel_html = render_to_string(
            "music/_music_edit_orgs_panel.html",
            {"music": music, "swap_oob": True},
            request=request,
        )
        modal_html = render_to_string(
            "music/_music_orgs_modal.html",
            {
                "music": music,
                "form": MusicOrganizationLinkForm(),
                "organization_quick_form": OrganizationQuickAddForm(),
                "is_modal": True,
            },
            request=request,
        )
        return HttpResponse(modal_html + panel_html)

    return redirect("music:music_edit", pk=music_pk)
