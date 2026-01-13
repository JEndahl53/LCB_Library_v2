# people/views/role_type_edit.py

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from people.forms.role_type_form import RoleTypeForm
from people.models import PersonRoleType


@staff_member_required
def role_type_edit(request, pk):
    role_type = get_object_or_404(PersonRoleType, pk=pk)

    if request.method == "POST":
        form = RoleTypeForm(request.POST, instance=role_type)
        if form.is_valid():
            form.save()
            return redirect("people:role_type_list")
    else:
        form = RoleTypeForm(instance=role_type)

    return render(
        request,
        "people/role_type_edit.html",
        {
            "form": form,
            "role_type": role_type,
        },
    )
