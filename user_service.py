from models.user import User, Admin, Analyst
from utils.file_manager import FileManager


class UserService:
    def __init__(self):
        self.storage = FileManager("users.json")

    def _records(self):
        data = self.storage.load_data([])
        if not isinstance(data, list):
            raise TypeError("users.json must contain a list.")
        return data

    def get_all(self):
        return self._records()

    def exists(self, field, value, exclude_id=None):
        return any(
            str(row.get(field, "")).lower() == str(value).lower()
            and str(row.get("user_id")) != str(exclude_id)
            for row in self._records()
        )

    def add_user(self, user):
        if not isinstance(user, User):
            raise TypeError("Expected a User object.")
        for field, value in (("user_id", user.user_id), ("username", user.username),
                             ("email", user.email), ("phone", user.phone)):
            if self.exists(field, value):
                raise ValueError(f"Duplicate {field}: {value}")
        self.storage.append_data(user.to_dict())

    def authenticate(self, username, password):
        for row in self._records():
            if row.get("username", "").lower() == username.lower():
                user_cls = Admin if row.get("role") == "admin" else Analyst
                user = user_cls.from_dict(row)
                user.login(password)
                return user
        raise ValueError("Username not found.")

    def find_by_id(self, user_id):
        return next((r for r in self._records() if str(r.get("user_id")) == str(user_id)), None)

    def search(self, term):
        rows = self._records()
        if term is None:
            return rows

        term = str(term).strip().lower()
        if not term:
            return rows
        return [r for r in rows if any(term in str(r.get(k, "")).lower()
                for k in ("user_id", "username", "email", "phone", "role"))]

    def update(self, user_id, email=None, phone=None, password=None, role=None):
        rows = self._records()
        for i, row in enumerate(rows):
            if str(row.get("user_id")) == str(user_id):
                if email is not None:
                    from utils.validators import validate_email
                    email = str(email).strip()
                    if not email:
                        raise ValueError("Email cannot be empty.")
                    email = validate_email(email)
                    if self.exists("email", email, user_id):
                        raise ValueError("Duplicate email.")
                    row["email"] = email

                if phone is not None:
                    from utils.validators import validate_phone
                    phone = str(phone).strip()
                    if not phone:
                        raise ValueError("Phone cannot be empty.")
                    phone = validate_phone(phone)
                    if self.exists("phone", phone, user_id):
                        raise ValueError("Duplicate phone.")
                    row["phone"] = phone

                if password is not None:
                    password = str(password).strip()
                    if not password:
                        raise ValueError("Password cannot be empty.")
                    if len(password) < 6:
                        raise ValueError("Password must contain at least 6 characters.")
                    row["password"] = password

                if role is not None:
                    role = str(role).strip().lower()
                    if not role:
                        raise ValueError("Role cannot be empty.")
                    if role not in User.allowed_roles:
                        raise ValueError("Role must be admin or analyst.")
                    row["role"] = role

                self.storage.update_data(i, row)
                return row
        raise ValueError("User ID not found.")

    def delete(self, user_id):
        rows = self._records()
        for i, row in enumerate(rows):
            if str(row.get("user_id")) == str(user_id):
                return self.storage.delete_data(i)
        raise ValueError("User ID not found.")
