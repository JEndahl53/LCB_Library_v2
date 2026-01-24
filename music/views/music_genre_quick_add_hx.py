# music/views/music_genre_quick_add_hx.py

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render

from genres.forms import GenreQuickAddForm
from music.forms import MusicGenresAssignForm
from music.models import Music


@staff_member_required
def music_genre_quick_add_hx(request, pk):
    music = get_object_or_404(Music, pk=pk)
    form = GenreQuickAddForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        genre = form.save(commit=False)
        genre.is_active = True
        genre.needs_review = True
        genre.save()

        selected_ids = list(music.genres.values_list("id", flat=True)) + [genre.id]
        assign_form = MusicGenresAssignForm(
            instance=music,
            initial={"genres": selected_ids},
        )
        return render(
            request,
            "music/_music_genres_modal.html",
            {
                "music": music,
                "form": assign_form,
                "genre_quick_form": GenreQuickAddForm(),
                "is_modal": True,
            },
        )

    assign_form = MusicGenresAssignForm(instance=music)
    status = 400 if request.method == "POST" else 200

    return render(
        request,
        "music/_music_genres_modal.html",
        {
            "music": music,
            "form": assign_form,
            "genre_quick_form": form,
            "is_modal": True,
        },
        status=status,
    )
