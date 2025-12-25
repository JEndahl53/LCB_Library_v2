# venues/models.py
from django.db import models

# Create your models here.


class Venue(models.Model):
    """
    Model representing a concert venue.
    """

    name = models.CharField(max_length=100)
    address = models.CharField(max_length=300, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    map_link = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    # Function to get output City, State ZIP
    def get_address2(self):
        parts = []
        if self.city:
            parts.append(self.city)

        state_zip_part = ""
        if self.state:
            state_zip_part += self.state
        if self.zip_code:
            state_zip_part += f" {self.zip_code}" if state_zip_part else self.zip_code

        if state_zip_part:
            parts.append(state_zip_part)

        return ", ".join(parts)

