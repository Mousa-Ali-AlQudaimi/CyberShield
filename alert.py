from datetime import datetime
from utils.validators import validate_required


class Alert:
    total_alerts = 0

    def __init__(self, alert_id, alert_type, message, severity, source_ip="unknown", status="new", timestamp=None):
        self.alert_id = validate_required(str(alert_id), "Alert ID")
        self.alert_type = validate_required(alert_type, "Alert type")
        self.message = validate_required(message, "Message")
        self.severity = str(severity).lower()
        if self.severity not in ("low", "medium", "high", "critical"):
            raise ValueError("Invalid alert severity.")
        self.timestamp = timestamp or datetime.now().isoformat(timespec="seconds")
        self.status = status
        self.source_ip = source_ip
        Alert.total_alerts += 1

    def create_alert(self):
        self.status = "new"
        return self

    def mark_as_read(self):
        self.status = "read"

    def close_alert(self):
        self.status = "closed"

    def escalate(self):
        order = ["low", "medium", "high", "critical"]
        self.severity = order[min(order.index(self.severity) + 1, 3)]

    def to_dict(self):
        return self.__dict__.copy()

    def __str__(self):
        return f"Alert#{self.alert_id} [{self.severity}] {self.alert_type} - {self.status}"
