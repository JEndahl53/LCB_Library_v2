# concerts/models.py
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from venues.models import Venue

# Create your models here.


class Concert(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateTimeField(blank=True, null=True)

    venue = models.ForeignKey(
        'venues.Venue',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='concerts',
    )

    poster = models.ImageField(upload_to='posters/', blank=True)
    description = models.TextField(blank=True)

    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('concerts:concert_detail', args=[self.pk])

    def roles_by_type(self):
        """
        Returns concert roles grouped by role type (similar to Music.roles_by_type)
        Example:
        {
            "Conductor": [Person, Person],
            "Soloist": [Person],
        }
        """
        from collections import OrderedDict

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


class ConcertRole(models.Model):
    concert = models.ForeignKey(
        'concerts.Concert',
        on_delete=models.CASCADE,
        related_name='roles',
    )

    person = models.ForeignKey(
        "people.Person",
        on_delete=models.CASCADE,
        related_name='concert_roles',
    )

    role_type = models.ForeignKey(
        "people.PersonRoleType",
        on_delete=models.PROTECT,
        related_name='concert_roles',
    )

    is_active = models.BooleanField(
        default=True,
        help_text='Soft-disable roles without breaking history'
    )

    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order']
        unique_together = ('concert', 'person', 'role_type')

    def clean(self):
        if self.role_type.scope not in ("concert", "both"):
            raise ValidationError({
                "role_type": f"{self.role_type.name} is not a concert role."
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.person} -- {self.role_type}"


class ConcertProgram(models.Model):
    concert = models.ForeignKey(
        'concerts.Concert',
        on_delete=models.CASCADE,
        related_name='program_items',
    )

    music = models.ForeignKey(
        'music.Music',
        on_delete=models.PROTECT,
        related_name='program_appearances',
    )

    program_order = models.PositiveIntegerField(
        help_text="Order of performance in the concert program",
    )

    notes = models.TextField(
        blank=True,
        help_text="Optional program-specific notes (movements, excerpts, etc.)",
    )

    class Meta:
        ordering = ['program_order']
        constraints = [
            models.UniqueConstraint(
                fields=['concert', 'program_order'],
                name='uniq_program_order_per_concert',
            ),
        ]

    def __str__(self):
        return f"{self.concert} - #{self.program_order}: {self.music}"
