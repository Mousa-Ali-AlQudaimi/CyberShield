from services.security_analyzer import SecurityAnalyzer


class RiskAnalyzer(SecurityAnalyzer):
    risk_levels = ((0, "LOW"), (30, "MEDIUM"), (60, "HIGH"), (80, "CRITICAL"))

    def __init__(self):
        self.risk_score = 0
        self.risk_level = "LOW"

    def calculate_score(self, attacks, ip_reputation=50):
        weights = {
            "Brute Force": 25,
            "Port Scan": 30,
            "Suspicious IP": 35,
            "SQL Injection": 50
        }

        score = 0

        for attack in attacks:
            score += weights.get(attack, 20)

        score += max(0, 50 - int(ip_reputation))

        score = min(100, score)

        self.risk_score = score
        return score
    def calculate_level(self, score=None):
        score = self.risk_score if score is None else int(score)
        self.risk_level = next(level for threshold, level in reversed(self.risk_levels) if score >= threshold)
        return self.risk_level

    def analyze(self, attacks, ip_reputation=50, *args, **kwargs):
        score = self.calculate_score(attacks, ip_reputation)
        return {"score": score, "level": self.calculate_level(score)}

    def display_risk(self):
        return f"Risk: {self.risk_level} ({self.risk_score}/100)"
