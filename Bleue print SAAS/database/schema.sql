CREATE TABLE IF NOT EXISTS codes_sh (
    id SERIAL PRIMARY KEY,
    code_sh VARCHAR(20) NOT NULL,
    libelle TEXT NOT NULL,
    section VARCHAR(10),
    chapitre VARCHAR(10),
    taux_droit NUMERIC(10, 4),
    redevance_statistique NUMERIC(10, 4),
    prelevement_communautaire NUMERIC(10, 4),
    tva NUMERIC(10, 4),
    taxes_specifiques NUMERIC(10, 4),
    source_pdf TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_codes_sh_code
    ON codes_sh (code_sh);

CREATE INDEX IF NOT EXISTS idx_codes_sh_libelle_trgm
    ON codes_sh USING gin (to_tsvector('french', libelle));

CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE TABLE IF NOT EXISTS product_catalog (
    id SERIAL PRIMARY KEY,
    hs_heading VARCHAR(20) NOT NULL,
    libelle TEXT NOT NULL,
    aliases TEXT[] NOT NULL DEFAULT '{}',
    sector VARCHAR(80),
    is_importable BOOLEAN NOT NULL DEFAULT TRUE,
    is_exportable BOOLEAN NOT NULL DEFAULT TRUE,
    source TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_product_catalog_hs_heading
    ON product_catalog (hs_heading);

CREATE INDEX IF NOT EXISTS idx_product_catalog_aliases_gin
    ON product_catalog USING gin (aliases);

CREATE TABLE IF NOT EXISTS tariff_profiles (
    id SERIAL PRIMARY KEY,
    hs_heading VARCHAR(20) NOT NULL,
    customs_rate NUMERIC(10, 4) NOT NULL DEFAULT 0,
    rs_rate NUMERIC(10, 4) NOT NULL DEFAULT 0.01,
    pc_rate NUMERIC(10, 4) NOT NULL DEFAULT 0.02,
    vat_rate NUMERIC(10, 4) NOT NULL DEFAULT 0.18,
    specific_taxes NUMERIC(10, 4) NOT NULL DEFAULT 0,
    country VARCHAR(80) NOT NULL DEFAULT 'Senegal',
    origin_zone VARCHAR(80) NOT NULL DEFAULT 'Hors zone preferentielle',
    source TEXT,
    valid_from DATE,
    valid_until DATE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (hs_heading, country, origin_zone)
);

CREATE INDEX IF NOT EXISTS idx_tariff_profiles_hs_heading
    ON tariff_profiles (hs_heading);

CREATE TABLE IF NOT EXISTS global_hs_codes (
    id BIGSERIAL PRIMARY KEY,
    nomenclature_version VARCHAR(20) NOT NULL DEFAULT 'HS2022',
    section VARCHAR(10),
    hscode VARCHAR(20) NOT NULL,
    description TEXT NOT NULL,
    parent_hscode VARCHAR(20),
    level SMALLINT NOT NULL,
    source TEXT NOT NULL DEFAULT 'UN Comtrade / WCO nomenclature',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (nomenclature_version, hscode)
);

CREATE INDEX IF NOT EXISTS idx_global_hs_codes_hscode
    ON global_hs_codes (hscode);

CREATE INDEX IF NOT EXISTS idx_global_hs_codes_description_trgm
    ON global_hs_codes USING gin (to_tsvector('simple', description));

CREATE TABLE IF NOT EXISTS tec_tariff_bands (
    id SERIAL PRIMARY KEY,
    category SMALLINT NOT NULL UNIQUE,
    customs_rate NUMERIC(10, 4) NOT NULL,
    description TEXT NOT NULL,
    approximate_line_count VARCHAR(40),
    source TEXT
);

CREATE TABLE IF NOT EXISTS senegal_import_taxes (
    code VARCHAR(20) PRIMARY KEY,
    name TEXT NOT NULL,
    rate TEXT NOT NULL,
    base TEXT,
    source TEXT,
    notes TEXT
);
