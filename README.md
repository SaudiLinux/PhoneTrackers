# Phone Lookup Tool - أداة البحث برقم الهاتف

**Developer:** Saudi Linux  
**Email:** SaudiLinux7@gmail.com

## تحذير مهم - Important Warning

⚠️ **هذه الأداة للأغراض التعليمية فقط**  
⚠️ **This tool is for educational purposes only**

- لا تستخدم هذه الأداة لأنشطة غير قانونية
- لا تنتهك خصوصية الآخرين
- استخدم فقط المعلومات المتاحة عامة
- احترم القوانين المحلية والدولية

## الوصف - Description

أداة تعليمية للبحث عن المعلومات المتاحة عامة المرتبطة بأرقام الهواتف. تستخدم APIs مشروعة فقط ولا تتخطى أي جدران حماية.

Educational tool for searching publicly available information associated with phone numbers. Uses only legitimate APIs and does not bypass any firewalls.

## المميزات - Features

### المميزات الأساسية
- ✅ التحقق من صحة رقم الهاتف
- ✅ معلومات شركة الاتصالات
- ✅ تحديد الدولة
- ✅ حفظ النتائج في JSON و CSV
- ✅ سجلات شاملة
- ✅ معالجة الأخطاء والتحقق
- ✅ إعدادات قابلة للتخصيص
- ✅ توافق متعدد المنصات

### المميزات المتقدمة
- ✅ المعالجة المجمعة (أرقام متعددة)
- ✅ تحليل متعدد الخيوط
- ✅ تتبع التقدم
- ✅ تاريخ التحليل
- ✅ تنسيق طرفية غني
- ✅ تسجيل الثقة
- ✅ كشف المنطقة الزمنية

### خيارات الواجهة
- ✅ واجهة سطر الأوامر (CLI)
- ✅ واجهة رسومية (GUI)
- ✅ واجهة الويب
- ✅ نقاط REST API
- ✅ معالجة ملفات مجمعة

### تنسيقات التصدير
- ✅ ملفات JSON
- ✅ ملفات CSV
- ✅ ملفات Excel (اختياري)
- ✅ تقارير قابلة للتحميل

## التثبيت - Installation

### 1. تحميل المتطلبات - Install Requirements

```bash
pip install -r requirements.txt
```

### 2. تشغيل الأداة - Run the Tool

#### للمستخدمين على ويندوز (موصى به)
1. **انقر مرتين على `install.bat`** للتثبيت التلقائي
2. **انقر مرتين على `run.bat`** لتشغيل منصة الإطلاق

#### التثبيت اليدوي
```bash
# واجهة سطر الأوامر الأساسية
python phone_lookup.py

# أداة التحليل المتقدم
python advanced_lookup.py

# الواجهة الرسومية
python gui_version.py

# واجهة الويب
python web_interface.py
```

## طريقة الاستخدام - Usage

### 1. واجهة سطر الأوامر
```bash
# الأداة الأساسية
python phone_lookup.py

# الأداة المتقدمة مع المعالجة المجمعة
python advanced_lookup.py

# البحث المباشر
python advanced_lookup.py +1234567890
```

### 2. الواجهة الرسومية
```bash
python gui_version.py
```

### 3. واجهة الويب
```bash
# تشغيل خادم الويب
python web_interface.py

# مضيف ومنفذ مخصص
python web_interface.py --host 0.0.0.0 --port 8080

# ثم افتح http://localhost:5000 في المتصفح
```

### 4. التكامل مع كود Python
```python
from advanced_lookup import AdvancedPhoneLookup

# تهيئة الأداة
tool = AdvancedPhoneLookup()

# تحليل رقم واحد
result = tool.comprehensive_analysis("+1234567890")
print(result)

# التحليل المجمع
numbers = ["+1234567890", "+0987654321"]
results = tool.batch_analysis(numbers)
tool.display_results(results)

# حفظ النتائج
filepath = tool.save_results(results)
print(f"تم حفظ النتائج في: {filepath}")
```

### أمثلة على أرقام الهواتف - Phone Number Examples

```
+966501234567  (Saudi Arabia)
+1234567890    (US/Canada)
+447123456789  (UK)
0501234567     (Local Saudi format)
```

## هيكل المشروع - Project Structure

```
iPhonTracker/
├── phone_lookup.py      # الملف الرئيسي
├── advanced_lookup.py   # أداة التحليل المتقدم مع المعالجة المجمعة
├── gui_version.py      # نسخة الواجهة الرسومية
├── web_interface.py    # واجهة الويب
├── requirements.txt     # المكتبات المطلوبة
├── README.md           # ملف التوثيق
├── config.py           # ملف الإعدادات
├── install.bat         # ملف التثبيت التلقائي
└── run.bat             # ملف تشغيل ويندوز
```

## المكتبات المستخدمة - Libraries Used

- **requests**: للاتصال بـ APIs
- **json**: لمعالجة البيانات
- **re**: للتعبيرات النمطية
- **typing**: لتحديد أنواع البيانات
- **time**: للتوقيت
- **urllib**: لمعالجة URLs

## المكتبات الاختيارية - Optional Libraries

- **httpx**: عميل HTTP محسن
- **beautifulsoup4**: لتحليل صفحات الويب
- **selenium**: للتحكم في المتصفح
- **colorama**: لتلوين النصوص
- **rich**: لتحسين عرض النتائج
- **click**: لواجهة سطر الأوامر
- **pandas**: لتحليل البيانات
- **phonenumbers**: للتحقق من أرقام الهواتف

## الإعدادات - Configuration

يمكنك تخصيص الأداة عبر تعديل ملف `config.py`:

- تغيير User-Agent
- إضافة APIs جديدة
- تخصيص تنسيق النتائج
- إعداد قاعدة البيانات

## الأمان والقانونية - Security & Legal

### ما تفعله الأداة - What the Tool Does:
- ✅ البحث في المعلومات المتاحة عامة
- ✅ استخدام APIs مشروعة
- ✅ احترام حدود المعدل
- ✅ عدم تخزين بيانات حساسة

### ما لا تفعله الأداة - What the Tool Does NOT Do:
- ❌ تخطي جدران الحماية
- ❌ اختراق قواعد البيانات
- ❌ انتهاك الخصوصية
- ❌ أنشطة غير قانونية

## المساهمة - Contributing

نرحب بالمساهمات! يرجى:

1. عمل Fork للمشروع
2. إنشاء فرع جديد للميزة
3. إضافة التحسينات
4. إرسال Pull Request

## الترخيص - License

هذا المشروع للأغراض التعليمية. استخدمه بمسؤولية واحترم القوانين.

## الدعم - Support

للدعم والاستفسارات:
- **Email:** SaudiLinux7@gmail.com
- **Developer:** Saudi Linux

## إخلاء المسؤولية - Disclaimer

⚠️ **تحذير مهم:**

هذه الأداة مخصصة للأغراض التعليمية والبحثية فقط. المطور غير مسؤول عن أي استخدام غير قانوني أو غير أخلاقي للأداة. يجب على المستخدمين:

- احترام خصوصية الآخرين
- الامتثال للقوانين المحلية والدولية
- عدم استخدام الأداة لأغراض ضارة
- الحصول على إذن قبل البحث عن معلومات الآخرين

**استخدم الأداة بمسؤولية!**

---

**Made with ❤️ by Saudi Linux**