# migration_tools/management/commands/export_person_key_map.py

import csv
from pathlib import Path
from django.core.management.base import BaseCommand
from people.models import Person


class Command(BaseCommand):
    help = "Export person_key -> person.id mapping using external_key."

    def add_arguments(self, parser):
        parser.add_argument(
            "--out",
            default="migration_data/derived/person_key_to_id.csv",
            help="Output CSV path.",
        )

    def handle(self, *args, **options):
        out_path = Path(options["out"])
        out_path.parent.mkdir(parents=True, exist_ok=True)

        qs = Person.objects.exclude(external_key__isnull=True)

        with out_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["person_key", "person_id"],
            )
            writer.writeheader()
            for p in qs:
                writer.writerow({
                    "person_key": p.external_key,
                    "person_id": p.id,
                })

        self.stdout.write(self.style.SUCCESS(
            f"Exported {qs.count()} person_key mappings to {out_path}"
        ))
