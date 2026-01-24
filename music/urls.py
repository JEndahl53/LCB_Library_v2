# music/urls.py

from django.urls import path

from music.views.music_list import music_list
from music.views.music_detail import music_detail
from music.views.music_add import music_add
from music.views.music_edit import music_edit
from music.views.music_role_add import music_role_add
from music.views.music_roles_edit import music_roles_edit
from music.views.music_role_delete import music_role_delete
from music.views.music_org_link_add import music_org_link_add
from music.views.music_org_link_delete import music_org_link_delete
from music.views.music_genres_assign import music_genres_assign
from music.views.music_genre_quick_add_hx import music_genre_quick_add_hx
from music.views.music_person_quick_add_hx import music_person_quick_add_hx
from music.views.music_org_quick_add_hx import music_org_quick_add_hx

app_name = 'music'

urlpatterns = [
    path('', music_list, name='music_list'),
    path('add/', music_add, name='music_add'),
    path("<int:pk>/", music_detail, name="music_detail"),
    path("<int:pk>/edit/", music_edit, name="music_edit"),

    path(
        "<int:music_pk>/roles/add/",
        music_role_add,
        name="music_role_add",
    ),
    path(
        "<int:music_pk>/roles/<int:role_pk>/delete/",
        music_role_delete,
        name="music_role_delete",
    ),
    path(
        "<int:pk>/roles/",
        music_roles_edit,
        name="music_roles_edit",
    ),
    path(
        "<int:music_pk>/organizations/add/",
        music_org_link_add,
        name="music_org_link_add",
    ),
    path(
        "<int:music_pk>/organizations/<int:link_pk>/delete/",
        music_org_link_delete,
        name="music_org_link_delete",
    ),
    path(
        "<int:pk>/people/quick-add/",
        music_person_quick_add_hx,
        name="music_person_quick_add_hx",
    ),
    path(
        "<int:music_pk>/organizations/<int:link_pk>/delete/",
        music_org_link_delete,
        name="music_org_link_delete",
    ),

    # Genre add
    path(
        "<int:pk>/genres/",
        music_genres_assign,
        name="music_genres_assign",
    ),
    path(
        "<int:pk>/genres/quick-add/",
        music_genre_quick_add_hx,
        name="music_genre_quick_add_hx",
    ),
    path(
        "<int:pk>/organizations/quick-add/",
        music_org_quick_add_hx,
        name="music_org_quick_add_hx",
    ),
]
