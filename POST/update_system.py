#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تحديث نظام إدارة المتجر

هذا الملف يتحقق من التحديثات المتاحة
ويقوم بتحديث النظام إذا لزم الأمر
"""

import os
import sys
import shutil
import json
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

class SystemUpdater:
    def __init__(self):
        self.current_version = "1.0.0"
        self.update_info_file = "update_info.json"
        self.backup_dir = "update_backups"
        
    def check_for_updates(self):
        """التحقق من وجود تحديثات"""
        # في التطبيق الحقيقي، هذا سيتصل بخادم التحديثات
        # هنا سنحاكي وجود تحديث
        
        update_info = {
            "available": False,
            "latest_version": "1.0.0",
            "download_url": "",
            "changelog": [],
            "critical": False
        }
        
        # محاكاة فحص التحديثات
        if os.path.exists("new_version.txt"):
            with open("new_version.txt", "r") as f:
                new_version = f.read().strip()
                if new_version != self.current_version:
                    update_info["available"] = True
                    update_info["latest_version"] = new_version
                    update_info["changelog"] = [
                        "إصلاح أخطاء في حساب الخصومات",
                        "تحسين أداء التقارير",
                        "إضافة ميزات جديدة للنسخ الاحتياطي"
                    ]
        
        return update_info
    
    def create_backup(self):
        """إنشاء نسخة احتياطية قبل التحديث"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(self.backup_dir, f"backup_{timestamp}")
        
        try:
            # نسخ الملفات المهمة
            important_files = [
                "store_management.db",
                "config.json",
                "logs"
            ]
            
            os.makedirs(backup_path)
            
            for item in important_files:
                if os.path.exists(item):
                    if os.path.isfile(item):
                        shutil.copy2(item, backup_path)
                    else:
                        shutil.copytree(item, os.path.join(backup_path, item))
            
            return backup_path
            
        except Exception as e:
            print(f"خطأ في إنشاء النسخة الاحتياطية: {e}")
            return None
    
    def apply_update(self, update_files):
        """تطبيق التحديث"""
        try:
            # نسخ الملفات الجديدة
            for file_path, new_content in update_files.items():
                # إنشاء نسخة احتياطية من الملف الحالي
                if os.path.exists(file_path):
                    backup_file = f"{file_path}.backup"
                    shutil.copy2(file_path, backup_file)
                
                # كتابة المحتوى الجديد
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
            
            return True
            
        except Exception as e:
            print(f"خطأ في تطبيق التحديث: {e}")
            return False
    
    def rollback_update(self):
        """التراجع عن التحديث"""
        try:
            # استعادة الملفات من النسخة الاحتياطية
            backup_files = [f for f in os.listdir(".") if f.endswith(".backup")]
            
            for backup_file in backup_files:
                original_file = backup_file.replace(".backup", "")
                shutil.move(backup_file, original_file)
            
            return True
            
        except Exception as e:
            print(f"خطأ في التراجع عن التحديث: {e}")
            return False

