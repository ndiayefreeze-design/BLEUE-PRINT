from dataclasses import dataclass


@dataclass(frozen=True)
class TariffProfile:
    code_sh: str
    customs_rate: float
    rs_rate: float = 0.01
    pc_rate: float = 0.02
    vat_rate: float = 0.18
    specific_taxes: float = 0.0
    country: str = "Senegal"
    origin_zone: str = "Hors zone preferentielle"
    source: str = "Profil indicatif BLEUE PRINT a confirmer avec le TEC en vigueur"


# Tarifs de reperage, a remplacer par les lignes du TEC officiel lors de l'import.
TARIFF_PROFILES = {
    "0101": 0.05,
    "0302": 0.20,
    "0402": 0.20,
    "0901": 0.20,
    "1511": 0.20,
    "2523": 0.20,
    "2710": 0.10,
    "3004": 0.05,
    "3923": 0.20,
    "5205": 0.20,
    "6109": 0.20,
    "6403": 0.20,
    "7210": 0.10,
    "8418": 0.20,
    "8471": 0.10,
    "8504": 0.10,
    "8517": 0.10,
    "8703": 0.20,
    "8708": 0.20,
    "8711": 0.20,
    "8712": 0.20,
    "9403": 0.20,
    "3304": 0.20,
}


def get_tariff_profile(code_sh: str) -> TariffProfile:
    normalized_code = (code_sh or "").strip()
    customs_rate = TARIFF_PROFILES.get(normalized_code, 0.20)
    return TariffProfile(code_sh=normalized_code, customs_rate=customs_rate)
