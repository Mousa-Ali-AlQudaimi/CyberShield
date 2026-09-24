import unittest
from unittest.mock import patch

from main import CyberShieldApp
from services.user_service import UserService


class TestCyberShieldRegression(unittest.TestCase):
    def setUp(self):
        self.service = UserService()
        self.service.storage.save_data([
            {
                "user_id": "A1",
                "username": "AdminOne",
                "email": "admin@test.com",
                "phone": "711234567",
                "role": "admin",
                "password": "DEMO_ONLY",
            },
            {
                "user_id": "U1",
                "username": "AnalystOne",
                "email": "analyst@test.com",
                "phone": "731234567",
                "role": "analyst",
                "password": "DEMO_ONLY",
            },
        ])

    def tearDown(self):
        self.service.storage.save_data([])

    def test_user_search_is_case_insensitive_and_partial(self):
        results = self.service.search("admin")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["username"], "AdminOne")

    def test_delete_record_works_without_report_variable(self):
        with patch("builtins.input", side_effect=["A1", "DELETE"]):
            CyberShieldApp.delete_record(self.service, "User ID")

        self.assertEqual(len(self.service.get_all()), 1)
        self.assertEqual(self.service.get_all()[0]["user_id"], "U1")


if __name__ == "__main__":
    unittest.main()
