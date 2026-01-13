# people/views/role_type_add.py

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from people.forms.role_type_form import RoleTypeForm


@staff_member_required
def role_type_add(request):
    if request.method == "POST":
        form = RoleTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("people:role_type_list")
    else:
        form = RoleTypeForm()

    return render(
        request,
        "people/role_type_add.html",
        {"form": form},
    )
