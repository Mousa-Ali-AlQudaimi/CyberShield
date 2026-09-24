"""
Simple tests for CyberShield Stage 1.
Run: python test_stage1.py
"""

from utils.validators import (
    validate_phone,
    validate_numeric,
    validate_email,
    validate_username,
    validate_ip,
)
from utils.file_manager import FileManager


def test_validators():
    print("=== Validators Test ===")

    print(validate_phone("711234567"))
    print(validate_numeric("12345"))
    print(validate_email("admin@example.com"))
    print(validate_username("admin_01"))
    print(validate_ip("192.168.1.10"))

    invalid_phones = [
        "701234567",
        "71123456",
        "7112345678",
        "71ABC4567",
        "71@234567",
    ]

    for phone in invalid_phones:
        try:
            validate_phone(phone)
        except (ValueError, TypeError) as error:
            print(f"Rejected phone {phone}: {error}")

    try:
        validate_numeric("12@3")
    except (ValueError, TypeError) as error:
        print(f"Rejected numeric value: {error}")


def test_file_manager():
    print("\n=== FileManager Test ===")

    manager = FileManager("stage1_test.json")

    manager.save_data([
        {"id": 1, "name": "Admin"},
        {"id": 2, "name": "Analyst"},
    ])

    print("Saved:", manager.load_data())

    manager.append_data({"id": 3, "name": "User"})
    print("After append:", manager.load_data())

    manager.update_data(0, {"id": 1, "name": "Administrator"})
    print("After update:", manager.load_data())

    manager.delete_data(2)
    print("After delete:", manager.load_data())

    manager.clear_data()
    print("After clear:", manager.load_data())


if __name__ == "__main__":
    test_validators()
    test_file_manager()
    print("\nStage 1 completed successfully.")
