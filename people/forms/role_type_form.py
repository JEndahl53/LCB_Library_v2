# people/forms/role_type_form.py

from django import forms
from people.models import PersonRoleType


class RoleTypeForm(forms.ModelForm):
    class Meta:
        model = PersonRoleType
        fields = [
            "code",
            "name",
            "display_order",
            "scope",
            "is_active",
        ]
