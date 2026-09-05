import unittest

from backend.app.calculation import CalculationRequest, calculate_landed_cost, generate_pdf_devis, render_devis_html


class TestCalculation(unittest.TestCase):
    def test_calculate_landed_cost_basic(self):
        request = CalculationRequest(
            code_sh="8504",
            product_label="Chargeur téléphone USB",
            cif_value=100000,
            customs_rate=0.10,
            rs_rate=0.01,
            pc_rate=0.02,
            vat_rate=0.18,
            specific_taxes=0.00,
        )

        result = calculate_landed_cost(request)
        self.assertAlmostEqual(result.breakdown.customs, 10000.0)
        self.assertAlmostEqual(result.breakdown.rs, 1000.0)
        self.assertAlmostEqual(result.breakdown.pc, 2000.0)
        self.assertAlmostEqual(result.total_cost, 133340.0)
        self.assertIn("GAINDE", result.legal_note)

    def test_generate_pdf_devis_creates_file(self):
        request = CalculationRequest(
            code_sh="8504",
            product_label="Chargeur téléphone USB",
            cif_value=50000,
            customs_rate=0.10,
            rs_rate=0.01,
            pc_rate=0.02,
            vat_rate=0.18,
            specific_taxes=0.00,
        )
        result = calculate_landed_cost(request)
        path = generate_pdf_devis(result, "docs/devis_test.txt")

        self.assertTrue(path.endswith("devis_test.txt"))
        self.assertTrue(path.lower().endswith(".txt"))

    def test_freight_and_insurance_are_added_to_cif(self):
        request = CalculationRequest(
            code_sh="8504",
            product_label="Chargeur téléphone USB",
            cif_value=100000,
            freight_value=10000,
            insurance_value=1000,
            customs_rate=0.10,
        )

        result = calculate_landed_cost(request)

        self.assertEqual(result.cif_value, 111000)
        self.assertEqual(result.breakdown.customs, 11100)

    def test_render_devis_html_uses_bleue_print_branding(self):
        result = calculate_landed_cost(
            CalculationRequest(code_sh="8504", product_label="Chargeur", cif_value=100000)
        )

        html = render_devis_html(result)

        self.assertIn("BLEUE PRINT", html)
        self.assertIn("--violet: #4A2B5C", html)
        self.assertIn("Imprimer / enregistrer en PDF", html)
        self.assertIn("Généré avec BLEUE PRINT", html)


if __name__ == "__main__":
    unittest.main()
