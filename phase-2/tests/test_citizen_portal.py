import json
import tempfile
import threading
import unittest
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError

import web_app


class CitizenPortalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        web_app.DATA_FILE = Path(cls.temp.name) / "applications.json"
        cls.server = web_app.create_server(port=0)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)
        cls.temp.cleanup()

    def get_json(self, path):
        with urlopen(self.base + path) as response:
            return response.status, json.loads(response.read())

    def post_json(self, path, payload):
        req = Request(self.base + path, data=json.dumps(payload).encode(),
                      headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urlopen(req) as response:
                return response.status, json.loads(response.read())
        except HTTPError as exc:
            return exc.code, json.loads(exc.read())

    def test_homepage_is_citizen_portal_not_scheduler_console(self):
        with urlopen(self.base + "/") as response:
            html = response.read().decode()
        self.assertIn("Public services,", html)
        self.assertIn("Explore citizen services", html)
        self.assertNotIn("Run schedule", html)

    def test_service_catalog(self):
        status, data = self.get_json("/api/services")
        self.assertEqual(status, 200)
        self.assertGreaterEqual(len(data["services"]), 5)
        self.assertIn("birth-certificate", [x["id"] for x in data["services"]])

    def test_submit_and_track_application(self):
        status, data = self.post_json("/api/applications", {
            "service_id": "birth-certificate", "name": "Demo Citizen",
            "email": "demo@example.test", "mobile": "9876543210",
            "details": "Synthetic test application"
        })
        self.assertEqual(status, 201)
        ref = data["application"]["reference"]
        self.assertTrue(ref.startswith("CIV-2026-"))
        status, tracked = self.get_json("/api/applications/" + ref)
        self.assertEqual(status, 200)
        self.assertEqual(tracked["application"]["status"], "Submitted")
        self.assertNotIn("email", tracked["application"])

    def test_invalid_mobile_rejected(self):
        status, data = self.post_json("/api/applications", {
            "service_id": "grievance", "name": "Demo Citizen",
            "email": "demo@example.test", "mobile": "123",
            "details": "Synthetic test application"
        })
        self.assertEqual(status, 400)
        self.assertIn("10 digits", data["error"])

    def test_unknown_reference_returns_404(self):
        status, data = self.get_json("/api/applications/CIV-2026-FFFFFF")
        self.assertEqual(status, 404)
        self.assertIn("No application found", data["error"])


if __name__ == "__main__":
    unittest.main()
