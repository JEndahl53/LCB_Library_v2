# music/models.py
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.

"""
In this revision, Music does not have composer, arranger, or other specific roles. These are
assigned via a ConcertRole field. This allows defining additional roles without having to modify
the model.
"""


class Music(models.Model):

    EASY = 'E'
    MODERATELY_EASY = 'ME'
    MODERATE = 'M'
    MODERATELY_DIFFICULT = 'MD'
    DIFFICULT = 'D'

    DIFFICULTY_CHOICES = (
        (EASY, 'Easy'),
        (MODERATELY_EASY, 'Moderately Easy'),
        (MODERATE, 'Moderate'),
        (MODERATELY_DIFFICULT, 'Moderately Difficult'),
        (DIFFICULT, 'Difficult'),
    )

    title = models.CharField(max_length=250)

    location_drawer = models.PositiveIntegerField(
        blank=True,
        null=True,
        db_index=True,
        help_text="Physical drawer number"
    )

    location_number = models.PositiveIntegerField(
        blank=True,
        null=True,
        db_index=True,
        help_text="Folder number within the drawer"
    )

    difficulty = models.CharField(
        max_length=2,
        choices=DIFFICULTY_CHOICES,
        blank=True,
        default=""
    )

    year_composed = models.CharField(
        max_length=20,
        blank=True,
        help_text="Year or range (free text, e.g.'1936', 'c. 1900')"
    )

    genres = models.ManyToManyField(
        "genres.Genre",
        blank=True,
        related_name="music"
    )

    notes = models.TextField(blank=True)
    score_missing = models.BooleanField(blank=True, default=False)
    needs_review = models.BooleanField(blank=True, default=False)

    is_active = models.BooleanField(
        blank=True,
        default=True,
        help_text='Is this piece part of our active library collection?'
    )
    duration = models.DurationField(help_text="Enter duration as mm:ss", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Music"
        verbose_name = "Music"
        ordering = ("title",)

    def __str__(self):
        return self.title

    def get_duration_display(self):
        """Return duration in MM:SS format"""
        if not self.duration:
            return "-"

        total_seconds = int(self.duration.total_seconds())
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    def contributes_roles(self) -> bool:
        """
        Whether this music should contribute roles to
        derived role calculations.

        Rule:
        - Only active music contributes roles
        """
        return self.is_active


class MusicRole(models.Model):
    music = models.ForeignKey(
        'music.Music',
        on_delete=models.CASCADE,
        related_name='roles',
    )

    person = models.ForeignKey(
        'people.Person',
        on_delete=models.CASCADE,
        related_name='music_roles',
    )

    role_type = models.ForeignKey(
        'people.PersonRoleType',
        on_delete=models.PROTECT,
        related_name='music_roles',
    )

    is_active = models.BooleanField(
        default=True,
        help_text='Soft-disable role types without breaking history')

    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order']
        unique_together = ('music', 'person', 'role_type')

    def clean(self):
        if self.role_type.scope not in ("music", "both"):
            raise ValidationError({
                "role_type": f"{self.role_type.name} is not a music role."
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.person} as {self.role_type}"
