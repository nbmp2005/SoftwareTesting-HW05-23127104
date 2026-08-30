import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("analyze_jtl.py")
SPEC = importlib.util.spec_from_file_location("analyze_jtl", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class AnalyzeJtlTests(unittest.TestCase):
    def test_summary_preserves_counts_errors_and_percentiles(self):
        rows = [
            {"timeStamp": "1000", "elapsed": "100", "label": "login", "responseCode": "200", "success": "true"},
            {"timeStamp": "1100", "elapsed": "200", "label": "login", "responseCode": "500", "success": "false"},
            {"timeStamp": "1300", "elapsed": "300", "label": "read", "responseCode": "200", "success": "true"},
        ]

        result = MODULE.summarize(rows)

        self.assertEqual(result["__overall__"]["samples"], 3)
        self.assertEqual(result["__overall__"]["failures"], 1)
        self.assertEqual(result["__overall__"]["elapsed_ms"]["median"], 200.0)
        self.assertEqual(result["login"]["response_codes"], {"200": 1, "500": 1})

    def test_missing_required_columns_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Missing required JTL columns"):
            MODULE.summarize([{"elapsed": "100"}])


if __name__ == "__main__":
    unittest.main()
