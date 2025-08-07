#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار قاعدة البيانات
"""

import sqlite3
import os

def test_database():
    """اختبار قاعدة البيانات"""
    print("🔍 اختبار قاعدة البيانات...")
    
    try:
        # إنشاء قاعدة البيانات
        db_name = "test_store.db"
        
        # حذف قاعدة البيانات إذا كانت موجودة
        if os.path.exists(db_name):
            os.remove(db_name)
            print("✅ تم حذف قاعدة البيانات القديمة")
        
        # إنشاء الاتصال
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        print("✅ تم إنشاء الاتصال")
        
        # إنشاء الجدول
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                cost_price REAL NOT NULL,
                sell_price REAL NOT NULL,
                quantity INTEGER NOT NULL
            )
        ''')
        print("✅ تم إنشاء جدول المنتجات")
        
        # إضافة منتج تجريبي
        cursor.execute(
            "INSERT INTO products (name, cost_price, sell_price, quantity) VALUES (?, ?, ?, ?)",
            ("منتج تجريبي", 10.0, 15.0, 100)
        )
        conn.commit()
        print("✅ تم إضافة منتج تجريبي")
        
        # قراءة المنتجات
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        print(f"✅ تم جلب {len(products)} منتج")
        
        for product in products:
            print(f"   - {product}")
        
        conn.close()
        print("✅ تم إغلاق الاتصال")
        
        # حذف قاعدة البيانات التجريبية
        os.remove(db_name)
        print("✅ تم حذف قاعدة البيانات التجريبية")
        
        print("🎉 اختبار قاعدة البيانات نجح!")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار قاعدة البيانات: {e}")
        return False

def test_imports():
    """اختبار الاستيرادات"""
    print("🔍 اختبار الاستيرادات...")
    
    try:
        import http.server
        print("✅ http.server")
        
        import socketserver
        print("✅ socketserver")
        
        import webbrowser
        print("✅ webbrowser")
        
        import threading
        print("✅ threading")
        
        import time
        print("✅ time")
        
        import json
        print("✅ json")
        
        import urllib.parse
        print("✅ urllib.parse")
        
        import sqlite3
        print("✅ sqlite3")
        
        import os
        print("✅ os")
        
        print("🎉 جميع الاستيرادات نجحت!")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في الاستيرادات: {e}")
        return False

if __name__ == "__main__":
    print("🚀 بدء الاختبارات...")
    
    # اختبار الاستيرادات
    imports_ok = test_imports()
    print()
    
    # اختبار قاعدة البيانات
    db_ok = test_database()
    print()
    
    if imports_ok and db_ok:
        print("🎉 جميع الاختبارات نجحت! النظام جاهز للعمل.")
    else:
        print("❌ بعض الاختبارات فشلت. يرجى مراجعة الأخطاء.")
