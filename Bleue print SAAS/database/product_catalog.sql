-- Catalogue de demarrage : familles et alias, a valider avec le TEC officiel.
-- Les positions SH sont des reperes de recherche, pas une classification douaniere officielle.
INSERT INTO product_catalog (hs_heading, libelle, aliases, sector, source)
VALUES
('0101', 'Animaux vivants', ARRAY['cheval', 'ane', 'bovin', 'volaille', 'betail'], 'agriculture', 'Catalogue de demarrage BLEUE PRINT'),
('0302', 'Poissons et produits de la peche', ARRAY['poisson', 'thon', 'crevette', 'fruits de mer'], 'agriculture', 'Catalogue de demarrage BLEUE PRINT'),
('0402', 'Lait et produits laitiers', ARRAY['lait', 'fromage', 'yaourt', 'beurre'], 'agroalimentaire', 'Catalogue de demarrage BLEUE PRINT'),
('0713', 'Legumes secs', ARRAY['haricot', 'lentille', 'pois chiche', 'legumes secs'], 'agroalimentaire', 'Catalogue de demarrage BLEUE PRINT'),
('0901', 'Cafe, the et epices', ARRAY['cafe', 'the', 'poivre', 'epice', 'cacao'], 'agroalimentaire', 'Catalogue de demarrage BLEUE PRINT'),
('1511', 'Huiles vegetales', ARRAY['huile', 'huile palme', 'huile arachide', 'huile alimentaire'], 'agroalimentaire', 'Catalogue de demarrage BLEUE PRINT'),
('1701', 'Sucres et produits sucres', ARRAY['sucre', 'confiserie', 'bonbon'], 'agroalimentaire', 'Catalogue de demarrage BLEUE PRINT'),
('2203', 'Boissons et boissons alcoolisees', ARRAY['boisson', 'biere', 'jus', 'eau minerale'], 'agroalimentaire', 'Catalogue de demarrage BLEUE PRINT'),
('2523', 'Ciments et materiaux de construction', ARRAY['ciment', 'beton', 'materiau construction'], 'construction', 'Catalogue de demarrage BLEUE PRINT'),
('2710', 'Huiles minerales et carburants', ARRAY['essence', 'gasoil', 'diesel', 'carburant', 'lubrifiant'], 'energie', 'Catalogue de demarrage BLEUE PRINT'),
('3004', 'Medicaments et produits pharmaceutiques', ARRAY['medicament', 'comprime', 'pharmacie', 'sirop'], 'sante', 'Catalogue de demarrage BLEUE PRINT'),
('3923', 'Emballages et articles en plastique', ARRAY['plastique', 'emballage', 'sachet', 'bouteille plastique'], 'industrie', 'Catalogue de demarrage BLEUE PRINT'),
('6109', 'Vetements et articles dhabillement', ARRAY['maillot', 'polo', 'chemise', 'tshirt', 'vetement', 'habillement'], 'textile', 'Catalogue de demarrage BLEUE PRINT'),
('5205', 'Fils, toiles et tissus de coton', ARRAY['tissu', 'coton', 'wax', 'toile', 'textile'], 'textile', 'Catalogue de demarrage BLEUE PRINT'),
('6403', 'Chaussures et parties de chaussures', ARRAY['chaussure', 'sandal', 'bottine', 'basket'], 'textile', 'Catalogue de demarrage BLEUE PRINT'),
('6907', 'Carreaux et produits ceramiques', ARRAY['carreau', 'ceramique', 'faience'], 'construction', 'Catalogue de demarrage BLEUE PRINT'),
('7210', 'Produits siderurgiques et toles', ARRAY['acier', 'tole', 'fer', 'metal'], 'industrie', 'Catalogue de demarrage BLEUE PRINT'),
('8418', 'Refrigerateurs et equipements frigorifiques', ARRAY['frigo', 'refrigerateur', 'congelateur', 'climatisation'], 'equipement', 'Catalogue de demarrage BLEUE PRINT'),
('8471', 'Ordinateurs et equipements informatiques', ARRAY['ordinateur', 'pc', 'laptop', 'imprimante', 'informatique'], 'electronique', 'Catalogue de demarrage BLEUE PRINT'),
('8504', 'Chargeurs, transformateurs et adaptateurs', ARRAY['chargeur', 'adaptateur', 'transformateur', 'usb'], 'electronique', 'Catalogue de demarrage BLEUE PRINT'),
('8517', 'Telephones et appareils de communication', ARRAY['telephone', 'smartphone', 'portable', 'routeur'], 'electronique', 'Catalogue de demarrage BLEUE PRINT'),
('8703', 'Voitures et autres vehicules automobiles', ARRAY['voiture', 'automobile', 'vehicule', '4x4'], 'transport', 'Catalogue de demarrage BLEUE PRINT'),
('8708', 'Pieces et accessoires automobiles', ARRAY['piece auto', 'pneu', 'moteur', 'frein', 'filtre'], 'transport', 'Catalogue de demarrage BLEUE PRINT'),
('8711', 'Motocycles, cycles a moteur et scooters', ARRAY['deux roues', 'moto', 'motocyclette', 'scooter', 'cyclomoteur', 'mobylettes', 'quad'], 'transport', 'Catalogue de demarrage BLEUE PRINT'),
('8712', 'Bicyclettes et autres cycles sans moteur', ARRAY['deux roues', 'velo', 'bicyclette', 'cycle', 'vtt', 'tricycle'], 'transport', 'Catalogue de demarrage BLEUE PRINT'),
('9403', 'Meubles et articles dameublement', ARRAY['meuble', 'chaise', 'table', 'canape', 'bureau'], 'maison', 'Catalogue de demarrage BLEUE PRINT'),
('3304', 'Produits cosmetiques et de toilette', ARRAY['cosmetique', 'savon', 'parfum', 'beaute', 'creme'], 'sante-beaute', 'Catalogue de demarrage BLEUE PRINT')
ON CONFLICT DO NOTHING;