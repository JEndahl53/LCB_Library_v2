# music/views/music_add.py
# Common form for music creation and editing (people used two different views)

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect

from music.forms import MusicForm

@staff_member_required
def music_add(request):
    if request.method == "POST":
        form = MusicForm(request.POST)
        if form.is_valid():
            music = form.save()
            return redirect("music:music_detail", pk=music.pk)
    else:
        form = MusicForm()

    return render(
        request,
        "music/music_add.html",
        {
            "form": form,
        }
    )
