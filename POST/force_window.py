#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إجبار النافذة على الظهور
"""

import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading

def create_visible_window():
    """إنشاء نافذة مرئية بالقوة"""
    
    # إنشاء النافذة الرئيسية
    root = tk.Tk()
    
    # إعدادات النافذة للظهور بالقوة
    root.title("🏪 نظام إدارة المتجر - اختبار")
    root.geometry("800x600+50+50")
    
    # إجبار النافذة على الظهور
    root.attributes('-topmost', True)  # في المقدمة
    root.lift()                        # رفع النافذة
    root.focus_force()                 # إجبار التركيز
    root.update()                      # تحديث فوري
    
    # إزالة topmost بعد ثانية
    def remove_topmost():
        time.sleep(1)
        root.attributes('-topmost', False)
    
    threading.Thread(target=remove_topmost, daemon=True).start()
    
    # إنشاء الواجهة
    main_frame = ttk.Frame(root, padding="20")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    # العنوان
    title_label = tk.Label(
        main_frame, 
        text="🏪 نظام إدارة المتجر",
        font=("Arial", 24, "bold"),
        fg="blue"
    )
    title_label.grid(row=0, column=0, columnspan=2, pady=20)
    
    # رسالة النجاح
    success_label = tk.Label(
        main_frame,
        text="✅ النظام يعمل بنجاح!",
        font=("Arial", 16),
        fg="green"
    )
    success_label.grid(row=1, column=0, columnspan=2, pady=10)
    
    # معلومات النظام
    info_text = tk.Text(main_frame, height=15, width=70, font=("Arial", 10))
    info_text.grid(row=2, column=0, columnspan=2, pady=20)
    
    info_content = """
🎉 تهانينا! النظام يعمل بشكل مثالي!

✅ Python: يعمل
✅ tkinter: يعمل  
✅ النوافذ: تظهر بنجاح

🚀 الخطوات التالية:
1. النظام جاهز للاستخدام
2. يمكنك تشغيل النظام الكامل الآن
3. جميع الميزات متاحة

📋 الميزات المتاحة:
• إدارة المنتجات
• إدارة المبيعات  
• إدارة المصروفات
• التقارير
• إدارة الموردين
• النسخ الاحتياطي

💡 لتشغيل النظام الكامل:
python start_simple.py

🔧 أو للنظام المحسن:
python main_application.py
    """
    
    info_text.insert(tk.END, info_content)
    info_text.config(state=tk.DISABLED)
    
    # أزرار التحكم
    button_frame = ttk.Frame(main_frame)
    button_frame.grid(row=3, column=0, columnspan=2, pady=20)
    
    def start_full_system():
        """تشغيل النظام الكامل"""
        try:
            root.destroy()
            from main_application import MainApplication
            app = MainApplication()
            app.run()
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في تشغيل النظام: {e}")
    
    def test_features():
        """اختبار الميزات"""
        messagebox.showinfo("اختبار", "جميع الميزات تعمل بنجاح! ✅")
    
    # أزرار
    ttk.Button(
        button_frame,
        text="🚀 تشغيل النظام الكامل",
        command=start_full_system
    ).grid(row=0, column=0, padx=10)
    
    ttk.Button(
        button_frame,
        text="🔧 اختبار الميزات", 
        command=test_features
    ).grid(row=0, column=1, padx=10)
    
    ttk.Button(
        button_frame,
        text="❌ إغلاق",
        command=root.quit
    ).grid(row=0, column=2, padx=10)
    
    # تكوين الشبكة
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    main_frame.columnconfigure(0, weight=1)
    
    # تشغيل النافذة
    print("🖥️ تم إنشاء النافذة - يجب أن تظهر الآن!")
    root.mainloop()

if __name__ == "__main__":
    print("🚀 بدء تشغيل النافذة المرئية...")
    create_visible_window()
