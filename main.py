
from getpass import getpass
import sys
from pathlib import Path

# Allow direct execution from VS Code/Windows: python main.py
PROJECT_DIR = Path(__file__).resolve().parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from models.user import Admin, Analyst
from models.ip_address import IPAddress
from models.log import Log
from models.alert import Alert
from models.incident import SecurityIncident
from services.user_service import UserService
from services.crud_service import CRUDService
from services.attack_detector import AttackDetector
from services.risk_analyzer import RiskAnalyzer
from services.security_report import SecurityReport
from services.dashboard import Dashboard
from utils.file_manager import FileManager
from utils.validators import validate_phone, validate_numeric, validate_ip, validate_required


class CyberShieldApp:
    MAIN_MENU = {
        "1": "Register User",
        "2": "Login",
        "0": "Exit",
    }

    AUTH_MENU = {
        "1": "Logout",
        "2": "Manage Users",
        "3": "Manage IP Addresses",
        "4": "Manage Security Logs",
        "5": "Analyze Logs / Detect Attacks",
        "6": "Manage Alerts",
        "7": "Manage Security Incidents",
        "8": "Dashboard",
        "9": "Reports",
        "0": "Exit",
    }

    USER_MENU = {
        "1": "Add User",
        "2": "Display Users",
        "3": "Search Users",
        "4": "Update User",
        "5": "Delete User",
        "0": "Back",
    }

    IP_MENU = {
        "1": "Add IP",
        "2": "Display IPs",
        "3": "Search IPs",
        "4": "Update IP",
        "5": "Delete IP",
        "6": "Block / Change Status",
        "0": "Back",
    }

    LOG_MENU = {
        "1": "Add Log",
        "2": "Display Logs",
        "3": "Search Logs",
        "4": "Update Log",
        "5": "Delete Log",
        "0": "Back",
    }

    ALERT_MENU = {
        "1": "Display Alerts",
        "2": "Search Alerts",
        "3": "Update Alert Status",
        "4": "Delete Alert",
        "0": "Back",
    }

    INCIDENT_MENU = {
        "1": "Add Incident",
        "2": "Display Incidents",
        "3": "Search Incidents",
        "4": "Update Incident",
        "5": "Delete Incident",
        "0": "Back",
    }

    REPORT_MENU = {
        "1": "Generate Report",
        "2": "Display Reports",
        "3": "Search Reports",
        "4": "Delete Report",
        "0": "Back",
    }

    def __init__(self):
        self.user_service = UserService()
        self.current_user = None
        self.detector = AttackDetector()
        self.risk_analyzer = RiskAnalyzer()
        self.ip_crud = CRUDService("ips.json", "ip_id")
        self.log_crud = CRUDService("logs.json", "log_id")
        self.alert_crud = CRUDService("alerts.json", "alert_id")
        self.incident_crud = CRUDService("incidents.json", "incident_id")
        self.report_crud = CRUDService("reports.json", "report_id")

    @staticmethod
    def display_header(title, width=60):
        print(f"\n{'=' * width}")
        print(f"{title:^{width}}")
        print(f"{'=' * width}")

    @staticmethod
    def show_menu(title, options):
        print(f"\n{'-' * 60}")
        print(title)
        print('-' * 60)
        for key, label in options.items():
            print(f"{key}. {label}")

    def run(self):
        while True:
            self.display_header("CyberShield - Security Platform")
            print(f"Current user: {self.current_user.username if self.current_user else 'Guest'}")
            menu = self.MAIN_MENU if self.current_user is None else self.AUTH_MENU
            self.show_menu("Main Menu", menu)
            try:
                choice = input("Enter your choice: ").strip()
                if choice == "0":
                    print("Goodbye.")
                    break

                if self.current_user is None:
                    actions = {"1": self.register_user, "2": self.login}
                else:
                    actions = {
                        "1": self.logout,
                        "2": self.manage_users,
                        "3": self.manage_ips,
                        "4": self.manage_logs,
                        "5": self.analyze_logs,
                        "6": self.manage_alerts,
                        "7": self.manage_incidents,
                        "8": self.dashboard,
                        "9": self.manage_reports,
                    }

                if choice not in actions:
                    raise ValueError("Invalid menu choice.")
                actions[choice]()
            except (ValueError, TypeError, FileNotFoundError, IndexError) as error:
                print(f"Error: {error}")

    def require_login(self):
        if not self.current_user:
            raise ValueError("Please login first.")

    def require_admin(self):
        self.require_login()
        if self.current_user.role != "admin": raise PermissionError("Admin permission required.")

    def register_user(self):
        print("\n--- Register New User ---")
        user_id = validate_required(input("User ID: "), "User ID")
        username = input("Username: ").strip()
        password = getpass("Password: ")
        email = input("Email: ").strip()
        phone = validate_phone(input("Phone (9 digits): ").strip())
        role = input("Role (admin/analyst): ").strip().lower()
        if role not in ("admin", "analyst"):
            raise ValueError("Role must be admin or analyst.")
        user = Admin(user_id, username, password, email, phone) if role == "admin" else Analyst(user_id, username, password, email, phone)
        self.user_service.add_user(user)
        print("User registered successfully.")

    def login(self):
        username = input("Username: ").strip()
        password = getpass("Password: ")
        self.current_user = self.user_service.authenticate(username, password)
        print(f"Welcome {self.current_user.username}! {self.current_user.show_permissions()}")

    def logout(self):
        if self.current_user: self.current_user.logout(); self.current_user = None; print("Logged out.")
        else: print("No active session.")

    @staticmethod
    def format_record_display(row):
        if isinstance(row, dict):
            preferred_order = (
                "user_id", "username", "email", "phone", "role",
                "ip_id", "address", "country", "status", "reputation",
                "log_id", "timestamp", "source_ip", "destination_ip", "action","message", "severity",
                "alert_id", "title", "incident_id", "assigned_to",
                "report_id", "generated_at"
            )
            parts = []
            for key in preferred_order:
                if key in row:
                    parts.append(f"{key}: {row[key]}")
            if not parts:
                for key, value in row.items():
                    parts.append(f"{key}: {value}")
            return " | ".join(parts)
        return str(row)

    @staticmethod
    def print_rows(rows, title="Records"):
        print(f"\n{'-' * 60}")
        print(f"{title} ({len(rows)})")
        print('-' * 60)
        if not rows:
            print("No records found.")
            return

        for i, row in enumerate(rows, 1):
            print(f"{i:>2}. {CyberShieldApp.format_record_display(row)}")

    def manage_users(self):
        self.require_admin()
        while True:
            self.show_menu("Users Menu", self.USER_MENU)
            c = input("Choice: ").strip()
            if c == "0": return
            if c == "1": self.register_user()
            elif c == "2": self.print_rows(self.user_service.get_all(), "Users")
            elif c == "3": self.print_rows(self.user_service.search(input("Search: ").strip()), "Search Results")
            elif c == "4": self.update_user()
            elif c == "5": self.delete_user()
            else: raise ValueError("Invalid user menu choice.")

    def update_user(self):
        user_id = input("User ID to update: ").strip()
        if not self.user_service.find_by_id(user_id): raise ValueError("User ID not found.")
        print("Leave a field empty to keep its current value. ID and username cannot be changed.")
        email = input("New email: ").strip() or None
        phone = input("New phone: ").strip() or None
        password = getpass("New password (empty = keep): ") or None
        role = input("New role (admin/analyst, empty = keep): ").strip().lower() or None
        self.user_service.update(user_id, email, phone, password, role)
        print("User updated successfully.")

    def delete_user(self):
        user_id = input("User ID to delete: ").strip()
        if self.current_user and str(self.current_user.user_id) == str(user_id): raise ValueError("You cannot delete the currently logged-in user.")
        confirm = input("Type DELETE to confirm: ")
        if confirm == "DELETE": self.user_service.delete(user_id); print("User deleted.")
        else: print("Delete cancelled.")

    def manage_ips(self):
        self.require_login()
        while True:
            self.show_menu("IP Management", self.IP_MENU)
            c = input("Choice: ").strip()
            if c == "0": return
            if c == "1": self.add_ip()
            elif c == "2": self.print_rows(self.ip_crud.all(), "IP Addresses")
            elif c == "3": self.print_rows(self.ip_crud.search(input("Search: ").strip()), "IP Search")
            elif c == "4": self.update_ip()
            elif c == "5": self.delete_record(self.ip_crud, "IP ID")
            elif c == "6": self.change_ip_status()
            else: raise ValueError("Invalid IP menu choice.")

    def add_ip(self):
        ip_id = validate_required(input("IP ID: "), "IP ID")
        address = validate_ip(input("IP address: "))
        country = input("Country: ").strip() or "Unknown"
        status = input("Status (active/blocked/watchlist): ").strip().lower() or "active"
        reputation = validate_numeric(input("Reputation (0-100): "))
        self.ip_crud.add(IPAddress(ip_id, address, country, status, reputation).to_dict())
        print("IP added.")

    def update_ip(self):
        ip_id = input("IP ID: ").strip(); row = self.ip_crud.find(ip_id)
        if not row: raise ValueError("IP ID not found.")
        address = input(f"New address [{row['address']}]: ").strip() or row['address']
        country = input(f"New country [{row.get('country','Unknown')}]: ").strip() or row.get('country','Unknown')
        status = input(f"New status [{row['status']}]: ").strip().lower() or row['status']
        reputation = input(f"New reputation [{row['reputation']}]: ").strip()
        changes = {"address": validate_ip(address), "country": country, "status": status,
                   "reputation": validate_numeric(reputation) if reputation else row['reputation']}
        self.ip_crud.update(ip_id, changes, protected=("ip_id",)); print("IP updated.")

    def change_ip_status(self):
        ip_id = input("IP ID: ").strip(); status = input("Status (active/blocked/watchlist): ").strip().lower()
        self.ip_crud.update(ip_id, {"status": status}, protected=("ip_id",)); print("Status updated.")

    def manage_logs(self):
        self.require_login()
        while True:
            self.show_menu("Logs Management", self.LOG_MENU)
            c = input("Choice: ").strip()
            if c == "0": return
            if c == "1": self.add_log()
            elif c == "2": self.print_rows(self.log_crud.all(), "Security Logs")
            elif c == "3": self.print_rows(self.log_crud.search(input("Search: ").strip()), "Log Search")
            elif c == "4": self.update_log()
            elif c == "5": self.delete_record(self.log_crud, "Log ID")
            else: raise ValueError("Invalid log menu choice.")

    def add_log(self):
        log_id = validate_required(input("Log ID: "), "Log ID")
        source = validate_ip(input("Source IP: ")); destination = validate_ip(input("Destination IP: "))
        timestamp = validate_required(input("Timestamp: "), "Timestamp")
        action = validate_required(input("Action: "), "Action")
        message = input("Message: ").strip(); severity = input("Severity (low/medium/high/critical): ").strip().lower() or "low"
        log = Log(log_id, timestamp, source, destination, action, self.current_user.username, message, severity)
        self.log_crud.add(log.to_dict()); print("Log added.")

    def update_log(self):
        log_id = input("Log ID: ").strip(); row = self.log_crud.find(log_id)
        if not row: raise ValueError("Log ID not found.")
        for key in ("timestamp", "action", "message", "severity"):
            value = input(f"New {key} [{row.get(key,'')}]: ").strip()
            if value: row[key] = value
        self.log_crud.update(log_id, row, protected=("log_id",)); print("Log updated.")

    def analyze_logs(self):
        self.require_login()

        logs = [Log.from_dict(r) for r in self.log_crud.all()]
        results = self.detector.analyze(logs)

        if not results:
            print("No attacks detected.")
            return

        existing_alerts = self.alert_crud.all()
        new_alerts = 0

        for result in results:
            risk = self.risk_analyzer.analyze(result["attacks"])

            print(
                f"Log {result['log_id']} | "
                f"{result['source_ip']} | "
                f"{result['attacks']} | "
                f"{risk}"
            )

            attack_type = result["attacks"][0]
            message = f"Detected: {', '.join(result['attacks'])}"
            source_ip = result["source_ip"]

            # Check if the same alert already exists
            duplicate = any(
                str(alert.get("source_ip")) == str(source_ip)
                and str(alert.get("alert_type")) == str(attack_type)
                and str(alert.get("message")) == str(message)
                for alert in existing_alerts
            )

            if duplicate:
                continue

            alert_id = f"AL{len(existing_alerts) + 1:03d}"
            alert_severity = risk["level"].lower()

            alert = Alert(
                alert_id,
                attack_type,
                message,
                alert_severity,
                source_ip
            )

            self.alert_crud.add(alert.to_dict())
            existing_alerts.append(alert.to_dict())
            new_alerts += 1

        print(
            f"Analysis completed. {len(results)} suspicious logs found. "
            f"{new_alerts} new alerts created."
    )
    def manage_alerts(self):
        self.require_login()
        while True:
            self.show_menu("Alerts Management", self.ALERT_MENU)
            c = input("Choice: ").strip()
            if c == "0": return
            if c == "1": self.print_rows(self.alert_crud.all(), "Alerts")
            elif c == "2": self.print_rows(self.alert_crud.search(input("Search: ").strip()), "Alert Search")
            elif c == "3": self.update_alert()
            elif c == "4": self.delete_record(self.alert_crud, "Alert ID")
            else: raise ValueError("Invalid alert menu choice.")

    def update_alert(self):
        alert_id = input("Alert ID: ").strip(); status = input("New status (new/read/closed): ").strip().lower()
        self.alert_crud.update(alert_id, {"status": status}, protected=("alert_id",)); print("Alert updated.")

    def manage_incidents(self):
        self.require_login()
        while True:
            self.show_menu("Incidents Management", self.INCIDENT_MENU)
            c = input("Choice: ").strip()
            if c == "0": return
            if c == "1": self.add_incident()
            elif c == "2": self.print_rows(self.incident_crud.all(), "Incidents")
            elif c == "3": self.print_rows(self.incident_crud.search(input("Search: ").strip()), "Incident Search")
            elif c == "4": self.update_incident()
            elif c == "5": self.delete_record(self.incident_crud, "Incident ID")
            else: raise ValueError("Invalid incident menu choice.")

    def add_incident(self):
        incident_id = validate_required(input("Incident ID: "), "Incident ID")
        title = input("Title: "); description = input("Description: "); attack = input("Attack type: ")
        source = validate_ip(input("Source IP: ")); score = validate_numeric(input("Risk score (0-100): "))
        obj = SecurityIncident(incident_id, title, description, attack, source, score)
        self.incident_crud.add(obj.to_dict()); print("Incident created.")

    def update_incident(self):
        incident_id = input("Incident ID: ").strip(); row = self.incident_crud.find(incident_id)
        if not row: raise ValueError("Incident ID not found.")
        status = input(f"Status [{row['status']}] (open/investigating/contained/closed): ").strip().lower() or row['status']
        assigned = input(f"Assigned to [{row.get('assigned_to') or ''}]: ").strip() or row.get('assigned_to')
        self.incident_crud.update(incident_id, {"status": status, "assigned_to": assigned}, protected=("incident_id",)); print("Incident updated.")
    def dashboard(self):
        self.require_login()
        files = {
            name: FileManager(name).load_data([])
            for name in ("users.json", "logs.json", "alerts.json", "incidents.json")
            }

        logs = [Log.from_dict(row) for row in files["logs.json"]]
        attacks = self.detector.analyze(logs)
        data = Dashboard(
            files["users.json"],
            files["logs.json"],
            attacks,
            files["alerts.json"],
            files["incidents.json"]
            ).show_summary()
        print("\n--- SECURITY DASHBOARD ---")
        for k, v in data.items():
            print(f"{k}: {v}")

    def manage_reports(self):
        self.require_login()
        while True:
            self.show_menu("Reports Management", self.REPORT_MENU)
            c = input("Choice: ").strip()
            if c == "0": return
            if c == "1": self.generate_report()
            elif c == "2": self.print_rows(self.report_crud.all(), "Reports")
            elif c == "3": self.print_rows(self.report_crud.search(input("Search: ").strip()), "Report Search")
            elif c == "4": self.delete_record(self.report_crud, "Report ID")
            else: raise ValueError("Invalid report menu choice.")
    def generate_report(self):
        self.require_login()

        # Generate a unique Report ID automatically
        existing_reports = self.report_crud.all()
        numbers = []

        for report in existing_reports:
            report_id = str(report.get("report_id", ""))

            if report_id.startswith("R") and report_id[1:].isdigit():
                numbers.append(int(report_id[1:]))

        next_number = max(numbers, default=0) + 1
        report_id = f"R{next_number:03d}"

        title = input("Report title [Security Report]: ").strip() or "Security Report"

        report = SecurityReport(report_id, title)

        # Load logs and detect attacks
        logs = [Log.from_dict(r) for r in self.log_crud.all()]
        attacks = self.detector.analyze(logs)

        # Calculate risk summary
        risk_summary = {}

        for item in attacks:
            risk = self.risk_analyzer.analyze(item["attacks"])
            level = risk["level"]
            risk_summary[level] = risk_summary.get(level, 0) + 1

        # Generate report
        report.generate_report(
            self.log_crud.all(),
            attacks,
            self.alert_crud.all(),
            self.incident_crud.all(),
            risk_summary
        )

        self.report_crud.add(report.to_dict())

        print(f"Report generated successfully: {report_id}")
        print(report.display_report())

    @staticmethod
    def delete_record(service, label):
        item_id = input(f"{label} to delete: ").strip()
        if not item_id:
            print("Delete cancelled: empty ID.")
            return

        confirm = input("Type DELETE to confirm: ")
        if confirm == "DELETE":
            try:
                service.delete(item_id)
                print("Deleted successfully.")
            except ValueError as error:
                print(f"Delete failed: {error}")
        else:
            print("Delete cancelled.")


if __name__ == "__main__":
    CyberShieldApp().run()
