import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from utils import BackupManager
from datetime import datetime
import threading
import time
import os

class BackupSystemWindow:
    def __init__(self, parent=None):
        self.parent = parent
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("نظام النسخ الاحتياطي")
        self.window.geometry("700x600")
        self.window.configure(bg='#f0f0f0')
        
        # إنشاء مدير النسخ الاحتياطي
        self.backup_manager = BackupManager()
        
        # متغيرات النموذج
        self.setup_variables()
        
        # إنشاء الواجهة
        self.create_widgets()
        
        # تحديث قائمة النسخ الاحتياطية
        self.refresh_backup_list()
        
        # بدء النسخ الاحتياطي التلقائي
        self.auto_backup_running = False
        self.auto_backup_thread = None
    
    def setup_variables(self):
        """إعداد متغيرات النموذج"""
        self.var_auto_backup = tk.BooleanVar(value=False)
        self.var_backup_interval = tk.StringVar(value="24")  # ساعات
        self.var_status = tk.StringVar(value="جاهز")
    
    def create_widgets(self):
        """إنشاء عناصر الواجهة"""
        # الإطار الرئيسي
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # إطار النسخ اليدوي
        manual_frame = ttk.LabelFrame(main_frame, text="النسخ الاحتياطي اليدوي", padding=15)
        manual_frame.pack(fill=tk.X, pady=(0, 10))
        
        # أزرار النسخ اليدوي
        manual_buttons = ttk.Frame(manual_frame)
        manual_buttons.pack(fill=tk.X)
        
        ttk.Button(manual_buttons, text="إنشاء نسخة احتياطية", 
                  command=self.create_manual_backup, style='Accent.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(manual_buttons, text="استعادة نسخة احتياطية", 
                  command=self.restore_backup).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(manual_buttons, text="تصدير نسخة احتياطية", 
                  command=self.export_backup).pack(side=tk.LEFT)
        
        # إطار النسخ التلقائي
        auto_frame = ttk.LabelFrame(main_frame, text="النسخ الاحتياطي التلقائي", padding=15)
        auto_frame.pack(fill=tk.X, pady=(0, 10))
        
        # خيارات النسخ التلقائي
        auto_options = ttk.Frame(auto_frame)
        auto_options.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Checkbutton(auto_options, text="تفعيل النسخ الاحتياطي التلقائي", 
                       variable=self.var_auto_backup, command=self.toggle_auto_backup).pack(side=tk.LEFT)
        
        ttk.Label(auto_options, text="كل").pack(side=tk.LEFT, padx=(20, 5))
        interval_combo = ttk.Combobox(auto_options, textvariable=self.var_backup_interval, 
                                    width=5, state='readonly')
        interval_combo['values'] = ['1', '6', '12', '24', '48', '72']
        interval_combo.pack(side=tk.LEFT, padx=(0, 5))
        ttk.Label(auto_options, text="ساعة").pack(side=tk.LEFT)
        
        # حالة النسخ التلقائي
        status_frame = ttk.Frame(auto_frame)
        status_frame.pack(fill=tk.X)
        
        ttk.Label(status_frame, text="الحالة:").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Label(status_frame, textvariable=self.var_status, foreground='blue').pack(side=tk.LEFT)
        
        # إطار قائمة النسخ الاحتياطية
        list_frame = ttk.LabelFrame(main_frame, text="النسخ الاحتياطية المتاحة", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # إنشاء Treeview
        columns = ('الاسم', 'التاريخ', 'الحجم')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=12)
        
        # تعريف العناوين
        self.tree.heading('الاسم', text='اسم الملف')
        self.tree.heading('التاريخ', text='تاريخ الإنشاء')
        self.tree.heading('الحجم', text='الحجم (KB)')
        
        self.tree.column('الاسم', width=250, anchor=tk.CENTER)
        self.tree.column('التاريخ', width=150, anchor=tk.CENTER)
        self.tree.column('الحجم', width=100, anchor=tk.CENTER)
        
        # شريط التمرير
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # تخطيط العناصر
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # أزرار إدارة النسخ
        list_buttons = ttk.Frame(list_frame)
        list_buttons.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(list_buttons, text="تحديث القائمة", 
                  command=self.refresh_backup_list).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(list_buttons, text="حذف نسخة احتياطية", 
                  command=self.delete_backup).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(list_buttons, text="استعادة محددة", 
                  command=self.restore_selected_backup).pack(side=tk.LEFT)
        
        # شريط الحالة
        self.status_bar = ttk.Label(self.window, text="جاهز", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_manual_backup(self):
        """إنشاء نسخة احتياطية يدوية"""
        try:
            self.status_bar.config(text="جاري إنشاء النسخة الاحتياطية...")
            self.window.update()
            
            backup_path = self.backup_manager.create_backup()
            
            if backup_path:
                messagebox.showinfo("نجح", f"تم إنشاء النسخة الاحتياطية بنجاح:\n{os.path.basename(backup_path)}")
                self.refresh_backup_list()
                self.status_bar.config(text="تم إنشاء النسخة الاحتياطية بنجاح")
            else:
                messagebox.showerror("خطأ", "فشل في إنشاء النسخة الاحتياطية")
                self.status_bar.config(text="فشل في إنشاء النسخة الاحتياطية")
        
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ: {str(e)}")
            self.status_bar.config(text="حدث خطأ أثناء إنشاء النسخة الاحتياطية")
    
    def restore_backup(self):
        """استعادة نسخة احتياطية من ملف خارجي"""
        file_path = filedialog.askopenfilename(
            title="اختر ملف النسخة الاحتياطية",
            filetypes=[("Database files", "*.db"), ("All files", "*.*")]
        )
        
        if file_path:
            result = messagebox.askyesno("تأكيد الاستعادة", 
                                       "هل أنت متأكد من استعادة هذه النسخة الاحتياطية؟\n"
                                       "سيتم استبدال البيانات الحالية!")
            if result:
                try:
                    success = self.backup_manager.restore_backup(file_path)
                    
                    if success:
                        messagebox.showinfo("نجح", "تم استعادة النسخة الاحتياطية بنجاح")
                        self.status_bar.config(text="تم استعادة النسخة الاحتياطية بنجاح")
                    else:
                        messagebox.showerror("خطأ", "فشل في استعادة النسخة الاحتياطية")
                        self.status_bar.config(text="فشل في استعادة النسخة الاحتياطية")
                
                except Exception as e:
                    messagebox.showerror("خطأ", f"حدث خطأ: {str(e)}")
    
    def export_backup(self):
        """تصدير نسخة احتياطية"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "يرجى تحديد نسخة احتياطية للتصدير")
            return
        
        item = self.tree.item(selection[0])
        backup_name = item['values'][0]
        backup_path = os.path.join(self.backup_manager.backup_dir, backup_name)
        
        export_path = filedialog.asksaveasfilename(
            title="حفظ النسخة الاحتياطية",
            defaultextension=".db",
            filetypes=[("Database files", "*.db"), ("All files", "*.*")]
        )
        
        if export_path:
            try:
                import shutil
                shutil.copy2(backup_path, export_path)
                messagebox.showinfo("نجح", f"تم تصدير النسخة الاحتياطية إلى:\n{export_path}")
                self.status_bar.config(text="تم تصدير النسخة الاحتياطية بنجاح")
            
            except Exception as e:
                messagebox.showerror("خطأ", f"حدث خطأ في التصدير: {str(e)}")
    
    def refresh_backup_list(self):
        """تحديث قائمة النسخ الاحتياطية"""
        # مسح القائمة الحالية
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # جلب النسخ الاحتياطية
        backups = self.backup_manager.list_backups()
        
        for backup in backups:
            size_kb = backup['size'] / 1024
            values = (
                backup['name'],
                backup['created'],
                f"{size_kb:.1f}"
            )
            self.tree.insert('', tk.END, values=values)
        
        self.status_bar.config(text=f"تم تحميل {len(backups)} نسخة احتياطية")
    
    def delete_backup(self):
        """حذف نسخة احتياطية"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "يرجى تحديد نسخة احتياطية للحذف")
            return
        
        item = self.tree.item(selection[0])
        backup_name = item['values'][0]
        
        result = messagebox.askyesno("تأكيد الحذف", f"هل أنت متأكد من حذف النسخة الاحتياطية:\n{backup_name}؟")
        if result:
            try:
                backup_path = os.path.join(self.backup_manager.backup_dir, backup_name)
                os.remove(backup_path)
                messagebox.showinfo("نجح", "تم حذف النسخة الاحتياطية بنجاح")
                self.refresh_backup_list()
                self.status_bar.config(text="تم حذف النسخة الاحتياطية بنجاح")
            
            except Exception as e:
                messagebox.showerror("خطأ", f"حدث خطأ في الحذف: {str(e)}")
    
    def restore_selected_backup(self):
        """استعادة النسخة الاحتياطية المحددة"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "يرجى تحديد نسخة احتياطية للاستعادة")
            return
        
        item = self.tree.item(selection[0])
        backup_name = item['values'][0]
        backup_path = os.path.join(self.backup_manager.backup_dir, backup_name)
        
        result = messagebox.askyesno("تأكيد الاستعادة", 
                                   f"هل أنت متأكد من استعادة النسخة الاحتياطية:\n{backup_name}؟\n"
                                   "سيتم استبدال البيانات الحالية!")
        if result:
            try:
                success = self.backup_manager.restore_backup(backup_path)
                
                if success:
                    messagebox.showinfo("نجح", "تم استعادة النسخة الاحتياطية بنجاح")
                    self.status_bar.config(text="تم استعادة النسخة الاحتياطية بنجاح")
                else:
                    messagebox.showerror("خطأ", "فشل في استعادة النسخة الاحتياطية")
            
            except Exception as e:
                messagebox.showerror("خطأ", f"حدث خطأ: {str(e)}")
    
    def toggle_auto_backup(self):
        """تفعيل/إلغاء النسخ الاحتياطي التلقائي"""
        if self.var_auto_backup.get():
            self.start_auto_backup()
        else:
            self.stop_auto_backup()
    
    def start_auto_backup(self):
        """بدء النسخ الاحتياطي التلقائي"""
        if not self.auto_backup_running:
            self.auto_backup_running = True
            self.auto_backup_thread = threading.Thread(target=self.auto_backup_worker, daemon=True)
            self.auto_backup_thread.start()
            self.var_status.set("النسخ التلقائي مفعل")
            self.status_bar.config(text="تم تفعيل النسخ الاحتياطي التلقائي")
    
    def stop_auto_backup(self):
        """إيقاف النسخ الاحتياطي التلقائي"""
        self.auto_backup_running = False
        self.var_status.set("النسخ التلقائي متوقف")
        self.status_bar.config(text="تم إيقاف النسخ الاحتياطي التلقائي")
    
    def auto_backup_worker(self):
        """عامل النسخ الاحتياطي التلقائي"""
        while self.auto_backup_running:
            try:
                interval_hours = int(self.var_backup_interval.get())
                interval_seconds = interval_hours * 3600
                
                # انتظار الفترة المحددة
                for _ in range(interval_seconds):
                    if not self.auto_backup_running:
                        return
                    time.sleep(1)
                
                # إنشاء نسخة احتياطية
                if self.auto_backup_running:
                    backup_path = self.backup_manager.auto_backup()
                    if backup_path:
                        # تحديث الواجهة في الخيط الرئيسي
                        self.window.after(0, self.refresh_backup_list)
                        self.window.after(0, lambda: self.status_bar.config(text="تم إنشاء نسخة احتياطية تلقائية"))
            
            except Exception as e:
                print(f"خطأ في النسخ الاحتياطي التلقائي: {e}")

# تشغيل النافذة إذا تم تشغيل الملف مباشرة
if __name__ == "__main__":
    app = BackupSystemWindow()
    app.window.mainloop()
