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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["is_active"].help_text = (
            "Show this genre in selection dropdowns."
        )
        self.fields["needs_review"].help_text = ""

class GenreQuickAddForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ["name"]
