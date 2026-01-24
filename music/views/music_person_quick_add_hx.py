# music/views/music_person_quick_add_hx.py

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render

from music.forms import MusicRoleForm
from music.models import Music
from people.forms.person_form import PersonQuickAddForm


@staff_member_required
def music_person_quick_add_hx(request, pk):
    music = get_object_or_404(Music, pk=pk)
    form = PersonQuickAddForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        person = form.save(commit=False)
        person.needs_review = True
        person.is_active = True
        person.save()
        created_person = person
        form = PersonQuickAddForm()
    else:
        created_person = None

    roles = (
        music.roles.select_related("person", "role_type")
        .order_by("role_type__display_order", "person__last_name")
    )

    status = 200 if created_person else 400

    return render(
        request,
        "music/_music_roles_modal.html",
        {
            "music": music,
            "roles": roles,
            "form": MusicRoleForm(),
            "person_quick_form": form,
            "created_person": created_person,
            "is_modal": True,
        },
        status=status,
    )
