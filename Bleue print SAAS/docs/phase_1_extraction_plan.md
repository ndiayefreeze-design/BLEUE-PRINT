# Phase 1 — Extraction et structuration du TEC

## Objectif

Extraire les lignes tarifaires du PDF officiel du Tarif Extérieur Commun (TEC) CEDEAO/UEMOA, en conserver les données structurées dans une table `codes_sh`, puis mesurer la qualité d'extraction.

## Livrables

- Script Python de parsing du PDF officiel
- Table `codes_sh` dans PostgreSQL
- Fichier de journal / rapport de qualité
- Liste des lignes à vérifier manuellement

## Phase d'extraction

1. Télécharger le PDF officiel du TEC sur le site des douanes sénégalaises
2. Identifier les colonnes clés : code SH, libellé, droit, RS, PC, TVA, taxes spécifiques
3. Extraire le document en pixels puis en table structurée
4. Normaliser les libellés et les codes
5. Stocker dans `codes_sh`

## Mécanique technique

- Utiliser `pdfplumber` pour lire les tables et vérifier le texte
- Utiliser `camelot` si les tables sont fragmentées ou en colonnes multiples
- Nettoyer les valeurs en supprimant les caractères parasites
- Convertir les taux en `NUMERIC` pour faciliter le calcul

## Contrôles qualité

- Vérifier 30 lignes aléatoires ou représentatives du document
- Comparer chaque ligne au PDF source
- Définir le taux d'erreur comme :

```text
erreurs / lignes vérifiées * 100
```

- Cible : < 2%

## Cas d'écarts

- libellé tronqué ou fusionné
- code SH mal décodé
- colonnes de droit et de TVA inversées
- taxes spécifiques ambiguës ou absentes

## Rapport attendu

```json
{
  "total_rows": 1200,
  "valid_rows": 1182,
  "quality_rate_percent": 98.5,
  "manual_review_required": ["lines 211", "lines 318", "lines 900"]
}
```
