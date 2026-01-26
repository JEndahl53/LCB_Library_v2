# concerts/views/concert_add.py

from django.contrib.admin.views.decorators import staff_member_required
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.urls import reverse
from concerts.forms import ConcertForm


@staff_member_required
def concert_add(request):
    add_action = request.path
    add_form_hx = 'hx-post="{}" hx-target="#concert-add-container" hx-swap="outerHTML" hx-encoding="multipart/form-data"'.format(
        request.path,
    )

    if request.method == "POST":
        form = ConcertForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                concert = form.save()
            except IntegrityError:
                form.add_error(
                    None,
                    "Save failed due to a duplicate database id. "
                    "The concert ID sequence may be out of sync; ask an admin to reset it.",
                )
                concert = None
            if request.headers.get("HX-Request"):
                if concert:
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
            if concert:
                return redirect("concerts:concert_edit", pk=concert.pk)
        if request.headers.get("HX-Request"):
            return render(
                request,
                "concerts/_concert_add_container.html",
                {
                    "concert": None,
                    "form": form,
                    "add_action": add_action,
                    "add_form_hx": add_form_hx,
                },
            )
    else:
        form = ConcertForm()

    return render(
        request,
        "concerts/concert_add.html",
        {
            "form": form,
            "add_action": add_action,
            "add_form_hx": add_form_hx,
        },
    )
