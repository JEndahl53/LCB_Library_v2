# music/views/music_genres_assign.py
# this view allows us to assign genres to a piece

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from genres.forms import GenreQuickAddForm
from music.forms import MusicGenresAssignForm
from music.models import Music

@staff_member_required
def music_genres_assign(request, pk):
    music = get_object_or_404(Music, pk=pk)
    genre_quick_form = GenreQuickAddForm()

    if request.method == "POST":
        form = MusicGenresAssignForm(request.POST, instance=music)
        if form.is_valid():
            form.save()
            if request.headers.get("HX-Request"):
                panel_html = render_to_string(
                    "music/_music_edit_genres_panel.html",
                    {"music": music, "swap_oob": True},
                    request=request,
                )
                modal_html = render_to_string(
                    "music/_music_genres_modal.html",
                    {
                        "music": music,
                        "form": MusicGenresAssignForm(instance=music),
                        "genre_quick_form": GenreQuickAddForm(),
                        "is_modal": True,
                    },
                    request=request,
                )
                return HttpResponse(modal_html + panel_html)
            return redirect("music:music_edit", pk=music.pk)
        if request.headers.get("HX-Request"):
            return render(
                request,
                "music/_music_genres_modal.html",
                {
                    "music": music,
                    "form": form,
                    "genre_quick_form": genre_quick_form,
                    "is_modal": True,
                },
                status=400,
            )
    else:
        form = MusicGenresAssignForm(instance=music)

    if request.headers.get("HX-Request"):
        return render(
            request,
            "music/_music_genres_modal.html",
            {
                "music": music,
                "form": form,
                "genre_quick_form": genre_quick_form,
                "is_modal": True,
            },
        )

    return render(
        request,
        "music/music_genres_assign.html",
        {
            "music": music,
            "form": form,
            "genre_quick_form": genre_quick_form,
            "is_modal": False,
        },
    )
