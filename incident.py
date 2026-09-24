from datetime import datetime
from utils.validators import validate_required


class SecurityIncident:
    total_incidents = 0
    statuses = ("open", "investigating", "contained", "closed")

    def __init__(self, incident_id, title, description, attack_type, source_ip,
                 risk_score=0, status="open", created_at=None, assigned_to=None):
        self.incident_id = validate_required(str(incident_id), "Incident ID")
        self.title = validate_required(title, "Title")
        self.description = validate_required(description, "Description")
        self.attack_type = validate_required(attack_type, "Attack type")
        self.source_ip = source_ip
        self.risk_score = int(risk_score)
        if not 0 <= self.risk_score <= 100:
            raise ValueError("Risk score must be between 0 and 100.")
        self.status = status
        if self.status not in self.statuses:
            raise ValueError("Invalid incident status.")
        self.created_at = created_at or datetime.now().isoformat(timespec="seconds")
        self.assigned_to = assigned_to
        self.closed_at = None
        SecurityIncident.total_incidents += 1

    def create_incident(self):
        self.status = "open"
        return self

    def update_status(self, status):
        if status not in self.statuses:
            raise ValueError("Invalid incident status.")
        self.status = status
        if status == "closed":
            self.closed_at = datetime.now().isoformat(timespec="seconds")

    def assign_user(self, username):
        self.assigned_to = validate_required(username, "Assigned user")

    def close_incident(self):
        self.update_status("closed")

    def calculate_duration(self):
        start = datetime.fromisoformat(self.created_at)
        end = datetime.fromisoformat(self.closed_at) if self.closed_at else datetime.now()
        return end - start

    def to_dict(self):
        return self.__dict__.copy()

    def __str__(self):
        return f"Incident#{self.incident_id}: {self.title} [{self.status}] risk={self.risk_score}"
