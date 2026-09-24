from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

pdf_filename = "CyberShield_Classes_Documentation.pdf"
doc = SimpleDocTemplate(
    pdf_filename,
    pagesize=letter,
    rightMargin=36,
    leftMargin=36,
    topMargin=36,
    bottomMargin=36,
)

styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    "TitleStyle",
    parent=styles["Heading1"],
    fontSize=18,
    leading=22,
    textColor=colors.HexColor("#0f172a"),
)
subtitle_style = ParagraphStyle(
    "SubTitleStyle",
    parent=styles["Normal"],
    fontSize=10,
    leading=14,
    textColor=colors.HexColor("#475569"),
)
section_style = ParagraphStyle(
    "SectionStyle",
    parent=styles["Heading2"],
    fontSize=13,
    leading=17,
    textColor=colors.HexColor("#0284c7"),
    spaceBefore=10,
    spaceAfter=4,
)
cell_bold = ParagraphStyle(
    "CellBold",
    parent=styles["Normal"],
    fontSize=9,
    leading=12,
    fontName="Helvetica-Bold",
    textColor=colors.HexColor("#0f172a"),
)
cell_text = ParagraphStyle(
    "CellText",
    parent=styles["Normal"],
    fontSize=8.5,
    leading=11.5,
    textColor=colors.HexColor("#334155"),
)

story = []

# العنوان الرئيسي
story.append(Paragraph("CyberShield System - Architecture & Classes", title_style))
story.append(
    Paragraph("Layered Architecture Documentation based on Visio Diagram", subtitle_style)
)
story.append(Spacer(1, 8))
story.append(
    HRFlowable(
        width="100%", thickness=1.5, color=colors.HexColor("#0284c7"), spaceAfter=12
    )
)

data = [
    # Application Layer
    ("1. Application Layer", "", "", ""),
    (
        "CyberShieldApp",
        "main.py",
        "CLI Interface, Session state",
        "Main entry point, controls menu loops, dispatches actions to services.",
    ),
    # Models Layer
    ("2. Models Layer", "", "", ""),
    (
        "User",
        "models/user.py",
        "user_id, username, password_hash, role, is_active",
        "Represents system users, authenticates and checks privileges.",
    ),
    (
        "IPAddress",
        "models/ip_address.py",
        "ip_id, ip_address, status, reputation_score",
        "Tracks IP states (whitelisted/blacklisted/monitored) and reputation.",
    ),
    (
        "Log (SecurityLog)",
        "models/log.py",
        "log_id, timestamp, source_ip, event_type, severity",
        "Represents raw security events ingested from network or system.",
    ),
    (
        "Alert",
        "models/alert.py",
        "alert_id, source_ip, message, severity, status, timestamp",
        "Represents alarms generated from attack detection mechanisms.",
    ),
    (
        "Incident",
        "models/incident.py",
        "incident_id, title, severity, status, assigned_to",
        "Confirmed severe security incidents requiring analyst response.",
    ),
    # Services Layer
    ("3. Services Layer", "", "", ""),
    (
        "CRUDService",
        "services/crud_service.py",
        "add(), get_all(), get_by_id(), update(), delete()",
        "Generic Base Class providing reusable CRUD logic.",
    ),
    (
        "UserService",
        "services/user_service.py",
        "login(), logout(), authenticate(), manage_users()",
        "Handles user authentication, session security, and account management.",
    ),
    (
        "AttackDetector",
        "services/attack_detector.py",
        "detect_attacks(), match_patterns(), trigger_alert()",
        "Scans logs against attack patterns (Brute Force, SQLi, Port Scan) and generates Alerts.",
    ),
    (
        "RiskAnalyzer",
        "services/risk_analyzer.py",
        "calculate_risk(), get_distribution()",
        "Calculates security risk scores and categorizes threat severity levels.",
    ),
    (
        "SecurityAnalyzer",
        "services/security_analyzer.py",
        "correlate_events(), trace_ip_activity()",
        "Performs in-depth analysis and correlation between logs and IP behaviors.",
    ),
    (
        "DashboardService",
        "services/dashboard.py",
        "get_stats(), calculate_top_ips(), risk_summary()",
        "Aggregates metrics: total counts, risk breakdown, and top attacker IPs.",
    ),
    (
        "SecurityReport",
        "services/security_report.py",
        "generate_report(), export_summary()",
        "Creates periodic security posture reports and analytical summaries.",
    ),
    # Utils Layer
    ("4. Utils Layer", "", "", ""),
    (
        "FileManager",
        "utils/file_manager.py",
        "read_json(), write_json(), append_data()",
        "Handles safe persistence of entities inside data/ JSON storage.",
    ),
    (
        "Validators",
        "utils/validators.py",
        "is_valid_ip(), validate_password(), check_date()",
        "Validates input formats, IP integrity, and security constraints.",
    ),
]

table_rows = [
    [
        Paragraph("Class Name", cell_bold),
        Paragraph("File Path", cell_bold),
        Paragraph("Attributes / Core Methods", cell_bold),
        Paragraph("Role & Description", cell_bold),
    ]
]

header_indices = []
row_idx = 1

for item in data:
    if item[1] == "":
        table_rows.append(
            [Paragraph(f"<b>{item[0]}</b>", section_style), "", "", ""]
        )
        header_indices.append(row_idx)
    else:
        table_rows.append(
            [
                Paragraph(item[0], cell_bold),
                Paragraph(item[1], cell_text),
                Paragraph(item[2], cell_text),
                Paragraph(item[3], cell_text),
            ]
        )
    row_idx += 1

col_widths = [105, 110, 140, 185]
t = Table(table_rows, colWidths=col_widths, repeatRows=1)

table_style = [
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
    ("BOTTOMPADDING", (0, 0), (-1, 0), 5),
    ("TOPPADDING", (0, 0), (-1, 0), 5),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
]

for idx in header_indices:
    table_style.extend(
        [
            ("SPAN", (0, idx), (3, idx)),
            ("BACKGROUND", (0, idx), (3, idx), colors.HexColor("#e2e8f0")),
            ("TOPPADDING", (0, idx), (3, idx), 3),
            ("BOTTOMPADDING", (0, idx), (3, idx), 3),
        ]
    )

t.setStyle(TableStyle(table_style))
story.append(t)

doc.build(story)
print(f"تم إنشاء الملف بنجاح باسم: {pdf_filename}")