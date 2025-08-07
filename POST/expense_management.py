import tkinter as tk
from tkinter import ttk, messagebox
from models import Expense
from utils import ValidationUtils
from datetime import datetime
from tkcalendar import DateEntry

class ExpenseManagementWindow:
    def __init__(self, parent=None):
        self.parent = parent
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("إدارة المصروفات")
        self.window.geometry("900x700")
        self.window.configure(bg='#f0f0f0')
        
        # إنشاء النموذج
        self.expense_model = Expense()
        
        # متغيرات النموذج
        self.setup_variables()
        
        # إنشاء الواجهة
        self.create_widgets()
        
        # تحديث القائمة
        self.refresh_expenses_list()
        
        # تحديد المصروف المحدد
        self.selected_expense_id = None
    
    def setup_variables(self):
        """إعداد متغيرات النموذج"""
        self.var_description = tk.StringVar()
        self.var_amount = tk.StringVar()
        self.var_date = tk.StringVar()
        self.var_total_expenses = tk.StringVar(value="0.00")
    
    def create_widgets(self):
        """إنشاء عناصر الواجهة"""
        # الإطار الرئيسي
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # إطار النموذج
        form_frame = ttk.LabelFrame(main_frame, text="بيانات المصروف", padding=20)
        form_frame.pack(fill=tk.X, pady=(0, 10))
        
        # الصف الأول - وصف المصروف
        row1 = ttk.Frame(form_frame)
        row1.pack(fill=tk.X, pady=10)
        
        ttk.Label(row1, text="وصف المصروف:", font=('Arial', 12)).pack(side=tk.LEFT, padx=(0, 10))
        description_entry = ttk.Entry(row1, textvariable=self.var_description, font=('Arial', 12), width=40)
        description_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # الصف الثاني - المبلغ والتاريخ
        row2 = ttk.Frame(form_frame)
        row2.pack(fill=tk.X, pady=10)
        
        ttk.Label(row2, text="المبلغ:", font=('Arial', 12)).pack(side=tk.LEFT, padx=(0, 10))
        amount_entry = ttk.Entry(row2, textvariable=self.var_amount, font=('Arial', 12), width=15)
        amount_entry.pack(side=tk.LEFT, padx=(0, 30))
        
        ttk.Label(row2, text="التاريخ:", font=('Arial', 12)).pack(side=tk.LEFT, padx=(0, 10))
        
        # استخدام DateEntry إذا كان متاحاً، وإلا استخدام Entry عادي
        try:
            self.date_entry = DateEntry(row2, textvariable=self.var_date, 
                                      date_pattern='yyyy-mm-dd', font=('Arial', 12))
            self.date_entry.set_date(datetime.now().date())
        except:
            # في حالة عدم توفر tkcalendar، استخدم Entry عادي
            self.date_entry = ttk.Entry(row2, textvariable=self.var_date, font=('Arial', 12), width=15)
            self.var_date.set(datetime.now().strftime('%Y-%m-%d'))
        
        self.date_entry.pack(side=tk.LEFT)
        
        # إطار الأزرار
        buttons_frame = ttk.Frame(form_frame)
        buttons_frame.pack(fill=tk.X, pady=15)
        
        # أزرار العمليات
        ttk.Button(buttons_frame, text="إضافة مصروف", command=self.add_expense, 
                  style='Accent.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="تحديث مصروف", command=self.update_expense).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="حذف مصروف", command=self.delete_expense).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="مسح النموذج", command=self.clear_form).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="تحديث القائمة", command=self.refresh_expenses_list).pack(side=tk.LEFT)
        
        # إطار الإحصائيات
        stats_frame = ttk.LabelFrame(main_frame, text="إحصائيات المصروفات", padding=10)
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        # إجمالي المصروفات
        total_frame = ttk.Frame(stats_frame)
        total_frame.pack(fill=tk.X)
        
        ttk.Label(total_frame, text="إجمالي المصروفات:", font=('Arial', 14, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Entry(total_frame, textvariable=self.var_total_expenses, width=20, state='readonly',
                 font=('Arial', 14, 'bold')).pack(side=tk.LEFT)
        
        # أزرار التصفية
        filter_frame = ttk.Frame(stats_frame)
        filter_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(filter_frame, text="مصروفات اليوم", command=self.show_today_expenses).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(filter_frame, text="مصروفات الشهر", command=self.show_month_expenses).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(filter_frame, text="جميع المصروفات", command=self.refresh_expenses_list).pack(side=tk.LEFT)
        
        # إطار قائمة المصروفات
        list_frame = ttk.LabelFrame(main_frame, text="قائمة المصروفات", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # إنشاء Treeview
        columns = ('ID', 'الوصف', 'المبلغ', 'التاريخ')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # تعريف العناوين وعرض الأعمدة
        self.tree.heading('ID', text='المعرف')
        self.tree.heading('الوصف', text='وصف المصروف')
        self.tree.heading('المبلغ', text='المبلغ')
        self.tree.heading('التاريخ', text='التاريخ')
        
        self.tree.column('ID', width=80, anchor=tk.CENTER)
        self.tree.column('الوصف', width=300, anchor=tk.CENTER)
        self.tree.column('المبلغ', width=120, anchor=tk.CENTER)
        self.tree.column('التاريخ', width=120, anchor=tk.CENTER)
        
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
    
    def refresh_expenses_list(self):
        """تحديث قائمة المصروفات"""
        # مسح القائمة الحالية
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # جلب المصروفات
        expenses = self.expense_model.get_all_expenses()
        
        total_amount = 0
        for expense in expenses:
            values = (
                expense['expense_id'],
                expense['description'],
                f"{expense['amount']:.2f}",
                expense['date'][:10] if len(expense['date']) > 10 else expense['date']  # عرض التاريخ فقط
            )
            self.tree.insert('', tk.END, values=values)
            total_amount += expense['amount']
        
        # تحديث الإجمالي
        self.var_total_expenses.set(f"{total_amount:.2f}")
        
        # تحديث شريط الحالة
        self.status_bar.config(text=f"تم تحميل {len(expenses)} مصروف - الإجمالي: {total_amount:.2f}")
    
    def show_today_expenses(self):
        """عرض مصروفات اليوم"""
        today = datetime.now().strftime('%Y-%m-%d')
        self.show_expenses_by_date(today, today)
    
    def show_month_expenses(self):
        """عرض مصروفات الشهر الحالي"""
        now = datetime.now()
        start_date = f"{now.year}-{now.month:02d}-01"
        
        # حساب آخر يوم في الشهر
        if now.month == 12:
            end_date = f"{now.year + 1}-01-01"
        else:
            end_date = f"{now.year}-{now.month + 1:02d}-01"
        
        # تحويل إلى datetime وطرح يوم واحد
        from datetime import datetime, timedelta
        end_datetime = datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=1)
        end_date = end_datetime.strftime('%Y-%m-%d')
        
        self.show_expenses_by_date(start_date, end_date)
    
    def show_expenses_by_date(self, start_date, end_date):
        """عرض المصروفات في فترة زمنية محددة"""
        # مسح القائمة الحالية
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # جلب المصروفات في الفترة المحددة
        expenses = self.expense_model.get_expenses_by_date_range(start_date, end_date)
        
        total_amount = 0
        for expense in expenses:
            values = (
                expense['expense_id'],
                expense['description'],
                f"{expense['amount']:.2f}",
                expense['date'][:10] if len(expense['date']) > 10 else expense['date']
            )
            self.tree.insert('', tk.END, values=values)
            total_amount += expense['amount']
        
        # تحديث الإجمالي
        self.var_total_expenses.set(f"{total_amount:.2f}")
        
        # تحديث شريط الحالة
        period_text = f"من {start_date} إلى {end_date}" if start_date != end_date else start_date
        self.status_bar.config(text=f"المصروفات {period_text}: {len(expenses)} مصروف - الإجمالي: {total_amount:.2f}")
    
    def on_select(self, event):
        """عند تحديد مصروف من القائمة"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            
            self.selected_expense_id = values[0]
            
            # تحديث النموذج
            self.var_description.set(values[1])
            self.var_amount.set(values[2])
            self.var_date.set(values[3])
    
    def validate_form(self):
        """التحقق من صحة النموذج"""
        if not ValidationUtils.validate_required_field(self.var_description.get()):
            messagebox.showerror("خطأ", "وصف المصروف مطلوب")
            return False
        
        if not ValidationUtils.validate_price(self.var_amount.get()):
            messagebox.showerror("خطأ", "المبلغ غير صحيح")
            return False
        
        if not ValidationUtils.validate_required_field(self.var_date.get()):
            messagebox.showerror("خطأ", "التاريخ مطلوب")
            return False
        
        return True

    def add_expense(self):
        """إضافة مصروف جديد"""
        if not self.validate_form():
            return

        try:
            expense_id = self.expense_model.add_expense(
                description=self.var_description.get().strip(),
                amount=float(self.var_amount.get()),
                date=self.var_date.get()
            )

            if expense_id:
                messagebox.showinfo("نجح", "تم إضافة المصروف بنجاح")
                self.clear_form()
                self.refresh_expenses_list()
                self.status_bar.config(text="تم إضافة مصروف جديد بنجاح")
            else:
                messagebox.showerror("خطأ", "فشل في إضافة المصروف")
                self.status_bar.config(text="فشل في إضافة المصروف")

        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ: {str(e)}")
            self.status_bar.config(text="حدث خطأ أثناء إضافة المصروف")

    def update_expense(self):
        """تحديث مصروف موجود"""
        if not self.selected_expense_id:
            messagebox.showwarning("تحذير", "يرجى تحديد مصروف للتحديث")
            return

        if not self.validate_form():
            return

        try:
            success = self.expense_model.update_expense(
                expense_id=self.selected_expense_id,
                description=self.var_description.get().strip(),
                amount=float(self.var_amount.get()),
                date=self.var_date.get()
            )

            if success:
                messagebox.showinfo("نجح", "تم تحديث المصروف بنجاح")
                self.clear_form()
                self.refresh_expenses_list()
                self.status_bar.config(text="تم تحديث المصروف بنجاح")
            else:
                messagebox.showerror("خطأ", "فشل في تحديث المصروف")
                self.status_bar.config(text="فشل في تحديث المصروف")

        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ: {str(e)}")
            self.status_bar.config(text="حدث خطأ أثناء تحديث المصروف")

    def delete_expense(self):
        """حذف مصروف"""
        if not self.selected_expense_id:
            messagebox.showwarning("تحذير", "يرجى تحديد مصروف للحذف")
            return

        result = messagebox.askyesno("تأكيد الحذف", "هل أنت متأكد من حذف هذا المصروف؟")
        if result:
            try:
                success = self.expense_model.delete_expense(self.selected_expense_id)

                if success:
                    messagebox.showinfo("نجح", "تم حذف المصروف بنجاح")
                    self.clear_form()
                    self.refresh_expenses_list()
                    self.status_bar.config(text="تم حذف المصروف بنجاح")
                else:
                    messagebox.showerror("خطأ", "فشل في حذف المصروف")
                    self.status_bar.config(text="فشل في حذف المصروف")

            except Exception as e:
                messagebox.showerror("خطأ", f"حدث خطأ: {str(e)}")
                self.status_bar.config(text="حدث خطأ أثناء حذف المصروف")

    def clear_form(self):
        """مسح النموذج"""
        self.selected_expense_id = None
        self.var_description.set("")
        self.var_amount.set("")
        self.var_date.set(datetime.now().strftime('%Y-%m-%d'))
        self.status_bar.config(text="تم مسح النموذج")

# تشغيل النافذة إذا تم تشغيل الملف مباشرة
if __name__ == "__main__":
    app = ExpenseManagementWindow()
    app.window.mainloop()
