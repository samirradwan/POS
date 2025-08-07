#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار سريع لميزات الاستعلام الجديدة
"""

import sys
import os

def test_imports():
    """اختبار استيراد الوحدات الجديدة"""
    print("🔍 اختبار استيراد ميزات الاستعلام...")
    
    try:
        from models import ProductQuery, Invoice
        print("✅ تم استيراد ProductQuery و Invoice")
    except ImportError as e:
        print(f"❌ خطأ في استيراد النماذج: {e}")
        return False
    
    try:
        from invoice_inquiry import InvoiceInquiryWindow
        print("✅ تم استيراد InvoiceInquiryWindow")
    except ImportError as e:
        print(f"❌ خطأ في استيراد واجهة استعلام الفواتير: {e}")
        return False
    
    try:
        from product_inquiry import ProductInquiryWindow
        print("✅ تم استيراد ProductInquiryWindow")
    except ImportError as e:
        print(f"❌ خطأ في استيراد واجهة استعلام المنتجات: {e}")
        return False
    
    return True

def test_database_tables():
    """اختبار جداول قاعدة البيانات الجديدة"""
    print("\n🗄️ اختبار جداول قاعدة البيانات الجديدة...")
    
    try:
        from database import Database
        
        # إنشاء قاعدة بيانات اختبار
        db = Database("test_inquiry.db")
        conn = db.connect()
        cursor = conn.cursor()
        
        # التحقق من جدول product_queries
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='product_queries'")
        if cursor.fetchone():
            print("✅ جدول product_queries موجود")
        else:
            print("❌ جدول product_queries غير موجود")
            return False
        
        # التحقق من جدول invoices
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='invoices'")
        if cursor.fetchone():
            print("✅ جدول invoices موجود")
        else:
            print("❌ جدول invoices غير موجود")
            return False
        
        # اختبار إدراج بيانات تجريبية
        cursor.execute("""INSERT INTO product_queries 
                         (product_name, price, quantity, notes, query_date, executed)
                         VALUES (?, ?, ?, ?, ?, ?)""",
                      ("منتج تجريبي", 25.0, 1, "اختبار", "2024-08-05", False))
        
        cursor.execute("SELECT COUNT(*) FROM product_queries")
        count = cursor.fetchone()[0]
        if count > 0:
            print(f"✅ تم إدراج بيانات تجريبية في product_queries ({count} سجل)")
        
        db.disconnect()
        
        # حذف ملف الاختبار
        if os.path.exists("test_inquiry.db"):
            os.remove("test_inquiry.db")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار قاعدة البيانات: {e}")
        return False

def test_models_functionality():
    """اختبار وظائف النماذج الجديدة"""
    print("\n🧪 اختبار وظائف النماذج الجديدة...")
    
    try:
        from models import ProductQuery, Invoice
        from database import Database
        
        # إنشاء قاعدة بيانات اختبار
        db = Database("test_models.db")
        
        # اختبار ProductQuery
        pq = ProductQuery()
        query_id = pq.add_query(None, "لمبة LED", 25.0, 2, "اختبار")
        
        if query_id:
            print("✅ تم إضافة استعلام منتج")
            
            # جلب الاستعلام
            query = pq.get_query_by_id(query_id)
            if query and query['product_name'] == "لمبة LED":
                print("✅ تم جلب الاستعلام بنجاح")
            else:
                print("❌ فشل في جلب الاستعلام")
                return False
            
            # البحث عن المنتجات
            results = pq.search_products("LED")
            print(f"✅ البحث عن المنتجات: {len(results)} نتيجة")
            
        else:
            print("❌ فشل في إضافة استعلام منتج")
            return False
        
        # اختبار Invoice
        invoice_model = Invoice()
        
        # جلب جميع الفواتير (قد تكون فارغة)
        invoices = invoice_model.get_all_invoices()
        print(f"✅ جلب الفواتير: {len(invoices)} فاتورة")
        
        # حذف ملف الاختبار
        if os.path.exists("test_models.db"):
            os.remove("test_models.db")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار النماذج: {e}")
        return False

def test_gui_creation():
    """اختبار إنشاء الواجهات الرسومية"""
    print("\n🖥️ اختبار إنشاء الواجهات الرسومية...")
    
    try:
        import tkinter as tk
        
        # إنشاء نافذة جذر مؤقتة
        root = tk.Tk()
        root.withdraw()  # إخفاء النافذة
        
        # اختبار إنشاء واجهة استعلام الفواتير
        from invoice_inquiry import InvoiceInquiryWindow
        invoice_window = InvoiceInquiryWindow(root)
        invoice_window.window.withdraw()  # إخفاء النافذة
        print("✅ تم إنشاء واجهة استعلام الفواتير")
        
        # اختبار إنشاء واجهة استعلام المنتجات
        from product_inquiry import ProductInquiryWindow
        product_window = ProductInquiryWindow(root)
        product_window.window.withdraw()  # إخفاء النافذة
        print("✅ تم إنشاء واجهة استعلام المنتجات")
        
        # إغلاق النوافذ
        invoice_window.window.destroy()
        product_window.window.destroy()
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في إنشاء الواجهات: {e}")
        return False

def test_main_app_integration():
    """اختبار التكامل مع التطبيق الرئيسي"""
    print("\n🔗 اختبار التكامل مع التطبيق الرئيسي...")
    
    try:
        from main_application import MainApplication
        
        # التحقق من وجود الوظائف الجديدة
        app = MainApplication()
        
        if hasattr(app, 'open_invoice_inquiry'):
            print("✅ وظيفة open_invoice_inquiry موجودة")
        else:
            print("❌ وظيفة open_invoice_inquiry غير موجودة")
            return False
        
        if hasattr(app, 'open_product_inquiry'):
            print("✅ وظيفة open_product_inquiry موجودة")
        else:
            print("❌ وظيفة open_product_inquiry غير موجودة")
            return False
        
        # إغلاق التطبيق
        app.root.destroy()
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار التكامل: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("🚀 اختبار سريع لميزات الاستعلام الجديدة")
    print("=" * 60)
    
    tests = [
        ("استيراد الوحدات", test_imports),
        ("جداول قاعدة البيانات", test_database_tables),
        ("وظائف النماذج", test_models_functionality),
        ("إنشاء الواجهات", test_gui_creation),
        ("التكامل مع التطبيق الرئيسي", test_main_app_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: نجح")
            else:
                print(f"❌ {test_name}: فشل")
        except Exception as e:
            print(f"❌ {test_name}: خطأ - {e}")
    
    print("\n" + "=" * 60)
    print("نتائج الاختبار السريع:")
    print(f"نجح: {passed}/{total}")
    print(f"فشل: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 جميع اختبارات ميزات الاستعلام نجحت!")
        print("✅ الميزات الجديدة جاهزة للاستخدام:")
        print("   • استعلام الفواتير وطباعتها")
        print("   • استعلام المنتجات وحفظ الطلبات")
        print("   • إدارة الطلبات المحفوظة")
        print("   • التكامل مع النظام الرئيسي")
        return True
    else:
        print(f"\n⚠️ {total - passed} اختبار فشل من أصل {total}")
        print("يرجى مراجعة الأخطاء أعلاه")
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🚀 يمكنك الآن تشغيل النظام واختبار الميزات الجديدة:")
        print("   python run_system.py")
        print("   ثم انقر على 'استعلامات' في القائمة العلوية")
    
    sys.exit(0 if success else 1)
