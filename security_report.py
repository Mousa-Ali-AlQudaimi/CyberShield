from datetime import datetime
from utils.file_manager import FileManager


class SecurityReport:
    report_count = 0

    def __init__(self, report_id, title="Security Report"):
        self.report_id = str(report_id)
        self.title = title
        self.generated_at = None
        self.total_logs = 0
        self.total_attacks = 0
        self.total_alerts = 0
        self.total_incidents = 0
        self.risk_summary = {}
        SecurityReport.report_count += 1

    def generate_report(self, logs, attacks, alerts, incidents, risks=None):
        self.generated_at = datetime.now().isoformat(timespec="seconds")
        self.total_logs = len(logs)
        self.total_attacks = sum(len(item.get("attacks", [])) for item in attacks)
        self.total_alerts = len(alerts)
        self.total_incidents = len(incidents)
        self.risk_summary = risks or {}
        return self.to_dict()

    def get_statistics(self):
        return {"logs": self.total_logs, "attacks": self.total_attacks,
                "alerts": self.total_alerts, "incidents": self.total_incidents}

    def export_report(self):
        FileManager("reports.json").append_data(self.to_dict())

    def to_dict(self):
        return self.__dict__.copy()

    def display_report(self):
        stats = self.get_statistics()
        return (f"{self.title}\nLogs: {stats['logs']} | Attacks: {stats['attacks']} | "
                f"Alerts: {stats['alerts']} | Incidents: {stats['incidents']}\nRisk: {self.risk_summary}")
