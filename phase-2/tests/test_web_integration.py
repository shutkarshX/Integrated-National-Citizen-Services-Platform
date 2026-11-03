import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import web_app

class WebIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = Path(self.temp.name) / "requests.json"
        self.patch = patch.object(web_app, "DATA_FILE", self.store)
        self.patch.start()

    def tearDown(self):
        self.patch.stop()
        self.temp.cleanup()

    def test_empty_store_returns_empty_list(self):
        self.assertEqual(web_app.load_requests(), [])

    def test_save_and_load_round_trip(self):
        sample = [{"pid": 101, "citizen": "Demo", "service": "Tax services", "burst": 3, "arrival": 0, "priority": 1}]
        web_app.save_requests(sample)
        self.assertEqual(web_app.load_requests(), sample)

    def test_corrupt_store_is_reported(self):
        self.store.write_text("{broken", encoding="utf-8")
        with self.assertRaises(ValueError):
            web_app.load_requests()

    def test_index_contains_api_and_scheduling_controls(self):
        self.assertIn("/api/requests", web_app.INDEX)
        self.assertIn("Round Robin", web_app.INDEX)
        self.assertIn("scheduleResult", web_app.INDEX)

if __name__ == "__main__":
    unittest.main()