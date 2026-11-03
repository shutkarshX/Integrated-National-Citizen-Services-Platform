import json
import tempfile
import threading
import unittest
from http.cookiejar import CookieJar
from pathlib import Path
from urllib.request import Request, build_opener, HTTPCookieProcessor
from urllib.error import HTTPError

import web_app


class AdminDashboardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        web_app.DATA_FILE = Path(cls.temp.name) / "applications.json"
        web_app.ADMIN_PASSWORD = "test-admin-password"
        web_app.ADMIN_SESSIONS.clear()
        cls.server = web_app.create_server(port=0)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_address[1]}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)
        cls.temp.cleanup()
        web_app.ADMIN_SESSIONS.clear()

    def setUp(self):
        self.opener = build_opener(HTTPCookieProcessor(CookieJar()))
        self.ref = "CIV-2026-ADM123"
        web_app.write_store([{
            "reference": self.ref, "service": "Birth Certificate",
            "service_id": "birth-certificate", "name": "Demo Applicant",
            "email": "demo@example.test", "mobile": "9876543210",
            "details": "Synthetic application", "status": "Submitted",
            "submitted_at": "03 Nov 2026, 10:00 AM"
        }])

    def call(self, path, payload=None):
        data = None if payload is None else json.dumps(payload).encode()
        req = Request(self.base + path, data=data, headers={"Content-Type": "application/json"},
                      method="GET" if payload is None else "POST")
        try:
            with self.opener.open(req) as r:
                return r.status, json.loads(r.read())
        except HTTPError as e:
            return e.code, json.loads(e.read())

    def test_admin_api_requires_login(self):
        status, body = self.call("/api/admin/applications")
        self.assertEqual(status, 401)
        self.assertIn("sign-in", body["error"])

    def test_admin_can_list_and_update_status(self):
        status, _ = self.call("/api/admin/login", {"password": "test-admin-password"})
        self.assertEqual(status, 200)
        status, data = self.call("/api/admin/applications")
        self.assertEqual(status, 200)
        self.assertEqual(data["applications"][0]["reference"], self.ref)
        status, updated = self.call("/api/admin/status", {
            "reference": self.ref, "status": "Under Review"
        })
        self.assertEqual(status, 200)
        self.assertEqual(updated["application"]["status"], "Under Review")
        stored = web_app.read_store()[0]
        self.assertEqual(stored["status"], "Under Review")
        self.assertEqual(stored["status_history"][-1]["status"], "Under Review")

    def test_invalid_status_is_rejected(self):
        self.call("/api/admin/login", {"password": "test-admin-password"})
        status, body = self.call("/api/admin/status", {
            "reference": self.ref, "status": "Paid"
        })
        self.assertEqual(status, 400)
        self.assertIn("valid application status", body["error"])

    def test_wrong_password_is_rejected(self):
        status, body = self.call("/api/admin/login", {"password": "wrong"})
        self.assertEqual(status, 401)
        self.assertIn("Incorrect", body["error"])


if __name__ == "__main__":
    unittest.main()
