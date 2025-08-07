#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تشخيص مشاكل التشغيل
"""

import sys
import os
import traceback

print("🔍 تشخيص النظام...")
print("=" * 50)

# فحص Python
print(f"✅ Python: {sys.version}")
print(f"✅ المجلد الحالي: {os.getcwd()}")

# فحص الملفات المطلوبة
required_files = [
    'main_application.py',
    'database.py', 
    'models.py',
    'utils.py'
]

print("\n📁 فحص الملفات:")
missing_files = []
for file in required_files:
    if os.path.exists(file):
        print(f"✅ {file}")
    else:
        print(f"❌ {file} مفقود")
        missing_files.append(file)

if missing_files:
    print(f"\n❌ ملفات مفقودة: {missing_files}")
    input("اضغط Enter للخروج...")
    sys.exit(1)

# فحص tkinter
print("\n🖥️ فحص tkinter:")
try:
    import tkinter as tk
    print("✅ tkinter متاح")
    
    # اختبار إنشاء نافذة بسيطة
    print("🔄 اختبار إنشاء نافذة...")
    root = tk.Tk()
    root.withdraw()  # إخفاء النافذة
    print("✅ يمكن إنشاء نوافذ tkinter")
    root.destroy()
    
except Exception as e:
    print(f"❌ مشكلة في tkinter: {e}")
    input("اضغط Enter للخروج...")
    sys.exit(1)

# فحص استيراد الملفات
print("\n📦 فحص الاستيراد:")
try:
    print("🔄 استيراد database...")
    import database
    print("✅ database")
    
    print("🔄 استيراد models...")
    import models
    print("✅ models")
    
    print("🔄 استيراد utils...")
    import utils
    print("✅ utils")
    
    print("🔄 استيراد main_application...")
    import main_application
    print("✅ main_application")
    
except Exception as e:
    print(f"❌ خطأ في الاستيراد: {e}")
    print("\n🔍 تفاصيل الخطأ:")
    traceback.print_exc()
    input("اضغط Enter للخروج...")
    sys.exit(1)

# محاولة إنشاء التطبيق
print("\n🚀 اختبار إنشاء التطبيق:")
try:
    print("🔄 إنشاء MainApplication...")
    from main_application import MainApplication
    
    app = MainApplication()
    print("✅ تم إنشاء التطبيق بنجاح!")
    
    print("\n🎉 كل شيء يعمل! سيتم تشغيل النظام...")
    print("=" * 50)
    
    # تشغيل النظام
    app.run()
    
except Exception as e:
    print(f"❌ خطأ في إنشاء التطبيق: {e}")
    print("\n🔍 تفاصيل الخطأ:")
    traceback.print_exc()
    
    print("\n💡 حلول مقترحة:")
    print("1. تأكد من وجود قاعدة البيانات")
    print("2. جرب حذف store_management.db")
    print("3. تأكد من صحة ملفات النظام")
    
    input("اضغط Enter للخروج...")
