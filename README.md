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

- ✅ التحقق من صحة رقم الهاتف
- ✅ معلومات شركة الاتصالات
- ✅ تحديد الدولة
- ✅ واجهة سهلة الاستخدام
- ✅ حفظ النتائج في ملف JSON
- ✅ وضع تعليمي آمن

## التثبيت - Installation

### 1. تحميل المتطلبات - Install Requirements

```bash
pip install -r requirements.txt
```

### 2. تشغيل الأداة - Run the Tool

```bash
python phone_lookup.py
```

## طريقة الاستخدام - Usage

1. شغل الأداة باستخدام الأمر أعلاه
2. أدخل رقم الهاتف المراد البحث عنه
3. انتظر النتائج
4. اختر حفظ النتائج إذا أردت

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
├── requirements.txt     # المكتبات المطلوبة
├── README.md           # ملف التوثيق
├── config.py           # ملف الإعدادات
├── gui_version.py      # نسخة الواجهة الرسومية
└── install.bat         # ملف التثبيت التلقائي
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