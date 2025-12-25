# migration_tools/management/commands/import_concerts.py

import csv
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.dateparse import parse_datetime, parse_date

from concerts.models import Concert
from venues.models import Venue  # required for venue_id mapping


class Command(BaseCommand):
    help = "Import Concert rows from v1, preserving IDs and mapping core fields."

    def add_arguments(self, parser):
        parser.add_argument(
            "--csv",
            default="migration_data/exports/concerts_concert.csv",
            help="Path to v1 concert.csv",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Parse and report, but do not write to the database",
        )

    def handle(self, *args, **opts):
        path = Path(opts["csv"])
        dry = opts["dry_run"]

        if not path.exists():
            raise CommandError(f"CSV not found: {path}")

        rows = list(csv.DictReader(path.open(newline="", encoding="utf-8")))

        if dry:
            self.stdout.write(self.style.WARNING(
                f"DRY RUN: would import {len(rows)} Concert rows"
            ))
            return

        created = skipped = 0

        with transaction.atomic():
            for r in rows:
                # --- Parse date safely ---
                date_value = None
                if r.get("date"):
                    date_value = (
                        parse_datetime(r["date"])
                        or parse_date(r["date"])
                    )

                # --- Resolve venue (must already exist) ---
                venue = None
                venue_id = r.get("venue_id")
                if venue_id:
                    try:
                        venue = Venue.objects.get(id=venue_id)
                    except Venue.DoesNotExist:
                        raise CommandError(
                            f"Venue id={venue_id} not found for concert id={r['id']}"
                        )

                defaults = {
                    "title": r["title"].strip(),
                    "date": date_value,
                    "venue": venue,
                    "description": r.get("description", "").strip(),
                }

                # NOTE:
                # poster files are NOT copied during migration.
                # If v1 poster paths exist, we intentionally ignore them for now.
                # Poster files can be reattached later once media strategy is finalized.

                obj, was_created = Concert.objects.get_or_create(
                    id=r["id"],
                    defaults=defaults,
                )

                if was_created:
                    created += 1
                else:
                    skipped += 1

        self.stdout.write(self.style.SUCCESS(
            f"Concert import complete: created={created}, skipped={skipped}"
        ))
