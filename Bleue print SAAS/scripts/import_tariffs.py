"""Importe les bandes TEC et taxes Senegal fournies dans PostgreSQL."""

import csv
import os
from pathlib import Path

import psycopg


DATABASE_DIR = Path(__file__).resolve().parents[1] / "database"


def import_tariffs(database_url: str) -> tuple[int, int]:
    with psycopg.connect(database_url) as connection:
        with connection.cursor() as cursor:
            with (DATABASE_DIR / "bandes_tarifaires_tec_cedeao.csv").open(encoding="utf-8-sig", newline="") as source:
                bands = list(csv.DictReader(source))
            cursor.executemany(
                """
                INSERT INTO tec_tariff_bands (category, customs_rate, description, approximate_line_count, source)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (category) DO UPDATE SET
                    customs_rate = EXCLUDED.customs_rate,
                    description = EXCLUDED.description,
                    approximate_line_count = EXCLUDED.approximate_line_count,
                    source = EXCLUDED.source
                """,
                [(int(row["categorie"]), float(row["taux_droit_douane"].strip("%")) / 100, row["description"], row["nombre_lignes_tarifaires_approx"], row["source"]) for row in bands],
            )

            with (DATABASE_DIR / "taxes_parafiscales_senegal.csv").open(encoding="utf-8-sig", newline="") as source:
                taxes = list(csv.DictReader(source))
            cursor.executemany(
                """
                INSERT INTO senegal_import_taxes (code, name, rate, base, source, notes)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (code) DO UPDATE SET
                    name = EXCLUDED.name, rate = EXCLUDED.rate, base = EXCLUDED.base,
                    source = EXCLUDED.source, notes = EXCLUDED.notes
                """,
                [(row["code"], row["nom_complet"], row["taux"], row["assiette"], row["source"], row["notes"]) for row in taxes],
            )
        connection.commit()
    return len(bands), len(taxes)


if __name__ == "__main__":
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise SystemExit("Definir DATABASE_URL avant l'import.")
    bands_count, taxes_count = import_tariffs(database_url)
    print(f"{bands_count} bandes TEC et {taxes_count} taxes importees.")