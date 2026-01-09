import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from organizations.models import Organization, OrganizationRole, OrganizationRoleType

User = get_user_model()

@pytest.fixture
def staff_user(db):
    return User.objects.create_user(username='staff', password='password', is_staff=True)

@pytest.fixture
def organization(db):
    return Organization.objects.create(name='Test Org')

@pytest.fixture
def role_type(db):
    return OrganizationRoleType.objects.create(code='TEST', name='Test Role')

@pytest.mark.django_db
class TestOrganizationViews:
    def test_organization_add(self, client, staff_user):
        client.login(username='staff', password='password')
        url = reverse('organizations:organization_add')
        response = client.get(url)
        assert response.status_code == 200
        
        response = client.post(url, {'name': 'New Org', 'is_active': True})
        assert response.status_code == 302
        assert Organization.objects.filter(name='New Org').exists()

    def test_organization_detail(self, client, staff_user, organization, role_type):
        client.login(username='staff', password='password')
        
        # Add a role
        OrganizationRole.objects.create(organization=organization, role_type=role_type)
        
        # Add a music link
        from music.models import Music
        from organizations.models import MusicOrganizationLink
        music = Music.objects.create(title='Test Piece')
        MusicOrganizationLink.objects.create(music=music, organization=organization, role_type=role_type)
        
        url = reverse('organizations:organization_detail', args=[organization.pk])
        response = client.get(url)
        assert response.status_code == 200
        content = response.content.decode()
        assert 'Test Org' in content
        assert 'Test Role' in content
        assert 'Test Piece' in content
        assert 'Total Unique Music Pieces:' in content
        assert '1' in content  # Stats count

    def test_organization_edit(self, client, staff_user, organization):
        client.login(username='staff', password='password')
        url = reverse('organizations:organization_edit', args=[organization.pk])
        response = client.get(url)
        assert response.status_code == 200
        
        response = client.post(url, {'name': 'Updated Org', 'is_active': True})
        assert response.status_code == 302
        organization.refresh_from_db()
        assert organization.name == 'Updated Org'

    def test_organization_deactivate(self, client, staff_user, organization):
        client.login(username='staff', password='password')
        url = reverse('organizations:organization_deactivate', args=[organization.pk])
        response = client.post(url)
        assert response.status_code == 302
        organization.refresh_from_db()
        assert not organization.is_active

    def test_organization_activate(self, client, staff_user, organization):
        organization.is_active = False
        organization.save()
        client.login(username='staff', password='password')
        url = reverse('organizations:organization_activate', args=[organization.pk])
        response = client.get(url)
        assert response.status_code == 302
        organization.refresh_from_db()
        assert organization.is_active

@pytest.mark.django_db
class TestOrganizationRoleViews:
    def test_organization_role_add(self, client, staff_user, organization, role_type):
        client.login(username='staff', password='password')
        url = reverse('organizations:organization_role_add', args=[organization.pk])
        response = client.get(url)
        assert response.status_code == 200
        
        response = client.post(url, {'role_type': role_type.pk, 'notes': 'Test notes'})
        assert response.status_code == 302
        assert OrganizationRole.objects.filter(organization=organization, role_type=role_type).exists()

    def test_organization_role_deactivate(self, client, staff_user, organization, role_type):
        role = OrganizationRole.objects.create(organization=organization, role_type=role_type)
        client.login(username='staff', password='password')
        url = reverse('organizations:organization_role_deactivate', args=[role.pk])
        response = client.get(url)
        assert response.status_code == 302
        role.refresh_from_db()
        assert not role.is_active

    def test_organization_role_activate(self, client, staff_user, organization, role_type):
        role = OrganizationRole.objects.create(organization=organization, role_type=role_type, is_active=False)
        client.login(username='staff', password='password')
        url = reverse('organizations:organization_role_activate', args=[role.pk])
        response = client.get(url)
        assert response.status_code == 302
        role.refresh_from_db()
        assert role.is_active
