# music/models.py
from django.core.exceptions import ValidationError
from django.db import models
from collections import OrderedDict

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

    def roles_by_type(self):
        """
        Returns roles grouped by role type, ordered by role_type.display_order
        Example:
        {
            "Composer": [Person, Person],
            "Arranger": [Person],
        }
        """
        roles = (
            self.roles
            .select_related("role_type", "person")
            .order_by(
                "role_type__display_order",
                "display_order",
                "person__last_name"
            )
        )

        grouped = OrderedDict()

        for role in roles:
            role_type = role.role_type
            grouped.setdefault(role_type, []).append(role.person)

        return grouped

    def update_availability_from_organizations(self, *, save=True):
        """
        Derive is_active based on current organization relationships.

        Rules:
        – Active LOANED_TO -> Inactive
        – Active BORROWED_FROM / RENTAL_VENDOR -> active
        – End-dated relationships ignored
        """
        active_links = self.organization_links.filter(
            end_date__isnull=True
        ).select_related("role_type")

        # Default: do not change availability
        new_active = self.is_active

        for link in active_links:
            code = link.role_type.code

            if code == "LOANED_TO":
                new_active = False
                break

            if code in {"BORROWED_FROM", "RENTAL_VENDOR", "OWNED_BY"}:
                new_active = True

        if new_active != self.is_active:
            self.is_active = new_active
            if save:
                self.save(update_fields=["is_active"])


    def get_availability_badge(self):
        """
        Return a short availability label for list display, or None.
        """
        if not self.is_active:
            return "Unavailable"

        active_links = self.organization_links.filter(
            end_date__isnull=True
        ).select_related("role_type")

        for link in active_links:
            code = link.role_type.code

            if code == "BORROWED_FROM":
                return "Borrowed"
            if code == "RENTAL_VENDOR":
                return "Rented"

        return None


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
        ordering = ["display_order"]
        unique_together = ("music", "person", "role_type")

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


class MusicOrganizationLink(models.Model):
    music = models.ForeignKey(
        "music.Music",
        on_delete=models.CASCADE,
        related_name="organization_links",
    )

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="music_links",
    )

    role_type = models.ForeignKey(
        "organizations.OrganizationRoleType",
        on_delete=models.PROTECT,
        related_name="music_links",
    )

    start_date = models.DateField(
        null=True,
        blank=True,
        help_text="When this relationship began"
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        help_text="When this relationship ended"
    )

    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ("music", "organization", "role_type", "start_date")
        ordering = ["role_type__name", "start_date"]

    def __str__(self):
        return f"{self.organization} - {self.role_type}  ({self.music})"
