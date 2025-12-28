from people.models import PersonRoleType, Person
from music.models import Music, MusicRole
import pytest
from django.core.exceptions import ValidationError

# Create your tests here.


@pytest.mark.django_db
def test_music_role_rejects_concert_scope(db):
    concert_role = PersonRoleType.objects.create(
        code="CONDUCTOR",
        name="Conductor",
        scope=PersonRoleType.RoleScope.CONCERT,
    )

    person = Person.objects.create(
        first_name="John",
        last_name="Doe",
    )

    music = Music.objects.create(
        title="Test Music",
    )

    role = MusicRole(
        music=music,
        person=person,
        role_type=concert_role,
    )

    with pytest.raises(ValidationError):
        role.full_clean()
