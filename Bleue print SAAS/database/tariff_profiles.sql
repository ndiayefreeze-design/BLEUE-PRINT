-- Profils indicatifs a confirmer avec le TEC Senegal/UEMOA en vigueur.
-- Les taux sont stockes en decimal : 0.18 = 18 pour cent.
INSERT INTO tariff_profiles
    (hs_heading, customs_rate, rs_rate, pc_rate, vat_rate, country, origin_zone, source)
VALUES
('0101', 0.05, 0.01, 0.02, 0.18, 'Senegal', 'Hors zone preferentielle', 'Profil indicatif BLEUE PRINT'),
('0302', 0.20, 0.01, 0.02, 0.18, 'Senegal', 'Hors zone preferentielle', 'Profil indicatif BLEUE PRINT'),
('0402', 0.20, 0.01, 0.02, 0.18, 'Senegal', 'Hors zone preferentielle', 'Profil indicatif BLEUE PRINT'),
('0901', 0.20, 0.01, 0.02, 0.18, 'Senegal', 'Hors zone preferentielle', 'Profil indicatif BLEUE PRINT'),
('1511', 0.20, 0.01, 0.02, 0.18, 'Senegal', 'Hors zone preferentielle', 'Profil indicatif BLEUE PRINT'),
('2523', 0.20, 0.01, 0.02, 0.18, 'Senegal', 'Hors zone preferentielle', 'Profil indicatif BLEUE PRINT'),
('2710', 0.10, 0.01, 0.02, 0.18, 'Senegal', 'Hors zone preferentielle', 'Profil indicatif BLEUE PRINT'),
('3004', 0.05, 0.01, 0.02, 0.18, 'Senegal', 'Hors zone preferentielle', 'Profil indicatif BLEUE PRINT'),
('3923', 0.20, 0.01, 0.02, 0.18, 'Senegal', 'Hors zone preferentielle', 'Profil indicatif BLEUE PRINT'),
('6109', 0.20, 0.01, 0.02, 0.18, 'Senegal', 'Hors zone preferentielle', 'Profil indicatif BLEUE PRINT'),
('6403', 0.20, 0.01, 0.02, 0.18, 'Senegal', 'Hors zone preferentielle', 'Profil indicatif BLEUE PRINT'),
('7210', 0.10, 0.01, 0.02, 0.18, 'Senegal', 'Hors zone preferentielle', 'Profil indicatif BLEUE PRINT'),
('8418', 0.20, 0.01, 0.02, 0.18, 'Senegal', 'Hors zone preferentielle', 'Profil indicatif BLEUE PRINT'),
('8471', 0.10, 0.01, 0.02, 0.18, 'Senegal', 'Hors zone preferentielle', 'Profil indicatif BLEUE PRINT'),
('8504', 0.10, 0.01, 0.02, 0.18, 'Senegal', 'Hors zone preferentielle', 'Profil indicatif BLEUE PRINT'),
('8517', 0.10, 0.01, 0.02, 0.18, 'Senegal', 'Hors zone preferentielle', 'Profil indicatif BLEUE PRINT'),
('8703', 0.20, 0.01, 0.02, 0.18, 'Senegal', 'Hors zone preferentielle', 'Profil indicatif BLEUE PRINT'),
('8708', 0.20, 0.01, 0.02, 0.18, 'Senegal', 'Hors zone preferentielle', 'Profil indicatif BLEUE PRINT'),
('8711', 0.20, 0.01, 0.02, 0.18, 'Senegal', 'Hors zone preferentielle', 'Profil indicatif BLEUE PRINT'),
('8712', 0.20, 0.01, 0.02, 0.18, 'Senegal', 'Hors zone preferentielle', 'Profil indicatif BLEUE PRINT'),
('9403', 0.20, 0.01, 0.02, 0.18, 'Senegal', 'Hors zone preferentielle', 'Profil indicatif BLEUE PRINT'),
('3304', 0.20, 0.01, 0.02, 0.18, 'Senegal', 'Hors zone preferentielle', 'Profil indicatif BLEUE PRINT')
ON CONFLICT (hs_heading, country, origin_zone) DO NOTHING;