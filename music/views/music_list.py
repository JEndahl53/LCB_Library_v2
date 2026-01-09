# music/views/music_list.py

from django.shortcuts import render

from genres.models import Genre
from music.services.music_queryset import get_music_list_queryset


def music_list(request):
    q = request.GET.get('q') or None
    genre_id = request.GET.get('genre') or None
    score_missing = request.GET.get('score_missing')
    needs_review = request.GET.get('needs_review')

    def parse_bool(value):
        if value == "1":
            return True
        if value == "0":
            return False
        return None

    music_qs = get_music_list_queryset(
        q=q,
        genre_id=genre_id,
        score_missing=parse_bool(score_missing),
        needs_review=parse_bool(needs_review),
    )

    context = {
        "music_list": music_qs,
        "genres": Genre.objects.filter(is_active=True),
        "q": q or "",
        "selected_genre": int(genre_id) if genre_id else None,
        "score_missing": score_missing,
        "needs_review": needs_review,
    }

    return render(request, 'music/music_list.html', context)