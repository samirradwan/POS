#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام إدارة متجر الأدوات الكهربائية
ملف التشغيل الرئيسي

هذا الملف يقوم بتشغيل النظام مع التحقق من المتطلبات
والتعامل مع الأخطاء المحتملة
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox
import traceback

def check_python_version():
    """التحقق من إصدار Python"""
    if sys.version_info < (3, 7):
        messagebox.showerror("خطأ في الإصدار", 
                           f"هذا البرنامج يتطلب Python 3.7 أو أحدث\n"
                           f"الإصدار الحالي: {sys.version}")
        return False
    return True

def check_required_modules():
    """التحقق من وجود الوحدات المطلوبة"""
    required_modules = [
        'tkinter',
        'sqlite3',
        'datetime',
        'threading',
        'shutil',
        'os'
    ]
    
    optional_modules = [
        'matplotlib',
        'tkcalendar',
        'cryptography'
    ]
    
    missing_required = []
    missing_optional = []
    
    # فحص الوحدات المطلوبة
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_required.append(module)
    
    # فحص الوحدات الاختيارية
    for module in optional_modules:
        try:
            __import__(module)
        except ImportError:
            missing_optional.append(module)
    
    if missing_required:
        messagebox.showerror("وحدات مفقودة", 
                           f"الوحدات التالية مطلوبة ولكنها غير مثبتة:\n"
                           f"{', '.join(missing_required)}\n\n"
                           f"يرجى تثبيتها باستخدام pip install")
        return False
    
    if missing_optional:
        messagebox.showwarning("وحدات اختيارية مفقودة", 
                             f"الوحدات التالية اختيارية ولكنها غير مثبتة:\n"
                             f"{', '.join(missing_optional)}\n\n"
                             f"بعض الميزات قد لا تعمل بشكل كامل")
    
    return True

def check_database_permissions():
    """التحقق من صلاحيات قاعدة البيانات"""
    try:
        # محاولة إنشاء ملف اختبار
        test_file = "test_permissions.tmp"
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        return True
    except PermissionError:
        messagebox.showerror("خطأ في الصلاحيات", 
                           "البرنامج لا يملك صلاحيات الكتابة في المجلد الحالي\n"
                           "يرجى تشغيل البرنامج كمدير أو نقله إلى مجلد آخر")
        return False
    except Exception as e:
        messagebox.showerror("خطأ", f"حدث خطأ في فحص الصلاحيات: {str(e)}")
        return False

def create_directories():
    """إنشاء المجلدات المطلوبة"""
    directories = [
        'backups',
        'reports',
        'logs',
        'images'
    ]
    
    for directory in directories:
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except Exception as e:
            print(f"تحذير: لا يمكن إنشاء المجلد {directory}: {str(e)}")

def setup_error_logging():
    """إعداد تسجيل الأخطاء"""
    import logging
    from datetime import datetime
    
    # إنشاء مجلد السجلات إذا لم يكن موجوداً
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # إعداد ملف السجل
    log_filename = f"logs/system_{datetime.now().strftime('%Y%m%d')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

def handle_exception(exc_type, exc_value, exc_traceback):
    """معالج الأخطاء العام"""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    
    # تسجيل الخطأ
    logger = setup_error_logging()
    logger.error(f"خطأ غير متوقع: {error_msg}")
    
    # عرض رسالة للمستخدم
    messagebox.showerror("خطأ غير متوقع", 
                        f"حدث خطأ غير متوقع في البرنامج:\n\n"
                        f"{str(exc_value)}\n\n"
                        f"تم تسجيل تفاصيل الخطأ في ملف السجل")

def main():
    """الدالة الرئيسية لتشغيل النظام"""
    try:
        # إعداد معالج الأخطاء
        sys.excepthook = handle_exception
        
        # إعداد التسجيل
        logger = setup_error_logging()
        logger.info("بدء تشغيل نظام إدارة المتجر")
        
        # فحص المتطلبات
        print("فحص متطلبات النظام...")
        
        if not check_python_version():
            return
        
        if not check_required_modules():
            return
        
        if not check_database_permissions():
            return
        
        # إنشاء المجلدات المطلوبة
        create_directories()
        
        print("جميع المتطلبات متوفرة، بدء تشغيل النظام...")
        logger.info("جميع المتطلبات متوفرة")
        
        # استيراد وتشغيل التطبيق الرئيسي
        from main_application import MainApplication
        
        app = MainApplication()
        logger.info("تم تشغيل التطبيق بنجاح")
        
        # تشغيل التطبيق
        app.run()
        
        logger.info("تم إغلاق التطبيق بنجاح")
        
    except ImportError as e:
        messagebox.showerror("خطأ في الاستيراد", 
                           f"فشل في استيراد الوحدات المطلوبة:\n{str(e)}\n\n"
                           f"تأكد من وجود جميع ملفات البرنامج في نفس المجلد")
    
    except Exception as e:
        messagebox.showerror("خطأ في التشغيل", 
                           f"حدث خطأ أثناء تشغيل البرنامج:\n{str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
