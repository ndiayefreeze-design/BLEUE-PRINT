# BLEUE PRINT

BLEUE PRINT est un SaaS de calcul de conformité douanière pour le Sénégal et la zone CEDEAO/UEMOA.

## Objectif

Aider un importateur ou un commissionnaire à estimer le coût total d'une marchandise avant déclaration officielle, sans se substituer à GAINDE ni à la classification tarifaire officielle d'un commissionnaire agréé.

> Estimation à titre indicatif — la classification tarifaire officielle et la déclaration en douane relèvent exclusivement d'un commissionnaire en douane agréé via GAINDE.

## Hypothèses de démarrage

- Stack par défaut : Python + FastAPI + Postgres
- Extraction du TEC à partir du PDF officiel publié par les douanes sénégalaises
- Base de données relationnelle PostgreSQL, table `codes_sh` dédiée
- Aucune dépense d'hébergement ou de nom de domaine n'est engagée sans validation explicite

## Structure du projet

```text
.
├── README.md
├── requirements.txt
├── backend/
│   └── app/
│       ├── main.py
│       └── config.py
├── database/
│   └── schema.sql
├── scripts/
│   └── tec_extraction/
│       ├── extract_tec.py
│       └── README.md
├── docs/
│   ├── brief_lancement_bleue_print.md
│   ├── phase_1_extraction_plan.md
│   └── validation_phase_1.md
└── .gitignore
```

## Phases de lancement

1. Phase 1 — Extraire et structurer le TEC
2. Phase 2 — Matching produit → code SH
3. Phase 3 — Calcul complet et génération de devis
4. Phase 4 — Cibler 3 à 5 commissionnaires agréés à Dakar
5. Phase 5 — Ouvrir aux PME importatrices et à l'API

## Règles de travail

- Ne jamais présenter un calcul comme une classification officielle
- Ne jamais lancer une phase avant validation de la précédente
- Toujours proposer plusieurs codes SH candidats, jamais un unique résultat tranché
- Produire des livrables concrets et vérifiables à chaque étape

## Démarrage rapide

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Prochaine étape

La Phase 1 est lancée : extraction structurée du TEC, contrôle de qualité et génération d’un rapport de validation exploitable.

### Exécution Phase 1

```bash
python scripts/tec_extraction/extract_tec.py --output docs/phase_1_quality_report.json
```

> Le script est conçu pour traiter le PDF réel si celui-ci est fourni dans le workspace. En l’absence du PDF officiel, il génère un rapport de démonstration `demo_mode` pour maintenir la structure et la validation sans masquer la réalité.

### Nomenclature mondiale HS

Le fichier `database/global_hs_codes.csv` contient la nomenclature mondiale HS 2022
fournie dans `BLEUE PRINT SH DATA`, avec les codes, niveaux, parents et descriptions.
Les fichiers `sections_fr.csv`, `bandes_tarifaires_tec_cedeao.csv` et
`taxes_parafiscales_senegal.csv` sont également utilisés comme sources de référence.
Pour importer la nomenclature dans PostgreSQL :

```bash
set DATABASE_URL=postgresql://user:password@localhost:5432/bleue_print
python scripts/import_global_hs.py
```

Puis importer les bandes TEC et taxes Sénégal :

```bash
python scripts/import_tariffs.py
```

Cette nomenclature fournit les codes et libellés internationaux. Les taux de droits
restent dans `tariff_profiles` et doivent être validés selon le pays, l'origine et le
TEC en vigueur.
