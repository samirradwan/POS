#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تشغيل النظام مع ضمان ظهور النافذة
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os
import time

def force_window_to_front(window):
    """إجبار النافذة على الظهور في المقدمة"""
    window.lift()
    window.attributes('-topmost', True)
    window.update()
    window.attributes('-topmost', False)
    window.focus_force()
    window.grab_set()
    window.grab_release()

def main():
    """تشغيل النظام مع ضمان الظهور"""
    print("🚀 تشغيل نظام إدارة المتجر...")
    print("=" * 50)
    
    try:
        # إنشاء نافذة تحميل أولاً
        splash = tk.Tk()
        splash.title("تحميل النظام")
        splash.geometry("400x200")
        splash.configure(bg='#2c3e50')
        splash.resizable(False, False)
        
        # جعل النافذة في وسط الشاشة
        splash.eval('tk::PlaceWindow . center')
        
        # محتوى نافذة التحميل
        title_label = tk.Label(splash, text="نظام إدارة متجر الأدوات الكهربائية", 
                              font=('Arial', 14, 'bold'), 
                              bg='#2c3e50', fg='white')
        title_label.pack(pady=30)
        
        status_label = tk.Label(splash, text="جاري تحميل النظام...", 
                               font=('Arial', 12), 
                               bg='#2c3e50', fg='#ecf0f1')
        status_label.pack(pady=10)
        
        progress_label = tk.Label(splash, text="⏳ يرجى الانتظار", 
                                 font=('Arial', 10), 
                                 bg='#2c3e50', fg='#95a5a6')
        progress_label.pack(pady=10)
        
        # إجبار النافذة على الظهور
        force_window_to_front(splash)
        
        # تحديث النافذة
        splash.update()
        time.sleep(1)
        
        # تحديث حالة التحميل
        status_label.config(text="تحميل الوحدات...")
        splash.update()
        time.sleep(0.5)
        
        # استيراد النظام الرئيسي
        from main_application import MainApplication
        
        status_label.config(text="إنشاء الواجهة...")
        splash.update()
        time.sleep(0.5)
        
        # إنشاء التطبيق الرئيسي
        app = MainApplication()
        
        status_label.config(text="تم التحميل بنجاح!")
        splash.update()
        time.sleep(0.5)
        
        # إغلاق نافذة التحميل
        splash.destroy()
        
        # إجبار النافذة الرئيسية على الظهور
        force_window_to_front(app.root)
        
        print("✅ تم تشغيل النظام بنجاح!")
        print("🖥️ النافذة الرئيسية مفتوحة الآن")
        
        # تشغيل النظام
        app.run()
        
    except ImportError as e:
        messagebox.showerror("خطأ في الاستيراد", 
                           f"فشل في تحميل النظام:\n{str(e)}\n\n"
                           f"تأكد من وجود جميع الملفات المطلوبة")
        
    except Exception as e:
        messagebox.showerror("خطأ", f"حدث خطأ: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