class UpdaterGUI:
    def __init__(self):
        self.updater = SystemUpdater()
        self.root = tk.Tk()
        self.root.title("تحديث النظام")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        self.create_widgets()
        
    def create_widgets(self):
        """إنشاء واجهة التحديث"""
        # العنوان
        title_label = tk.Label(self.root, text="تحديث نظام إدارة المتجر", 
                              font=('Arial', 16, 'bold'))
        title_label.pack(pady=20)
        
        # معلومات الإصدار الحالي
        current_frame = tk.Frame(self.root)
        current_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(current_frame, text="الإصدار الحالي:", font=('Arial', 12, 'bold')).pack(side=tk.LEFT)
        tk.Label(current_frame, text=self.updater.current_version, font=('Arial', 12)).pack(side=tk.LEFT, padx=(10, 0))
        
        # منطقة المعلومات
        info_frame = tk.LabelFrame(self.root, text="معلومات التحديث", padding=10)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.info_text = tk.Text(info_frame, wrap=tk.WORD, height=10)
        scrollbar = tk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=scrollbar.set)
        
        self.info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # شريط التقدم
        self.progress = ttk.Progressbar(self.root, mode='indeterminate')
        self.progress.pack(fill=tk.X, padx=20, pady=10)
        
        # الأزرار
        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(fill=tk.X, padx=20, pady=20)
        
        self.check_button = tk.Button(buttons_frame, text="فحص التحديثات", 
                                     command=self.check_updates, bg='#3498db', fg='white')
        self.check_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.update_button = tk.Button(buttons_frame, text="تحديث", 
                                      command=self.start_update, bg='#27ae60', fg='white', state=tk.DISABLED)
        self.update_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.close_button = tk.Button(buttons_frame, text="إغلاق", 
                                     command=self.root.destroy, bg='#e74c3c', fg='white')
        self.close_button.pack(side=tk.RIGHT)
        
        # عرض معلومات أولية
        self.info_text.insert(tk.END, "مرحباً بك في أداة تحديث النظام\n\n")
        self.info_text.insert(tk.END, f"الإصدار الحالي: {self.updater.current_version}\n")
        self.info_text.insert(tk.END, "انقر 'فحص التحديثات' للبحث عن إصدارات جديدة\n")
    
    def check_updates(self):
        """فحص التحديثات"""
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, "جاري فحص التحديثات...\n")
        self.progress.start()
        self.check_button.config(state=tk.DISABLED)
        
        # محاكاة فحص التحديثات
        self.root.after(2000, self.update_check_complete)
    
    def update_check_complete(self):
        """اكتمال فحص التحديثات"""
        self.progress.stop()
        self.check_button.config(state=tk.NORMAL)
        
        update_info = self.updater.check_for_updates()
        
        if update_info["available"]:
            self.info_text.insert(tk.END, f"\n✅ تحديث متاح!\n")
            self.info_text.insert(tk.END, f"الإصدار الجديد: {update_info['latest_version']}\n\n")
            self.info_text.insert(tk.END, "التحسينات الجديدة:\n")
            
            for change in update_info["changelog"]:
                self.info_text.insert(tk.END, f"• {change}\n")
            
            self.info_text.insert(tk.END, "\nانقر 'تحديث' لتثبيت الإصدار الجديد\n")
            self.update_button.config(state=tk.NORMAL)
            
            if update_info["critical"]:
                self.info_text.insert(tk.END, "\n⚠️ هذا تحديث مهم ويُنصح بتثبيته فوراً\n")
        else:
            self.info_text.insert(tk.END, "\n✅ النظام محدث إلى أحدث إصدار\n")
            self.info_text.insert(tk.END, "لا توجد تحديثات متاحة حالياً\n")
    
    def start_update(self):
        """بدء عملية التحديث"""
        result = messagebox.askyesno("تأكيد التحديث", 
                                   "هل أنت متأكد من تحديث النظام؟\n"
                                   "سيتم إنشاء نسخة احتياطية تلقائياً")
        
        if result:
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, "بدء عملية التحديث...\n")
            self.progress.start()
            self.update_button.config(state=tk.DISABLED)
            
            # محاكاة عملية التحديث
            self.root.after(1000, self.create_backup_step)
    
    def create_backup_step(self):
        """خطوة إنشاء النسخة الاحتياطية"""
        self.info_text.insert(tk.END, "إنشاء نسخة احتياطية...\n")
        
        backup_path = self.updater.create_backup()
        if backup_path:
            self.info_text.insert(tk.END, f"✅ تم إنشاء نسخة احتياطية: {backup_path}\n")
            self.root.after(1000, self.download_step)
        else:
            self.info_text.insert(tk.END, "❌ فشل في إنشاء النسخة الاحتياطية\n")
            self.update_failed()
    
    def download_step(self):
        """خطوة تحميل التحديث"""
        self.info_text.insert(tk.END, "تحميل ملفات التحديث...\n")
        
        # محاكاة التحميل
        self.root.after(2000, self.install_step)
    
    def install_step(self):
        """خطوة تثبيت التحديث"""
        self.info_text.insert(tk.END, "تثبيت التحديث...\n")
        
        # محاكاة التثبيت
        update_files = {
            "version.txt": "1.0.1",
            "changelog.txt": "إصدار محدث مع إصلاحات وتحسينات"
        }
        
        success = self.updater.apply_update(update_files)
        
        if success:
            self.root.after(1000, self.update_complete)
        else:
            self.update_failed()
    
    def update_complete(self):
        """اكتمال التحديث"""
        self.progress.stop()
        self.info_text.insert(tk.END, "\n🎉 تم التحديث بنجاح!\n")
        self.info_text.insert(tk.END, "يُنصح بإعادة تشغيل النظام لتطبيق التحديثات\n")
        
        messagebox.showinfo("تم التحديث", "تم تحديث النظام بنجاح!\nيُنصح بإعادة تشغيل البرنامج")
    
    def update_failed(self):
        """فشل التحديث"""
        self.progress.stop()
        self.info_text.insert(tk.END, "\n❌ فشل في التحديث\n")
        self.update_button.config(state=tk.NORMAL)
        
        messagebox.showerror("خطأ", "فشل في تحديث النظام")
    
    def run(self):
        """تشغيل واجهة التحديث"""
        self.root.mainloop()

def main():
    """الدالة الرئيسية"""
    print("أداة تحديث نظام إدارة المتجر")
    
    # فحص سريع للتحديثات
    updater = SystemUpdater()
    update_info = updater.check_for_updates()
    
    if update_info["available"]:
        print(f"تحديث متاح: {update_info['latest_version']}")
        
        # فتح واجهة التحديث
        gui = UpdaterGUI()
        gui.run()
    else:
        print("النظام محدث إلى أحدث إصدار")

if __name__ == "__main__":
    main()
