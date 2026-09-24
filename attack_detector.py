from services.security_analyzer import SecurityAnalyzer


class AttackDetector(SecurityAnalyzer):
    attack_rules = {
        "brute_force": ("failed login", "multiple failed login"),
        "sql_injection": ("union select", "or 1=1", "drop table", "select * from"),
        "port_scan": ("port scan", "nmap", "multiple ports"),
        "suspicious_ip": ("blocked ip", "malicious ip"),
    }

    def __init__(self):
        self.detected_attacks = []

    def detect_brute_force(self, log):
        text = f"{log.action} {log.message}".lower()
        return "failed login" in text or "multiple failed login" in text

    def detect_port_scan(self, log):
        text = f"{log.action} {log.message}".lower()
        return any(x in text for x in ("port scan", "nmap", "multiple ports"))

    def detect_sql_injection(self, log):
        text = f"{log.action} {log.message}".lower()
        return any(x in text for x in self.attack_rules["sql_injection"])

    def detect_suspicious_ip(self, log):
        text = f"{log.action} {log.message}".lower()
        return any(x in text for x in self.attack_rules["suspicious_ip"])

    def detect_attack(self, log):
        checks = (("Brute Force", self.detect_brute_force), ("SQL Injection", self.detect_sql_injection),
                  ("Port Scan", self.detect_port_scan), ("Suspicious IP", self.detect_suspicious_ip))
        found = [name for name, checker in checks if checker(log)]
        self.detected_attacks.extend(found)
        return found

    def analyze(self, logs, *args, **kwargs):
        results = []
        for log in logs:
            attacks = self.detect_attack(log)
            if attacks:
                results.append({"log_id": log.log_id, "attacks": attacks, "source_ip": log.source_ip})
        return results
