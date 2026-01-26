# music/views/music_org_quick_add_hx.py

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render

from music.forms import MusicOrganizationLinkForm
from music.models import Music
from organizations.forms import OrganizationQuickAddForm


@staff_member_required
def music_org_quick_add_hx(request, pk):
    music = get_object_or_404(Music, pk=pk)
    form = OrganizationQuickAddForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        organization = form.save(commit=False)
        organization.is_active = True
        organization.needs_review = True
        organization.save()
        created_org = organization
        form = OrganizationQuickAddForm()
    else:
        created_org = None

    link_form = MusicOrganizationLinkForm(
        initial={"organization": created_org.pk} if created_org else None
    )

    status = 200 if created_org else 400

    return render(
        request,
        "music/_music_orgs_modal.html",
        {
            "music": music,
            "form": link_form,
            "organization_quick_form": form,
            "is_modal": True,
        },
        status=status,
    )
