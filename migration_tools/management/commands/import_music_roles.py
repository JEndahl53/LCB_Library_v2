# migration_tools/management/commands/import_music_roles.py

import csv
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from people.models import Person, PersonRoleType
from music.models import Music, MusicRole


class Command(BaseCommand):
    help = "Import music roles (COMPOSER, ARRANGER) from v1 CSVs."

    def add_arguments(self, parser):
        parser.add_argument("--v1-dir", default="migration_data/exports")
        parser.add_argument("--identity-csv", default="migration_data/derived/person_identity_map.csv")
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **opts):
        v1_dir = Path(opts["v1_dir"])
        identity_csv = Path(opts["identity_csv"])
        dry = opts["dry_run"]

        if not identity_csv.exists():
            raise CommandError(identity_csv)

        # (v1_table, v1_id) -> person_key
        v1_to_key = {}
        with identity_csv.open(newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                v1_to_key[(r["v1_table"], r["v1_id"])] = r["person_key"]

        role_by_code = {
            "COMPOSER": PersonRoleType.objects.get(code="COMPOSER"),
            "ARRANGER": PersonRoleType.objects.get(code="ARRANGER"),
        }

        total = created = skipped = 0

        @transaction.atomic
        def run():
            nonlocal total, created, skipped
            specs = [
                ("music_composer.csv", "composer", "composer_id", "music_id", "COMPOSER"),
                ("music_arranger.csv", "arranger", "arranger_id", "music_id", "ARRANGER"),
            ]
            for fname, table_key, person_col, music_col, role_code in specs:
                path = v1_dir / fname
                if not path.exists():
                    raise CommandError(path)

                with path.open(newline="", encoding="utf-8") as f:
                    for r in csv.DictReader(f):
                        total = total + 1
                        person_key = v1_to_key.get((table_key, r[person_col]))
                        if not person_key:
                            raise CommandError(f"No person_key for {fname} row {r}")

                        person = Person.objects.get(external_key=person_key)
                        music = Music.objects.get(id=r[music_col])
                        role = role_by_code[role_code]

                        exists = MusicRole.objects.filter(
                            person=person, role_type=role, music=music
                        ).exists()

                        if exists:
                            skipped = skipped + 1
                            continue

                        if not dry:
                            MusicRole.objects.create(
                                person=person, role_type=role, music=music
                            )
                            created = created + 1

        run()

        self.stdout.write(
            self.style.SUCCESS(
                f"Music roles: total={total}, created={created}, skipped={skipped}, dry_run={dry}"
            ))
