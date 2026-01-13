# people/views/role_type_list.py

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from people.models import PersonRoleType


@staff_member_required
def role_type_list(request):
    role_types = PersonRoleType.objects.all()
    return render(
        request,
        "people/role_type_list.html",
        {"role_types": role_types},
    )
