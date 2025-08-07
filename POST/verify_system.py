#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
التحقق من النظام والميزات الجديدة
"""

import sys
import os

def check_files():
    """التحقق من وجود الملفات"""
    print("📁 التحقق من الملفات...")
    
    required_files = [
        'database.py',
        'models.py',
        'main_application.py',
        'invoice_inquiry.py',
        'product_inquiry.py',
        'utils.py'
    ]
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} مفقود")
            missing.append(file)
    
    return len(missing) == 0

def check_imports():
    """التحقق من الاستيرادات"""
    print("\n📦 التحقق من الاستيرادات...")
    
    try:
        import tkinter
        print("✅ tkinter")
    except:
        print("❌ tkinter")
        return False
    
    try:
        import sqlite3
        print("✅ sqlite3")
    except:
        print("❌ sqlite3")
        return False
    
    try:
        from database import Database
        print("✅ Database")
    except Exception as e:
        print(f"❌ Database: {e}")
        return False
    
    try:
        from models import ProductQuery, Invoice
        print("✅ ProductQuery, Invoice")
    except Exception as e:
        print(f"❌ ProductQuery, Invoice: {e}")
        return False
    
    return True

def check_database():
    """التحقق من قاعدة البيانات"""
    print("\n🗄️ التحقق من قاعدة البيانات...")
    
    try:
        from database import Database
        
        db = Database("test_verify.db")
        conn = db.connect()
        
        if conn:
            print("✅ اتصال قاعدة البيانات")
            
            cursor = conn.cursor()
            
            # التحقق من الجداول الجديدة
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='product_queries'")
            if cursor.fetchone():
                print("✅ جدول product_queries")
            else:
                print("❌ جدول product_queries")
                return False
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='invoices'")
            if cursor.fetchone():
                print("✅ جدول invoices")
            else:
                print("❌ جدول invoices")
                return False
            
            db.disconnect()
            
            # حذف ملف الاختبار
            if os.path.exists("test_verify.db"):
                os.remove("test_verify.db")
            
            return True
        else:
            print("❌ فشل الاتصال")
            return False
    
    except Exception as e:
        print(f"❌ خطأ: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("🔍 التحقق من نظام إدارة المتجر والميزات الجديدة")
    print("=" * 60)
    
    checks = [
        ("الملفات", check_files),
        ("الاستيرادات", check_imports),
        ("قاعدة البيانات", check_database)
    ]
    
    passed = 0
    for name, check_func in checks:
        if check_func():
            passed += 1
        else:
            print(f"\n❌ فشل في: {name}")
    
    print(f"\n📊 النتيجة: {passed}/{len(checks)}")
    
    if passed == len(checks):
        print("\n🎉 النظام جاهز!")
        print("✅ جميع الفحوصات نجحت")
        print("\n🚀 الميزات المتاحة:")
        print("   • إدارة المنتجات والمخزون")
        print("   • نقطة البيع مع الخصومات")
        print("   • إدارة الموردين والعملاء")
        print("   • تتبع المصروفات")
        print("   • تقارير شاملة")
        print("   • نظام النسخ الاحتياطي")
        print("   • استعلام الفواتير وطباعتها")
        print("   • استعلام المنتجات وحفظ الطلبات")
        
        print("\n▶️ لتشغيل النظام:")
        print("   python run_system.py")
        
        return True
    else:
        print("\n⚠️ يوجد مشاكل في النظام")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
