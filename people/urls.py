# people/urls.py
from django.urls import path

from people.views.person_list import person_list
from people.views.person_detail import person_detail
from people.views.person_edit import person_edit
from people.views.person_delete import person_delete
from people.views.person_reactivate import person_reactivate
from people.views.person_add import person_add
from people.views.role_type_list import role_type_list
from people.views.role_type_add import role_type_add
from people.views.role_type_edit import role_type_edit
from people.views.role_type_delete import role_type_delete

app_name = "people"

urlpatterns = [
    path("", person_list, name="person_list"),
    path("<int:pk>/", person_detail, name="person_detail"),
    path('<int:pk>/edit/', person_edit, name='person_edit'),
    path('<int:pk>/delete/', person_delete, name='person_delete'),
    path('<int:pk>/reactivate/', person_reactivate, name='person_reactivate'),
    path('add/', person_add, name='person_add'),
    path('role-types/', role_type_list, name='role_type_list'),
    path('role-types/add/', role_type_add, name='role_type_add'),
    path('role-types/<int:pk>/edit/', role_type_edit, name='role_type_edit'),
    path('role-types/<int:pk>/delete/', role_type_delete, name='role_type_delete'),
]
