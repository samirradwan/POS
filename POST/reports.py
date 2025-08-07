import tkinter as tk
from tkinter import ttk, messagebox
from utils import ReportGenerator
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates

class ReportsWindow:
    def __init__(self, parent=None):
        self.parent = parent
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("التقارير والإحصائيات")
        self.window.geometry("1200x800")
        self.window.configure(bg='#f0f0f0')
        
        # إنشاء مولد التقارير
        self.report_generator = ReportGenerator()
        
        # متغيرات النموذج
        self.setup_variables()
        
        # إنشاء الواجهة
        self.create_widgets()
        
        # تحديث التقرير اليومي تلقائياً
        self.generate_daily_report()
    
    def setup_variables(self):
        """إعداد متغيرات النموذج"""
        self.var_report_date = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        self.var_week_start = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        self.var_month = tk.StringVar(value=str(datetime.now().month))
        self.var_year = tk.StringVar(value=str(datetime.now().year))
    
    def create_widgets(self):
        """إنشاء عناصر الواجهة"""
        # الإطار الرئيسي
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # إطار التحكم
        control_frame = ttk.LabelFrame(main_frame, text="خيارات التقارير", padding=10)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # أزرار التقارير
        buttons_row1 = ttk.Frame(control_frame)
        buttons_row1.pack(fill=tk.X, pady=5)
        
        ttk.Button(buttons_row1, text="تقرير يومي", command=self.show_daily_report_dialog).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_row1, text="تقرير أسبوعي", command=self.show_weekly_report_dialog).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_row1, text="تقرير شهري", command=self.show_monthly_report_dialog).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_row1, text="تقرير المنتجات", command=self.generate_product_report).pack(side=tk.LEFT, padx=(0, 10))
        
        # إطار النتائج
        results_frame = ttk.Frame(main_frame)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # إطار النص
        text_frame = ttk.LabelFrame(results_frame, text="تفاصيل التقرير", padding=10)
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # منطقة النص
        self.text_area = tk.Text(text_frame, wrap=tk.WORD, font=('Arial', 11))
        text_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text_area.yview)
        self.text_area.configure(yscrollcommand=text_scrollbar.set)
        
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # إطار الرسم البياني
        chart_frame = ttk.LabelFrame(results_frame, text="الرسم البياني", padding=10)
        chart_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # إعداد matplotlib
        self.setup_chart(chart_frame)
        
        # شريط الحالة
        self.status_bar = ttk.Label(self.window, text="جاهز", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def setup_chart(self, parent):
        """إعداد الرسم البياني"""
        try:
            self.fig, self.ax = plt.subplots(figsize=(6, 4))
            self.canvas = FigureCanvasTkAgg(self.fig, parent)
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # إعداد الخط العربي إذا كان متاحاً
            plt.rcParams['font.family'] = ['Arial Unicode MS', 'Tahoma', 'DejaVu Sans']
            
        except Exception as e:
            # في حالة عدم توفر matplotlib
            ttk.Label(parent, text="الرسم البياني غير متاح\nيرجى تثبيت matplotlib").pack(expand=True)
    
    def show_daily_report_dialog(self):
        """عرض حوار التقرير اليومي"""
        dialog = tk.Toplevel(self.window)
        dialog.title("تقرير يومي")
        dialog.geometry("300x150")
        dialog.transient(self.window)
        dialog.grab_set()
        
        ttk.Label(dialog, text="اختر التاريخ:", font=('Arial', 12)).pack(pady=10)
        
        date_entry = ttk.Entry(dialog, textvariable=self.var_report_date, font=('Arial', 12))
        date_entry.pack(pady=5)
        
        buttons_frame = ttk.Frame(dialog)
        buttons_frame.pack(pady=20)
        
        ttk.Button(buttons_frame, text="إنشاء التقرير", 
                  command=lambda: [self.generate_daily_report(), dialog.destroy()]).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="إلغاء", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def show_weekly_report_dialog(self):
        """عرض حوار التقرير الأسبوعي"""
        dialog = tk.Toplevel(self.window)
        dialog.title("تقرير أسبوعي")
        dialog.geometry("300x150")
        dialog.transient(self.window)
        dialog.grab_set()
        
        ttk.Label(dialog, text="تاريخ بداية الأسبوع:", font=('Arial', 12)).pack(pady=10)
        
        date_entry = ttk.Entry(dialog, textvariable=self.var_week_start, font=('Arial', 12))
        date_entry.pack(pady=5)
        
        buttons_frame = ttk.Frame(dialog)
        buttons_frame.pack(pady=20)
        
        ttk.Button(buttons_frame, text="إنشاء التقرير", 
                  command=lambda: [self.generate_weekly_report(), dialog.destroy()]).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="إلغاء", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def show_monthly_report_dialog(self):
        """عرض حوار التقرير الشهري"""
        dialog = tk.Toplevel(self.window)
        dialog.title("تقرير شهري")
        dialog.geometry("300x200")
        dialog.transient(self.window)
        dialog.grab_set()
        
        ttk.Label(dialog, text="اختر الشهر والسنة:", font=('Arial', 12)).pack(pady=10)
        
        month_frame = ttk.Frame(dialog)
        month_frame.pack(pady=5)
        
        ttk.Label(month_frame, text="الشهر:").pack(side=tk.LEFT, padx=5)
        month_combo = ttk.Combobox(month_frame, textvariable=self.var_month, width=10, state='readonly')
        month_combo['values'] = [str(i) for i in range(1, 13)]
        month_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(month_frame, text="السنة:").pack(side=tk.LEFT, padx=5)
        year_entry = ttk.Entry(month_frame, textvariable=self.var_year, width=10)
        year_entry.pack(side=tk.LEFT, padx=5)
        
        buttons_frame = ttk.Frame(dialog)
        buttons_frame.pack(pady=20)
        
        ttk.Button(buttons_frame, text="إنشاء التقرير", 
                  command=lambda: [self.generate_monthly_report(), dialog.destroy()]).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="إلغاء", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def generate_daily_report(self):
        """إنشاء التقرير اليومي"""
        try:
            date = self.var_report_date.get()
            report = self.report_generator.generate_daily_report(date)
            
            # عرض التقرير
            self.display_report(f"التقرير اليومي - {date}", report)
            
            # رسم بياني بسيط
            self.draw_daily_chart(report)
            
            self.status_bar.config(text=f"تم إنشاء التقرير اليومي لتاريخ {date}")
            
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في إنشاء التقرير: {str(e)}")
    
    def generate_weekly_report(self):
        """إنشاء التقرير الأسبوعي"""
        try:
            start_date = self.var_week_start.get()
            report = self.report_generator.generate_weekly_report(start_date)
            
            # عرض التقرير
            self.display_report(f"التقرير الأسبوعي - {report['period']}", report)
            
            self.status_bar.config(text=f"تم إنشاء التقرير الأسبوعي للفترة {report['period']}")
            
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في إنشاء التقرير: {str(e)}")
    
    def generate_monthly_report(self):
        """إنشاء التقرير الشهري"""
        try:
            year = int(self.var_year.get())
            month = int(self.var_month.get())
            report = self.report_generator.generate_monthly_report(year, month)
            
            # عرض التقرير
            self.display_report(f"التقرير الشهري - {report['period']}", report)
            
            self.status_bar.config(text=f"تم إنشاء التقرير الشهري للفترة {report['period']}")
            
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في إنشاء التقرير: {str(e)}")
    
    def generate_product_report(self):
        """إنشاء تقرير المنتجات"""
        try:
            report = self.report_generator.generate_product_report()
            
            # عرض التقرير
            self.display_product_report(report)
            
            self.status_bar.config(text="تم إنشاء تقرير المنتجات والمخزون")
            
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في إنشاء التقرير: {str(e)}")
    
    def display_report(self, title, report):
        """عرض التقرير في منطقة النص"""
        self.text_area.delete(1.0, tk.END)
        
        content = f"{title}\n"
        content += "=" * 50 + "\n\n"
        
        # بيانات المبيعات
        content += "📊 بيانات المبيعات:\n"
        content += f"   عدد المبيعات: {report['sales']['total_sales']}\n"
        content += f"   إجمالي الإيرادات: {report['sales']['total_revenue']:.2f}\n"
        content += f"   إجمالي الأرباح: {report['sales']['total_profit']:.2f}\n"
        content += f"   المبلغ النهائي: {report['sales']['total_final_amount']:.2f}\n\n"
        
        # بيانات المصروفات
        content += "💰 بيانات المصروفات:\n"
        content += f"   إجمالي المصروفات: {report['expenses']['total_expenses']:.2f}\n\n"
        
        # صافي الربح
        content += "📈 النتيجة النهائية:\n"
        content += f"   صافي الربح: {report['net_profit']:.2f}\n\n"
        
        # تفاصيل إضافية للتقارير الأسبوعية والشهرية
        if 'sales_details' in report and report['sales_details']:
            content += "📋 تفاصيل المبيعات:\n"
            for sale in report['sales_details'][:10]:  # أول 10 مبيعات
                content += f"   - فاتورة #{sale['sale_id']}: {sale['final_amount']:.2f} (ربح: {sale['profit']:.2f})\n"
            
            if len(report['sales_details']) > 10:
                content += f"   ... و {len(report['sales_details']) - 10} مبيعة أخرى\n"
        
        self.text_area.insert(tk.END, content)
    
    def display_product_report(self, report):
        """عرض تقرير المنتجات"""
        self.text_area.delete(1.0, tk.END)
        
        content = "تقرير المنتجات والمخزون\n"
        content += "=" * 50 + "\n\n"
        
        content += f"📦 إجمالي المنتجات: {report['total_products']}\n\n"
        
        # المنتجات منخفضة المخزون
        if report['low_stock_products']:
            content += "⚠️ منتجات منخفضة المخزون:\n"
            for product in report['low_stock_products']:
                content += f"   - {product['name']}: {product['stock_quantity']} قطعة\n"
            content += "\n"
        
        # المنتجات نفدت من المخزون
        if report['out_of_stock_products']:
            content += "🚫 منتجات نفدت من المخزون:\n"
            for product in report['out_of_stock_products']:
                content += f"   - {product['name']}\n"
            content += "\n"
        
        if not report['low_stock_products'] and not report['out_of_stock_products']:
            content += "✅ جميع المنتجات متوفرة بكميات كافية\n"
        
        self.text_area.insert(tk.END, content)
    
    def draw_daily_chart(self, report):
        """رسم بياني للتقرير اليومي"""
        try:
            self.ax.clear()
            
            categories = ['الإيرادات', 'الأرباح', 'المصروفات', 'صافي الربح']
            values = [
                report['sales']['total_revenue'],
                report['sales']['total_profit'],
                report['expenses']['total_expenses'],
                report['net_profit']
            ]
            
            colors = ['#2E8B57', '#32CD32', '#DC143C', '#4169E1']
            bars = self.ax.bar(categories, values, color=colors)
            
            self.ax.set_title('التقرير اليومي', fontsize=14, fontweight='bold')
            self.ax.set_ylabel('المبلغ')
            
            # إضافة القيم على الأعمدة
            for bar, value in zip(bars, values):
                height = bar.get_height()
                self.ax.text(bar.get_x() + bar.get_width()/2., height + max(values)*0.01,
                           f'{value:.1f}', ha='center', va='bottom')
            
            plt.xticks(rotation=45)
            plt.tight_layout()
            self.canvas.draw()
            
        except Exception as e:
            print(f"خطأ في الرسم البياني: {e}")

# تشغيل النافذة إذا تم تشغيل الملف مباشرة
if __name__ == "__main__":
    app = ReportsWindow()
    app.window.mainloop()
