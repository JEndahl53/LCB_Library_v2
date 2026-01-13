# genres/views/genre-add.py

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from genres.forms import GenreForm


@staff_member_required
def genre_add(request):
    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == "POST":
        form = GenreForm(request.POST)
        if form.is_valid():
            form.save()
            if next_url:
                return redirect(next_url)
            return redirect("genres:genre_list")
    else:
        form = GenreForm()

    return render(
        request,
        "genres/genre_add.html",
        {
            "form": form,
            "next": next_url,
        },
    )