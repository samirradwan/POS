#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تشغيل سريع لنظام إدارة المتجر
"""

import sys
import os

def main():
    print("🏪 نظام إدارة متجر الأدوات الكهربائية")
    print("=" * 50)
    
    # التحقق من Python
    print(f"إصدار Python: {sys.version}")
    
    if sys.version_info < (3, 7):
        print("❌ يتطلب Python 3.7 أو أحدث")
        return
    
    print("✅ إصدار Python مناسب")
    
    # التحقق من الوحدات الأساسية
    try:
        import tkinter as tk
        print("✅ tkinter متاح")
    except ImportError:
        print("❌ tkinter غير متاح")
        return
    
    try:
        import sqlite3
        print("✅ sqlite3 متاح")
    except ImportError:
        print("❌ sqlite3 غير متاح")
        return
    
    # التحقق من ملفات النظام
    required_files = [
        'database.py',
        'models.py', 
        'utils.py',
        'main_application.py',
        'product_management.py',
        'supplier_management.py',
        'sales_management.py',
        'expense_management.py',
        'reports.py',
        'backup_system.py'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} مفقود")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ ملفات مفقودة: {', '.join(missing_files)}")
        return
    
    print("\n🚀 بدء تشغيل النظام...")
    
    try:
        # استيراد وتشغيل النظام
        from main_application import MainApplication
        
        print("✅ تم تحميل النظام بنجاح")
        print("🖥️ فتح الواجهة الرسومية...")
        
        app = MainApplication()
        app.run()
        
    except Exception as e:
        print(f"❌ خطأ في تشغيل النظام: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
