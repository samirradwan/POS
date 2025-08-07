#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار بسيط للنظام
"""

import sys
import os

def test_imports():
    """اختبار استيراد الوحدات"""
    print("اختبار استيراد الوحدات...")
    
    try:
        import tkinter as tk
        print("✓ tkinter متاح")
    except ImportError as e:
        print(f"✗ خطأ في tkinter: {e}")
        return False
    
    try:
        import sqlite3
        print("✓ sqlite3 متاح")
    except ImportError as e:
        print(f"✗ خطأ في sqlite3: {e}")
        return False
    
    try:
        from database import Database
        print("✓ database.py متاح")
    except ImportError as e:
        print(f"✗ خطأ في database.py: {e}")
        return False
    
    try:
        from models import Product, Category, Supplier
        print("✓ models.py متاح")
    except ImportError as e:
        print(f"✗ خطأ في models.py: {e}")
        return False
    
    try:
        from utils import CalculationUtils, ValidationUtils
        print("✓ utils.py متاح")
    except ImportError as e:
        print(f"✗ خطأ في utils.py: {e}")
        return False
    
    return True

def test_database():
    """اختبار قاعدة البيانات"""
    print("\nاختبار قاعدة البيانات...")
    
    try:
        from database import Database
        
        # إنشاء قاعدة بيانات اختبار
        db = Database("test_simple.db")
        print("✓ تم إنشاء قاعدة البيانات")
        
        # اختبار الاتصال
        conn = db.connect()
        if conn:
            print("✓ تم الاتصال بقاعدة البيانات")
            db.disconnect()
        else:
            print("✗ فشل الاتصال بقاعدة البيانات")
            return False
        
        # حذف ملف الاختبار
        if os.path.exists("test_simple.db"):
            os.remove("test_simple.db")
            print("✓ تم حذف ملف الاختبار")
        
        return True
        
    except Exception as e:
        print(f"✗ خطأ في اختبار قاعدة البيانات: {e}")
        return False

def test_calculations():
    """اختبار الحسابات"""
    print("\nاختبار الحسابات...")
    
    try:
        from utils import CalculationUtils
        
        # اختبار حساب الخصم
        result = CalculationUtils.calculate_discount(100, 10, 5)
        expected = 85.0  # 100 - (100*0.1) - 5 = 85
        
        if result == expected:
            print(f"✓ حساب الخصم صحيح: {result}")
        else:
            print(f"✗ خطأ في حساب الخصم: توقع {expected}, حصل على {result}")
            return False
        
        # اختبار حساب الربح
        profit = CalculationUtils.calculate_profit(25, 15, 2)
        expected_profit = 20.0  # (25-15) * 2 = 20
        
        if profit == expected_profit:
            print(f"✓ حساب الربح صحيح: {profit}")
        else:
            print(f"✗ خطأ في حساب الربح: توقع {expected_profit}, حصل على {profit}")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ خطأ في اختبار الحسابات: {e}")
        return False

def test_validation():
    """اختبار التحقق من صحة البيانات"""
    print("\nاختبار التحقق من صحة البيانات...")
    
    try:
        from utils import ValidationUtils
        
        # اختبار التحقق من الأسعار
        if ValidationUtils.validate_price("25.50"):
            print("✓ التحقق من السعر الصحيح")
        else:
            print("✗ فشل التحقق من السعر الصحيح")
            return False
        
        if not ValidationUtils.validate_price("-10"):
            print("✓ رفض السعر السالب")
        else:
            print("✗ قبول السعر السالب خطأ")
            return False
        
        # اختبار التحقق من نسبة الخصم
        if ValidationUtils.validate_discount_percentage("15"):
            print("✓ التحقق من نسبة الخصم الصحيحة")
        else:
            print("✗ فشل التحقق من نسبة الخصم الصحيحة")
            return False
        
        if not ValidationUtils.validate_discount_percentage("150"):
            print("✓ رفض نسبة الخصم الخاطئة")
        else:
            print("✗ قبول نسبة الخصم الخاطئة")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ خطأ في اختبار التحقق: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("=" * 50)
    print("اختبار بسيط لنظام إدارة المتجر")
    print("=" * 50)
    
    tests = [
        ("استيراد الوحدات", test_imports),
        ("قاعدة البيانات", test_database),
        ("الحسابات", test_calculations),
        ("التحقق من البيانات", test_validation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        if test_func():
            passed += 1
            print(f"✓ {test_name}: نجح")
        else:
            print(f"✗ {test_name}: فشل")
    
    print("\n" + "=" * 50)
    print("نتائج الاختبار:")
    print(f"نجح: {passed}/{total}")
    print(f"فشل: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 جميع الاختبارات نجحت! النظام جاهز للاستخدام.")
        return True
    else:
        print(f"\n⚠️ {total - passed} اختبار فشل. يرجى مراجعة الأخطاء.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
