# people/services/derived_roles.py

"""
Purpose (Restated)
Provide a single authoritative
mechanism to compute derived role badges for one or more Person objects, based on:
    MusicRole
    ConcertRole
    role lifecycle rules
    music status semantics
This service is read-only, deterministic, and side-effect free.

Usage:
    Single person - get_derived_roles_for_person(person) -> list[RoleType]
    Multi-person - get_derived_roles_for_people(people) -> dict[person_id, list[RoleType]]

Output:
    {
    person.id: [RoleType, RoleType, ...],
    ...
}
Requirements:
Service does not perform prefetching, protect against missing prefetches, and may assert in debug mode.
    .prefetch_related(
    "music_roles__role_type",
    "music_roles__music",
    "concert_roles__role_type",
)
Inclusion Rules (Embedded Logic)
A RoleType is included if and only if:
From MusicRole
    music_role.is_active == True
    music_role.music.status != ARCHIVED
    music_role.role_type.is_active == True
From ConcertRole
    concert_role.is_active == True
    concert_role.role_type.is_active == True

"""

from __future__ import annotations

from collections import defaultdict
from typing import Iterable, Dict, List, Set

from people.models import Person, PersonRoleType
from music.models import Music


def _role_type_sort_key(rt: PersonRoleType):
    """
    Deterministic ordering for badges. PersonRoleType is ordered by name in Meta
    but we sort explicitly to avoid depending on query ordering or set ordering.
    """
    return (rt.name or "", rt.code or "")


def _music_contributes_roles(music: Music) -> bool:
    """
    Roles remain visible for ON_LOAN / BORROWED / RENTAL, etc.
    Only ARCHIVED suppresses role visibility
    """
    return music.status != Music.ARCHIVED


def get_derived_roles_for_person(person: Person) -> List[PersonRoleType]:
    """
    Compute derived role badges for a single Person.

    Inclusion rules:
      - MusicRole counts if:
          MusicRole.is_active == True AND music.status != ARCHIVED AND role_type.is_active == True
      - ConcertRole counts if:
          ConcertRole.is_active == True AND role_type.is_active == True

    Prefetch required by caller
      - music_roles__role_type
      - music_roles__music
      - concert_roles__role_type
    """
    role_types: Set[PersonRoleType] = set()

    for mr in person.music_roles.all():
        if not mr.is_active:
            continue
        if not _music_contributes_roles(mr.music):
            continue
        if mr.role_type and mr.role_type.is_active:
            role_types.add(mr.role_type)

    for cr in person.concert_roles.all():
        if not cr.is_active:
            continue
        if cr.role_type and cr.role_type.is_active:
            role_types.add(cr.role_type)

    return sorted(role_types, key=_role_type_sort_key)


def get_derived_roles_for_people(people: Iterable[Person]) -> Dict[int, List[PersonRoleType]]:
    """
    Bulk-derived role computation for list views.

    Returns:
        { person_id: [PersonRoleType, ...] }

    Prefetch required by caller:
    - music_roles__role_type
    - music_roles__music
    - concert_roles__role_type
    """
    buckets: Dict[int, Set[PersonRoleType]] = defaultdict(set)

    for person in people:
        pid = person.id
        buckets[pid]  # ensure key exists even if no roles

        for mr in person.music_roles.all():
            if not mr.is_active:
                continue
            if not _music_contributes_roles(mr.music):
                continue
            if mr.role_type and mr.role_type.is_active:
                buckets[pid].add(mr.role_type)

        for cr in person.concert_roles.all():
            if not cr.is_active:
                continue
            if cr.role_type and cr.role_type.is_active:
                buckets[pid].add(cr.role_type)

    return {
        pid: sorted(role_types, key=_role_type_sort_key)
        for pid, role_types in buckets.items()
    }
