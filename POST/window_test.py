#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار النوافذ - تشخيص مشكلة عدم الظهور
"""

import tkinter as tk
import sys
import os
import time

def test_basic_window():
    """اختبار نافذة أساسية"""
    print("🔧 اختبار النافذة الأساسية...")
    
    try:
        root = tk.Tk()
        root.title("اختبار أساسي")
        root.geometry("400x300+100+100")
        
        # إجبار الظهور
        root.lift()
        root.focus_force()
        root.attributes('-topmost', True)
        
        # نص
        label = tk.Label(root, text="هل ترى هذه النافذة؟", font=("Arial", 16))
        label.pack(pady=50)
        
        # زر
        def close_window():
            print("✅ تم الضغط على الزر - النافذة تعمل!")
            root.quit()
        
        button = tk.Button(root, text="نعم أراها!", command=close_window, font=("Arial", 12))
        button.pack(pady=20)
        
        print("🖥️ النافذة جاهزة - ابحث عنها على الشاشة")
        print("📍 العنوان: 'اختبار أساسي'")
        
        # إزالة topmost بعد 3 ثواني
        root.after(3000, lambda: root.attributes('-topmost', False))
        
        root.mainloop()
        return True
        
    except Exception as e:
        print(f"❌ خطأ: {e}")
        return False

def test_message_box():
    """اختبار صندوق الرسائل"""
    print("🔧 اختبار صندوق الرسائل...")
    
    try:
        import tkinter.messagebox as msgbox
        
        # إنشاء نافذة مخفية
        root = tk.Tk()
        root.withdraw()  # إخفاء النافذة الرئيسية
        
        # إظهار رسالة
        result = msgbox.askyesno(
            "اختبار النوافذ", 
            "هل ترى هذه الرسالة؟\n\nإذا كنت ترى هذا، فالنوافذ تعمل!"
        )
        
        root.destroy()
        
        if result:
            print("✅ المستخدم رأى الرسالة - النوافذ تعمل!")
            return True
        else:
            print("⚠️ المستخدم لم يؤكد رؤية الرسالة")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في صندوق الرسائل: {e}")
        return False

def check_system():
    """فحص النظام"""
    print("\n🔍 معلومات النظام:")
    print(f"📍 OS: {os.name}")
    print(f"📍 Platform: {sys.platform}")
    print(f"📍 Python: {sys.version}")
    
    # فحص tkinter
    try:
        import tkinter
        print("✅ tkinter متاح")
        
        # فحص إصدار tkinter
        root = tkinter.Tk()
        tk_version = root.tk.eval('info patchlevel')
        print(f"📍 Tk version: {tk_version}")
        root.destroy()
        
    except Exception as e:
        print(f"❌ مشكلة في tkinter: {e}")
        return False
    
    return True

def main():
    """الدالة الرئيسية"""
    print("🚀 بدء تشخيص النوافذ...")
    print("=" * 50)
    
    # فحص النظام
    if not check_system():
        print("❌ فشل فحص النظام")
        return
    
    print("\n" + "=" * 50)
    
    # اختبار صندوق الرسائل أولاً
    print("🔸 الاختبار 1: صندوق الرسائل")
    if test_message_box():
        print("✅ صندوق الرسائل يعمل")
    else:
        print("❌ صندوق الرسائل لا يعمل")
    
    print("\n" + "=" * 50)
    
    # اختبار النافذة الأساسية
    print("🔸 الاختبار 2: النافذة الأساسية")
    if test_basic_window():
        print("✅ النافذة الأساسية تعمل")
    else:
        print("❌ النافذة الأساسية لا تعمل")
    
    print("\n" + "=" * 50)
    print("🏁 انتهى التشخيص")
    
    # انتظار
    print("\n⏸️ اضغط Enter للخروج...")
    input()

if __name__ == "__main__":
    main()
