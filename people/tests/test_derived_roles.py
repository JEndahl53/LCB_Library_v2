# people/tests/test_derived_roles.py

from django.test import TestCase

from people.models import Person, PersonRoleType
from music.models import Music, MusicRole
from concerts.models import Concert, ConcertRole

from people.services.derived_roles import (
    get_derived_roles_for_person,
    get_derived_roles_for_people,
)


# Test setup helpers

class DerivedRoleTestBase(TestCase):
    def setUp(self):
        self.composer = PersonRoleType.objects.create(
            code="COMPOSER",
            name="Composer",
            scope=PersonRoleType.RoleScope.MUSIC,
        )
        self.arranger = PersonRoleType.objects.create(
            code="ARRANGER",
            name="Arranger",
            scope=PersonRoleType.RoleScope.MUSIC,
        )
        self.conductor = PersonRoleType.objects.create(
            code="CONDUCTOR",
            name="Conductor",
            scope=PersonRoleType.RoleScope.CONCERT,
        )

        self.person = Person.objects.create(
            first_name="John",
            last_name="Smith",
            person_type=Person.INDIVIDUAL,
        )

# 1) Music role appears when music is active
class TestMusicRoles(DerivedRoleTestBase):
    def test_music_role_included_when_music_active(self):
        music = Music.objects.create(
            title="Test Piece",
            status=Music.OWNED,
        )

        MusicRole.objects.create(
            music=music,
            person=self.person,
            role_type=self.composer,
        )

        roles = get_derived_roles_for_person(self.person)

        self.assertEqual(roles, [self.composer])

# 2) ARCHIVED music suppresses role
    def test_music_role_suppressed_when_archived(self):
        music = Music.objects.create(
            title="Archived Piece",
            status=Music.ARCHIVED,
        )

        MusicRole.objects.create(
            music=music,
            person=self.person,
            role_type=self.composer,
        )

        roles = get_derived_roles_for_person(self.person)

        self.assertEqual(roles, [])


# 3) ON_LOAN music DOES NOT suppress role
    def test_music_role_visible_when_on_loan(self):
        music = Music.objects.create(
            title="Loaned Piece",
            status=Music.ON_LOAN,
        )

        MusicRole.objects.create(
            music=music,
            person=self.person,
            role_type=self.composer,
        )

        roles = get_derived_roles_for_person(self.person)

        self.assertEqual(roles, [self.composer])

# 4) Inactive MusicRole is ignored
    def test_inactive_music_role_ignored(self):
        music = Music.objects.create(
            title="Inactive Role Piece",
            status=Music.OWNED,
        )

        MusicRole.objects.create(
            music=music,
            person=self.person,
            role_type=self.composer,
            is_active=False,
        )

        roles = get_derived_roles_for_person(self.person)

        self.assertEqual(roles, [])

# 5) Concert role appears
class TestConcertRoles(DerivedRoleTestBase):
    def test_concert_role_included(self):
        concert = Concert.objects.create(title="Spring Concert")

        ConcertRole.objects.create(
            concert=concert,
            person=self.person,
            role_type=self.conductor,
        )

        roles = get_derived_roles_for_person(self.person)

        self.assertEqual(roles, [self.conductor])

# 6) Inactive role type is ignored
    def test_inactive_role_type_ignored(self):
        self.conductor.is_active = False
        self.conductor.save()

        concert = Concert.objects.create(title="Inactive Role Concert")

        ConcertRole.objects.create(
            concert=concert,
            person=self.person,
            role_type=self.conductor,
        )

        roles = get_derived_roles_for_person(self.person)

        self.assertEqual(roles, [])

# 7) Duplicate roles are de-duplicated
class TestDeDuplication(DerivedRoleTestBase):
    def test_duplicate_roles_are_deduplicated(self):
        music1 = Music.objects.create(title="Piece 1", status=Music.OWNED)
        music2 = Music.objects.create(title="Piece 2", status=Music.OWNED)

        MusicRole.objects.create(
            music=music1,
            person=self.person,
            role_type=self.composer,
        )
        MusicRole.objects.create(
            music=music2,
            person=self.person,
            role_type=self.composer,
        )

        roles = get_derived_roles_for_person(self.person)

        self.assertEqual(roles, [self.composer])

# 8) Bulk API works for multiple people
class TestBulkAPI(DerivedRoleTestBase):
    def test_bulk_role_computation(self):
        person2 = Person.objects.create(
            first_name="Jane",
            last_name="Doe",
            person_type=Person.INDIVIDUAL,
        )

        music = Music.objects.create(title="Shared Piece", status=Music.OWNED)

        MusicRole.objects.create(
            music=music,
            person=self.person,
            role_type=self.composer,
        )
        MusicRole.objects.create(
            music=music,
            person=person2,
            role_type=self.arranger,
        )

        people = Person.objects.prefetch_related(
            "music_roles__role_type",
            "music_roles__music",
            "concert_roles__role_type",
        )

        result = get_derived_roles_for_people(people)

        self.assertEqual(result[self.person.id], [self.composer])
        self.assertEqual(result[person2.id], [self.arranger])
