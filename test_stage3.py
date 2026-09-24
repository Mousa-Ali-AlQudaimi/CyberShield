from models.ip_address import IPAddress
from models.log import Log
from services.attack_detector import AttackDetector
from services.risk_analyzer import RiskAnalyzer

ip = IPAddress("IP01", "192.168.1.10", reputation=20)
log = Log("L01", "2026-09-14 10:00", ip.address, "10.0.0.5", "login", "admin", "failed login from unknown source")
found = AttackDetector().analyze([log])
assert found and "Brute Force" in found[0]["attacks"]
risk = RiskAnalyzer().analyze(found[0]["attacks"], ip.reputation)
assert risk["level"] in ("MEDIUM", "HIGH", "CRITICAL")
print("Stage 3 OK - IP, logs, attack detection and risk analysis.")
