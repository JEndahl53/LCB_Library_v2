# people/tests/test_person_queryset.py

from django.test import TestCase

from people.models import Person
from people.services.person_queryset import get_person_list_queryset

# Test setup


class PersonQuerysetTestBase(TestCase):
    def setUp(self):
        self.active_individual = Person.objects.create(
            first_name="Alice",
            last_name="Smith",
            person_type=Person.INDIVIDUAL,
            is_active=True,
        )

        self.inactive_individual = Person.objects.create(
            first_name="Bob",
            last_name="Smith",
            person_type=Person.INDIVIDUAL,
            is_active=False,
        )

        self.active_ensemble = Person.objects.create(
            last_name="City Band",
            person_type=Person.ENSEMBLE,
            is_active=True,
        )


# 1) Default queryset returns active only
class TestDefaultBehavior(PersonQuerysetTestBase):
    def test_default_returns_active_only(self):
        qs = get_person_list_queryset()

        self.assertIn(self.active_individual, qs)
        self.assertIn(self.active_ensemble, qs)
        self.assertNotIn(self.inactive_individual, qs)


# 2) Inactive filter works
class TestActiveFilter(PersonQuerysetTestBase):
    def test_inactive_only(self):
        qs = get_person_list_queryset(active="inactive")

        self.assertIn(self.inactive_individual, qs)
        self.assertNotIn(self.active_individual, qs)
        self.assertNotIn(self.active_ensemble, qs)


# 3) Active = all returns everything
def test_active_all(self):
    qs = get_person_list_queryset(active="all")

    self.assertIn(self.active_individual, qs)
    self.assertIn(self.inactive_individual, qs)
    self.assertIn(self.active_ensemble, qs)


# 4) Person type filtering
class TestPersonTypeFilter(PersonQuerysetTestBase):
    def test_individual_only(self):
        qs = get_person_list_queryset(person_type="individual")

        self.assertIn(self.active_individual, qs)
        self.assertNotIn(self.active_ensemble, qs)

    def test_ensemble_only(self):
        qs = get_person_list_queryset(person_type="ensemble")

        self.assertIn(self.active_ensemble, qs)
        self.assertNotIn(self.active_individual, qs)


# 5) Ordering is last_name, first_name
class TestOrdering(TestCase):
    def test_ordering_by_last_then_first_name(self):
        p1 = Person.objects.create(
            first_name="Charlie",
            last_name="Adams",
            person_type=Person.INDIVIDUAL,
        )
        p2 = Person.objects.create(
            first_name="Alice",
            last_name="Brown",
            person_type=Person.INDIVIDUAL,
        )
        p3 = Person.objects.create(
            first_name="Bob",
            last_name="Brown",
            person_type=Person.INDIVIDUAL,
        )

        qs = list(get_person_list_queryset(active="all"))

        self.assertEqual(qs, [p1, p2, p3])


# 6) Prefetching is present (non-brittle check)
class TestPrefetching(PersonQuerysetTestBase):
    def test_required_prefetches_present(self):
        qs = get_person_list_queryset()

        prefetches = set(qs._prefetch_related_lookups)

        self.assertIn("music_roles__role_type", prefetches)
        self.assertIn("music_roles__music", prefetches)
        self.assertIn("concert_roles__role_type", prefetches)
