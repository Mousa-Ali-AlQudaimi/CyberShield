from models.user import Admin, Analyst
from services.user_service import UserService

service = UserService()
service.storage.save_data([])
admin = Admin("A01", "admin01", "secret1", "admin@test.com", "711234567")
analyst = Analyst("U01", "analyst01", "secret2", "analyst@test.com", "731234567")
service.add_user(admin)
service.add_user(analyst)
assert admin.user_id == "A01"
assert admin.show_permissions() != analyst.show_permissions()
assert service.authenticate("admin01", "secret1").role == "admin"
try:
    service.add_user(Analyst("U01", "another", "secret2", "another@test.com", "771234567"))
except ValueError:
    pass
else:
    raise AssertionError("Duplicate ID was accepted")
service.storage.save_data([])
print("Stage 2 OK - OOP, inheritance, polymorphism, properties and duplicate checks.")
