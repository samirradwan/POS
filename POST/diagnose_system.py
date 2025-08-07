#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تشخيص مشاكل النظام
"""

import sys
import os

def check_python():
    """فحص Python"""
    print("🐍 فحص Python:")
    print(f"   الإصدار: {sys.version}")
    print(f"   المسار: {sys.executable}")
    
    if sys.version_info >= (3, 7):
        print("   ✅ إصدار Python مناسب")
        return True
    else:
        print("   ❌ إصدار Python قديم (يتطلب 3.7+)")
        return False

def check_files():
    """فحص الملفات المطلوبة"""
    print("\n📁 فحص الملفات:")
    
    required_files = [
        'run_system.py',
        'main_application.py',
        'database.py',
        'models.py',
        'utils.py'
    ]
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} مفقود")
            missing.append(file)
    
    return len(missing) == 0

def check_modules():
    """فحص الوحدات المطلوبة"""
    print("\n📦 فحص الوحدات:")
    
    modules = [
        ('tkinter', 'مطلوب'),
        ('sqlite3', 'مطلوب'),
        ('datetime', 'مطلوب'),
        ('matplotlib', 'اختياري'),
        ('tkcalendar', 'اختياري')
    ]
    
    for module, status in modules:
        try:
            __import__(module)
            print(f"   ✅ {module} ({status})")
        except ImportError:
            if status == 'مطلوب':
                print(f"   ❌ {module} ({status}) - مفقود")
            else:
                print(f"   ⚠️ {module} ({status}) - مفقود")

def check_permissions():
    """فحص الصلاحيات"""
    print("\n🔐 فحص الصلاحيات:")
    
    try:
        # اختبار الكتابة
        test_file = "test_write.tmp"
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        print("   ✅ صلاحيات الكتابة متاحة")
        return True
    except Exception as e:
        print(f"   ❌ مشكلة في الصلاحيات: {e}")
        return False

def test_imports():
    """اختبار الاستيرادات"""
    print("\n🔄 اختبار الاستيرادات:")
    
    try:
        from database import Database
        print("   ✅ database.py")
    except Exception as e:
        print(f"   ❌ database.py: {e}")
        return False
    
    try:
        from models import Product
        print("   ✅ models.py")
    except Exception as e:
        print(f"   ❌ models.py: {e}")
        return False
    
    try:
        from utils import ValidationUtils
        print("   ✅ utils.py")
    except Exception as e:
        print(f"   ❌ utils.py: {e}")
        return False
    
    try:
        from main_application import MainApplication
        print("   ✅ main_application.py")
    except Exception as e:
        print(f"   ❌ main_application.py: {e}")
        return False
    
    return True

def test_database():
    """اختبار قاعدة البيانات"""
    print("\n🗄️ اختبار قاعدة البيانات:")
    
    try:
        from database import Database
        db = Database("test_db.db")
        conn = db.connect()
        
        if conn:
            print("   ✅ اتصال قاعدة البيانات")
            db.disconnect()
            
            # حذف ملف الاختبار
            if os.path.exists("test_db.db"):
                os.remove("test_db.db")
            
            return True
        else:
            print("   ❌ فشل اتصال قاعدة البيانات")
            return False
    
    except Exception as e:
        print(f"   ❌ خطأ في قاعدة البيانات: {e}")
        return False

def test_gui():
    """اختبار الواجهة الرسومية"""
    print("\n🖥️ اختبار الواجهة الرسومية:")
    
    try:
        import tkinter as tk
        
        # إنشاء نافذة اختبار
        root = tk.Tk()
        root.withdraw()  # إخفاء النافذة
        
        # اختبار إنشاء عناصر
        label = tk.Label(root, text="اختبار")
        button = tk.Button(root, text="اختبار")
        
        print("   ✅ إنشاء عناصر الواجهة")
        
        # إغلاق النافذة
        root.destroy()
        
        return True
    
    except Exception as e:
        print(f"   ❌ خطأ في الواجهة الرسومية: {e}")
        return False

def run_simple_test():
    """تشغيل اختبار بسيط للنظام"""
    print("\n🧪 اختبار بسيط للنظام:")
    
    try:
        # استيراد النظام
        from main_application import MainApplication
        
        # إنشاء التطبيق (بدون تشغيل)
        app = MainApplication()
        
        print("   ✅ إنشاء التطبيق نجح")
        
        # إغلاق التطبيق
        app.root.destroy()
        
        return True
    
    except Exception as e:
        print(f"   ❌ فشل اختبار النظام: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """الدالة الرئيسية"""
    print("🔍 تشخيص مشاكل نظام إدارة المتجر")
    print("=" * 50)
    
    tests = [
        ("Python", check_python),
        ("الملفات", check_files),
        ("الوحدات", check_modules),
        ("الصلاحيات", check_permissions),
        ("الاستيرادات", test_imports),
        ("قاعدة البيانات", test_database),
        ("الواجهة الرسومية", test_gui),
        ("النظام", run_simple_test)
    ]
    
    passed = 0
    failed_tests = []
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed_tests.append(test_name)
        except Exception as e:
            print(f"   ❌ خطأ في اختبار {test_name}: {e}")
            failed_tests.append(test_name)
    
    print("\n" + "=" * 50)
    print("📊 نتائج التشخيص:")
    print(f"نجح: {passed}/{len(tests)}")
    print(f"فشل: {len(failed_tests)}/{len(tests)}")
    
    if failed_tests:
        print(f"\nالاختبارات الفاشلة: {', '.join(failed_tests)}")
        
        print("\n💡 اقتراحات الحلول:")
        
        if "Python" in failed_tests:
            print("• قم بتحديث Python إلى إصدار 3.7 أو أحدث")
        
        if "الملفات" in failed_tests:
            print("• تأكد من وجود جميع ملفات النظام في نفس المجلد")
        
        if "الوحدات" in failed_tests:
            print("• قم بتثبيت الوحدات المفقودة: pip install tkinter matplotlib tkcalendar")
        
        if "الصلاحيات" in failed_tests:
            print("• شغل البرنامج كمدير أو انقل المجلد إلى مكان آخر")
        
        if "الاستيرادات" in failed_tests:
            print("• تحقق من وجود أخطاء في ملفات Python")
        
        if "قاعدة البيانات" in failed_tests:
            print("• تحقق من صلاحيات الكتابة وحذف أي ملفات قاعدة بيانات تالفة")
        
        if "الواجهة الرسومية" in failed_tests:
            print("• تأكد من تثبيت tkinter وأن النظام يدعم الواجهات الرسومية")
        
        if "النظام" in failed_tests:
            print("• راجع رسائل الخطأ أعلاه لمعرفة السبب المحدد")
    
    else:
        print("\n🎉 جميع الاختبارات نجحت!")
        print("النظام جاهز للتشغيل")
        print("\nلتشغيل النظام:")
        print("python run_system.py")
    
    return len(failed_tests) == 0

if __name__ == "__main__":
    success = main()
    
    if not success:
        print("\n⚠️ يوجد مشاكل تحتاج إلى حل قبل تشغيل النظام")
        input("\nاضغط Enter للخروج...")
    
    sys.exit(0 if success else 1)
