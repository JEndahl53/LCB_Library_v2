# concerts/models.py

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

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('concert_detail', args=[self.pk])


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

    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order']
        unique_together = ('concert', 'person', 'role_type')

    def __str__(self):
        return f"{self.person} -- {self.role_type}"
