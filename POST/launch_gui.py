#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تشغيل الواجهة الرسومية مباشرة
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

def create_simple_gui():
    """إنشاء واجهة بسيطة للاختبار"""
    root = tk.Tk()
    root.title("اختبار النظام")
    root.geometry("400x300")
    root.configure(bg='#f0f0f0')
    
    # عنوان
    title = tk.Label(root, text="نظام إدارة المتجر", 
                    font=('Arial', 16, 'bold'), bg='#f0f0f0')
    title.pack(pady=20)
    
    # رسالة
    message = tk.Label(root, text="النظام يعمل بنجاح!", 
                      font=('Arial', 12), bg='#f0f0f0', fg='green')
    message.pack(pady=10)
    
    # معلومات النظام
    info_frame = tk.Frame(root, bg='#f0f0f0')
    info_frame.pack(pady=20)
    
    tk.Label(info_frame, text=f"Python: {sys.version[:5]}", 
            bg='#f0f0f0').pack()
    tk.Label(info_frame, text=f"المجلد: {os.getcwd()}", 
            bg='#f0f0f0').pack()
    
    # أزرار
    button_frame = tk.Frame(root, bg='#f0f0f0')
    button_frame.pack(pady=20)
    
    def launch_main_system():
        try:
            root.destroy()
            from main_application import MainApplication
            app = MainApplication()
            app.run()
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في تشغيل النظام الرئيسي:\n{str(e)}")
    
    def test_features():
        messagebox.showinfo("اختبار", "الواجهة الرسومية تعمل بنجاح!")
    
    tk.Button(button_frame, text="تشغيل النظام الكامل", 
             command=launch_main_system, bg='#4CAF50', fg='white',
             font=('Arial', 10, 'bold')).pack(pady=5)
    
    tk.Button(button_frame, text="اختبار الواجهة", 
             command=test_features, bg='#2196F3', fg='white',
             font=('Arial', 10, 'bold')).pack(pady=5)
    
    tk.Button(button_frame, text="إغلاق", 
             command=root.destroy, bg='#f44336', fg='white',
             font=('Arial', 10, 'bold')).pack(pady=5)
    
    # جعل النافذة في المقدمة
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    
    return root

def main():
    """الدالة الرئيسية"""
    print("🚀 تشغيل واجهة الاختبار...")
    
    try:
        # إنشاء الواجهة
        root = create_simple_gui()
        
        # تشغيل الواجهة
        root.mainloop()
        
    except Exception as e:
        print(f"❌ خطأ: {e}")
        import traceback
        traceback.print_exc()
        
        # محاولة عرض رسالة خطأ
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("خطأ في التشغيل", 
                               f"حدث خطأ أثناء تشغيل الواجهة:\n{str(e)}")
        except:
            pass

if __name__ == "__main__":
    main()
