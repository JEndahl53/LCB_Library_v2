# music/views/music_list.py

from django.shortcuts import render
from django.core.paginator import Paginator

from genres.models import Genre
from music.services.music_queryset import get_music_list_queryset


def music_list(request):
    q = request.GET.get('q')
    genre_id = request.GET.get('genre')
    score_missing = request.GET.get('score_missing')
    needs_review = request.GET.get('needs_review')

    def parse_bool(value):
        if value == "1":
            return True
        if value == "0":
            return False
        return None

    # Safely convert genre_id to int to avoid ValueError
    try:
        selected_genre_id = int(genre_id) if genre_id else None
    except ValueError:
        selected_genre_id = None

    music_qs = get_music_list_queryset(
        q=q or None,
        genre_id=selected_genre_id,
        score_missing=parse_bool(score_missing),
        needs_review=parse_bool(needs_review),
    )

    # Implement pagination (e.g., 25 items per page)
    paginator = Paginator(music_qs, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "music_list": music_qs,
        "genres": Genre.objects.filter(is_active=True),
        "q": q,
        "selected_genre": selected_genre_id,
        "score_missing": score_missing,
        "needs_review": needs_review,
    }

    # Future-proofing for HTMX: return a partial template if requested
    if request.headers.get("HX-Request"):
        return render(request, "music/_music_list_table.html", context)

    return render(request, 'music/music_list.html', context)