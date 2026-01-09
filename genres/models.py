# genres/models.py

from django.db import models
from django.urls import reverse
# Create your models here.


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    notes = models.TextField(blank=True)

    needs_review = models.BooleanField(
        default=False,
        help_text="Flag for librarian review",
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Hide genre from normal selection without deleting history.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("genres:genre_detail", args=[self.pk])

