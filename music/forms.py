# music/forms.py

from django import forms

from music.models import Music, MusicRole, MusicOrganizationLink
from genres.models import Genre
from people.models import Person, PersonRoleType
from organizations.models import Organization, OrganizationRoleType


class MusicForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = [
            "title",
            "location_drawer",
            "location_number",
            "difficulty",
            "year_composed",
            "duration",
            "genres",
            "score_missing",
            "needs_review",
            "is_active",
            "notes",
        ]

        widgets = {
            "notes": forms.Textarea(attrs={"rows": 4}),
            "genres": forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Only allow active genres to be selected
        self.fields['genres'].queryset = Genre.objects.filter(is_active=True)

        # Friendly labels
        self.fields["location_drawer"].label = "Drawer"
        self.fields["location_number"].label = "Folder"
        self.fields["year_composed"].label = "Year composed"


class MusicRoleForm(forms.ModelForm):
    class Meta:
        model = MusicRole
        fields = [
            "person",
            "role_type",
            "display_order",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Limit roles to music-scoped (or both)
        self.fields['role_type'].queryset = PersonRoleType.objects.filter(
            scope__in=['music', 'both'],
            is_active=True,
        ).order_by('display_order', 'name')

        # Only active people should be selectable
        self.fields['person'].queryset = Person.objects.filter(
            is_active=True
        ).order_by('last_name', 'first_name')

        # Friendly defaults
        self.fields["display_order"].required = False
        self.fields["display_order"].initial = 0

        self.fields['person'].label = "Person"
        self.fields['role_type'].label = "Role"
        self.fields['display_order'].label = "Order (optional)"


class MusicOrganizationLinkForm(forms.ModelForm):
    class Meta:
        model = MusicOrganizationLink
        fields = [
            "organization",
            "role_type",
            "start_date",
            "end_date",
            "notes",
        ]

        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["organization"].queryset = Organization.objects.filter(
            is_active=True
        ).order_by("name")

        self.fields["role_type"].queryset = OrganizationRoleType.objects.filter(
            is_active=True
        ).order_by("name")

        self.fields["organization"].label = "Organization"
        self.fields["role_type"].label = "Relationship"
