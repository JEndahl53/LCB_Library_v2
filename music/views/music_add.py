# music/views/music_add.py
# Common form for music creation and editing (people used two different views)

from django.contrib.admin.views.decorators import staff_member_required
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.urls import reverse

from music.forms import MusicForm

@staff_member_required
def music_add(request):
    add_action = request.path
    add_form_hx = 'hx-post="{}" hx-target="#music-add-container" hx-swap="outerHTML"'.format(
        request.path,
    )

    if request.method == "POST":
        form = MusicForm(request.POST)
        if form.is_valid():
            try:
                music = form.save()
            except IntegrityError:
                form.add_error(
                    None,
                    "Save failed due to a duplicate database id. "
                    "The music ID sequence may be out of sync; ask an admin to reset it.",
                )
                music = None
            if request.headers.get("HX-Request"):
                if music:
                    response = render(
                        request,
                        "music/_music_add_container.html",
                        {
                            "music": music,
                            "form": MusicForm(instance=music),
                            "open_roles_modal": True,
                        },
                    )
                    response["HX-Push-Url"] = reverse("music:music_edit", args=[music.pk])
                    return response
            if music:
                return redirect("music:music_edit", pk=music.pk)
        if request.headers.get("HX-Request"):
            return render(
                request,
                "music/_music_add_container.html",
                {
                    "music": None,
                    "form": form,
                    "add_action": add_action,
                    "add_form_hx": add_form_hx,
                },
            )
    else:
        form = MusicForm()

    return render(
        request,
        "music/music_add.html",
        {
            "form": form,
            "add_action": add_action,
            "add_form_hx": add_form_hx,
        },
    )
