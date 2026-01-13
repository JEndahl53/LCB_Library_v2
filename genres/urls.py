# genres/urls.py

from django.urls import path
from genres.views.genre_list import genre_list
from genres.views.genre_add import genre_add
from genres.views.genre_delete import genre_delete
from genres.views.genre_edit import genre_edit

app_name = "genres"

urlpatterns = [
    path("", genre_list, name="genre_list"),
    path("add/", genre_add, name="genre_add"),
    path("<int:pk>/edit/", genre_edit, name="genre_edit"),
    path("<int:pk>/delete/", genre_delete, name="genre_delete"),
]
