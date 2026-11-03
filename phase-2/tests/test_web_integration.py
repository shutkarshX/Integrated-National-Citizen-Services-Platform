import json
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import web_app

class WebIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = Path(self.temp.name) / "requests.json"
        self.patch = patch.object(web_app, "DATA_FILE", self.store)
        self.patch.start()
        self.server = web_app.create_server(port=0)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base = f"http://127.0.0.1:{self.server.server_port}"

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        self.patch.stop()
        self.temp.cleanup()

    def request(self, path, payload=None):
        data = None if payload is None else json.dumps(payload).encode("utf-8")
        req = Request(self.base + path, data=data, headers={"Content-Type": "application/json"})
        try:
            with urlopen(req, timeout=3) as response:
                return response.status, json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            return exc.code, json.loads(exc.read().decode("utf-8"))

    def test_homepage_serves_browser_interface(self):
        with urlopen(self.base + "/", timeout=3) as response:
            html = response.read().decode("utf-8")
        self.assertEqual(response.status, 200)
        self.assertIn("Service operations", html)
        self.assertIn("Run schedule", html)

    def test_request_creation_persists_and_returns_pid(self):
        status, result = self.request("/api/requests", {"citizen": "Demo User", "service": "Tax services", "burst": 3, "arrival": 0, "priority": 1})
        self.assertEqual(status, 201)
        self.assertEqual(result["request"]["pid"], 101)
        self.assertEqual(web_app.load_requests()[0]["citizen"], "Demo User")

    def test_invalid_request_is_rejected(self):
        status, result = self.request("/api/requests", {"citizen": "", "service": "Tax services", "burst": 0, "arrival": 0, "priority": 1})
        self.assertEqual(status, 400)
        self.assertIn("error", result)

    def test_schedule_endpoint_uses_phase_one_scheduler(self):
        self.request("/api/requests", {"citizen": "Asha", "service": "Certificate services", "burst": 4, "arrival": 0, "priority": 2})
        self.request("/api/requests", {"citizen": "Ravi", "service": "Tax services", "burst": 2, "arrival": 0, "priority": 1})
        status, result = self.request("/api/schedule", {"algorithm": "sjf"})
        self.assertEqual(status, 200)
        self.assertEqual(result["algorithm"], "SJF (non-preemptive)")
        self.assertEqual(len(result["timeline"]), 2)
        self.assertEqual(result["processes"][0]["finish"], 6)

    def test_schedule_without_requests_returns_validation_error(self):
        status, result = self.request("/api/schedule", {"algorithm": "fcfs"})
        self.assertEqual(status, 400)
        self.assertIn("Add at least one", result["error"])

if __name__ == "__main__":
    unittest.main()