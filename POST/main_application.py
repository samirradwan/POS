import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from datetime import datetime

# استيراد الوحدات
from product_management import ProductManagementWindow
from supplier_management import SupplierManagementWindow
from sales_management import SalesManagementWindow
from expense_management import ExpenseManagementWindow
from reports import ReportsWindow
from backup_system import BackupSystemWindow
from invoice_inquiry import InvoiceInquiryWindow
from product_inquiry import ProductInquiryWindow
from database import Database

class MainApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("نظام إدارة متجر الأدوات الكهربائية")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        
        # تعيين أيقونة التطبيق (إذا كانت متوفرة)
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        
        # إنشاء قاعدة البيانات
        self.db = Database()
        
        # متغيرات التطبيق
        self.current_user = "المدير"  # يمكن تطويرها لاحقاً لنظام المستخدمين
        
        # إنشاء الواجهة
        self.create_main_interface()
        
        # تحديث شريط الحالة
        self.update_status()
        
        # بدء النسخ الاحتياطي التلقائي
        self.schedule_auto_backup()
    
    def create_main_interface(self):
        """إنشاء الواجهة الرئيسية"""
        # شريط القوائم
        self.create_menu_bar()
        
        # الشريط العلوي
        self.create_header()
        
        # الجزء الرئيسي
        self.create_main_content()
        
        # شريط الحالة
        self.create_status_bar()
    
    def create_menu_bar(self):
        """إنشاء شريط القوائم"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # قائمة الملف
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="ملف", menu=file_menu)
        file_menu.add_command(label="نسخة احتياطية", command=self.open_backup_system)
        file_menu.add_separator()
        file_menu.add_command(label="خروج", command=self.exit_application)
        
        # قائمة الإدارة
        manage_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="إدارة", menu=manage_menu)
        manage_menu.add_command(label="إدارة المنتجات", command=self.open_product_management)
        manage_menu.add_command(label="إدارة الموردين", command=self.open_supplier_management)
        manage_menu.add_command(label="إدارة المصروفات", command=self.open_expense_management)
        
        # قائمة المبيعات
        sales_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="مبيعات", menu=sales_menu)
        sales_menu.add_command(label="نقطة البيع", command=self.open_sales_management)
        sales_menu.add_command(label="التقارير", command=self.open_reports)

        # قائمة الاستعلامات
        inquiry_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="استعلامات", menu=inquiry_menu)
        inquiry_menu.add_command(label="استعلام الفواتير", command=self.open_invoice_inquiry)
        inquiry_menu.add_command(label="استعلام المنتجات", command=self.open_product_inquiry)
        
        # قائمة المساعدة
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="مساعدة", menu=help_menu)
        help_menu.add_command(label="حول البرنامج", command=self.show_about)
    
    def create_header(self):
        """إنشاء الشريط العلوي"""
        header_frame = tk.Frame(self.root, bg='#34495e', height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # عنوان التطبيق
        title_label = tk.Label(header_frame, text="نظام إدارة متجر الأدوات الكهربائية", 
                              font=('Arial', 20, 'bold'), fg='white', bg='#34495e')
        title_label.pack(side=tk.LEFT, padx=20, pady=20)
        
        # معلومات المستخدم والوقت
        info_frame = tk.Frame(header_frame, bg='#34495e')
        info_frame.pack(side=tk.RIGHT, padx=20, pady=20)
        
        user_label = tk.Label(info_frame, text=f"المستخدم: {self.current_user}", 
                             font=('Arial', 12), fg='white', bg='#34495e')
        user_label.pack(anchor=tk.E)
        
        self.time_label = tk.Label(info_frame, text="", font=('Arial', 10), 
                                  fg='#bdc3c7', bg='#34495e')
        self.time_label.pack(anchor=tk.E)
        
        # تحديث الوقت
        self.update_time()
    
    def create_main_content(self):
        """إنشاء المحتوى الرئيسي"""
        main_frame = tk.Frame(self.root, bg='#ecf0f1')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # عنوان الترحيب
        welcome_label = tk.Label(main_frame, text="مرحباً بك في نظام إدارة المتجر", 
                                font=('Arial', 16, 'bold'), bg='#ecf0f1', fg='#2c3e50')
        welcome_label.pack(pady=(0, 30))
        
        # إنشاء البطاقات الرئيسية
        cards_frame = tk.Frame(main_frame, bg='#ecf0f1')
        cards_frame.pack(fill=tk.BOTH, expand=True)
        
        # الصف الأول من البطاقات
        row1 = tk.Frame(cards_frame, bg='#ecf0f1')
        row1.pack(fill=tk.X, pady=(0, 20))
        
        self.create_card(row1, "إدارة المنتجات", "إضافة وتعديل المنتجات والمخزون", 
                        "#3498db", self.open_product_management)
        self.create_card(row1, "نقطة البيع", "إجراء عمليات البيع والفواتير", 
                        "#e74c3c", self.open_sales_management)
        self.create_card(row1, "التقارير", "عرض تقارير المبيعات والأرباح", 
                        "#f39c12", self.open_reports)
        
        # الصف الثاني من البطاقات
        row2 = tk.Frame(cards_frame, bg='#ecf0f1')
        row2.pack(fill=tk.X, pady=(0, 20))
        
        self.create_card(row2, "إدارة الموردين", "إدارة معلومات الموردين", 
                        "#9b59b6", self.open_supplier_management)
        self.create_card(row2, "المصروفات", "تسجيل ومتابعة المصروفات",
                        "#e67e22", self.open_expense_management)
        self.create_card(row2, "النسخ الاحتياطي", "إدارة النسخ الاحتياطية",
                        "#27ae60", self.open_backup_system)

        # الصف الثالث من البطاقات
        row3 = tk.Frame(cards_frame, bg='#ecf0f1')
        row3.pack(fill=tk.X)

        self.create_card(row3, "استعلام الفواتير", "البحث عن الفواتير وطباعتها",
                        "#8e44ad", self.open_invoice_inquiry)
        self.create_card(row3, "استعلام المنتجات", "البحث وحفظ طلبات المنتجات",
                        "#16a085", self.open_product_inquiry)
    
    def create_card(self, parent, title, description, color, command):
        """إنشاء بطاقة وظيفة"""
        card_frame = tk.Frame(parent, bg=color, relief=tk.RAISED, bd=2)
        card_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        # جعل البطاقة قابلة للنقر
        card_frame.bind("<Button-1>", lambda e: command())
        card_frame.bind("<Enter>", lambda e: card_frame.config(relief=tk.RAISED, bd=4))
        card_frame.bind("<Leave>", lambda e: card_frame.config(relief=tk.RAISED, bd=2))
        
        # محتوى البطاقة
        content_frame = tk.Frame(card_frame, bg=color)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        content_frame.bind("<Button-1>", lambda e: command())
        
        title_label = tk.Label(content_frame, text=title, font=('Arial', 14, 'bold'), 
                              fg='white', bg=color)
        title_label.pack(pady=(0, 10))
        title_label.bind("<Button-1>", lambda e: command())
        
        desc_label = tk.Label(content_frame, text=description, font=('Arial', 10), 
                             fg='white', bg=color, wraplength=150)
        desc_label.pack()
        desc_label.bind("<Button-1>", lambda e: command())
        
        # زر الوصول
        btn = tk.Button(content_frame, text="فتح", font=('Arial', 10, 'bold'), 
                       bg='white', fg=color, command=command, relief=tk.FLAT, 
                       padx=20, pady=5)
        btn.pack(pady=(15, 0))
    
    def create_status_bar(self):
        """إنشاء شريط الحالة"""
        status_frame = tk.Frame(self.root, bg='#34495e', height=30)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(status_frame, text="جاهز", font=('Arial', 10), 
                                    fg='white', bg='#34495e', anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # معلومات قاعدة البيانات
        self.db_status_label = tk.Label(status_frame, text="", font=('Arial', 10), 
                                       fg='#bdc3c7', bg='#34495e', anchor=tk.E)
        self.db_status_label.pack(side=tk.RIGHT, padx=10, pady=5)
    
    def update_time(self):
        """تحديث الوقت"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
    
    def update_status(self):
        """تحديث شريط الحالة"""
        try:
            # فحص حالة قاعدة البيانات
            conn = self.db.connect()
            if conn:
                self.db_status_label.config(text="قاعدة البيانات متصلة", fg='#27ae60')
                self.db.disconnect()
            else:
                self.db_status_label.config(text="خطأ في قاعدة البيانات", fg='#e74c3c')
        except Exception as e:
            self.db_status_label.config(text="خطأ في قاعدة البيانات", fg='#e74c3c')
    
    def schedule_auto_backup(self):
        """جدولة النسخ الاحتياطي التلقائي"""
        # نسخة احتياطية كل 24 ساعة
        self.root.after(24 * 60 * 60 * 1000, self.auto_backup)
    
    def auto_backup(self):
        """النسخ الاحتياطي التلقائي"""
        try:
            backup_path = self.db.backup_database()
            if backup_path:
                self.status_label.config(text="تم إنشاء نسخة احتياطية تلقائية")
        except Exception as e:
            print(f"خطأ في النسخ الاحتياطي التلقائي: {e}")
        
        # جدولة النسخة التالية
        self.schedule_auto_backup()
    
    # وظائف فتح النوافذ
    def open_product_management(self):
        """فتح نافذة إدارة المنتجات"""
        try:
            ProductManagementWindow(self.root)
            self.status_label.config(text="تم فتح نافذة إدارة المنتجات")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في فتح نافذة إدارة المنتجات: {str(e)}")
    
    def open_supplier_management(self):
        """فتح نافذة إدارة الموردين"""
        try:
            SupplierManagementWindow(self.root)
            self.status_label.config(text="تم فتح نافذة إدارة الموردين")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في فتح نافذة إدارة الموردين: {str(e)}")
    
    def open_sales_management(self):
        """فتح نافذة المبيعات"""
        try:
            SalesManagementWindow(self.root)
            self.status_label.config(text="تم فتح نقطة البيع")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في فتح نقطة البيع: {str(e)}")
    
    def open_expense_management(self):
        """فتح نافذة إدارة المصروفات"""
        try:
            ExpenseManagementWindow(self.root)
            self.status_label.config(text="تم فتح نافذة إدارة المصروفات")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في فتح نافذة إدارة المصروفات: {str(e)}")
    
    def open_reports(self):
        """فتح نافذة التقارير"""
        try:
            ReportsWindow(self.root)
            self.status_label.config(text="تم فتح نافذة التقارير")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في فتح نافذة التقارير: {str(e)}")
    
    def open_backup_system(self):
        """فتح نظام النسخ الاحتياطي"""
        try:
            BackupSystemWindow(self.root)
            self.status_label.config(text="تم فتح نظام النسخ الاحتياطي")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في فتح نظام النسخ الاحتياطي: {str(e)}")

    def open_invoice_inquiry(self):
        """فتح نافذة استعلام الفواتير"""
        try:
            InvoiceInquiryWindow(self.root)
            self.status_label.config(text="تم فتح نافذة استعلام الفواتير")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في فتح نافذة استعلام الفواتير: {str(e)}")

    def open_product_inquiry(self):
        """فتح نافذة استعلام المنتجات"""
        try:
            ProductInquiryWindow(self.root)
            self.status_label.config(text="تم فتح نافذة استعلام المنتجات")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في فتح نافذة استعلام المنتجات: {str(e)}")
    
    def show_about(self):
        """عرض معلومات البرنامج"""
        about_text = """
نظام إدارة متجر الأدوات الكهربائية
الإصدار 1.0

تم تطوير هذا النظام لإدارة متاجر الأدوات الكهربائية
بشكل شامل ومتكامل.

الميزات:
• إدارة المنتجات والمخزون
• نقطة البيع مع حساب الخصومات
• إدارة الموردين والعملاء
• تتبع المصروفات
• تقارير شاملة
• نظام النسخ الاحتياطي
• استعلام الفواتير وطباعتها
• استعلام المنتجات وحفظ الطلبات

تطوير: فريق التطوير
        """
        messagebox.showinfo("حول البرنامج", about_text)
    
    def exit_application(self):
        """إغلاق التطبيق"""
        result = messagebox.askyesno("تأكيد الخروج", "هل أنت متأكد من إغلاق البرنامج؟")
        if result:
            self.root.quit()
    
    def run(self):
        """تشغيل التطبيق"""
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApplication()
    app.run()
