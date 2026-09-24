import unittest

from main import CyberShieldApp


class TestMenuNumbers(unittest.TestCase):
    def test_main_menu_has_valid_keys(self):
        self.assertEqual(list(CyberShieldApp.MAIN_MENU.keys()), ["1", "2", "0"])

    def test_authenticated_menu_starts_from_one_and_keeps_zero_exit(self):
        keys = list(CyberShieldApp.AUTH_MENU.keys())
        self.assertEqual(keys, ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"])


if __name__ == "__main__":
    unittest.main()
