#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تشغيل مبسط للنظام
"""

import sys
import os

print("🚀 بدء تشغيل نظام إدارة المتجر...")
print("=" * 40)

# فحص Python
print(f"Python: {sys.version}")

# فحص الملفات
required_files = ['main_application.py', 'database.py', 'models.py']
for file in required_files:
    if os.path.exists(file):
        print(f"✅ {file}")
    else:
        print(f"❌ {file} مفقود")
        sys.exit(1)

# فحص tkinter
try:
    import tkinter as tk
    print("✅ tkinter متاح")
except ImportError:
    print("❌ tkinter غير متاح")
    sys.exit(1)

# محاولة تشغيل النظام
try:
    print("\n🔄 تحميل النظام...")
    
    # استيراد التطبيق
    from main_application import MainApplication
    print("✅ تم تحميل التطبيق")
    
    # إنشاء التطبيق
    print("🖥️ إنشاء الواجهة...")
    app = MainApplication()
    print("✅ تم إنشاء الواجهة")
    
    # تشغيل التطبيق
    print("🎉 تشغيل النظام...")
    app.run()
    
except ImportError as e:
    print(f"❌ خطأ في الاستيراد: {e}")
    print("\nتأكد من وجود جميع الملفات:")
    print("- main_application.py")
    print("- database.py") 
    print("- models.py")
    print("- utils.py")
    
except Exception as e:
    print(f"❌ خطأ في التشغيل: {e}")
    import traceback
    traceback.print_exc()
    
    print("\n💡 حلول مقترحة:")
    print("1. تأكد من وجود جميع الملفات")
    print("2. تأكد من تثبيت Python 3.7+")
    print("3. تأكد من تثبيت tkinter")
    print("4. جرب حذف ملف store_management.db وإعادة التشغيل")

input("\nاضغط Enter للخروج...")
