from datetime import datetime
from utils.validators import validate_required


class Log:
    total_logs = 0

    def __init__(self, log_id, timestamp, source_ip, destination_ip, action,
                 username="unknown", message="", severity="low"):
        self.log_id = validate_required(str(log_id), "Log ID")
        self.timestamp = validate_required(str(timestamp), "Timestamp")
        self.source_ip = validate_required(source_ip, "Source IP")
        self.destination_ip = validate_required(destination_ip, "Destination IP")
        self.action = validate_required(action, "Action")
        self.username = validate_required(username, "Username")
        self.message = str(message)
        self.severity = str(severity).lower()
        if self.severity not in ("low", "medium", "high", "critical"):
            raise ValueError("Invalid severity.")
        Log.total_logs += 1

    def parse_log(self):
        return {"source_ip": self.source_ip, "destination_ip": self.destination_ip,
                "action": self.action.lower(), "message": self.message.lower()}

    def validate_log(self):
        return all((self.source_ip, self.destination_ip, self.action, self.timestamp))

    def get_source_ip(self):
        return self.source_ip

    def is_failed_login(self):
        text = f"{self.action} {self.message}".lower()
        return "failed login" in text or ("login" in text and "fail" in text)

    def to_dict(self):
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, data):
        return cls(data["log_id"], data["timestamp"], data["source_ip"], data["destination_ip"],
                   data["action"], data.get("username", "unknown"), data.get("message", ""),
                   data.get("severity", "low"))

    def __str__(self):
        return f"Log#{self.log_id}: {self.source_ip} -> {self.destination_ip} | {self.action}"
