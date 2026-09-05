import unittest

from fastapi.testclient import TestClient

from backend.app.main import app, MatchRequest, match_product
from backend.app.matching import normalize_text
from backend.app.tariffs import get_tariff_profile


class TestMatchApi(unittest.TestCase):
    def test_match_product_returns_multiple_candidates(self):
        payload = MatchRequest(product_description="chargeur téléphone usb rapide")
        result = match_product(payload)

        self.assertGreaterEqual(len(result.candidates), 1)
        self.assertLessEqual(len(result.candidates), 3)
        self.assertIn("GAINDE", result.legal_note)

    def test_match_product_with_unknown_description_still_returns_candidates(self):
        payload = MatchRequest(product_description="objet très spécifique sans correspondance claire")
        result = match_product(payload)

        self.assertLessEqual(len(result.candidates), 3)
        self.assertTrue(all(candidate.code_sh for candidate in result.candidates))

    def test_match_product_recognizes_two_wheelers(self):
        payload = MatchRequest(product_description="deux roues scooter electrique")
        result = match_product(payload)

        self.assertTrue(any(candidate.code_sh == "8711" for candidate in result.candidates))
        self.assertTrue(any(candidate.code_sh == "8712" for candidate in result.candidates))

    def test_match_product_uses_global_hs_catalog(self):
        payload = MatchRequest(product_description="raw sugar")
        result = match_product(payload)

        self.assertTrue(any(candidate.code_sh.startswith("1701") for candidate in result.candidates))

    def test_normalize_text_filters_unknown_noise_words(self):
        tokens = normalize_text("mot inconnu chargeur usb word")

        self.assertNotIn("mot", tokens)
        self.assertNotIn("inconnu", tokens)
        self.assertNotIn("word", tokens)
        self.assertIn("chargeur", tokens)
        self.assertIn("usb", tokens)

    def test_match_product_handles_synonyms_and_category_hint(self):
        payload = MatchRequest(
            product_description="maillot polo pour homme en coton",
            category_hint="textile",
        )
        result = match_product(payload)

        self.assertTrue(any(candidate.code_sh == "6109" for candidate in result.candidates))
        self.assertTrue(any(candidate.code_sh == "5205" for candidate in result.candidates))

    def test_match_product_reduces_false_positive_on_generic_oil(self):
        payload = MatchRequest(product_description="huile moteur")
        result = match_product(payload)

        self.assertNotIn("3304", [candidate.code_sh for candidate in result.candidates])

    def test_match_product_recognizes_reformulations(self):
        cases = {
            "allimunium": "7606",
            "parfums": "3303",
            "boissons": "2202",
            "panneau solaire": "8541",
            "groupe electrogene": "8502",
        }

        for description, expected_code in cases.items():
            with self.subTest(description=description):
                result = match_product(MatchRequest(product_description=description))
                self.assertEqual(result.candidates[0].code_sh, expected_code)

    def test_match_product_recognizes_btp_families(self):
        cases = {
            "ciment": "2523",
            "parpaing": "6904",
            "carrelage": "6907",
            "perceuse": "8467",
            "robinetterie": "8481",
            "pelleteuse": "8429",
            "poste a souder": "8468",
            "extincteur": "8424",
            "topographie": "9015",
        }

        for description, expected_code in cases.items():
            with self.subTest(description=description):
                result = match_product(MatchRequest(product_description=description))
                self.assertEqual(result.candidates[0].code_sh, expected_code)

    def test_match_product_recognizes_agriculture_and_agrofood(self):
        cases = {
            "semences": "1209",
            "engrais": "3105",
            "pesticide": "3808",
            "tracteur": "8701",
            "aliment animaux": "2309",
            "poulet": "0207",
            "pansement": "3005",
            "enceinte audio": "8518",
            "camera": "8525",
            "gps": "8526",
        }

        for description, expected_code in cases.items():
            with self.subTest(description=description):
                result = match_product(MatchRequest(product_description=description))
                self.assertEqual(result.candidates[0].code_sh, expected_code)

    def test_calculation_endpoint_returns_breakdown(self):
        client = TestClient(app)
        response = client.post(
            "/calculate",
            json={
                "code_sh": "8504",
                "product_label": "Chargeur téléphone USB",
                "cif_value": 100000,
                "customs_rate": 0.10,
                "rs_rate": 0.01,
                "pc_rate": 0.02,
                "vat_rate": 0.18,
                "specific_taxes": 0.0,
            },
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("total_cost", payload)
        self.assertIn("breakdown", payload)
        self.assertEqual(payload["code_sh"], "8504")

    def test_tariff_profile_for_two_wheeler(self):
        profile = get_tariff_profile("8711")

        self.assertEqual(profile.code_sh, "8711")
        self.assertEqual(profile.customs_rate, 0.20)
        self.assertEqual(profile.vat_rate, 0.18)


if __name__ == "__main__":
    unittest.main()
