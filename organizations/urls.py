# organizations/urls.py

from django.urls import path
from organizations.views.organization_list import organization_list
from organizations.views.organization_detail import organization_detail
from organizations.views.organization_add import organization_add
from organizations.views.organization_edit import organization_edit
from organizations.views.organization_deactivate import organization_deactivate
from organizations.views.organization_activate import organization_activate
from organizations.views.organization_role_add import organization_role_add
from organizations.views.organization_role_activate import organization_role_activate
from organizations.views.organization_role_deactivate import organization_role_deactivate
from organizations.views.org_role_type_list import org_role_type_list
from organizations.views.org_role_type_add import org_role_type_add
from organizations.views.org_role_type_edit import org_role_type_edit
from organizations.views.org_role_type_delete import org_role_type_delete

app_name = "organizations"

urlpatterns = [
    path('', organization_list, name='organization_list'),
    path('<int:pk>/', organization_detail, name='organization_detail'),
    path('add/', organization_add, name='organization_add'),
    path('<int:pk>/edit/', organization_edit, name='organization_edit'),
    path('<int:pk>/deactivate/', organization_deactivate, name='organization_deactivate'),
    path('<int:pk>/activate/', organization_activate, name='organization_activate'),
    path('<int:org_pk>/role/add/', organization_role_add, name='organization_role_add'),
    path('role/<int:pk>/activate/', organization_role_activate, name='organization_role_activate'),
    path('role/<int:pk>/deactivate/', organization_role_deactivate, name='organization_role_deactivate'),
    path('role-types/', org_role_type_list, name='org_role_type_list'),
    path('role-types/add/', org_role_type_add, name='org_role_type_add'),
    path('role-types/<int:pk>/edit/', org_role_type_edit, name='org_role_type_edit'),
    path('role-types/<int:pk>/delete/', org_role_type_delete, name='org_role_type_delete'),
]