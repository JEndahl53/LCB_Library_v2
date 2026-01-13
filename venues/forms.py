# venues/forms.py

from django import forms
from venues.models import Venue


class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = [
            'name',
            'address',
            'city',
            'state',
            'zip_code',
            'map_link',
            'notes',
            'is_active',
            'needs_review',
        ]

        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
        }


class VenueQuickAddForm(forms.ModelForm):
    """Quick add form for inline venue creation during concert creation"""
    class Meta:
        model = Venue
        fields = ['name']

    def save(self, commit=True):
        venue = super().save(commit=False)
        venue.needs_review = True
        if commit:
            venue.save()
        return venue
