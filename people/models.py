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

    first_name = models.CharField(max_length=100, blank=True, null=True,)
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
        if self.display_name:
            return self.display_name
        return " ".join(p for p in [self.first_name, self.last_name] if p)

    def clean(self):
        from django.core.exceptions import ValidationError

        if not self.last_name:
            raise ValidationError("All persons must have a name in the last_name field.")


class PersonRoleType(models.Model):
    """Role types, e.g. conductor, soloist, composer, arranger, etc."""
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

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk:
            original = PersonRoleType.objects.get(pk=self.pk)
            if original.code != self.code:
                raise ValueError("PersonRoleType.code is immutable")
        super().save(*args, **kwargs)
