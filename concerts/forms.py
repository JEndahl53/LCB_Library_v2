# concerts/forms.py

from django import forms
from concerts.models import Concert, ConcertRole, ConcertProgram
from people.models import Person, PersonRoleType
from music.models import Music
from venues.models import Venue


class ConcertForm(forms.ModelForm):
    class Meta:
        model = Concert
        fields = [
            'title',
            'date',
            'venue',
            'description',
            "poster"
        ]

        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', "class": "input input-bordered w-full"}),
            "title": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
            "venue": forms.Select(attrs={"class": "select select-bordered w-full"}),
            'description': forms.Textarea(attrs={"class": "textarea testarea-bordered w-full",'rows': 4}),
            "poster": forms.FileInput(attrs={"class": "file-input file-input-bordered w-full"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show active venues
        self.fields['venue'].queryset = Venue.objects.filter(is_active=True).order_by('name')


class ConcertRoleForm(forms.ModelForm):
    class Meta:
        model = ConcertRole
        fields = [
            'person',
            'role_type',
            'display_order',
        ]

    person = forms.ModelChoiceField(
        queryset=Person.objects.filter(is_active=True).order_by('last_name', 'first_name'),
        required=True,
    )

    role_type = forms.ModelChoiceField(
        queryset=PersonRoleType.objects.filter(
            is_active=True,
            scope__in=['concert', 'both'],
        ).order_by('display_order', 'name'),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filter roles to concert-scoped (or both)
        self.fields['role_type'].queryset = PersonRoleType.objects.filter(
            scope__in=['concert', 'both'],
            is_active=True,
        ).order_by('display_order', 'name')

        # Only active people should be selectable
        self.fields['person'].queryset = Person.objects.filter(
            is_active=True
        ).order_by('last_name', 'first_name')

        # Friendly defaults
        self.fields['display_order'].required = False
        self.fields['display_order'].initial = 0

        self.fields['person'].label = 'Person'
        self.fields['role_type'].label = 'Role'
        self.fields['display_order'].label = 'Order (optional)'


class ConcertProgramForm(forms.ModelForm):
    class Meta:
        model = ConcertProgram
        fields = [
            'music',
            'program_order',
            'notes',
        ]

        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Only show active music
        self.fields['music'].queryset = Music.objects.filter(
            is_active=True
        ).order_by('title')

        self.fields['music'].label = 'Music'
        self.fields['program_order'].label = 'Order'
        self.fields['notes'].label = 'Notes (optional)'
