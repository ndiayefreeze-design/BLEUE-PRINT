# Brief de lancement BLEUE PRINT

## Rôle

Agent produit et technique responsable de la mise en œuvre de BLEUE PRINT, un SaaS de calcul de conformité douanière pour le Sénégal et la zone CEDEAO/UEMOA.

## Problème

Le Tarif Extérieur Commun (TEC) est un document officiel volumineux, structurée par sections et chapitres du Système Harmonisé, difficilement exploitable pour un non-spécialiste. GAINDE est réservé aux commissionnaires agréés et n'est pas un outil de simulation rapide. Il manque un calculateur de cout landed cost accessible et compréhensible avant la déclaration.

## Solution proposée

- Prendre une description produit en français courant
- Proposer 2 à 3 codes SH candidats à valider par l'utilisateur
- Calculer un coût estimé incluant : droit de douane, RS, PC, TVA, taxes spécifiques éventuelles
- Afficher les documents requis selon la catégorie de produit
- Rappeler explicitement le caractère indicatif de l'estimation

## Marché cible

1. Commissionnaires en douane agréés à Dakar
2. PME importatrices régulières
3. Plateformes e-commerce transfrontalières
4. Banques et institutions de financement

## Contrainte légale

Chaque calcul affiché doit comporter la mention :

"Estimation à titre indicatif — la classification tarifaire officielle et la déclaration en douane relèvent exclusivement d'un commissionnaire en douane agréé via GAINDE."

## Modèle économique

- PME : 5 calculs gratuits/mois, puis abonnement ~15 000–25 000 CFA/mois
- Commissionnaires : abonnement pro, export PDF de devis
- API : facturation au call ou par paliers mensuels

## Stack de démarrage

- Extraction : Python + pdfplumber / camelot
- Backend : FastAPI
- Base : PostgreSQL
- Matching : recherche full-text + LLM de désambiguïsation
- Frontend : webapp mobile-first ou WhatsApp
- Hébergement : Railway ou Render

## Phase 1 — Objectif

Récupérer le PDF du TEC, l'extraire en table structurée et stocker les lignes tarifaires dans une base PostgreSQL dédiée.

## Livrables prévus

- Script d'extraction
- Base Postgres peuplée
- Rapport de qualité d'extraction
- Échantillon de 30 lignes vérifiées manuellement

## Validation Phase 1

- Taux d'erreur inférieur à 2%
- Lignes à corriger listées
- Contrôles de cohérence sur les colonnes critiques

## Hypothèses à confirmer

- Choix du format de stockage exact des taux (numériques, décimaux, string)
- Source PDF du TEC retenue pour la première extraction
- Profil de données exact à capturer pour les taxes spécifiques
- Niveau d'intégration souhaité des documents requis

## Point de décision à demander au client

- Nom de domaine / URL de production
- Wording du pitch commercial
- Priorité entre validation expert douanier et vitesse de MVP
