# migration_tools/management/commands/import_concert_roles.py

import csv
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from people.models import Person, PersonRoleType
from concerts.models import Concert, ConcertRole


class Command(BaseCommand):
    help = "Import concert roles (CONDUCTOR, GUEST) from v1 CSVs."

    def add_arguments(self, parser):
        parser.add_argument('--v1-dir', default="migration_data/exports")
        parser.add_argument('--identity-csv', default="migration_data/derived/person_identity_map.csv")
        parser.add_argument('--dry-run', action="store_true")

    def handle(self, *args, **opts):
        v1_dir = Path(opts['v1_dir'])
        identity_csv = Path(opts['identity_csv'])
        dry = opts['dry_run']

        if not identity_csv.exists():
            raise CommandError(f"Identity CSV file not found: {identity_csv}")

        v1_to_key = {}
        with identity_csv.open(newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                v1_to_key[(r["v1_table"], r["v1_id"])] = r["person_key"]

        role_by_code = {
            "CONDUCTOR": PersonRoleType.objects.get(code="CONDUCTOR"),
            "GUEST": PersonRoleType.objects.get(code="GUEST"),
        }

        total = created = skipped = 0

        @transaction.atomic
        def run():
            nonlocal total, created, skipped
            specs = [
                ("concert_conductor.csv", "conductor", "conductor_id", "concert_id", "CONDUCTOR"),
                ("concert_guest.csv", "guest", "guest_id", "concert_id", "GUEST"),
            ]
            for fname, table_key, person_col, concert_col, role_code in specs:
                path = v1_dir / fname
                if not path.exists():
                    raise CommandError(f"CSV file not found: {path}")

                with path.open(newline="", encoding="utf-8") as f:
                    for r in csv.DictReader(f):
                        total += 1
                        person_key = v1_to_key.get((table_key, r[person_col]))
                        if not person_key:
                            raise CommandError(f"No person_key for {fname} row {r}")

                        person = Person.objects.get(external_key=person_key)
                        concert = Concert.objects.get(id=r[concert_col])
                        role = role_by_code[role_code]

                        exists = ConcertRole.objects.filter(
                            person=person, concert=concert, role_type=role
                        ).exists()

                        if exists:
                            skipped += 1
                            continue

                        if not dry:
                            ConcertRole.objects.create(
                                person=person, concert=concert, role_type=role
                            )
                        created += 1

        run()

        self.stdout.write(self.style.SUCCESS(
            f"Concert toles: total={total}, created={created}, skipped={skipped}, dry_run={dry}"
        ))
