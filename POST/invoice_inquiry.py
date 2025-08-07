import tkinter as tk
from tkinter import ttk, messagebox
from models import Invoice
from utils import ValidationUtils
import webbrowser
import tempfile
import os

class InvoiceInquiryWindow:
    def __init__(self, parent=None):
        self.parent = parent
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("استعلام الفواتير")
        self.window.geometry("900x700")
        self.window.configure(bg='#f0f0f0')
        
        # إنشاء النموذج
        self.invoice_model = Invoice()
        
        # متغيرات النموذج
        self.setup_variables()
        
        # إنشاء الواجهة
        self.create_widgets()
        
        # بيانات الفاتورة الحالية
        self.current_invoice = None
    
    def setup_variables(self):
        """إعداد متغيرات النموذج"""
        self.var_invoice_number = tk.StringVar()
        self.var_search_result = tk.StringVar()
    
    def create_widgets(self):
        """إنشاء عناصر الواجهة"""
        # الإطار الرئيسي
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # إطار البحث
        search_frame = ttk.LabelFrame(main_frame, text="استعلام عن فاتورة", padding=20)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        # حقل رقم الفاتورة
        invoice_row = ttk.Frame(search_frame)
        invoice_row.pack(fill=tk.X, pady=10)
        
        ttk.Label(invoice_row, text="رقم الفاتورة:", font=('Arial', 12, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
        
        # حقل إدخال رقم الفاتورة مع التحقق من الأرقام فقط
        self.invoice_entry = ttk.Entry(invoice_row, textvariable=self.var_invoice_number, 
                                      font=('Arial', 12), width=25)
        self.invoice_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.invoice_entry.bind('<KeyRelease>', self.validate_invoice_input)
        self.invoice_entry.bind('<Return>', lambda e: self.search_invoice())
        
        # أزرار البحث
        ttk.Button(invoice_row, text="استعلام", command=self.search_invoice,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(invoice_row, text="مسح", command=self.clear_search).pack(side=tk.LEFT)
        
        # نتيجة البحث
        result_row = ttk.Frame(search_frame)
        result_row.pack(fill=tk.X, pady=(10, 0))
        
        self.result_label = ttk.Label(result_row, textvariable=self.var_search_result, 
                                     font=('Arial', 11), foreground='blue')
        self.result_label.pack(side=tk.LEFT)
        
        # إطار تفاصيل الفاتورة
        self.details_frame = ttk.LabelFrame(main_frame, text="تفاصيل الفاتورة", padding=15)
        self.details_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # إنشاء منطقة التفاصيل
        self.create_details_area()
        
        # إطار الأزرار
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X)
        
        self.print_button = ttk.Button(buttons_frame, text="طباعة الفاتورة", 
                                      command=self.print_invoice, state=tk.DISABLED)
        self.print_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.export_button = ttk.Button(buttons_frame, text="تصدير PDF", 
                                       command=self.export_pdf, state=tk.DISABLED)
        self.export_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(buttons_frame, text="إغلاق", command=self.window.destroy).pack(side=tk.RIGHT)
        
        # شريط الحالة
        self.status_bar = ttk.Label(self.window, text="أدخل رقم الفاتورة للاستعلام", 
                                   relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_details_area(self):
        """إنشاء منطقة تفاصيل الفاتورة"""
        # إطار المعلومات الأساسية
        info_frame = ttk.Frame(self.details_frame)
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        # العمود الأول
        col1 = ttk.Frame(info_frame)
        col1.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.invoice_info_labels = {}
        info_fields = [
            ("رقم الفاتورة:", "invoice_number"),
            ("تاريخ الإصدار:", "issue_date"),
            ("اسم العميل:", "customer_name")
        ]
        
        for label_text, field_name in info_fields:
            row = ttk.Frame(col1)
            row.pack(fill=tk.X, pady=2)
            ttk.Label(row, text=label_text, font=('Arial', 10, 'bold')).pack(side=tk.LEFT, anchor=tk.W)
            self.invoice_info_labels[field_name] = ttk.Label(row, text="", font=('Arial', 10))
            self.invoice_info_labels[field_name].pack(side=tk.LEFT, padx=(10, 0))
        
        # العمود الثاني
        col2 = ttk.Frame(info_frame)
        col2.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        amount_fields = [
            ("المبلغ الإجمالي:", "total_amount"),
            ("الربح:", "profit"),
            ("المبلغ النهائي:", "final_amount")
        ]
        
        for label_text, field_name in amount_fields:
            row = ttk.Frame(col2)
            row.pack(fill=tk.X, pady=2)
            ttk.Label(row, text=label_text, font=('Arial', 10, 'bold')).pack(side=tk.LEFT, anchor=tk.W)
            self.invoice_info_labels[field_name] = ttk.Label(row, text="", font=('Arial', 10))
            self.invoice_info_labels[field_name].pack(side=tk.LEFT, padx=(10, 0))
        
        # جدول المنتجات
        products_label = ttk.Label(self.details_frame, text="المنتجات المباعة:", 
                                  font=('Arial', 12, 'bold'))
        products_label.pack(anchor=tk.W, pady=(10, 5))
        
        # إنشاء Treeview للمنتجات
        columns = ('المنتج', 'الكمية', 'سعر البيع', 'سعر الشراء', 'الخصم', 'السعر النهائي')
        self.products_tree = ttk.Treeview(self.details_frame, columns=columns, show='headings', height=8)
        
        # تعريف العناوين
        for col in columns:
            self.products_tree.heading(col, text=col)
            self.products_tree.column(col, width=120, anchor=tk.CENTER)
        
        # شريط التمرير
        products_scrollbar = ttk.Scrollbar(self.details_frame, orient=tk.VERTICAL, 
                                          command=self.products_tree.yview)
        self.products_tree.configure(yscrollcommand=products_scrollbar.set)
        
        # تخطيط الجدول
        products_frame = ttk.Frame(self.details_frame)
        products_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.products_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        products_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def validate_invoice_input(self, event=None):
        """التحقق من صحة إدخال رقم الفاتورة"""
        current_text = self.var_invoice_number.get()
        
        # السماح بالأرقام والشرطات والحروف (لأرقام الفواتير مثل INV-20240805-0001)
        valid_chars = set('0123456789-ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        filtered_text = ''.join(c for c in current_text.upper() if c in valid_chars)
        
        if filtered_text != current_text:
            self.var_invoice_number.set(filtered_text)
    
    def search_invoice(self):
        """البحث عن الفاتورة"""
        invoice_number = self.var_invoice_number.get().strip()
        
        if not invoice_number:
            messagebox.showwarning("تحذير", "يرجى إدخال رقم الفاتورة")
            return
        
        try:
            self.status_bar.config(text="جاري البحث عن الفاتورة...")
            self.window.update()
            
            # البحث عن الفاتورة
            invoice_data = self.invoice_model.get_invoice_by_number(invoice_number)
            
            if invoice_data:
                self.current_invoice = invoice_data
                self.display_invoice_details(invoice_data)
                self.var_search_result.set("✅ تم العثور على الفاتورة")
                self.print_button.config(state=tk.NORMAL)
                self.export_button.config(state=tk.NORMAL)
                self.status_bar.config(text="تم العثور على الفاتورة بنجاح")
            else:
                self.clear_invoice_details()
                self.var_search_result.set("❌ لم يتم العثور على الفاتورة")
                self.print_button.config(state=tk.DISABLED)
                self.export_button.config(state=tk.DISABLED)
                self.status_bar.config(text="لم يتم العثور على الفاتورة")
                messagebox.showinfo("نتيجة البحث", f"لم يتم العثور على فاتورة برقم: {invoice_number}")
        
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء البحث: {str(e)}")
            self.status_bar.config(text="حدث خطأ أثناء البحث")
    
    def display_invoice_details(self, invoice_data):
        """عرض تفاصيل الفاتورة"""
        invoice = invoice_data['invoice']
        details = invoice_data['details']
        
        # عرض المعلومات الأساسية
        self.invoice_info_labels['invoice_number'].config(text=invoice['invoice_number'])
        self.invoice_info_labels['issue_date'].config(text=invoice['issue_date'][:10])
        self.invoice_info_labels['customer_name'].config(text=invoice['customer_name'] or "عميل عادي")
        self.invoice_info_labels['total_amount'].config(text=f"{invoice['total_amount']:.2f}")
        self.invoice_info_labels['profit'].config(text=f"{invoice['profit']:.2f}")
        self.invoice_info_labels['final_amount'].config(text=f"{invoice['final_amount']:.2f}")
        
        # مسح جدول المنتجات
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        # إضافة المنتجات
        for detail in details:
            values = (
                detail['product_name'],
                detail['quantity'],
                f"{detail['selling_price']:.2f}",
                f"{detail['purchasing_price']:.2f}",
                f"{detail['discount_applied'] + detail['manual_discount']:.2f}",
                f"{detail['final_price']:.2f}"
            )
            self.products_tree.insert('', tk.END, values=values)
    
    def clear_invoice_details(self):
        """مسح تفاصيل الفاتورة"""
        for label in self.invoice_info_labels.values():
            label.config(text="")
        
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        self.current_invoice = None
    
    def clear_search(self):
        """مسح البحث"""
        self.var_invoice_number.set("")
        self.var_search_result.set("")
        self.clear_invoice_details()
        self.print_button.config(state=tk.DISABLED)
        self.export_button.config(state=tk.DISABLED)
        self.status_bar.config(text="أدخل رقم الفاتورة للاستعلام")
    
    def print_invoice(self):
        """طباعة الفاتورة"""
        if not self.current_invoice:
            messagebox.showwarning("تحذير", "لا توجد فاتورة لطباعتها")
            return
        
        try:
            # إنشاء ملف HTML للطباعة
            html_content = self.generate_invoice_html()
            
            # حفظ الملف المؤقت
            temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.html', 
                                                   delete=False, encoding='utf-8')
            temp_file.write(html_content)
            temp_file.close()
            
            # فتح الملف في المتصفح للطباعة
            webbrowser.open(f'file://{temp_file.name}')
            
            self.status_bar.config(text="تم فتح الفاتورة للطباعة")
            
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء الطباعة: {str(e)}")
    
    def export_pdf(self):
        """تصدير الفاتورة كـ PDF"""
        if not self.current_invoice:
            messagebox.showwarning("تحذير", "لا توجد فاتورة للتصدير")
            return
        
        messagebox.showinfo("معلومات", "ميزة تصدير PDF ستكون متاحة في التحديث القادم")
    
    def generate_invoice_html(self):
        """إنشاء HTML للفاتورة"""
        if not self.current_invoice:
            return ""
        
        invoice = self.current_invoice['invoice']
        details = self.current_invoice['details']
        
        html = f"""
        <!DOCTYPE html>
        <html dir="rtl" lang="ar">
        <head>
            <meta charset="UTF-8">
            <title>فاتورة رقم {invoice['invoice_number']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ text-align: center; margin-bottom: 30px; }}
                .invoice-info {{ margin-bottom: 20px; }}
                .invoice-info table {{ width: 100%; }}
                .invoice-info td {{ padding: 5px; }}
                .products-table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                .products-table th, .products-table td {{ border: 1px solid #ddd; padding: 8px; text-align: center; }}
                .products-table th {{ background-color: #f2f2f2; }}
                .total {{ margin-top: 20px; text-align: right; font-weight: bold; }}
                @media print {{ body {{ margin: 0; }} }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>متجر الأدوات الكهربائية</h1>
                <h2>فاتورة مبيعات</h2>
            </div>
            
            <div class="invoice-info">
                <table>
                    <tr>
                        <td><strong>رقم الفاتورة:</strong> {invoice['invoice_number']}</td>
                        <td><strong>تاريخ الإصدار:</strong> {invoice['issue_date'][:10]}</td>
                    </tr>
                    <tr>
                        <td><strong>اسم العميل:</strong> {invoice['customer_name'] or 'عميل عادي'}</td>
                        <td><strong>تاريخ البيع:</strong> {invoice['sale_date'][:10]}</td>
                    </tr>
                </table>
            </div>
            
            <table class="products-table">
                <thead>
                    <tr>
                        <th>المنتج</th>
                        <th>الكمية</th>
                        <th>سعر البيع</th>
                        <th>الخصم</th>
                        <th>السعر النهائي</th>
                        <th>الإجمالي</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for detail in details:
            total_price = detail['final_price'] * detail['quantity']
            discount = detail['discount_applied'] + detail['manual_discount']
            html += f"""
                    <tr>
                        <td>{detail['product_name']}</td>
                        <td>{detail['quantity']}</td>
                        <td>{detail['selling_price']:.2f}</td>
                        <td>{discount:.2f}</td>
                        <td>{detail['final_price']:.2f}</td>
                        <td>{total_price:.2f}</td>
                    </tr>
            """
        
        html += f"""
                </tbody>
            </table>
            
            <div class="total">
                <p>المبلغ الإجمالي: {invoice['total_amount']:.2f}</p>
                <p>المبلغ النهائي: {invoice['final_amount']:.2f}</p>
            </div>
            
            <script>
                window.onload = function() {{
                    window.print();
                }}
            </script>
        </body>
        </html>
        """
        
        return html

# تشغيل النافذة إذا تم تشغيل الملف مباشرة
if __name__ == "__main__":
    app = InvoiceInquiryWindow()
    app.window.mainloop()
