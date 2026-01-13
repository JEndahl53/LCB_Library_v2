# organizations/forms.py

from django import forms
from organizations.models import Organization, OrganizationRole, OrganizationRoleType


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = [
            'name',
            'contact_person',
            'contact_email',
            'contact_phone',
            'street_address',
            'city',
            'state',
            'country',
            'zip_code',
            'website',
            'is_active',
        ]


class OrganizationRoleForm(forms.ModelForm):
    class Meta:
        model = OrganizationRole
        fields = ['role_type', 'notes']


class OrganizationRoleTypeForm(forms.ModelForm):
    class Meta:
        model = OrganizationRoleType
        fields = [
            'code',
            'name',
            'is_active',
        ]