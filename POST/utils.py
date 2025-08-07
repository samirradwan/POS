from datetime import datetime, timedelta
from models import Sale, Expense, Product
import os
import shutil

class CalculationUtils:
    """فئة للحسابات المختلفة"""
    
    @staticmethod
    def calculate_discount(price, discount_percentage=0, manual_discount=0):
        """حساب الخصم"""
        percentage_discount = price * (discount_percentage / 100)
        final_price = price - percentage_discount - manual_discount
        return max(0, final_price)
    
    @staticmethod
    def calculate_profit(selling_price, purchasing_price, quantity=1):
        """حساب الربح"""
        return (selling_price - purchasing_price) * quantity
    
    @staticmethod
    def calculate_total_with_discount(items):
        """حساب الإجمالي مع الخصومات"""
        total = 0
        total_discount = 0
        
        for item in items:
            item_total = item['selling_price'] * item['quantity']
            item_discount = item_total * (item.get('discount_percentage', 0) / 100)
            item_discount += item.get('manual_discount', 0)
            
            total += item_total
            total_discount += item_discount
        
        return {
            'subtotal': total,
            'total_discount': total_discount,
            'final_total': total - total_discount
        }

class ReportGenerator:
    """فئة لإنشاء التقارير"""
    
    def __init__(self):
        self.sale_model = Sale()
        self.expense_model = Expense()
        self.product_model = Product()
    
    def generate_daily_report(self, date):
        """إنشاء تقرير يومي"""
        # تقرير المبيعات
        sales_report = self.sale_model.get_daily_sales_report(date)
        
        # تقرير المصروفات
        total_expenses = self.expense_model.get_total_expenses_by_date(date)
        
        # حساب صافي الربح
        net_profit = (sales_report['total_profit'] if sales_report['total_profit'] else 0) - total_expenses
        
        return {
            'date': date,
            'sales': {
                'total_sales': sales_report['total_sales'] if sales_report else 0,
                'total_revenue': sales_report['total_revenue'] if sales_report else 0,
                'total_profit': sales_report['total_profit'] if sales_report else 0,
                'total_final_amount': sales_report['total_final_amount'] if sales_report else 0
            },
            'expenses': {
                'total_expenses': total_expenses
            },
            'net_profit': net_profit
        }
    
    def generate_weekly_report(self, start_date):
        """إنشاء تقرير أسبوعي"""
        end_date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=6)).strftime('%Y-%m-%d')
        
        # جلب المبيعات الأسبوعية
        sales = self.sale_model.get_sales_by_date_range(start_date, end_date)
        
        # جلب المصروفات الأسبوعية
        expenses = self.expense_model.get_expenses_by_date_range(start_date, end_date)
        
        # حساب الإجماليات
        total_revenue = sum(sale['total_amount'] for sale in sales)
        total_profit = sum(sale['profit'] for sale in sales)
        total_final_amount = sum(sale['final_amount'] for sale in sales)
        total_expenses = sum(expense['amount'] for expense in expenses)
        
        net_profit = total_profit - total_expenses
        
        return {
            'period': f"{start_date} إلى {end_date}",
            'sales': {
                'total_sales': len(sales),
                'total_revenue': total_revenue,
                'total_profit': total_profit,
                'total_final_amount': total_final_amount
            },
            'expenses': {
                'total_expenses': total_expenses
            },
            'net_profit': net_profit,
            'sales_details': sales,
            'expenses_details': expenses
        }
    
    def generate_monthly_report(self, year, month):
        """إنشاء تقرير شهري"""
        start_date = f"{year}-{month:02d}-01"
        
        # حساب آخر يوم في الشهر
        if month == 12:
            next_month = f"{year + 1}-01-01"
        else:
            next_month = f"{year}-{month + 1:02d}-01"
        
        end_date = (datetime.strptime(next_month, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')
        
        # جلب المبيعات الشهرية
        sales = self.sale_model.get_sales_by_date_range(start_date, end_date)
        
        # جلب المصروفات الشهرية
        expenses = self.expense_model.get_expenses_by_date_range(start_date, end_date)
        
        # حساب الإجماليات
        total_revenue = sum(sale['total_amount'] for sale in sales)
        total_profit = sum(sale['profit'] for sale in sales)
        total_final_amount = sum(sale['final_amount'] for sale in sales)
        total_expenses = sum(expense['amount'] for expense in expenses)
        
        net_profit = total_profit - total_expenses
        
        return {
            'period': f"{year}/{month:02d}",
            'sales': {
                'total_sales': len(sales),
                'total_revenue': total_revenue,
                'total_profit': total_profit,
                'total_final_amount': total_final_amount
            },
            'expenses': {
                'total_expenses': total_expenses
            },
            'net_profit': net_profit,
            'sales_details': sales,
            'expenses_details': expenses
        }
    
    def generate_product_report(self):
        """تقرير المنتجات والمخزون"""
        products = self.product_model.get_all_products()
        
        low_stock_products = []
        out_of_stock_products = []
        
        for product in products:
            if product['stock_quantity'] == 0:
                out_of_stock_products.append(product)
            elif product['stock_quantity'] <= 5:  # حد أدنى للمخزون
                low_stock_products.append(product)
        
        return {
            'total_products': len(products),
            'low_stock_products': low_stock_products,
            'out_of_stock_products': out_of_stock_products,
            'all_products': products
        }

class BackupManager:
    """فئة إدارة النسخ الاحتياطية"""
    
    def __init__(self, db_name="store_management.db"):
        self.db_name = db_name
        self.backup_dir = "backups"
        self.ensure_backup_directory()
    
    def ensure_backup_directory(self):
        """التأكد من وجود مجلد النسخ الاحتياطية"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
    
    def create_backup(self, backup_name=None):
        """إنشاء نسخة احتياطية"""
        if backup_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"backup_{timestamp}.db"
        
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        try:
            shutil.copy2(self.db_name, backup_path)
            return backup_path
        except Exception as e:
            print(f"خطأ في إنشاء النسخة الاحتياطية: {e}")
            return None
    
    def restore_backup(self, backup_path):
        """استعادة نسخة احتياطية"""
        try:
            if os.path.exists(backup_path):
                shutil.copy2(backup_path, self.db_name)
                return True
            return False
        except Exception as e:
            print(f"خطأ في استعادة النسخة الاحتياطية: {e}")
            return False
    
    def list_backups(self):
        """قائمة النسخ الاحتياطية المتاحة"""
        if not os.path.exists(self.backup_dir):
            return []
        
        backups = []
        for file in os.listdir(self.backup_dir):
            if file.endswith('.db'):
                file_path = os.path.join(self.backup_dir, file)
                file_stat = os.stat(file_path)
                backups.append({
                    'name': file,
                    'path': file_path,
                    'size': file_stat.st_size,
                    'created': datetime.fromtimestamp(file_stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
                })
        
        return sorted(backups, key=lambda x: x['created'], reverse=True)
    
    def auto_backup(self):
        """نسخ احتياطي تلقائي"""
        return self.create_backup()

class ValidationUtils:
    """فئة للتحقق من صحة البيانات"""
    
    @staticmethod
    def validate_price(price):
        """التحقق من صحة السعر"""
        try:
            price = float(price)
            return price >= 0
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_quantity(quantity):
        """التحقق من صحة الكمية"""
        try:
            quantity = int(quantity)
            return quantity >= 0
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_discount_percentage(percentage):
        """التحقق من صحة نسبة الخصم"""
        try:
            percentage = float(percentage)
            return 0 <= percentage <= 100
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_required_field(value):
        """التحقق من الحقول المطلوبة"""
        return value is not None and str(value).strip() != ""
