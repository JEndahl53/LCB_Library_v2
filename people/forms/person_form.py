# people/forms/person_form.py
# This form is used to edit person details

from django import forms
from people.models import Person


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            'first_name',
            'last_name',
            'display_name',
            # 'person_type',  # Removed due to confusing UI issues when editing a person
            'birth_date',
            'death_date',
            'is_active',
            'needs_review',
            'notes',
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'death_date': forms.DateInput(attrs={'type': 'date'}),
        }

# -------------------------------------------------------
# Inline / quick-add form (used from Concert editing modal via HTMX
# -------------------------------------------------------
class PersonQuickAddForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            "first_name",
            "last_name",
            "display_name",
            "person_type",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
            "last_name": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
            "display_name": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
            "person_type": forms.Select(attrs={"class": "select select-bordered w-full"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["first_name"].required = False
        self.fields["display_name"].required = False

        # Make intent explicit in the UI: last_name doubles as the ensemble name.
        self.fields["last_name"].help_text = "Required. For ensembles, enter the ensemble name here."
        self.fields["display_name"].help_text = (
            "Optional professional name. Include honorific and middle initial if applicable."
        )
        self.fields["person_type"].required = True
