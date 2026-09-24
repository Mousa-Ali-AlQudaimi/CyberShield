from models.alert import Alert
from models.incident import SecurityIncident
from services.security_report import SecurityReport
from services.dashboard import Dashboard

alert = Alert("AL01", "Brute Force", "Repeated failed login", "high", "192.168.1.10")
incident = SecurityIncident("IN01", "Brute Force Incident", "Repeated failed login", "Brute Force", "192.168.1.10", 85)
incident.assign_user("analyst01")
report = SecurityReport("R01")
report.generate_report([{"id": 1}], [{"attacks": ["Brute Force"]}], [alert.to_dict()], [incident.to_dict()], {"critical": 1})
assert report.total_attacks == 1
report.export_report()
db = Dashboard([], [{"source_ip": "192.168.1.10"}], [{"attacks": ["Brute Force"]}], [alert.to_dict()], [incident.to_dict()])
assert db.count_incidents() == 1
print("Stage 4 OK - alerts, incidents, reports and dashboard.")
