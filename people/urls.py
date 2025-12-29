# people/urls.py
from django.urls import path

from people.views.person_list import person_list
from people.views.person_detail import person_detail
from people.views.person_edit import person_edit
from people.views.person_delete import person_delete
from people.views.person_reactivate import person_reactivate
from people.views.person_add import person_add

urlpatterns = [
    path("", person_list, name="person_list"),
    path("<int:pk>/", person_detail, name="person_detail"),
    path('<int:pk>/edit/', person_edit, name='person_edit'),
    path('<int:pk>/delete/', person_delete, name='person_delete'),
    path('<int:pk>/reactivate/', person_reactivate, name='person_reactivate'),
    path('add/', person_add, name='person_add'),
]
