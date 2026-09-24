import unittest

from services.user_service import UserService
from services.crud_service import CRUDService


class TestValidationSuite(unittest.TestCase):
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

    def test_search_none_returns_all_users(self):
        results = self.service.search(None)
        self.assertEqual(len(results), 2)

    def test_crud_search_none_returns_all_records(self):
        crud = CRUDService("logs.json", "log_id")
        crud.storage.save_data([
            {"log_id": "L1", "action": "login"},
            {"log_id": "L2", "action": "failed login"},
        ])
        self.addCleanup(lambda: crud.storage.save_data([]))
        self.assertEqual(len(crud.search(None)), 2)

    def test_update_rejects_invalid_blank_email(self):
        with self.assertRaises(ValueError):
            self.service.update("A1", email="   ")

    def test_update_rejects_invalid_blank_phone(self):
        with self.assertRaises(ValueError):
            self.service.update("A1", phone="   ")


if __name__ == "__main__":
    unittest.main()
