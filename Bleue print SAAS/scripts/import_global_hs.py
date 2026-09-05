"""Importe la nomenclature mondiale HS CSV dans PostgreSQL."""

import csv
import os
from pathlib import Path

import psycopg


CSV_PATH = Path(__file__).resolve().parents[1] / "database" / "global_hs_codes.csv"


def import_codes(database_url: str, csv_path: Path = CSV_PATH) -> int:
    rows = []
    with csv_path.open("r", encoding="utf-8-sig", newline="") as source:
        for row in csv.DictReader(source):
            rows.append(
                (
                    "HS2022",
                    row["section"],
                    row["hscode"],
                    row.get("description_fr_a_completer") or row["description_en"],
                    row["parent"],
                    {"chapitre": 2, "position": 4, "sous_position": 6, "sous_position_intermediaire": 5}[row["niveau"]],
                    "Base fournie BLEUE PRINT SH DATA; UN Comtrade / WCO, HS2022",
                )
            )

    with psycopg.connect(database_url) as connection:
        with connection.cursor() as cursor:
            cursor.executemany(
                """
                INSERT INTO global_hs_codes
                    (nomenclature_version, section, hscode, description, parent_hscode, level, source)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (nomenclature_version, hscode) DO UPDATE SET
                    section = EXCLUDED.section,
                    description = EXCLUDED.description,
                    parent_hscode = EXCLUDED.parent_hscode,
                    level = EXCLUDED.level,
                    source = EXCLUDED.source,
                    updated_at = NOW()
                """,
                rows,
            )
        connection.commit()

    return len(rows)


if __name__ == "__main__":
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise SystemExit("Definir DATABASE_URL avant l'import.")
    print(f"{import_codes(database_url)} codes HS importes.")