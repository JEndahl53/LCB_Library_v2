# people/models.py
#
from django.db import models

# Create your models here.


class Person(models.Model):
    INDIVIDUAL = 'IND'
    ENSEMBLE = 'ENS'

    PERSON_TYPE_CHOICES = (
        (INDIVIDUAL, 'Individual'),
        (ENSEMBLE, 'Ensemble'),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    display_name = models.CharField(
        max_length=200,
        blank=True,
        help_text='Professional name, include honorific and middle initial, if needed'
        )
    notes = models.TextField(blank=True)

    person_type = models.CharField(
        max_length=3,
        choices=PERSON_TYPE_CHOICES,
    )

    birth_date = models.DateField(blank=True, null=True)
    death_date = models.DateField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.display_name or f"{self.first_name} {self.last_name}"


class ConcertRoleType(models.Model):
    """Concert role types, e.g. conductor, soloist, etc."""
    code = models.CharField(
        max_length=50,
        unique=True,
        help_text='Stable machine-readable identifier (e.g. CONDUCTOR)'
        )
    name = models.CharField(
        max_length=100,
        help_text='Human-readable name (e.g. Conductor)'
        )
    is_active = models.BooleanField(
        default=True,
        help_text='Soft-disable role types without breaking history')

    def __str__(self):
        return self.name

