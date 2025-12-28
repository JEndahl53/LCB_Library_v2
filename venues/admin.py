# venues/admin.py
from django.contrib import admin
from venues.models import Venue

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')
    search_fields = ('name', 'city')