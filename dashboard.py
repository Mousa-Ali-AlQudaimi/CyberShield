from collections import Counter


class Dashboard:
    def __init__(self, users=None, logs=None, attacks=None, alerts=None, incidents=None):
        self.users = users or []
        self.logs = logs or []
        self.attacks = attacks or []
        self.alerts = alerts or []
        self.incidents = incidents or []

    def count_logs(self): return len(self.logs)
    def count_attacks(self): return sum(len(a.get("attacks", [])) for a in self.attacks)
    def count_alerts(self): return len(self.alerts)
    def count_incidents(self): return len(self.incidents)

    def show_risk_statistics(self):
        return Counter(a.get("severity", "low") for a in self.alerts)

    def show_top_ips(self):
        return Counter(log.get("source_ip", "unknown") for log in self.logs).most_common(5)

    def show_summary(self):
        return {"users": len(self.users), "logs": self.count_logs(), "attacks": self.count_attacks(),
                "alerts": self.count_alerts(), "incidents": self.count_incidents(),
                "risk": dict(self.show_risk_statistics()), "top_ips": self.show_top_ips()}
