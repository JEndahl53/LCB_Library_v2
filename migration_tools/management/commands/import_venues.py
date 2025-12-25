# migration_tools/management/commands/import_venues.py

import csv
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from venues.models import Venue


class Command(BaseCommand):
    help = "Import Venue rows from v1, preserving IDs."

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv',
            default="migration_data/exports/venue.csv",
            help='Path to the CSV file to import',
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Parse and report, but do not write to the DB.",
        )

    def handle(self, *args, **opts):
        path = Path(opts['csv'])
        dry = opts['dry_run']

        if not path.exists():
            raise CommandError(f"CSV not found: {path}")

        rows = list(csv.DictReader(path.open(newline="", encoding="utf-8")))

        if dry:
            self.stdout.write(self.style.WARNING(
                f"DRY RUN: would import {len(rows)} Venue rows"
            ))
            return

        created = skipped = 0

        with transaction.atomic():
            for r in rows:
                obj, was_created = Venue.objects.get_or_create(
                    id=r["id"],
                    defaults={
                        "name": r["name"].strip(),
                        "address": r["address"].strip(),
                        "city": r["city"].strip(),
                        "state": r["state"].strip(),
                        "zip_code": r["zip_code"].strip(),
                        "map_link": r["map_link"].strip(),
                        "notes": r["notes"].strip(),
                    },
                )
                if was_created:
                    created += 1
                else:
                    skipped += 1

        self.stdout.write(self.style.SUCCESS(
            f"Venue import complete: created:{created}, skipped:{skipped}"
        ))