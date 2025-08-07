import tkinter as tk
from tkinter import ttk, messagebox
from models import ProductQuery, Customer
from utils import ValidationUtils
from datetime import datetime

class ProductInquiryWindow:
    def __init__(self, parent=None):
        self.parent = parent
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("استعلام المنتجات وحفظ الطلبات")
        self.window.geometry("1000x700")
        self.window.configure(bg='#f0f0f0')
        
        # إنشاء النماذج
        self.query_model = ProductQuery()
        self.customer_model = Customer()
        
        # متغيرات النموذج
        self.setup_variables()
        
        # إنشاء الواجهة
        self.create_widgets()
        
        # تحديث البيانات
        self.refresh_data()
    
    def setup_variables(self):
        """إعداد متغيرات النموذج"""
        self.var_search_term = tk.StringVar()
        self.var_customer = tk.StringVar()
        self.var_notes = tk.StringVar()
        self.var_quantity = tk.StringVar(value="1")
    
    def create_widgets(self):
        """إنشاء عناصر الواجهة"""
        # الإطار الرئيسي
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # إطار البحث
        search_frame = ttk.LabelFrame(main_frame, text="البحث عن المنتجات", padding=15)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        # صف البحث
        search_row = ttk.Frame(search_frame)
        search_row.pack(fill=tk.X, pady=5)
        
        ttk.Label(search_row, text="البحث:", font=('Arial', 12)).pack(side=tk.LEFT, padx=(0, 10))
        
        search_entry = ttk.Entry(search_row, textvariable=self.var_search_term, 
                                font=('Arial', 12), width=30)
        search_entry.pack(side=tk.LEFT, padx=(0, 10))
        search_entry.bind('<Return>', lambda e: self.search_products())
        
        ttk.Button(search_row, text="بحث", command=self.search_products,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(search_row, text="عرض الكل", command=self.show_all_products).pack(side=tk.LEFT)
        
        # تلميح البحث
        hint_label = ttk.Label(search_frame, text="يمكنك البحث باسم المنتج أو الوصف أو الفئة", 
                              font=('Arial', 9), foreground='gray')
        hint_label.pack(anchor=tk.W, pady=(5, 0))
        
        # إطار النتائج
        results_frame = ttk.LabelFrame(main_frame, text="نتائج البحث", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # جدول النتائج
        columns = ('المنتج', 'الوصف', 'سعر البيع', 'المخزون', 'الفئة', 'المورد')
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show='headings', height=10)
        
        # تعريف العناوين
        for col in columns:
            self.results_tree.heading(col, text=col)
            if col == 'الوصف':
                self.results_tree.column(col, width=200, anchor=tk.CENTER)
            else:
                self.results_tree.column(col, width=120, anchor=tk.CENTER)
        
        # شريط التمرير
        results_scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, 
                                         command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=results_scrollbar.set)
        
        # تخطيط الجدول
        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # ربط الأحداث
        self.results_tree.bind('<<TreeviewSelect>>', self.on_product_select)
        
        # إطار حفظ الاستعلام
        save_frame = ttk.LabelFrame(main_frame, text="حفظ طلب المنتج", padding=15)
        save_frame.pack(fill=tk.X, pady=(0, 10))
        
        # الصف الأول
        row1 = ttk.Frame(save_frame)
        row1.pack(fill=tk.X, pady=5)
        
        ttk.Label(row1, text="العميل:", font=('Arial', 11)).pack(side=tk.LEFT, padx=(0, 10))
        self.customer_combo = ttk.Combobox(row1, textvariable=self.var_customer, 
                                          width=25, state='readonly')
        self.customer_combo.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(row1, text="الكمية:", font=('Arial', 11)).pack(side=tk.LEFT, padx=(0, 10))
        quantity_entry = ttk.Entry(row1, textvariable=self.var_quantity, width=10)
        quantity_entry.pack(side=tk.LEFT, padx=(0, 20))
        
        # الصف الثاني
        row2 = ttk.Frame(save_frame)
        row2.pack(fill=tk.X, pady=5)
        
        ttk.Label(row2, text="ملاحظات:", font=('Arial', 11)).pack(side=tk.LEFT, padx=(0, 10))
        notes_entry = ttk.Entry(row2, textvariable=self.var_notes, width=50)
        notes_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 20))
        
        # أزرار الحفظ
        buttons_row = ttk.Frame(save_frame)
        buttons_row.pack(fill=tk.X, pady=(10, 0))
        
        self.save_button = ttk.Button(buttons_row, text="حفظ الطلب", 
                                     command=self.save_query, state=tk.DISABLED)
        self.save_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(buttons_row, text="عرض الطلبات المحفوظة", 
                  command=self.show_saved_queries).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(buttons_row, text="مسح النموذج", command=self.clear_form).pack(side=tk.LEFT)
        
        # معلومات المنتج المحدد
        self.selected_product_info = ttk.Label(save_frame, text="", 
                                              font=('Arial', 10, 'bold'), foreground='blue')
        self.selected_product_info.pack(anchor=tk.W, pady=(10, 0))
        
        # شريط الحالة
        self.status_bar = ttk.Label(self.window, text="جاهز للبحث", 
                                   relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # بيانات المنتج المحدد
        self.selected_product = None
    
    def refresh_data(self):
        """تحديث البيانات"""
        # تحديث قائمة العملاء
        customers = self.customer_model.get_all_customers()
        customer_values = ["عميل عادي"] + [f"{cust['customer_id']} - {cust['name']}" for cust in customers]
        self.customer_combo['values'] = customer_values
        self.customer_combo.set("عميل عادي")
        
        # عرض جميع المنتجات في البداية
        self.show_all_products()
    
    def search_products(self):
        """البحث عن المنتجات"""
        search_term = self.var_search_term.get().strip()
        
        if not search_term:
            messagebox.showwarning("تحذير", "يرجى إدخال كلمة البحث")
            return
        
        try:
            self.status_bar.config(text="جاري البحث...")
            self.window.update()
            
            # البحث عن المنتجات
            products = self.query_model.search_products(search_term)
            
            # عرض النتائج
            self.display_products(products)
            
            self.status_bar.config(text=f"تم العثور على {len(products)} منتج")
            
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء البحث: {str(e)}")
            self.status_bar.config(text="حدث خطأ أثناء البحث")
    
    def show_all_products(self):
        """عرض جميع المنتجات"""
        try:
            # جلب جميع المنتجات
            products = self.query_model.search_products("")
            
            # عرض النتائج
            self.display_products(products)
            
            self.status_bar.config(text=f"تم عرض {len(products)} منتج")
            
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء جلب المنتجات: {str(e)}")
    
    def display_products(self, products):
        """عرض المنتجات في الجدول"""
        # مسح الجدول
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # إضافة المنتجات
        for product in products:
            values = (
                product['name'],
                product['description'] or "",
                f"{product['selling_price']:.2f}",
                product['stock_quantity'],
                product['category_name'] or "غير محدد",
                product['supplier_name'] or "غير محدد"
            )
            
            # تلوين المنتجات منخفضة المخزون
            item_id = self.results_tree.insert('', tk.END, values=values)
            if product['stock_quantity'] <= 5:
                self.results_tree.set(item_id, 'المخزون', f"{product['stock_quantity']} ⚠️")
    
    def on_product_select(self, event):
        """عند تحديد منتج"""
        selection = self.results_tree.selection()
        if selection:
            item = self.results_tree.item(selection[0])
            values = item['values']
            
            # حفظ معلومات المنتج المحدد
            self.selected_product = {
                'name': values[0],
                'price': float(values[2]),
                'stock': int(str(values[3]).replace(' ⚠️', ''))
            }
            
            # عرض معلومات المنتج
            info_text = f"المنتج المحدد: {values[0]} - السعر: {values[2]} - المخزون: {values[3]}"
            self.selected_product_info.config(text=info_text)
            
            # تفعيل زر الحفظ
            self.save_button.config(state=tk.NORMAL)
    
    def save_query(self):
        """حفظ استعلام المنتج"""
        if not self.selected_product:
            messagebox.showwarning("تحذير", "يرجى تحديد منتج أولاً")
            return
        
        # التحقق من الكمية
        try:
            quantity = int(self.var_quantity.get())
            if quantity <= 0:
                messagebox.showerror("خطأ", "الكمية يجب أن تكون أكبر من صفر")
                return
        except ValueError:
            messagebox.showerror("خطأ", "يرجى إدخال كمية صحيحة")
            return
        
        # الحصول على معرف العميل
        customer_id = self.get_customer_id()
        
        try:
            # حفظ الاستعلام
            query_id = self.query_model.add_query(
                customer_id=customer_id,
                product_name=self.selected_product['name'],
                price=self.selected_product['price'],
                quantity=quantity,
                notes=self.var_notes.get()
            )
            
            if query_id:
                messagebox.showinfo("نجح", "تم حفظ طلب المنتج بنجاح")
                self.clear_form()
                self.status_bar.config(text="تم حفظ الطلب بنجاح")
            else:
                messagebox.showerror("خطأ", "فشل في حفظ الطلب")
        
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء حفظ الطلب: {str(e)}")
    
    def get_customer_id(self):
        """الحصول على معرف العميل"""
        customer_text = self.var_customer.get()
        if customer_text == "عميل عادي":
            return None
        elif " - " in customer_text:
            return int(customer_text.split(" - ")[0])
        return None
    
    def show_saved_queries(self):
        """عرض الطلبات المحفوظة"""
        SavedQueriesWindow(self.window)
    
    def clear_form(self):
        """مسح النموذج"""
        self.var_search_term.set("")
        self.var_customer.set("عميل عادي")
        self.var_notes.set("")
        self.var_quantity.set("1")
        self.selected_product = None
        self.selected_product_info.config(text="")
        self.save_button.config(state=tk.DISABLED)

class SavedQueriesWindow:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("الطلبات المحفوظة")
        self.window.geometry("800x600")
        self.window.configure(bg='#f0f0f0')
        
        # إنشاء النموذج
        self.query_model = ProductQuery()
        
        # إنشاء الواجهة
        self.create_widgets()
        
        # تحديث القائمة
        self.refresh_queries()
    
    def create_widgets(self):
        """إنشاء عناصر الواجهة"""
        # الإطار الرئيسي
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # أزرار التصفية
        filter_frame = ttk.Frame(main_frame)
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(filter_frame, text="جميع الطلبات", 
                  command=lambda: self.filter_queries(None)).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(filter_frame, text="غير منفذة", 
                  command=lambda: self.filter_queries(False)).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(filter_frame, text="منفذة", 
                  command=lambda: self.filter_queries(True)).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(filter_frame, text="تحديث", command=self.refresh_queries).pack(side=tk.RIGHT)
        
        # جدول الطلبات
        columns = ('المعرف', 'العميل', 'المنتج', 'السعر', 'الكمية', 'التاريخ', 'الحالة', 'ملاحظات')
        self.queries_tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=15)
        
        # تعريف العناوين
        for col in columns:
            self.queries_tree.heading(col, text=col)
            if col == 'ملاحظات':
                self.queries_tree.column(col, width=150, anchor=tk.CENTER)
            else:
                self.queries_tree.column(col, width=100, anchor=tk.CENTER)
        
        # شريط التمرير
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.queries_tree.yview)
        self.queries_tree.configure(yscrollcommand=scrollbar.set)
        
        # تخطيط الجدول
        self.queries_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # أزرار العمليات
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(buttons_frame, text="تنفيذ الطلب", 
                  command=self.execute_query).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="حذف الطلب", 
                  command=self.delete_query).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="إغلاق", 
                  command=self.window.destroy).pack(side=tk.RIGHT)
    
    def refresh_queries(self):
        """تحديث قائمة الطلبات"""
        self.filter_queries(None)
    
    def filter_queries(self, executed):
        """تصفية الطلبات"""
        # مسح الجدول
        for item in self.queries_tree.get_children():
            self.queries_tree.delete(item)
        
        # جلب الطلبات
        queries = self.query_model.get_all_queries(executed)
        
        for query in queries:
            status = "منفذ" if query['executed'] else "غير منفذ"
            values = (
                query['query_id'],
                query['customer_name'] or "عميل عادي",
                query['product_name'],
                f"{query['price']:.2f}",
                query['quantity'],
                query['query_date'][:10],
                status,
                query['notes'] or ""
            )
            self.queries_tree.insert('', tk.END, values=values)
    
    def execute_query(self):
        """تنفيذ الطلب"""
        selection = self.queries_tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "يرجى تحديد طلب للتنفيذ")
            return
        
        item = self.queries_tree.item(selection[0])
        query_id = item['values'][0]
        
        result = messagebox.askyesno("تأكيد التنفيذ", "هل تريد تنفيذ هذا الطلب وإنشاء فاتورة؟")
        if result:
            try:
                # تحديد الطلب كمنفذ
                success = self.query_model.mark_as_executed(query_id)
                
                if success:
                    messagebox.showinfo("نجح", "تم تنفيذ الطلب بنجاح")
                    self.refresh_queries()
                else:
                    messagebox.showerror("خطأ", "فشل في تنفيذ الطلب")
            
            except Exception as e:
                messagebox.showerror("خطأ", f"حدث خطأ: {str(e)}")
    
    def delete_query(self):
        """حذف الطلب"""
        selection = self.queries_tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "يرجى تحديد طلب للحذف")
            return
        
        item = self.queries_tree.item(selection[0])
        query_id = item['values'][0]
        
        result = messagebox.askyesno("تأكيد الحذف", "هل أنت متأكد من حذف هذا الطلب؟")
        if result:
            try:
                success = self.query_model.delete_query(query_id)
                
                if success:
                    messagebox.showinfo("نجح", "تم حذف الطلب بنجاح")
                    self.refresh_queries()
                else:
                    messagebox.showerror("خطأ", "فشل في حذف الطلب")
            
            except Exception as e:
                messagebox.showerror("خطأ", f"حدث خطأ: {str(e)}")

# تشغيل النافذة إذا تم تشغيل الملف مباشرة
if __name__ == "__main__":
    app = ProductInquiryWindow()
    app.window.mainloop()
