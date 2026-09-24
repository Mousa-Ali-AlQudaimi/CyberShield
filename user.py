from datetime import datetime
from utils.validators import validate_required, validate_phone, validate_email, validate_username


class User:
    total_users = 0
    allowed_roles = ("admin", "analyst")

    def __init__(self, user_id, username, password, email, phone, role="analyst"):
        self.__user_id = validate_required(str(user_id), "User ID")
        self.__username = validate_username(username)
        self.password = validate_required(password, "Password")
        self.email = validate_email(email)
        self.phone = validate_phone(phone)
        self.role = validate_required(role, "Role").lower()
        if self.role not in self.allowed_roles:
            raise ValueError("Role must be admin or analyst.")
        self.is_logged_in = False
        self.created_at = datetime.now().isoformat(timespec="seconds")
        User.total_users += 1

    @property
    def user_id(self):
        return self.__user_id

    @property
    def username(self):
        return self.__username

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        self.__email = validate_email(value)

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, value):
        self.__phone = validate_phone(value)

    def login(self, password):
        if password != self.password:
            raise ValueError("Invalid password.")
        self.is_logged_in = True
        return True

    def logout(self):
        self.is_logged_in = False
        return True

    def change_password(self, old_password, new_password):
        if old_password != self.password:
            raise ValueError("Old password is incorrect.")
        new_password = validate_required(new_password, "New password")
        if len(new_password) < 6:
            raise ValueError("Password must contain at least 6 characters.")
        self.password = new_password

    def show_permissions(self):
        return "Basic analyst permissions."

    def to_dict(self):
        return {
            "user_id": self.user_id, "username": self.username,
            "password": self.password, "email": self.email,
            "phone": self.phone, "role": self.role,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["user_id"], data["username"], data["password"],
                   data["email"], data["phone"])

    def __str__(self):
        return f"{self.username} ({self.role})"

    def __eq__(self, other):
        return isinstance(other, User) and self.user_id == other.user_id


class Admin(User):
    def __init__(self, *args, **kwargs):
        kwargs["role"] = "admin"
        super().__init__(*args, **kwargs)

    def show_permissions(self):
        return "Full access: users, logs, alerts, incidents and reports."


class Analyst(User):
    def __init__(self, *args, **kwargs):
        kwargs["role"] = "analyst"
        super().__init__(*args, **kwargs)

    def show_permissions(self):
        return "Analysis access: logs, attacks, alerts and reports."
