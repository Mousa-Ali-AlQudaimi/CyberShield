"""
CyberShield - Input Validation Utilities
Stage 1
"""

import re
import ipaddress


def validate_required(value, field_name="Value"):
    """Make sure a text value is not empty."""
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be text.")

    value = value.strip()

    if not value:
        raise ValueError(f"{field_name} cannot be empty.")

    return value


def validate_numeric(value, field_name="Number"):
    """
    Validate an integer input.
    Letters and special characters are rejected.
    """
    if isinstance(value, bool):
        raise TypeError(f"{field_name} must be a number.")

    if isinstance(value, int):
        return value

    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a number.")

    value = value.strip()

    if not value:
        raise ValueError(f"{field_name} cannot be empty.")

    if not value.isdigit():
        raise ValueError(
            f"{field_name} must contain digits only."
        )

    return int(value)


def validate_phone(phone):
    """
    Assignment requirement:
    - exactly 9 digits
    - starts with 71, 73, 77, or 78
    """
    if not isinstance(phone, str):
        raise TypeError("Phone number must be text.")

    phone = phone.strip()

    if not phone.isdigit():
        raise ValueError("Phone number must contain digits only.")

    if len(phone) != 9:
        raise ValueError("Phone number must contain exactly 9 digits.")

    if phone[:2] not in ("71", "73", "77", "78"):
        raise ValueError(
            "Phone number must start with 71, 73, 77, or 78."
        )

    return phone


def validate_email(email):
    """Basic email validation suitable for the student project."""
    if not isinstance(email, str):
        raise TypeError("Email must be text.")

    email = email.strip()

    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    if not re.fullmatch(pattern, email):
        raise ValueError("Invalid email address.")

    return email


def validate_username(username):
    """
    Username:
    - 3 to 20 characters
    - letters, numbers and underscore only
    """
    if not isinstance(username, str):
        raise TypeError("Username must be text.")

    username = username.strip()

    if not 3 <= len(username) <= 20:
        raise ValueError(
            "Username must be between 3 and 20 characters."
        )

    if not re.fullmatch(r"[A-Za-z0-9_]+", username):
        raise ValueError(
            "Username can contain letters, numbers and underscore only."
        )

    return username


def validate_ip(ip):
    """Validate IPv4/IPv6 address."""
    if not isinstance(ip, str):
        raise TypeError("IP address must be text.")

    ip = ip.strip()

    try:
        ipaddress.ip_address(ip)
    except ValueError:
        raise ValueError("Invalid IP address.")

    return ip


def validate_choice(choice, valid_choices):
    """Validate a menu choice against allowed values."""
    choice = str(choice).strip()

    if choice not in valid_choices:
        raise ValueError(
            f"Invalid choice. Allowed choices: {', '.join(valid_choices)}"
        )

    return choice
