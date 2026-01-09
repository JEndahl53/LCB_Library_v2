# music/views/music_detail.py

from django.shortcuts import render, get_object_or_404

from music.models import Music


def music_detail(request, pk):
    music = get_object_or_404(
        Music.objects.prefetch_related(
            'genres',
            'roles__person',
            'roles__role_type',
            'organization_links__organization',
            'organization_links__role_type',
        ),
        pk=pk,
    )

    context = {
        'music': music,
    }

    return render(request, 'music/music_detail.html', context)
