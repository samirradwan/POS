#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os

print("=" * 60)
print("🔍 تشخيص سريع لنظام إدارة المتجر")
print("Quick Diagnosis for Store Management System")
print("=" * 60)

print(f"🐍 إصدار Python: {sys.version}")
print(f"📁 مسار Python: {sys.executable}")
print(f"📂 مجلد العمل: {os.getcwd()}")
print()

# Test imports
print("🔍 فحص المكتبات المطلوبة...")
modules_to_test = [
    ('http.server', 'خادم الويب'),
    ('socketserver', 'دعم الشبكة'),
    ('sqlite3', 'قاعدة البيانات'),
    ('webbrowser', 'المتصفح'),
    ('threading', 'المعالجة المتوازية'),
    ('json', 'معالجة JSON'),
    ('urllib.parse', 'تحليل الروابط'),
    ('time', 'أدوات الوقت')
]

all_modules_ok = True
for module, description in modules_to_test:
    try:
        __import__(module)
        print(f"✅ {module} - متوفر ({description})")
    except ImportError:
        print(f"❌ {module} - مفقود ({description})")
        all_modules_ok = False

print()

# Test port
print("🔍 فحص المنفذ 8080...")
try:
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', 8080))
    sock.close()
    if result == 0:
        print("⚠️ المنفذ 8080 مستخدم حالياً")
        print("   يرجى إغلاق أي تطبيقات تستخدم هذا المنفذ")
    else:
        print("✅ المنفذ 8080 متاح")
except Exception as e:
    print(f"❌ خطأ في فحص المنفذ: {e}")

print()

# Test database
print("🔍 اختبار قاعدة البيانات...")
try:
    import sqlite3
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE test (id INTEGER, name TEXT)')
    cursor.execute('INSERT INTO test VALUES (1, "test")')
    cursor.execute('SELECT * FROM test')
    result = cursor.fetchone()
    conn.close()
    if result:
        print("✅ قاعدة البيانات تعمل بشكل صحيح")
    else:
        print("❌ مشكلة في قاعدة البيانات")
except Exception as e:
    print(f"❌ خطأ في قاعدة البيانات: {e}")

print()

# File check
print("🔍 فحص الملفات المطلوبة...")
files_to_check = [
    ('final_working_store.py', 'النظام الرئيسي'),
    ('start_final_store.bat', 'مشغل Windows'),
    ('FINAL_USER_GUIDE.md', 'دليل المستخدم'),
    ('requirements_final.txt', 'قائمة المتطلبات')
]

all_files_ok = True
for file, description in files_to_check:
    if os.path.exists(file):
        size = os.path.getsize(file)
        print(f"✅ {file} - موجود ({description}) - {size} بايت")
    else:
        print(f"❌ {file} - مفقود ({description})")
        all_files_ok = False

print()
print("=" * 60)

# Final assessment
if all_modules_ok and all_files_ok:
    print("🎉 جميع الفحوصات نجحت! النظام جاهز للعمل.")
    print("✅ All checks passed! System is ready to work.")
    print()
    print("للتشغيل:")
    print("1. اضغط مرتين على: start_final_store.bat")
    print("2. أو شغل: python final_working_store.py")
else:
    print("⚠️ بعض الفحوصات فشلت. يرجى مراجعة الأخطاء أعلاه.")
    print("⚠️ Some checks failed. Please review the errors above.")

print("=" * 60)
input("اضغط Enter للخروج... / Press Enter to exit...")
