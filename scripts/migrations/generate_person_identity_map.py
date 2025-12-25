import csv
import re
from pathlib import Path
from collections import defaultdict

# ---------- CONFIG ----------

V1_DIR = Path("/Volumes/Photos_Music_Web/web_projects/LCB_Library_v2/migration_data/exports")
OUTPUT_DIR = Path("/Volumes/Photos_Music_Web/web_projects/LCB_Library_v2/migration_data/derived")

TABLES = {
	"composer": {
		"file": "composer.csv",
		"first": "first_name",
		"last": "last_name",
	},
	"arranger": {
		"file": "arranger.csv",
		"first": "first_name",
		"last": "last_name",
	},
	"guest": {
		"file": "guest.csv",
		"first": "first_name",
		"last": "last_name",
	},
	"conductor": {
		"file": "conductor.csv",
		"first": "first_name",
		"last": "last_name",
		"title": "title",
		"middle": "middle_initial",
	},	
}

# ------------- HELPERS ------------

def normalize_name(first, last):
	def clean(s):
		return re.sub(r"[^\w]", "", s.strip().lower())
	return f"{clean(first)}_{clean(last)}"
	
def build_display_name(row, table):
	if table != "conductor":
		return ""
		
	title = row.get("title", "").strip()
	middle = row.get("middle_initial", "").strip()
	first = row["first_name"].strip()
	last = row["last_name"].strip()
	
	parts = []
	if title:
		parts.append(title)
	parts.append(first)
	if middle:
		parts.append(middle)
	parts:append(last)
	
	return " ".join(parts)
	
# ---------- MAIN ----------

def main():
	OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
	
	identity_rows = []
	person_index = {}
	person_counter = 1
	
	for table, cfg in TABLES.items():
		path = V1_DIR / cfg["file"]
		if not path.exists():
			raise FileNotFoundError(path)
			
		with path.open(newline="", encoding="utf-8") as f:
			reader = csv.DictReader(f)
			for row in reader:
				first = row[cfg["first"]]
				last = row[cfg["last"]]
				norm = normalize_name(first, last)
				
				if norm not in person_index:
					person_key = f"P{person_counter:04d}"
					person_index[norm] = person_key
					person_counter += 1
				else:
					person_key = person_index[norm]
					
				display_override = build_display_name(row, table)
				
				identity_rows.append({
					"v1_table": table,
					"v1_id": row["id"],
					"normalized_name": norm,
					"person_key": person_key,
					"display_name_override": display_override,
				})
				
	# Write person_identity_map.csv
	identity_path = OUTPUT_DIR / "person_identity_map.csv"
	with identity_path.open("w", newline="", encoding="utf-8") as f:
		writer = csv.DictWriter(
			f,
			fieldnames=[
				"v1_table",
				"v1_id",
				"normalized_name",
				"person_key",
				"display_name_override",
			],
		)
		writer.writeheader()
		writer.writerows(identity_rows)
		
	# Build person_table_import.csv
	seen = {}
	for row in identity_rows:
		key = row["person_key"]
		if key not in seen:
			first, last = row["normalized_name"].split("_", 1)
			seen[key] = {
				"person_key": key,
				"first_name": first.title(),
				"last_name": last.title(),
				"display_name": row["display_name_override"],
			}
		elif row["display_name_override"]:
			seen[key]["display_name"] = row["display_name_override"]
			
	person_table_path = OUTPUT_DIR / "person_table_import.csv"
	with person_table_path.open("w", newline="", encoding="utf-8") as f:
		writer = csv.DictWriter(
			f,
			fieldnames=["person_key", "first_name", "last_name", "display_name"],
		)
		writer.writeheader()
		writer.writerows(seen.values())
		
	# Summary
	print("=== Phase 3C Summary ===")
	print(f"Total v1 rows processed: {len(identity_rows)}")
	print(f"Unique persons created: {len(seen)}")
	print(f"Output written to: {OUTPUT_DIR.resolve()}")
	
if __name__ == "__main__":
	main()