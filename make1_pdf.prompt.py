import os
import subprocess

# 1. إعداد مسار حفظ ملف الـ PDF وصفحة الـ HTML المؤقتة
html_path = r"M:\CyberShield\temp_docs.html"
pdf_path = r"M:\CyberShield\CyberShield_Classes_Arabic.pdf"

# 2. إنشاء محتوى الـ HTML المنسق والداعم للعربية 100%
html_content = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>CyberShield Architecture</title>
    <style>
        @page { size: A4; margin: 12mm; }
        body { font-family: 'Segoe UI', Tahoma, Arial, sans-serif; color: #0f172a; line-height: 1.5; font-size: 11px; margin: 0; padding: 0; }
        .header { text-align: center; border-bottom: 2px solid #0284c7; padding-bottom: 8px; margin-bottom: 12px; }
        .header h1 { font-size: 18px; margin: 0; color: #0f172a; }
        .header p { color: #64748b; margin: 4px 0 0 0; font-size: 11px; }
        table { width: 100%; border-collapse: collapse; margin-top: 8px; }
        th, td { border: 1px solid #cbd5e1; padding: 6px 8px; text-align: right; vertical-align: top; }
        th { background-color: #f1f5f9; color: #0f172a; font-weight: bold; }
        .layer-title { background-color: #e2e8f0; font-weight: bold; color: #0369a1; }
        .code { font-family: Consolas, monospace; direction: ltr; text-align: left; font-size: 10px; color: #0f172a; }
        .path { font-family: Consolas, monospace; direction: ltr; text-align: left; color: #475569; font-size: 10px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🛡️ نظام CyberShield - توثيق الكلاسات والمعمارية البرمجية</h1>
        <p>توثيق شامل لجميع الفئات حسب المخطط الهيكلي (Layered Architecture)</p>
    </div>

    <table>
        <thead>
            <tr>
                <th style="width: 15%;">اسم الكلاس</th>
                <th style="width: 20%;">مسار الملف</th>
                <th style="width: 25%;">الخصائص والدوال الأساسية</th>
                <th style="width: 40%;">الوظيفة والشرح بالكامل</th>
            </tr>
        </thead>
        <tbody>
            <!-- Layer 1 -->
            <tr><td colspan="4" class="layer-title">1. طبقة التطبيق والتحكم (Application Layer)</td></tr>
            <tr>
                <td><b>CyberShieldApp</b></td>
                <td class="path">main.py</td>
                <td class="code">run(), current_user</td>
                <td>نقطة الدخول الرئيسية للنظام، إدارة الجلسات الحالية، التحكم في دورة القوائم التفاعلية (CLI)، وتوجيه المهام إلى الخدمات المختصة.</td>
            </tr>

            <!-- Layer 2 -->
            <tr><td colspan="4" class="layer-title">2. طبقة النماذج والبيانات (Models Layer)</td></tr>
            <tr>
                <td><b>User</b></td>
                <td class="path">models/user.py</td>
                <td class="code">user_id, username, role</td>
                <td>تمثيل حسابات المستخدمين وصلاحياتهم داخل النظام وتأكيد عمليات الدخول والتحقق الأمني.</td>
            </tr>
            <tr>
                <td><b>IPAddress</b></td>
                <td class="path">models/ip_address.py</td>
                <td class="code">ip_id, ip_address, status</td>
                <td>مراقبة وتصنيف عناوين الـ IP (حظر، سماح، مراقبة) وتحديد درجة سمعتها ومستوى خطورتها.</td>
            </tr>
            <tr>
                <td><b>Log</b></td>
                <td class="path">models/log.py</td>
                <td class="code">log_id, timestamp, source_ip</td>
                <td>تمثيل السجلات والأحداث الأمنية الواردة من الشبكة أو النظام لتخزينها وتحليلها.</td>
            </tr>
            <tr>
                <td><b>Alert</b></td>
                <td class="path">models/alert.py</td>
                <td class="code">alert_id, source_ip, severity</td>
                <td>إدارة التنبيهات الأمنية الصادرة عن محرك كشف الهجمات وتتبع حالات المعالجة (new, closed).</td>
            </tr>
            <tr>
                <td><b>Incident</b></td>
                <td class="path">models/incident.py</td>
                <td class="code">incident_id, title, status</td>
                <td>توثيق الحوادث الأمنية الحرجة والمؤكدة التي تتطلب تدخلاً ومتابعة من محلل أمني مخصص.</td>
            </tr>

            <!-- Layer 3 -->
            <tr><td colspan="4" class="layer-title">3. طبقة الخدمات ومعالجة البيانات (Services Layer)</td></tr>
            <tr>
                <td><b>CRUDService</b></td>
                <td class="path">services/crud_service.py</td>
                <td class="code">add(), get_all(), delete()</td>
                <td>كلاس أساسي عام يمنح عمليات الإدارة المشتركة (إضافة، استعراض، تعديل، حذف) لمنع تكرار الكود.</td>
            </tr>
            <tr>
                <td><b>UserService</b></td>
                <td class="path">services/user_service.py</td>
                <td class="code">login(), logout(), authenticate()</td>
                <td>إدارة منطق الحسابات، التحقق من كلمات المرور، وإدارة الصلاحيات وحفظ الجلسات.</td>
            </tr>
            <tr>
                <td><b>AttackDetector</b></td>
                <td class="path">services/attack_detector.py</td>
                <td class="code">detect_attacks(), match_patterns()</td>
                <td>محرك الفحص الذكي لمطابقة السجلات مع أنماط الهجمات (Brute Force, SQLi, Port Scan) وإنشاء التنبيهات.</td>
            </tr>
            <tr>
                <td><b>RiskAnalyzer</b></td>
                <td class="path">services/risk_analyzer.py</td>
                <td class="code">calculate_risk(), get_distribution()</td>
                <td>تقييم وحساب مستويات ومؤشرات الخطورة الإجمالية وتوزيع التهديدات (High, Medium, Low).</td>
            </tr>
            <tr>
                <td><b>SecurityAnalyzer</b></td>
                <td class="path">services/security_analyzer.py</td>
                <td class="code">correlate_events(), trace_ip()</td>
                <td>التحليل الأمني والربط المتقدم بين سلوكيات السجلات المتعددة وتتبع الأنشطة المشبوهة.</td>
            </tr>
            <tr>
                <td><b>DashboardService</b></td>
                <td class="path">services/dashboard.py</td>
                <td class="code">get_stats(), calculate_top_ips()</td>
                <td>تجميع وحساب مؤشرات لوحة التحكم المباشرة (إحصاء الكائنات، مستويات الخطورة، وأعلى الآيبيهات).</td>
            </tr>
            <tr>
                <td><b>SecurityReport</b></td>
                <td class="path">services/security_report.py</td>
                <td class="code">generate_report(), export_summary()</td>
                <td>إعداد واستخراج التقارير والملخصات الأمنية الشاملة وتصدير المخرجات.</td>
            </tr>

            <!-- Layer 4 -->
            <tr><td colspan="4" class="layer-title">4. طبقة الأدوات والتحقق (Utils Layer)</td></tr>
            <tr>
                <td><b>FileManager</b></td>
                <td class="path">utils/file_manager.py</td>
                <td class="code">read_json(), write_json()</td>
                <td>إدارة عمليات قراءة وكتابة وتحديث ملفات البيانات JSON في مجلد data بشكل آمن.</td>
            </tr>
            <tr>
                <td><b>Validators</b></td>
                <td class="path">utils/validators.py</td>
                <td class="code">is_valid_ip(), validate_password()</td>
                <td>التحقق من صحة بنية المدخلات وصيغ عناوين الـ IP وقوة كلمات المرور والتنسيقات.</td>
            </tr>
        </tbody>
    </table>
</body>
</html>
"""

# حفظ ملف الـ HTML
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

# 3. تحويل الـ HTML إلى PDF عبر متصفح Microsoft Edge بدون نوافذ (Headless)
edge_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(edge_exe):
    edge_exe = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

cmd = [
    edge_exe,
    "--headless",
    "--disable-gpu",
    f"--print-to-pdf={pdf_path}",
    html_path,
]

subprocess.run(cmd, check=True)

# تنظيف الملف المؤقت
if os.path.exists(html_path):
    os.remove(html_path)

print("SUCCESS: PDF Created successfully at:", pdf_path)