# migration_tools/management/commands/import_people.py

import csv
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from people.models import Person


class Command(BaseCommand):
    help = "Import Person rows from person_table_import.csv (idempotent)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--csv",
            default="migration_data/derived/person_table_import.csv",
            help="Path to person_table_import.csv.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Parse and report counts but do not write to the DB.",
        )

    def handle(self, *args, **options):
        csv_path = Path(options["csv"])
        dry_run = options["dry_run"]

        if not csv_path.exists():
            raise CommandError(f"CSV not found: {csv_path}")

        # Best practice: store mapping by a stable key.
        # If Person has no 'external_key' field, we use (first_name, last_name) uniqueness during migration.from
        # If you DO have a migration-safe field, swap lookup to that immediately.
        created = 0
        updated = 0
        seen = 0

        rows = []
        with csv_path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                seen += 1
                rows.append(row)

        if dry_run:
            self.stdout.write(self.style.WARNING(
                f"DRY RUN: parsed {seen} rows from {csv_path}"
            ))
            return

        with transaction.atomic():
            for row in rows:
                first = (row.get("first_name") or "").strip()
                last = (row.get("last_name") or "").strip()
                display = (row.get("display_name") or "").strip()

                if not last:
                    raise CommandError(f"Invalid row (missing last_name): {row}")

                # Default assumption
                person_type = Person.INDIVIDUAL

                # Optional: if you later add a signal from identity_map
                # person_type = Person.ENSEMBLE

                # Idempotent lookup:
                # If duplicates exist in DB already, you should stop and fix before continuing.from
                obj, was_created = Person.objects.get_or_create(
                    first_name=first,
                    last_name=last,
                    defaults={},
                )

                # Optional display_name field support
                # Adjust this block if your Person model uses a different field name.
                if hasattr(obj, "display_name"):
                    target_display = display if display else f"{first} {last}"
                    if obj.display_name != target_display:
                        obj.display_name = target_display
                        obj.save(update_fields=["display_name"])
                        if not was_created:
                            updated += 1

                if was_created:
                    created += 1

        self.stdout.write(self.style.SUCCESS(
            f"People import complete. rows={seen}, created={created}, updated={updated}, total_people={Person.objects.count()}"
        ))
