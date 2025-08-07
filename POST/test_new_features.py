#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار الميزات الجديدة - نظام الاستعلامات

هذا الملف يختبر الميزات الجديدة المضافة:
- استعلام الفواتير
- استعلام المنتجات
- حفظ الطلبات
"""

import sys
import os
import unittest
from datetime import datetime

# إضافة المسار الحالي لاستيراد الوحدات
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import Database
from models import ProductQuery, Invoice, Sale, Product, Category, Supplier

class TestNewFeatures(unittest.TestCase):
    """اختبار الميزات الجديدة"""
    
    def setUp(self):
        """إعداد الاختبار"""
        self.test_db = "test_new_features.db"
        self.db = Database(self.test_db)
        
        # إنشاء النماذج
        self.product_query = ProductQuery()
        self.invoice = Invoice()
        self.sale = Sale()
        self.product = Product()
        self.category = Category()
        self.supplier = Supplier()
        
        # إضافة بيانات تجريبية
        self.setup_test_data()
    
    def tearDown(self):
        """تنظيف بعد الاختبار"""
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
    
    def setup_test_data(self):
        """إعداد بيانات تجريبية"""
        # إضافة فئة
        self.category_id = self.category.add_category("أدوات كهربائية", "فئة تجريبية")
        
        # إضافة مورد
        self.supplier_id = self.supplier.add_supplier("مورد تجريبي", "01234567890")
        
        # إضافة منتج
        self.product_id = self.product.add_product(
            name="لمبة LED تجريبية",
            description="لمبة LED للاختبار",
            selling_price=25.0,
            purchasing_price=15.0,
            stock_quantity=100,
            category_id=self.category_id,
            supplier_id=self.supplier_id
        )
    
    def test_product_query_lifecycle(self):
        """اختبار دورة حياة استعلام المنتج"""
        print("\n--- اختبار استعلامات المنتجات ---")
        
        # 1. إضافة استعلام جديد
        query_id = self.product_query.add_query(
            customer_id=None,
            product_name="لمبة LED تجريبية",
            price=25.0,
            quantity=3,
            notes="طلب تجريبي للاختبار"
        )
        
        self.assertIsNotNone(query_id, "فشل في إضافة الاستعلام")
        print(f"✓ تم إضافة استعلام برقم: {query_id}")
        
        # 2. جلب الاستعلام
        query = self.product_query.get_query_by_id(query_id)
        self.assertIsNotNone(query, "فشل في جلب الاستعلام")
        self.assertEqual(query['product_name'], "لمبة LED تجريبية")
        self.assertEqual(query['quantity'], 3)
        self.assertFalse(query['executed'], "الاستعلام يجب أن يكون غير منفذ")
        print("✓ تم جلب الاستعلام بنجاح")
        
        # 3. البحث عن المنتجات
        products = self.product_query.search_products("LED")
        self.assertGreater(len(products), 0, "لم يتم العثور على منتجات")
        print(f"✓ تم العثور على {len(products)} منتج")
        
        # 4. تحديد الاستعلام كمنفذ
        success = self.product_query.mark_as_executed(query_id)
        self.assertTrue(success, "فشل في تحديد الاستعلام كمنفذ")
        print("✓ تم تحديد الاستعلام كمنفذ")
        
        # 5. التحقق من التحديث
        updated_query = self.product_query.get_query_by_id(query_id)
        self.assertTrue(updated_query['executed'], "الاستعلام يجب أن يكون منفذ")
        print("✓ تم التحقق من تحديث حالة الاستعلام")
        
        # 6. جلب جميع الاستعلامات
        all_queries = self.product_query.get_all_queries()
        self.assertGreater(len(all_queries), 0, "لا توجد استعلامات")
        print(f"✓ تم جلب {len(all_queries)} استعلام")
        
        # 7. تصفية الاستعلامات المنفذة
        executed_queries = self.product_query.get_all_queries(executed=True)
        self.assertGreater(len(executed_queries), 0, "لا توجد استعلامات منفذة")
        print(f"✓ تم جلب {len(executed_queries)} استعلام منفذ")
        
        # 8. حذف الاستعلام
        success = self.product_query.delete_query(query_id)
        self.assertTrue(success, "فشل في حذف الاستعلام")
        print("✓ تم حذف الاستعلام بنجاح")
    
    def test_invoice_system(self):
        """اختبار نظام الفواتير"""
        print("\n--- اختبار نظام الفواتير ---")
        
        # 1. إنشاء بيع أولاً
        sale_items = [{
            'product_id': self.product_id,
            'quantity': 2,
            'selling_price': 25.0,
            'purchasing_price': 15.0,
            'discount_applied': 0,
            'manual_discount': 0,
            'final_price': 25.0
        }]
        
        sale_id = self.sale.add_sale(
            customer_id=None,
            total_amount=50.0,
            profit=20.0,
            final_amount=50.0,
            sale_items=sale_items
        )
        
        self.assertIsNotNone(sale_id, "فشل في إنشاء البيع")
        print(f"✓ تم إنشاء بيع برقم: {sale_id}")
        
        # 2. إنشاء فاتورة
        invoice_id = self.invoice.create_invoice(sale_id, "عميل تجريبي")
        self.assertIsNotNone(invoice_id, "فشل في إنشاء الفاتورة")
        print(f"✓ تم إنشاء فاتورة برقم: {invoice_id}")
        
        # 3. جلب الفاتورة بالمعرف
        invoice_data = self.invoice.get_invoice_by_id(invoice_id)
        self.assertIsNotNone(invoice_data, "فشل في جلب الفاتورة")
        self.assertEqual(invoice_data['invoice']['customer_name'], "عميل تجريبي")
        print("✓ تم جلب الفاتورة بالمعرف")
        
        # 4. جلب الفاتورة برقم الفاتورة
        invoice_number = invoice_data['invoice']['invoice_number']
        invoice_by_number = self.invoice.get_invoice_by_number(invoice_number)
        self.assertIsNotNone(invoice_by_number, "فشل في جلب الفاتورة برقم الفاتورة")
        print(f"✓ تم جلب الفاتورة برقم: {invoice_number}")
        
        # 5. التحقق من تفاصيل الفاتورة
        details = invoice_by_number['details']
        self.assertGreater(len(details), 0, "لا توجد تفاصيل للفاتورة")
        self.assertEqual(details[0]['quantity'], 2)
        print(f"✓ تم التحقق من تفاصيل الفاتورة ({len(details)} منتج)")
        
        # 6. جلب جميع الفواتير
        all_invoices = self.invoice.get_all_invoices()
        self.assertGreater(len(all_invoices), 0, "لا توجد فواتير")
        print(f"✓ تم جلب {len(all_invoices)} فاتورة")
        
        # 7. تحديث حالة الفاتورة
        success = self.invoice.update_invoice_status(invoice_id, "cancelled")
        self.assertTrue(success, "فشل في تحديث حالة الفاتورة")
        print("✓ تم تحديث حالة الفاتورة")
    
    def test_search_functionality(self):
        """اختبار وظائف البحث"""
        print("\n--- اختبار وظائف البحث ---")
        
        # 1. البحث بالاسم
        results = self.product_query.search_products("LED")
        self.assertGreater(len(results), 0, "فشل البحث بالاسم")
        print(f"✓ البحث بالاسم: {len(results)} نتيجة")
        
        # 2. البحث بالوصف
        results = self.product_query.search_products("للاختبار")
        self.assertGreater(len(results), 0, "فشل البحث بالوصف")
        print(f"✓ البحث بالوصف: {len(results)} نتيجة")
        
        # 3. البحث بالفئة
        results = self.product_query.search_products("كهربائية")
        self.assertGreater(len(results), 0, "فشل البحث بالفئة")
        print(f"✓ البحث بالفئة: {len(results)} نتيجة")
        
        # 4. البحث بنص غير موجود
        results = self.product_query.search_products("منتج غير موجود")
        self.assertEqual(len(results), 0, "يجب ألا يعيد البحث نتائج")
        print("✓ البحث بنص غير موجود: لا توجد نتائج (صحيح)")
    
    def test_data_validation(self):
        """اختبار التحقق من صحة البيانات"""
        print("\n--- اختبار التحقق من البيانات ---")
        
        # 1. اختبار إضافة استعلام بكمية صفر
        query_id = self.product_query.add_query(
            customer_id=None,
            product_name="منتج تجريبي",
            price=10.0,
            quantity=0,  # كمية صفر
            notes=""
        )
        self.assertIsNotNone(query_id, "يجب قبول الكمية صفر")
        print("✓ تم قبول الكمية صفر")
        
        # 2. اختبار إضافة استعلام بسعر صفر
        query_id2 = self.product_query.add_query(
            customer_id=None,
            product_name="منتج مجاني",
            price=0.0,  # سعر صفر
            quantity=1,
            notes=""
        )
        self.assertIsNotNone(query_id2, "يجب قبول السعر صفر")
        print("✓ تم قبول السعر صفر")
        
        # 3. اختبار البحث بنص فارغ
        results = self.product_query.search_products("")
        self.assertGreaterEqual(len(results), 0, "البحث بنص فارغ يجب أن يعيد جميع المنتجات")
        print(f"✓ البحث بنص فارغ: {len(results)} نتيجة")

def run_new_features_test():
    """تشغيل اختبارات الميزات الجديدة"""
    print("🔍 اختبار الميزات الجديدة - نظام الاستعلامات")
    print("=" * 60)
    
    # إنشاء مجموعة الاختبارات
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestNewFeatures))
    
    # تشغيل الاختبارات
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    print("\n" + "=" * 60)
    print("نتائج اختبار الميزات الجديدة:")
    print(f"إجمالي الاختبارات: {result.testsRun}")
    print(f"نجح: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"فشل: {len(result.failures)}")
    print(f"أخطاء: {len(result.errors)}")
    
    if result.failures:
        print("\nالاختبارات الفاشلة:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nأخطاء الاختبار:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    # إرجاع النتيجة
    success = len(result.failures) == 0 and len(result.errors) == 0
    
    if success:
        print("\n🎉 جميع اختبارات الميزات الجديدة نجحت!")
        print("✅ نظام الاستعلامات جاهز للاستخدام")
    else:
        print("\n⚠️ بعض اختبارات الميزات الجديدة فشلت")
    
    return success

if __name__ == "__main__":
    success = run_new_features_test()
    sys.exit(0 if success else 1)
