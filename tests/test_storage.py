import json
import tempfile
import unittest
from pathlib import Path

from os_platform.models import ServiceRequest
from os_platform.storage import load_requests, save_requests


class StorageTests(unittest.TestCase):
    def test_save_and_load_round_trip(self):
        requests = [
            ServiceRequest("A", "Certificate", "Citizen A", 3),
            ServiceRequest("B", "Grievance", "Citizen B", 2),
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "nested" / "requests.json"
            save_requests(path, requests)
            loaded = load_requests(path)

        self.assertEqual([item.to_dict() for item in loaded],
                         [item.to_dict() for item in requests])

    def test_missing_file_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(load_requests(Path(directory) / "missing.json"), [])

    def test_empty_file_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "empty.json"
            path.write_text("", encoding="utf-8")
            self.assertEqual(load_requests(path), [])

    def test_non_list_payload_raises_value_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.json"
            path.write_text(json.dumps({"request_id": "A"}), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_requests(path)

    def test_invalid_json_raises_json_decode_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.json"
            path.write_text("[not json", encoding="utf-8")
            with self.assertRaises(json.JSONDecodeError):
                load_requests(path)


if __name__ == "__main__":
    unittest.main()
