# genres/forms.py

from django import forms
from genres.models import Genre


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = [
            "name",
            "is_active",
            "needs_review",
            "notes",
        ]

class GenreQuickAddForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ["name"]
