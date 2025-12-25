# migrations_tools/management/commands/seed_role_types.py

from django.core.management.base import BaseCommand
from django.db import transaction

from people.models import PersonRoleType

ROLE_TYPES = [
    ("COMPOSER", "Composer"),
    ("ARRANGER", "Arranger"),
    ("CONDUCTOR", "Conductor"),
    ("GUEST", "Guest"),
]

class Command(BaseCommand):
    HELP = "Seed canonical PersonRoleType rows (idempotent)."

    @transaction.atomic
    def handle(self, *args, **options):
        created = 0
        updated = 0

        for code, name in ROLE_TYPES:
            obj, was_created = PersonRoleType.objects.get_or_create(
                code=code,
                defaults={'name': name, 'is_active': True},
            )
            if was_created:
                created += 1
            else:
                # Keep code stable; allow name/is_active to be corrected
                changed = False
                if obj.name != name:
                    obj.name = name
                    changed = True
                if obj.is_active is not True:
                    obj.is_active = True
                    changed = True
                if changed:
                    obj.save(update_fields=['name', 'is_active'])
                    updated += 1

        self.stdout.write(self.style.SUCCESS(
            f'Role types seeded. created={created}, updated={updated}, total={PersonRoleType}'
        ))