# music/views/music_org_link_add.py

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods

from music.models import Music
from music.forms import MusicOrganizationLinkForm
from organizations.forms import OrganizationQuickAddForm


@require_http_methods(["GET", "POST"])
def music_org_link_add(request, music_pk):
    music = get_object_or_404(Music, pk=music_pk)
    organization_quick_form = OrganizationQuickAddForm()

    if request.method == "POST":
        form = MusicOrganizationLinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.music = music
            link.save()
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
        if request.headers.get("HX-Request"):
            return render(
                request,
                "music/_music_orgs_modal.html",
                {
                    "music": music,
                    "form": form,
                    "organization_quick_form": organization_quick_form,
                    "is_modal": True,
                },
                status=400,
            )
    else:
        form = MusicOrganizationLinkForm()

    if request.headers.get("HX-Request"):
        return render(
            request,
            "music/_music_orgs_modal.html",
            {
                "music": music,
                "form": form,
                "organization_quick_form": organization_quick_form,
                "is_modal": True,
            },
        )

    return render(
        request,
        "music/music_org_link_form.html",
        {
            "music": music,
            "form": form,
            "organization_quick_form": organization_quick_form,
            "is_modal": False,
        },
    )
