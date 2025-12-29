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
            'person_type',
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
