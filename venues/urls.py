# venues/urls.py

from django.urls import path
from venues.views.venue_list import venue_list
from venues.views.venue_add import venue_add
from venues.views.venue_edit import venue_edit
from venues.views.venue_delete import venue_delete

app_name = "venues"

urlpatterns = [
    path('', venue_list, name='venue_list'),
    path('add/', venue_add, name='venue_add'),
    path('<int:pk>/edit/', venue_edit, name='venue_edit'),
    path('<int:pk>/delete/', venue_delete, name='venue_delete'),
]
