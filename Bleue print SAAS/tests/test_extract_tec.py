import unittest

from scripts.tec_extraction.extract_tec import DEMO_ROWS, validate_extraction


class TestExtractTec(unittest.TestCase):
    def test_validate_extraction_demo_rows(self):
        report = validate_extraction(DEMO_ROWS)

        self.assertEqual(report["total_rows"], 3)
        self.assertEqual(report["valid_rows"], 3)
        self.assertEqual(report["quality_rate_percent"], 100.0)
        self.assertEqual(report["status"], "quality_ok")


if __name__ == "__main__":
    unittest.main()
