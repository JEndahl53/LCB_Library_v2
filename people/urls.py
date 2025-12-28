# people/urls.py
from django.urls import path

from people.views.person_list import person_list

urlpatterns = [
    path("", person_list, name="person_list"),
]
