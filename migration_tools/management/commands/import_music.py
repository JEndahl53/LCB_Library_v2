# migration_tools/management/commands/import_music.py

import csv
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from music.models import Music


class Command(BaseCommand):
    help = "Import Music from v1, preserving IDs and location fields."

    def add_arguments(self, parser):
        parser.add_argument("--csv", default="migration_data/exports/library_music.csv")
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **opts):
        path = Path(opts["csv"])
        dry = opts["dry_run"]

        if not path.exists():
            raise CommandError(path)

        rows = list(csv.DictReader(path.open(newline="", encoding="utf-8")))

        if dry:
            self.stdout.write(self.style.WARNING(
                f"DRY RUN: would import {len(rows)} music rows"
            ))
            return

        created = skipped = 0

        with transaction.atomic():
            for r in rows:
                obj, was_created = Music.objects.get_or_create(
                    id=r["id"],
                    defaults={
                        "title": r["title"],
                        "year_composed": str(r.get("year_published") or "").strip(),
                        "location_drawer": r.get("location_drawer") or None,
                        "location_number": r.get("location_number") or None,
                        "notes": r.get("notes", "").strip(),

                    },
                )
                if was_created:
                    created += 1
                else:
                    skipped += 1

        self.stdout.write(self.style.SUCCESS(
            f"Music import complete: created={created}, skipped={skipped}"
        ))
