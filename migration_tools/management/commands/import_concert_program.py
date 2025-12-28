# migration_tools/management/commands/import_concert_program.py

import csv
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from concerts.models import Concert, ConcertProgram
from  music.models import Music


class Command(BaseCommand):
    help = 'Import concert program order from v1 concerts_concertprogram.csv'

    def add_arguments(self, parser):
        parser.add_argument(
            "--csv",
            default="migration_data/exports/concerts_concertprogram.csv",
            help="Path to the CSV file containing concert program data",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Parse and report, but do not write to the database.",
        )

    def handle(self, *args, **opts):
        path = Path(opts["csv"])
        dry = opts["dry_run"]

        if not path.exists():
            raise CommandError(f"CSV not found at {path}")

        rows = list(csv.DictReader(path.open(newline="", encoding="utf-8")))

        if dry:
            self.stdout.write(self.style.WARNING(
                f"Dry run: would import {len(rows)} program rows."
            ))
            return

        created = skipped = 0

        with transaction.atomic():
            for r in rows:
                concert = Concert.objects.get(id=r["concert_id"])
                music = Music.objects.get(id=r["music_id"])
                order = int(r["performance_order"])

                exists = ConcertProgram.objects.filter(
                    concert=concert,
                    program_order=order,
                ).exists()

                if exists:
                    skipped += 1
                    continue

                ConcertProgram.objects.create(
                    concert=concert,
                    music=music,
                    program_order=order,
                    notes=r.get("notes", "").strip(),
                )
                created += 1
            self.stdout.write(self.style.SUCCESS(
                f"Concert program import complete: created={created}, skipped={skipped}"
            ))
