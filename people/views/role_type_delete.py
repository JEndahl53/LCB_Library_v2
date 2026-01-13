# people/views/role_type_delete.py

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from people.models import PersonRoleType


@staff_member_required
def role_type_delete(request, pk):
    role_type = get_object_or_404(PersonRoleType, pk=pk)

    if request.method == "POST":
        role_type.delete()
        return redirect("people:role_type_list")

    return render(
        request,
        "people/role_type_confirm_delete.html",
        {"role_type": role_type},
    )
