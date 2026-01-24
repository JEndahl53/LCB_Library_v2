# concerts/views/concert_add.py

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.urls import reverse
from concerts.forms import ConcertForm


@staff_member_required
def concert_add(request):
    if request.method == "POST":
        form = ConcertForm(request.POST, request.FILES)
        if form.is_valid():
            concert = form.save()
            if request.headers.get("HX-Request"):
                response = render(
                    request,
                    "concerts/_concert_add_container.html",
                    {
                        "concert": concert,
                        "form": ConcertForm(instance=concert),
                        "open_program_modal": True,
                    },
                )
                response["HX-Push-Url"] = reverse("concerts:concert_edit", args=[concert.pk])
                return response
            return redirect("concerts:concert_edit", pk=concert.pk)
    else:
        form = ConcertForm()

    return render(
        request,
        "concerts/concert_add.html",
        {
            "form": form,
            "add_action": request.path,
            "add_form_hx": 'hx-post="{}" hx-target="#concert-add-container" hx-swap="outerHTML" hx-encoding="multipart/form-data"'.format(
                request.path,
            ),
        },
    )
