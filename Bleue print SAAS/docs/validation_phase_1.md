# Validation Phase 1 — TEC

## Critères de validation

- Échantillon de 30 lignes vérifié contre le PDF source
- Taux d'erreur < 2%
- Codes SH présents et correctement formatés
- Libellés cohérents
- Valeurs de droit, RS, PC, TVA et taxes spécifiques conformes

## Processus

1. Sélectionner 30 lignes représentatives
2. Vérifier chaque ligne dans le PDF source
3. Note de validation : OK / OK avec correction / KO
4. Calculer le taux d'erreur
5. Lister les lignes à revoir manuellement

## Seuil d'acceptation

```text
Taux d'erreur < 2% => phase 1 validée
Taux d'erreur >= 2% => correction avant passage à la phase 2
```

## Hypothèse de travail

Sans accès au PDF officiel dans ce workspace, le script est lancé comme un squelette d'extraction exploitable et à faire évoluer selon la structure réelle du document.
