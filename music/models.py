# music/models.py
from django.db import models

# Create your models here.



class Music(models.Model):
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

    year_composed = models.CharField(
        max_length=20,
        blank=True,
        help_text="Year or range (free text, e.g.'1936', 'c. 1900')"
    )

    notes = models.TextField(blank=True)

    def __str__(self):
        return self.title


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

    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order']
        unique_together = ('music', 'person', 'role_type')

    def __str__(self):
        return f"{self.person} as {self.role_type}"