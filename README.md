# CyberShield - Stages 2 to 4

This package continues **Stage 1** and implements the remaining core OOP project.

## Stage 2 - Users & OOP
- `models/user.py`: `User`, `Admin`, `Analyst`
- Encapsulation with private attributes and properties
- Inheritance and polymorphism
- Class attributes, class methods, static methods, getters/setters
- Immutable `user_id` and `username`
- Login/logout and password change
- Duplicate ID, username, email and phone prevention

## Stage 3 - Cybersecurity Analysis
- `models/ip_address.py`
- `models/log.py`
- `services/security_analyzer.py` (abstract class)
- `services/attack_detector.py`
- `services/risk_analyzer.py`
- Detects brute force, SQL injection, port scan and suspicious IP patterns
- Risk score: 0-100 with LOW/MEDIUM/HIGH/CRITICAL

## Stage 4 - Response & Reporting
- `models/alert.py`
- `models/incident.py`
- `services/security_report.py`
- `services/dashboard.py`
- `main.py` interactive menu
- JSON file persistence

## Tests
Run from the `CyberShield` directory:
```bash
python test_stage1.py
python test_stage2.py
python test_stage3.py
python test_stage4.py
```

Then run:
```bash
python main.py
```

## OOP requirements covered
The project includes 4+ classes, the five core OOP concepts, instance/class attributes and methods, static/class methods, properties, getter/setter behavior, dunder methods, specific exception handling, validation, duplicate prevention, menus, files, lists/sets/tuples/dictionaries, `*args`, `**kwargs`, lambda-ready function usage, and multiple modules.
