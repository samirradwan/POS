import tkinter as tk
from tkinter import ttk, messagebox
from models import Product, Category, Supplier
from utils import ValidationUtils, CalculationUtils

class ProductManagementWindow:
    def __init__(self, parent=None):
        self.parent = parent
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("إدارة المنتجات")
        self.window.geometry("1200x700")
        self.window.configure(bg='#f0f0f0')
        
        # إنشاء النماذج
        self.product_model = Product()
        self.category_model = Category()
        self.supplier_model = Supplier()
        
        # متغيرات النموذج
        self.setup_variables()
        
        # إنشاء الواجهة
        self.create_widgets()
        
        # تحديث القوائم
        self.refresh_data()
        
        # تحديد المنتج المحدد
        self.selected_product_id = None
    
    def setup_variables(self):
        """إعداد متغيرات النموذج"""
        self.var_name = tk.StringVar()
        self.var_description = tk.StringVar()
        self.var_selling_price = tk.StringVar()
        self.var_purchasing_price = tk.StringVar()
        self.var_stock_quantity = tk.StringVar()
        self.var_discount_percentage = tk.StringVar(value="0")
        self.var_manual_discount = tk.StringVar(value="0")
        self.var_category = tk.StringVar()
        self.var_supplier = tk.StringVar()
        self.var_invoice_number = tk.StringVar()
        self.var_final_price = tk.StringVar()
    
    def create_widgets(self):
        """إنشاء عناصر الواجهة"""
        # الإطار الرئيسي
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # إطار النموذج
        form_frame = ttk.LabelFrame(main_frame, text="بيانات المنتج", padding=10)
        form_frame.pack(fill=tk.X, pady=(0, 10))
        
        # الصف الأول
        row1 = ttk.Frame(form_frame)
        row1.pack(fill=tk.X, pady=5)
        
        ttk.Label(row1, text="اسم المنتج:").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Entry(row1, textvariable=self.var_name, width=20).pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(row1, text="سعر البيع:").pack(side=tk.LEFT, padx=(0, 5))
        selling_price_entry = ttk.Entry(row1, textvariable=self.var_selling_price, width=15)
        selling_price_entry.pack(side=tk.LEFT, padx=(0, 20))
        selling_price_entry.bind('<KeyRelease>', self.calculate_final_price)
        
        ttk.Label(row1, text="سعر الشراء:").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Entry(row1, textvariable=self.var_purchasing_price, width=15).pack(side=tk.LEFT)
        
        # الصف الثاني
        row2 = ttk.Frame(form_frame)
        row2.pack(fill=tk.X, pady=5)
        
        ttk.Label(row2, text="الكمية:").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Entry(row2, textvariable=self.var_stock_quantity, width=10).pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(row2, text="نسبة الخصم (%):").pack(side=tk.LEFT, padx=(0, 5))
        discount_entry = ttk.Entry(row2, textvariable=self.var_discount_percentage, width=10)
        discount_entry.pack(side=tk.LEFT, padx=(0, 20))
        discount_entry.bind('<KeyRelease>', self.calculate_final_price)
        
        ttk.Label(row2, text="الخصم اليدوي:").pack(side=tk.LEFT, padx=(0, 5))
        manual_discount_entry = ttk.Entry(row2, textvariable=self.var_manual_discount, width=10)
        manual_discount_entry.pack(side=tk.LEFT, padx=(0, 20))
        manual_discount_entry.bind('<KeyRelease>', self.calculate_final_price)
        
        ttk.Label(row2, text="السعر النهائي:").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Entry(row2, textvariable=self.var_final_price, width=15, state='readonly').pack(side=tk.LEFT)
        
        # الصف الثالث
        row3 = ttk.Frame(form_frame)
        row3.pack(fill=tk.X, pady=5)
        
        ttk.Label(row3, text="الفئة:").pack(side=tk.LEFT, padx=(0, 5))
        self.category_combo = ttk.Combobox(row3, textvariable=self.var_category, width=18, state='readonly')
        self.category_combo.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(row3, text="المورد:").pack(side=tk.LEFT, padx=(0, 5))
        self.supplier_combo = ttk.Combobox(row3, textvariable=self.var_supplier, width=18, state='readonly')
        self.supplier_combo.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(row3, text="رقم الفاتورة:").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Entry(row3, textvariable=self.var_invoice_number, width=15).pack(side=tk.LEFT)
        
        # الصف الرابع - الوصف
        row4 = ttk.Frame(form_frame)
        row4.pack(fill=tk.X, pady=5)
        
        ttk.Label(row4, text="الوصف:").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Entry(row4, textvariable=self.var_description, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # أزرار العمليات
        buttons_frame = ttk.Frame(form_frame)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(buttons_frame, text="إضافة منتج", command=self.add_product).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="تحديث منتج", command=self.update_product).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="حذف منتج", command=self.delete_product).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="مسح النموذج", command=self.clear_form).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="تحديث القائمة", command=self.refresh_data).pack(side=tk.LEFT)
        
        # إطار قائمة المنتجات
        list_frame = ttk.LabelFrame(main_frame, text="قائمة المنتجات", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # إنشاء Treeview
        columns = ('ID', 'الاسم', 'سعر البيع', 'سعر الشراء', 'الكمية', 'الخصم%', 'الخصم اليدوي', 'السعر النهائي', 'الفئة', 'المورد')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # تعريف العناوين
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=tk.CENTER)
        
        # شريط التمرير
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # تخطيط العناصر
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # ربط الأحداث
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
    
    def calculate_final_price(self, event=None):
        """حساب السعر النهائي بعد الخصم"""
        try:
            selling_price = float(self.var_selling_price.get() or 0)
            discount_percentage = float(self.var_discount_percentage.get() or 0)
            manual_discount = float(self.var_manual_discount.get() or 0)
            
            final_price = CalculationUtils.calculate_discount(selling_price, discount_percentage, manual_discount)
            self.var_final_price.set(f"{final_price:.2f}")
        except ValueError:
            self.var_final_price.set("0.00")
    
    def refresh_data(self):
        """تحديث البيانات"""
        # تحديث قائمة الفئات
        categories = self.category_model.get_all_categories()
        category_values = [""] + [f"{cat['category_id']} - {cat['category_name']}" for cat in categories]
        self.category_combo['values'] = category_values
        
        # تحديث قائمة الموردين
        suppliers = self.supplier_model.get_all_suppliers()
        supplier_values = [""] + [f"{sup['supplier_id']} - {sup['supplier_name']}" for sup in suppliers]
        self.supplier_combo['values'] = supplier_values
        
        # تحديث قائمة المنتجات
        self.refresh_products_list()
    
    def refresh_products_list(self):
        """تحديث قائمة المنتجات"""
        # مسح القائمة الحالية
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # جلب المنتجات
        products = self.product_model.get_all_products()
        
        for product in products:
            # حساب السعر النهائي
            final_price = CalculationUtils.calculate_discount(
                product['selling_price'], 
                product['discount_percentage'], 
                product['manual_discount']
            )
            
            values = (
                product['product_id'],
                product['name'],
                f"{product['selling_price']:.2f}",
                f"{product['purchasing_price']:.2f}",
                product['stock_quantity'],
                f"{product['discount_percentage']:.1f}",
                f"{product['manual_discount']:.2f}",
                f"{final_price:.2f}",
                product['category_name'] or "غير محدد",
                product['supplier_name'] or "غير محدد"
            )
            
            self.tree.insert('', tk.END, values=values)

    def on_select(self, event):
        """عند تحديد منتج من القائمة"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']

            self.selected_product_id = values[0]

            # تحديث النموذج
            self.var_name.set(values[1])
            self.var_selling_price.set(values[2])
            self.var_purchasing_price.set(values[3])
            self.var_stock_quantity.set(values[4])
            self.var_discount_percentage.set(values[5])
            self.var_manual_discount.set(values[6])

            # جلب باقي البيانات
            product = self.product_model.get_product_by_id(self.selected_product_id)
            if product:
                self.var_description.set(product['description'] or "")
                self.var_invoice_number.set(product['invoice_number'] or "")

                # تحديد الفئة والمورد
                if product['category_id']:
                    category_text = f"{product['category_id']} - {product['category_name']}"
                    self.var_category.set(category_text)
                else:
                    self.var_category.set("")

                if product['supplier_id']:
                    supplier_text = f"{product['supplier_id']} - {product['supplier_name']}"
                    self.var_supplier.set(supplier_text)
                else:
                    self.var_supplier.set("")

            # حساب السعر النهائي
            self.calculate_final_price()

    def validate_form(self):
        """التحقق من صحة النموذج"""
        if not ValidationUtils.validate_required_field(self.var_name.get()):
            messagebox.showerror("خطأ", "اسم المنتج مطلوب")
            return False

        if not ValidationUtils.validate_price(self.var_selling_price.get()):
            messagebox.showerror("خطأ", "سعر البيع غير صحيح")
            return False

        if not ValidationUtils.validate_price(self.var_purchasing_price.get()):
            messagebox.showerror("خطأ", "سعر الشراء غير صحيح")
            return False

        if not ValidationUtils.validate_quantity(self.var_stock_quantity.get()):
            messagebox.showerror("خطأ", "الكمية غير صحيحة")
            return False

        if not ValidationUtils.validate_discount_percentage(self.var_discount_percentage.get()):
            messagebox.showerror("خطأ", "نسبة الخصم يجب أن تكون بين 0 و 100")
            return False

        return True

    def get_category_id(self):
        """استخراج معرف الفئة من النص المحدد"""
        category_text = self.var_category.get()
        if category_text and " - " in category_text:
            return int(category_text.split(" - ")[0])
        return None

    def get_supplier_id(self):
        """استخراج معرف المورد من النص المحدد"""
        supplier_text = self.var_supplier.get()
        if supplier_text and " - " in supplier_text:
            return int(supplier_text.split(" - ")[0])
        return None

    def add_product(self):
        """إضافة منتج جديد"""
        if not self.validate_form():
            return

        try:
            product_id = self.product_model.add_product(
                name=self.var_name.get(),
                description=self.var_description.get(),
                selling_price=float(self.var_selling_price.get()),
                purchasing_price=float(self.var_purchasing_price.get()),
                stock_quantity=int(self.var_stock_quantity.get()),
                discount_percentage=float(self.var_discount_percentage.get() or 0),
                manual_discount=float(self.var_manual_discount.get() or 0),
                category_id=self.get_category_id(),
                supplier_id=self.get_supplier_id(),
                invoice_number=self.var_invoice_number.get()
            )

            if product_id:
                messagebox.showinfo("نجح", "تم إضافة المنتج بنجاح")
                self.clear_form()
                self.refresh_products_list()
            else:
                messagebox.showerror("خطأ", "فشل في إضافة المنتج")

        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ: {str(e)}")

    def update_product(self):
        """تحديث منتج موجود"""
        if not self.selected_product_id:
            messagebox.showwarning("تحذير", "يرجى تحديد منتج للتحديث")
            return

        if not self.validate_form():
            return

        try:
            success = self.product_model.update_product(
                product_id=self.selected_product_id,
                name=self.var_name.get(),
                description=self.var_description.get(),
                selling_price=float(self.var_selling_price.get()),
                purchasing_price=float(self.var_purchasing_price.get()),
                stock_quantity=int(self.var_stock_quantity.get()),
                discount_percentage=float(self.var_discount_percentage.get() or 0),
                manual_discount=float(self.var_manual_discount.get() or 0),
                category_id=self.get_category_id(),
                supplier_id=self.get_supplier_id(),
                invoice_number=self.var_invoice_number.get()
            )

            if success:
                messagebox.showinfo("نجح", "تم تحديث المنتج بنجاح")
                self.clear_form()
                self.refresh_products_list()
            else:
                messagebox.showerror("خطأ", "فشل في تحديث المنتج")

        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ: {str(e)}")

    def delete_product(self):
        """حذف منتج"""
        if not self.selected_product_id:
            messagebox.showwarning("تحذير", "يرجى تحديد منتج للحذف")
            return

        result = messagebox.askyesno("تأكيد الحذف", "هل أنت متأكد من حذف هذا المنتج؟")
        if result:
            try:
                success = self.product_model.delete_product(self.selected_product_id)

                if success:
                    messagebox.showinfo("نجح", "تم حذف المنتج بنجاح")
                    self.clear_form()
                    self.refresh_products_list()
                else:
                    messagebox.showerror("خطأ", "فشل في حذف المنتج")

            except Exception as e:
                messagebox.showerror("خطأ", f"حدث خطأ: {str(e)}")

    def clear_form(self):
        """مسح النموذج"""
        self.selected_product_id = None
        self.var_name.set("")
        self.var_description.set("")
        self.var_selling_price.set("")
        self.var_purchasing_price.set("")
        self.var_stock_quantity.set("")
        self.var_discount_percentage.set("0")
        self.var_manual_discount.set("0")
        self.var_category.set("")
        self.var_supplier.set("")
        self.var_invoice_number.set("")
        self.var_final_price.set("")

# تشغيل النافذة إذا تم تشغيل الملف مباشرة
if __name__ == "__main__":
    app = ProductManagementWindow()
    app.window.mainloop()
