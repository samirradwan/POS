#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار نظام إدارة متجر الأدوات الكهربائية

هذا الملف يحتوي على اختبارات شاملة للنظام
للتأكد من عمل جميع الوظائف بشكل صحيح
"""

import unittest
import os
import sys
import tempfile
import shutil
from datetime import datetime

# إضافة المسار الحالي لاستيراد الوحدات
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import Database
from models import Product, Category, Supplier, Customer, Sale, Expense, ProductQuery, Invoice
from utils import CalculationUtils, ValidationUtils, ReportGenerator, BackupManager

class TestDatabase(unittest.TestCase):
    """اختبار قاعدة البيانات"""
    
    def setUp(self):
        """إعداد الاختبار"""
        self.test_db = "test_store.db"
        self.db = Database(self.test_db)
    
    def tearDown(self):
        """تنظيف بعد الاختبار"""
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
    
    def test_database_creation(self):
        """اختبار إنشاء قاعدة البيانات"""
        self.assertTrue(os.path.exists(self.test_db))
    
    def test_database_connection(self):
        """اختبار الاتصال بقاعدة البيانات"""
        conn = self.db.connect()
        self.assertIsNotNone(conn)
        self.db.disconnect()

class TestModels(unittest.TestCase):
    """اختبار النماذج"""
    
    def setUp(self):
        """إعداد الاختبار"""
        self.test_db = "test_models.db"
        self.db = Database(self.test_db)
        
        self.category = Category()
        self.supplier = Supplier()
        self.product = Product()
        self.customer = Customer()
        self.expense = Expense()
        self.product_query = ProductQuery()
        self.invoice = Invoice()
    
    def tearDown(self):
        """تنظيف بعد الاختبار"""
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
    
    def test_category_operations(self):
        """اختبار عمليات الفئات"""
        # إضافة فئة
        category_id = self.category.add_category("أدوات كهربائية", "فئة الأدوات الكهربائية")
        self.assertIsNotNone(category_id)
        
        # جلب الفئة
        category = self.category.get_category_by_id(category_id)
        self.assertIsNotNone(category)
        self.assertEqual(category['category_name'], "أدوات كهربائية")
        
        # تحديث الفئة
        success = self.category.update_category(category_id, "أدوات كهربائية محدثة", "وصف محدث")
        self.assertTrue(success)
        
        # حذف الفئة
        success = self.category.delete_category(category_id)
        self.assertTrue(success)
    
    def test_supplier_operations(self):
        """اختبار عمليات الموردين"""
        # إضافة مورد
        supplier_id = self.supplier.add_supplier("شركة الكهرباء", "01234567890")
        self.assertIsNotNone(supplier_id)
        
        # جلب المورد
        supplier = self.supplier.get_supplier_by_id(supplier_id)
        self.assertIsNotNone(supplier)
        self.assertEqual(supplier['supplier_name'], "شركة الكهرباء")
        
        # تحديث المورد
        success = self.supplier.update_supplier(supplier_id, "شركة الكهرباء المحدثة", "01234567891")
        self.assertTrue(success)
        
        # حذف المورد
        success = self.supplier.delete_supplier(supplier_id)
        self.assertTrue(success)
    
    def test_product_operations(self):
        """اختبار عمليات المنتجات"""
        # إضافة منتج
        product_id = self.product.add_product(
            name="لمبة LED",
            description="لمبة LED 10 واط",
            selling_price=25.0,
            purchasing_price=15.0,
            stock_quantity=100,
            discount_percentage=10.0,
            manual_discount=2.0
        )
        self.assertIsNotNone(product_id)
        
        # جلب المنتج
        product = self.product.get_product_by_id(product_id)
        self.assertIsNotNone(product)
        self.assertEqual(product['name'], "لمبة LED")
        
        # تحديث المنتج
        success = self.product.update_product(
            product_id=product_id,
            name="لمبة LED محدثة",
            description="لمبة LED 15 واط",
            selling_price=30.0,
            purchasing_price=18.0,
            stock_quantity=150,
            discount_percentage=15.0,
            manual_discount=3.0
        )
        self.assertTrue(success)
        
        # حذف المنتج
        success = self.product.delete_product(product_id)
        self.assertTrue(success)

    def test_product_query_operations(self):
        """اختبار عمليات استعلامات المنتجات"""
        # إضافة استعلام
        query_id = self.product_query.add_query(
            customer_id=None,
            product_name="لمبة LED",
            price=25.0,
            quantity=2,
            notes="استعلام تجريبي"
        )
        self.assertIsNotNone(query_id)

        # جلب الاستعلام
        query = self.product_query.get_query_by_id(query_id)
        self.assertIsNotNone(query)
        self.assertEqual(query['product_name'], "لمبة LED")

        # تحديد كمنفذ
        success = self.product_query.mark_as_executed(query_id)
        self.assertTrue(success)

        # حذف الاستعلام
        success = self.product_query.delete_query(query_id)
        self.assertTrue(success)

    def test_invoice_operations(self):
        """اختبار عمليات الفواتير"""
        # إنشاء بيع أولاً (مطلوب للفاتورة)
        from models import Sale
        sale_model = Sale()

        # بيانات بيع تجريبية
        sale_items = [{
            'product_id': 1,
            'quantity': 1,
            'selling_price': 25.0,
            'purchasing_price': 15.0,
            'discount_applied': 0,
            'manual_discount': 0,
            'final_price': 25.0
        }]

        sale_id = sale_model.add_sale(None, 25.0, 10.0, 25.0, sale_items)

        if sale_id:
            # إنشاء فاتورة
            invoice_id = self.invoice.create_invoice(sale_id, "عميل تجريبي")
            self.assertIsNotNone(invoice_id)

            # جلب الفاتورة
            invoice_data = self.invoice.get_invoice_by_id(invoice_id)
            self.assertIsNotNone(invoice_data)
            self.assertEqual(invoice_data['invoice']['customer_name'], "عميل تجريبي")

class TestCalculations(unittest.TestCase):
    """اختبار الحسابات"""
    
    def test_discount_calculation(self):
        """اختبار حساب الخصم"""
        # خصم نسبة مئوية فقط
        result = CalculationUtils.calculate_discount(100, 10, 0)
        self.assertEqual(result, 90.0)
        
        # خصم يدوي فقط
        result = CalculationUtils.calculate_discount(100, 0, 5)
        self.assertEqual(result, 95.0)
        
        # خصم نسبة مئوية + خصم يدوي
        result = CalculationUtils.calculate_discount(100, 10, 5)
        self.assertEqual(result, 85.0)
        
        # التأكد من عدم وجود قيم سالبة
        result = CalculationUtils.calculate_discount(10, 50, 10)
        self.assertEqual(result, 0.0)
    
    def test_profit_calculation(self):
        """اختبار حساب الربح"""
        profit = CalculationUtils.calculate_profit(25, 15, 10)
        self.assertEqual(profit, 100.0)  # (25-15) * 10 = 100
    
    def test_total_calculation(self):
        """اختبار حساب الإجمالي مع الخصومات"""
        items = [
            {
                'selling_price': 100,
                'quantity': 2,
                'discount_percentage': 10,
                'manual_discount': 5
            },
            {
                'selling_price': 50,
                'quantity': 1,
                'discount_percentage': 0,
                'manual_discount': 0
            }
        ]
        
        result = CalculationUtils.calculate_total_with_discount(items)
        
        # المجموع الفرعي: (100*2) + (50*1) = 250
        self.assertEqual(result['subtotal'], 250)
        
        # إجمالي الخصم: (200*0.1) + 5 + 0 = 25
        self.assertEqual(result['total_discount'], 25)
        
        # المجموع النهائي: 250 - 25 = 225
        self.assertEqual(result['final_total'], 225)

class TestValidation(unittest.TestCase):
    """اختبار التحقق من صحة البيانات"""
    
    def test_price_validation(self):
        """اختبار التحقق من صحة الأسعار"""
        self.assertTrue(ValidationUtils.validate_price("25.50"))
        self.assertTrue(ValidationUtils.validate_price("0"))
        self.assertFalse(ValidationUtils.validate_price("-10"))
        self.assertFalse(ValidationUtils.validate_price("abc"))
        self.assertFalse(ValidationUtils.validate_price(""))
    
    def test_quantity_validation(self):
        """اختبار التحقق من صحة الكميات"""
        self.assertTrue(ValidationUtils.validate_quantity("10"))
        self.assertTrue(ValidationUtils.validate_quantity("0"))
        self.assertFalse(ValidationUtils.validate_quantity("-5"))
        self.assertFalse(ValidationUtils.validate_quantity("abc"))
        self.assertFalse(ValidationUtils.validate_quantity(""))
    
    def test_discount_percentage_validation(self):
        """اختبار التحقق من صحة نسبة الخصم"""
        self.assertTrue(ValidationUtils.validate_discount_percentage("10"))
        self.assertTrue(ValidationUtils.validate_discount_percentage("0"))
        self.assertTrue(ValidationUtils.validate_discount_percentage("100"))
        self.assertFalse(ValidationUtils.validate_discount_percentage("150"))
        self.assertFalse(ValidationUtils.validate_discount_percentage("-10"))
        self.assertFalse(ValidationUtils.validate_discount_percentage("abc"))
    
    def test_required_field_validation(self):
        """اختبار التحقق من الحقول المطلوبة"""
        self.assertTrue(ValidationUtils.validate_required_field("نص صحيح"))
        self.assertFalse(ValidationUtils.validate_required_field(""))
        self.assertFalse(ValidationUtils.validate_required_field("   "))
        self.assertFalse(ValidationUtils.validate_required_field(None))

class TestBackupSystem(unittest.TestCase):
    """اختبار نظام النسخ الاحتياطي"""
    
    def setUp(self):
        """إعداد الاختبار"""
        self.test_db = "test_backup.db"
        self.backup_manager = BackupManager(self.test_db)
        
        # إنشاء قاعدة بيانات اختبار
        self.db = Database(self.test_db)
    
    def tearDown(self):
        """تنظيف بعد الاختبار"""
        # حذف ملفات الاختبار
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        
        # حذف مجلد النسخ الاحتياطية
        if os.path.exists(self.backup_manager.backup_dir):
            shutil.rmtree(self.backup_manager.backup_dir)
    
    def test_backup_creation(self):
        """اختبار إنشاء النسخة الاحتياطية"""
        backup_path = self.backup_manager.create_backup()
        self.assertIsNotNone(backup_path)
        self.assertTrue(os.path.exists(backup_path))
    
    def test_backup_list(self):
        """اختبار قائمة النسخ الاحتياطية"""
        # إنشاء نسخة احتياطية
        self.backup_manager.create_backup()
        
        # جلب القائمة
        backups = self.backup_manager.list_backups()
        self.assertGreater(len(backups), 0)
    
    def test_backup_restore(self):
        """اختبار استعادة النسخة الاحتياطية"""
        # إنشاء نسخة احتياطية
        backup_path = self.backup_manager.create_backup()
        
        # استعادة النسخة
        success = self.backup_manager.restore_backup(backup_path)
        self.assertTrue(success)

def run_all_tests():
    """تشغيل جميع الاختبارات"""
    print("بدء اختبار نظام إدارة المتجر...")
    print("=" * 50)
    
    # إنشاء مجموعة الاختبارات
    test_suite = unittest.TestSuite()
    
    # إضافة اختبارات قاعدة البيانات
    test_suite.addTest(unittest.makeSuite(TestDatabase))
    
    # إضافة اختبارات النماذج
    test_suite.addTest(unittest.makeSuite(TestModels))
    
    # إضافة اختبارات الحسابات
    test_suite.addTest(unittest.makeSuite(TestCalculations))
    
    # إضافة اختبارات التحقق
    test_suite.addTest(unittest.makeSuite(TestValidation))
    
    # إضافة اختبارات النسخ الاحتياطي
    test_suite.addTest(unittest.makeSuite(TestBackupSystem))
    
    # تشغيل الاختبارات
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    print("\n" + "=" * 50)
    print("نتائج الاختبار:")
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
    return len(result.failures) == 0 and len(result.errors) == 0

if __name__ == "__main__":
    success = run_all_tests()
    
    if success:
        print("\n✅ جميع الاختبارات نجحت! النظام جاهز للاستخدام.")
        sys.exit(0)
    else:
        print("\n❌ بعض الاختبارات فشلت. يرجى مراجعة الأخطاء أعلاه.")
        sys.exit(1)
