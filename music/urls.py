# music/urls.py

from django.urls import path
from music.views.music_list import music_list
from music.views.music_detail import music_detail

app_name = 'music'

urlpatterns = [
    path('', music_list, name='music_list'),
    path("<int:pk>/", music_detail, name="music_detail"),

]
