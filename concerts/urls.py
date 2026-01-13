# concerts/urls.py

from django.urls import path
from concerts.views.concert_list import concert_list
from concerts.views.concert_add import concert_add
from concerts.views.concert_edit import concert_edit
from concerts.views.concert_detail import concert_detail
from concerts.views.concert_delete import concert_delete
from concerts.views.concert_program_edit import concert_program_edit
from concerts.views.concert_program_delete import concert_program_delete
from concerts.views.concert_roles_edit import concert_roles_edit
from concerts.views.concert_role_delete import concert_role_delete

app_name = "concerts"

urlpatterns = [
    path('', concert_list, name='concert_list'),
    path('add/', concert_add, name='concert_add'),
    path('<int:pk>/', concert_detail, name='concert_detail'),
    path('<int:pk>/edit/', concert_edit, name='concert_edit'),
    path('<int:pk>/delete/', concert_delete, name='concert_delete'),

    # Program management
    path('<int:pk>/program/', concert_program_edit, name='concert_program_edit'),
    path('<int:concert_pk>/program/<int:program_pk>/delete/', concert_program_delete, name='concert_program_delete'),

    # Role management
    path('<int:pk>/roles/', concert_roles_edit, name='concert_roles_edit'),
    path('<int:concert_pk>/roles/<int:role_pk>/delete/', concert_role_delete, name='concert_role_delete'),
]
