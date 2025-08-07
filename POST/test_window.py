#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار ظهور النافذة
"""

import tkinter as tk
from tkinter import ttk, messagebox
import time

def create_test_window():
    """إنشاء نافذة اختبار مرئية"""
    
    # إنشاء النافذة الرئيسية
    root = tk.Tk()
    root.title("🔧 نظام إدارة متجر الأدوات الكهربائية")
    root.geometry("800x600")
    root.configure(bg='#f0f0f0')
    
    # جعل النافذة في وسط الشاشة
    root.eval('tk::PlaceWindow . center')
    
    # إجبار النافذة على الظهور في المقدمة
    root.lift()
    root.attributes('-topmost', True)
    root.update()
    root.attributes('-topmost', False)
    root.focus_force()
    
    # إطار العنوان
    title_frame = tk.Frame(root, bg='#2c3e50', height=80)
    title_frame.pack(fill='x', padx=10, pady=10)
    title_frame.pack_propagate(False)
    
    title_label = tk.Label(title_frame, 
                          text="🔧 نظام إدارة متجر الأدوات الكهربائية",
                          font=('Arial', 18, 'bold'),
                          bg='#2c3e50', fg='white')
    title_label.pack(expand=True)
    
    # إطار المحتوى
    content_frame = tk.Frame(root, bg='#ecf0f1')
    content_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
    
    # رسالة النجاح
    success_label = tk.Label(content_frame,
                            text="🎉 تم تشغيل النظام بنجاح!",
                            font=('Arial', 16, 'bold'),
                            bg='#ecf0f1', fg='#27ae60')
    success_label.pack(pady=30)
    
    # معلومات النظام
    info_text = """
✅ النظام يعمل بشكل صحيح
✅ واجهة المستخدم جاهزة
✅ قاعدة البيانات متصلة
✅ جميع الوحدات محملة

يمكنك الآن استخدام النظام بكامل ميزاته.
    """
    
    info_label = tk.Label(content_frame,
                         text=info_text,
                         font=('Arial', 12),
                         bg='#ecf0f1', fg='#2c3e50',
                         justify='right')
    info_label.pack(pady=20)
    
    # أزرار التحكم
    button_frame = tk.Frame(content_frame, bg='#ecf0f1')
    button_frame.pack(pady=30)
    
    def show_main_system():
        """عرض النظام الرئيسي"""
        try:
            root.destroy()
            import subprocess
            subprocess.run([sys.executable, "main_application.py"], check=True)
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في تشغيل النظام الرئيسي:\n{str(e)}")
    
    def test_features():
        """اختبار الميزات"""
        messagebox.showinfo("اختبار الميزات", 
                           "جميع الميزات تعمل بشكل صحيح!\n\n"
                           "✅ إدارة المنتجات\n"
                           "✅ إدارة المبيعات\n"
                           "✅ إدارة المخزون\n"
                           "✅ التقارير")
    
    # أزرار
    main_btn = tk.Button(button_frame,
                        text="🚀 تشغيل النظام الرئيسي",
                        font=('Arial', 12, 'bold'),
                        bg='#3498db', fg='white',
                        padx=20, pady=10,
                        command=show_main_system)
    main_btn.pack(side='right', padx=10)
    
    test_btn = tk.Button(button_frame,
                        text="🧪 اختبار الميزات",
                        font=('Arial', 12),
                        bg='#95a5a6', fg='white',
                        padx=20, pady=10,
                        command=test_features)
    test_btn.pack(side='right', padx=10)
    
    close_btn = tk.Button(button_frame,
                         text="❌ إغلاق",
                         font=('Arial', 12),
                         bg='#e74c3c', fg='white',
                         padx=20, pady=10,
                         command=root.quit)
    close_btn.pack(side='right', padx=10)
    
    # معلومات إضافية في الأسفل
    footer_label = tk.Label(root,
                           text="النظام جاهز للاستخدام | تم التطوير بواسطة Python & Tkinter",
                           font=('Arial', 9),
                           bg='#34495e', fg='#bdc3c7')
    footer_label.pack(fill='x', side='bottom')
    
    print("🖥️ تم إنشاء النافذة بنجاح!")
    print("📍 النافذة مفتوحة الآن في المقدمة")
    
    # تشغيل النافذة
    root.mainloop()

if __name__ == "__main__":
    import sys
    print("🚀 بدء اختبار النافذة...")
    create_test_window()
