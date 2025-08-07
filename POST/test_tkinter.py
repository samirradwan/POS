#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار tkinter بسيط
"""

print("اختبار tkinter...")

try:
    import tkinter as tk
    print("✅ تم استيراد tkinter")
    
    # إنشاء نافذة بسيطة
    root = tk.Tk()
    root.title("اختبار")
    root.geometry("300x200")
    
    # إضافة نص
    label = tk.Label(root, text="النظام يعمل!", font=('Arial', 14))
    label.pack(pady=50)
    
    # إضافة زر
    button = tk.Button(root, text="إغلاق", command=root.destroy)
    button.pack()
    
    print("✅ تم إنشاء النافذة")
    print("🖥️ فتح النافذة...")
    
    # جعل النافذة في المقدمة
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    
    # تشغيل النافذة
    root.mainloop()
    
    print("✅ تم إغلاق النافذة بنجاح")
    
except ImportError:
    print("❌ tkinter غير متاح")
    print("حل: pip install tk")
    
except Exception as e:
    print(f"❌ خطأ: {e}")
    import traceback
    traceback.print_exc()
