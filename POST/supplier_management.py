import tkinter as tk
from tkinter import ttk, messagebox
from models import Supplier
from utils import ValidationUtils

class SupplierManagementWindow:
    def __init__(self, parent=None):
        self.parent = parent
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("إدارة الموردين")
        self.window.geometry("800x600")
        self.window.configure(bg='#f0f0f0')
        
        # إنشاء النموذج
        self.supplier_model = Supplier()
        
        # متغيرات النموذج
        self.setup_variables()
        
        # إنشاء الواجهة
        self.create_widgets()
        
        # تحديث القائمة
        self.refresh_suppliers_list()
        
        # تحديد المورد المحدد
        self.selected_supplier_id = None
    
    def setup_variables(self):
        """إعداد متغيرات النموذج"""
        self.var_name = tk.StringVar()
        self.var_contact_info = tk.StringVar()
    
    def create_widgets(self):
        """إنشاء عناصر الواجهة"""
        # الإطار الرئيسي
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # إطار النموذج
        form_frame = ttk.LabelFrame(main_frame, text="بيانات المورد", padding=20)
        form_frame.pack(fill=tk.X, pady=(0, 10))
        
        # الصف الأول - اسم المورد
        row1 = ttk.Frame(form_frame)
        row1.pack(fill=tk.X, pady=10)
        
        ttk.Label(row1, text="اسم المورد:", font=('Arial', 12)).pack(side=tk.LEFT, padx=(0, 10))
        name_entry = ttk.Entry(row1, textvariable=self.var_name, font=('Arial', 12), width=30)
        name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # الصف الثاني - معلومات الاتصال
        row2 = ttk.Frame(form_frame)
        row2.pack(fill=tk.X, pady=10)
        
        ttk.Label(row2, text="معلومات الاتصال:", font=('Arial', 12)).pack(side=tk.LEFT, padx=(0, 10))
        contact_entry = ttk.Entry(row2, textvariable=self.var_contact_info, font=('Arial', 12), width=40)
        contact_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # إطار الأزرار
        buttons_frame = ttk.Frame(form_frame)
        buttons_frame.pack(fill=tk.X, pady=15)
        
        # أزرار العمليات
        ttk.Button(buttons_frame, text="إضافة مورد", command=self.add_supplier, 
                  style='Accent.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="تحديث مورد", command=self.update_supplier).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="حذف مورد", command=self.delete_supplier).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="مسح النموذج", command=self.clear_form).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="تحديث القائمة", command=self.refresh_suppliers_list).pack(side=tk.LEFT)
        
        # إطار قائمة الموردين
        list_frame = ttk.LabelFrame(main_frame, text="قائمة الموردين", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # إنشاء Treeview
        columns = ('ID', 'اسم المورد', 'معلومات الاتصال')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # تعريف العناوين وعرض الأعمدة
        self.tree.heading('ID', text='المعرف')
        self.tree.heading('اسم المورد', text='اسم المورد')
        self.tree.heading('معلومات الاتصال', text='معلومات الاتصال')
        
        self.tree.column('ID', width=80, anchor=tk.CENTER)
        self.tree.column('اسم المورد', width=200, anchor=tk.CENTER)
        self.tree.column('معلومات الاتصال', width=300, anchor=tk.CENTER)
        
        # شريط التمرير
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # تخطيط العناصر
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # ربط الأحداث
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        # إضافة شريط الحالة
        self.status_bar = ttk.Label(self.window, text="جاهز", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def refresh_suppliers_list(self):
        """تحديث قائمة الموردين"""
        # مسح القائمة الحالية
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # جلب الموردين
        suppliers = self.supplier_model.get_all_suppliers()
        
        for supplier in suppliers:
            values = (
                supplier['supplier_id'],
                supplier['supplier_name'],
                supplier['contact_info'] or "غير محدد"
            )
            self.tree.insert('', tk.END, values=values)
        
        # تحديث شريط الحالة
        self.status_bar.config(text=f"تم تحميل {len(suppliers)} مورد")
    
    def on_select(self, event):
        """عند تحديد مورد من القائمة"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            
            self.selected_supplier_id = values[0]
            
            # تحديث النموذج
            self.var_name.set(values[1])
            self.var_contact_info.set(values[2] if values[2] != "غير محدد" else "")
    
    def validate_form(self):
        """التحقق من صحة النموذج"""
        if not ValidationUtils.validate_required_field(self.var_name.get()):
            messagebox.showerror("خطأ", "اسم المورد مطلوب")
            return False
        
        return True
    
    def add_supplier(self):
        """إضافة مورد جديد"""
        if not self.validate_form():
            return
        
        try:
            supplier_id = self.supplier_model.add_supplier(
                name=self.var_name.get().strip(),
                contact_info=self.var_contact_info.get().strip()
            )
            
            if supplier_id:
                messagebox.showinfo("نجح", "تم إضافة المورد بنجاح")
                self.clear_form()
                self.refresh_suppliers_list()
                self.status_bar.config(text="تم إضافة مورد جديد بنجاح")
            else:
                messagebox.showerror("خطأ", "فشل في إضافة المورد")
                self.status_bar.config(text="فشل في إضافة المورد")
        
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ: {str(e)}")
            self.status_bar.config(text="حدث خطأ أثناء إضافة المورد")
    
    def update_supplier(self):
        """تحديث مورد موجود"""
        if not self.selected_supplier_id:
            messagebox.showwarning("تحذير", "يرجى تحديد مورد للتحديث")
            return
        
        if not self.validate_form():
            return
        
        try:
            success = self.supplier_model.update_supplier(
                supplier_id=self.selected_supplier_id,
                name=self.var_name.get().strip(),
                contact_info=self.var_contact_info.get().strip()
            )
            
            if success:
                messagebox.showinfo("نجح", "تم تحديث المورد بنجاح")
                self.clear_form()
                self.refresh_suppliers_list()
                self.status_bar.config(text="تم تحديث المورد بنجاح")
            else:
                messagebox.showerror("خطأ", "فشل في تحديث المورد")
                self.status_bar.config(text="فشل في تحديث المورد")
        
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ: {str(e)}")
            self.status_bar.config(text="حدث خطأ أثناء تحديث المورد")
    
    def delete_supplier(self):
        """حذف مورد"""
        if not self.selected_supplier_id:
            messagebox.showwarning("تحذير", "يرجى تحديد مورد للحذف")
            return
        
        # التحقق من وجود منتجات مرتبطة بهذا المورد
        result = messagebox.askyesno("تأكيد الحذف", 
                                   "هل أنت متأكد من حذف هذا المورد؟\n"
                                   "تحذير: قد يؤثر هذا على المنتجات المرتبطة بهذا المورد")
        if result:
            try:
                success = self.supplier_model.delete_supplier(self.selected_supplier_id)
                
                if success:
                    messagebox.showinfo("نجح", "تم حذف المورد بنجاح")
                    self.clear_form()
                    self.refresh_suppliers_list()
                    self.status_bar.config(text="تم حذف المورد بنجاح")
                else:
                    messagebox.showerror("خطأ", "فشل في حذف المورد")
                    self.status_bar.config(text="فشل في حذف المورد")
            
            except Exception as e:
                messagebox.showerror("خطأ", f"حدث خطأ: {str(e)}")
                self.status_bar.config(text="حدث خطأ أثناء حذف المورد")
    
    def clear_form(self):
        """مسح النموذج"""
        self.selected_supplier_id = None
        self.var_name.set("")
        self.var_contact_info.set("")
        self.status_bar.config(text="تم مسح النموذج")

# تشغيل النافذة إذا تم تشغيل الملف مباشرة
if __name__ == "__main__":
    app = SupplierManagementWindow()
    app.window.mainloop()
