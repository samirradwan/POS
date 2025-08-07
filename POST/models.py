from database import Database
from datetime import datetime
import sqlite3

class BaseModel:
    """الفئة الأساسية لجميع النماذج"""
    def __init__(self):
        self.db = Database()
    
    def execute_query(self, query, params=None):
        """تنفيذ استعلام قاعدة البيانات"""
        conn = self.db.connect()
        if conn:
            try:
                cursor = conn.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                conn.commit()
                return cursor
            except sqlite3.Error as e:
                print(f"خطأ في تنفيذ الاستعلام: {e}")
                return None
            finally:
                self.db.disconnect()
        return None
    
    def fetch_all(self, query, params=None):
        """جلب جميع النتائج"""
        cursor = self.execute_query(query, params)
        if cursor:
            return cursor.fetchall()
        return []
    
    def fetch_one(self, query, params=None):
        """جلب نتيجة واحدة"""
        cursor = self.execute_query(query, params)
        if cursor:
            return cursor.fetchone()
        return None

class Category(BaseModel):
    """نموذج الفئات"""
    
    def add_category(self, name, description=""):
        """إضافة فئة جديدة"""
        query = "INSERT INTO categories (category_name, description) VALUES (?, ?)"
        cursor = self.execute_query(query, (name, description))
        return cursor.lastrowid if cursor else None
    
    def get_all_categories(self):
        """جلب جميع الفئات"""
        query = "SELECT * FROM categories ORDER BY category_name"
        return self.fetch_all(query)
    
    def get_category_by_id(self, category_id):
        """جلب فئة بالمعرف"""
        query = "SELECT * FROM categories WHERE category_id = ?"
        return self.fetch_one(query, (category_id,))
    
    def update_category(self, category_id, name, description=""):
        """تحديث فئة"""
        query = "UPDATE categories SET category_name = ?, description = ? WHERE category_id = ?"
        cursor = self.execute_query(query, (name, description, category_id))
        return cursor.rowcount > 0 if cursor else False
    
    def delete_category(self, category_id):
        """حذف فئة"""
        query = "DELETE FROM categories WHERE category_id = ?"
        cursor = self.execute_query(query, (category_id,))
        return cursor.rowcount > 0 if cursor else False

class Supplier(BaseModel):
    """نموذج الموردين"""
    
    def add_supplier(self, name, contact_info=""):
        """إضافة مورد جديد"""
        query = "INSERT INTO suppliers (supplier_name, contact_info) VALUES (?, ?)"
        cursor = self.execute_query(query, (name, contact_info))
        return cursor.lastrowid if cursor else None
    
    def get_all_suppliers(self):
        """جلب جميع الموردين"""
        query = "SELECT * FROM suppliers ORDER BY supplier_name"
        return self.fetch_all(query)
    
    def get_supplier_by_id(self, supplier_id):
        """جلب مورد بالمعرف"""
        query = "SELECT * FROM suppliers WHERE supplier_id = ?"
        return self.fetch_one(query, (supplier_id,))
    
    def update_supplier(self, supplier_id, name, contact_info=""):
        """تحديث مورد"""
        query = "UPDATE suppliers SET supplier_name = ?, contact_info = ? WHERE supplier_id = ?"
        cursor = self.execute_query(query, (name, contact_info, supplier_id))
        return cursor.rowcount > 0 if cursor else False
    
    def delete_supplier(self, supplier_id):
        """حذف مورد"""
        query = "DELETE FROM suppliers WHERE supplier_id = ?"
        cursor = self.execute_query(query, (supplier_id,))
        return cursor.rowcount > 0 if cursor else False

class Customer(BaseModel):
    """نموذج العملاء"""
    
    def add_customer(self, name, contact_info=""):
        """إضافة عميل جديد"""
        query = "INSERT INTO customers (name, contact_info) VALUES (?, ?)"
        cursor = self.execute_query(query, (name, contact_info))
        return cursor.lastrowid if cursor else None
    
    def get_all_customers(self):
        """جلب جميع العملاء"""
        query = "SELECT * FROM customers ORDER BY name"
        return self.fetch_all(query)
    
    def get_customer_by_id(self, customer_id):
        """جلب عميل بالمعرف"""
        query = "SELECT * FROM customers WHERE customer_id = ?"
        return self.fetch_one(query, (customer_id,))
    
    def update_customer(self, customer_id, name, contact_info=""):
        """تحديث عميل"""
        query = "UPDATE customers SET name = ?, contact_info = ? WHERE customer_id = ?"
        cursor = self.execute_query(query, (name, contact_info, customer_id))
        return cursor.rowcount > 0 if cursor else False
    
    def delete_customer(self, customer_id):
        """حذف عميل"""
        query = "DELETE FROM customers WHERE customer_id = ?"
        cursor = self.execute_query(query, (customer_id,))
        return cursor.rowcount > 0 if cursor else False

class Product(BaseModel):
    """نموذج المنتجات"""
    
    def add_product(self, name, description, selling_price, purchasing_price, 
                   stock_quantity, discount_percentage=0, manual_discount=0,
                   category_id=None, supplier_id=None, invoice_number=""):
        """إضافة منتج جديد"""
        query = """INSERT INTO products 
                   (name, description, selling_price, purchasing_price, stock_quantity,
                    discount_percentage, manual_discount, category_id, supplier_id, invoice_number)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        params = (name, description, selling_price, purchasing_price, stock_quantity,
                 discount_percentage, manual_discount, category_id, supplier_id, invoice_number)
        cursor = self.execute_query(query, params)
        return cursor.lastrowid if cursor else None
    
    def get_all_products(self):
        """جلب جميع المنتجات مع معلومات الفئة والمورد"""
        query = """SELECT p.*, c.category_name, s.supplier_name 
                   FROM products p
                   LEFT JOIN categories c ON p.category_id = c.category_id
                   LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
                   ORDER BY p.name"""
        return self.fetch_all(query)
    
    def get_product_by_id(self, product_id):
        """جلب منتج بالمعرف"""
        query = """SELECT p.*, c.category_name, s.supplier_name 
                   FROM products p
                   LEFT JOIN categories c ON p.category_id = c.category_id
                   LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
                   WHERE p.product_id = ?"""
        return self.fetch_one(query, (product_id,))
    
    def update_product(self, product_id, name, description, selling_price, purchasing_price,
                      stock_quantity, discount_percentage=0, manual_discount=0,
                      category_id=None, supplier_id=None, invoice_number=""):
        """تحديث منتج"""
        query = """UPDATE products SET 
                   name = ?, description = ?, selling_price = ?, purchasing_price = ?,
                   stock_quantity = ?, discount_percentage = ?, manual_discount = ?,
                   category_id = ?, supplier_id = ?, invoice_number = ?
                   WHERE product_id = ?"""
        params = (name, description, selling_price, purchasing_price, stock_quantity,
                 discount_percentage, manual_discount, category_id, supplier_id, 
                 invoice_number, product_id)
        cursor = self.execute_query(query, params)
        return cursor.rowcount > 0 if cursor else False
    
    def delete_product(self, product_id):
        """حذف منتج"""
        query = "DELETE FROM products WHERE product_id = ?"
        cursor = self.execute_query(query, (product_id,))
        return cursor.rowcount > 0 if cursor else False
    
    def update_stock(self, product_id, quantity_sold):
        """تحديث المخزون بعد البيع"""
        query = "UPDATE products SET stock_quantity = stock_quantity - ? WHERE product_id = ?"
        cursor = self.execute_query(query, (quantity_sold, product_id))
        return cursor.rowcount > 0 if cursor else False
    
    def calculate_discounted_price(self, selling_price, discount_percentage, manual_discount):
        """حساب السعر بعد الخصم"""
        # حساب الخصم بالنسبة المئوية
        percentage_discount = selling_price * (discount_percentage / 100)
        # السعر بعد الخصم النسبي والخصم اليدوي
        final_price = selling_price - percentage_discount - manual_discount
        return max(0, final_price)  # التأكد من أن السعر لا يكون سالباً

class Sale(BaseModel):
    """نموذج المبيعات"""

    def add_sale(self, customer_id, total_amount, profit, final_amount, sale_items):
        """إضافة عملية بيع جديدة مع تفاصيلها"""
        conn = self.db.connect()
        if conn:
            try:
                cursor = conn.cursor()

                # إضافة البيع الرئيسي
                sale_query = """INSERT INTO sales (customer_id, date, total_amount, profit, final_amount)
                               VALUES (?, ?, ?, ?, ?)"""
                cursor.execute(sale_query, (customer_id, datetime.now().isoformat(),
                                          total_amount, profit, final_amount))
                sale_id = cursor.lastrowid

                # إضافة تفاصيل البيع
                for item in sale_items:
                    detail_query = """INSERT INTO sale_details
                                     (sale_id, product_id, quantity, selling_price, purchasing_price,
                                      discount_applied, manual_discount, final_price)
                                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
                    cursor.execute(detail_query, (sale_id, item['product_id'], item['quantity'],
                                                item['selling_price'], item['purchasing_price'],
                                                item['discount_applied'], item['manual_discount'],
                                                item['final_price']))

                    # تحديث المخزون
                    update_stock_query = """UPDATE products SET stock_quantity = stock_quantity - ?
                                           WHERE product_id = ?"""
                    cursor.execute(update_stock_query, (item['quantity'], item['product_id']))

                conn.commit()

                # إنشاء فاتورة تلقائياً
                if sale_id:
                    try:
                        invoice_model = Invoice()
                        customer_name = "عميل عادي"
                        if customer_id:
                            customer = Customer().get_customer_by_id(customer_id)
                            if customer:
                                customer_name = customer['name']

                        invoice_model.create_invoice(sale_id, customer_name)
                    except Exception as e:
                        print(f"خطأ في إنشاء الفاتورة: {e}")

                return sale_id

            except sqlite3.Error as e:
                print(f"خطأ في إضافة البيع: {e}")
                conn.rollback()
                return None
            finally:
                self.db.disconnect()
        return None

    def get_all_sales(self):
        """جلب جميع المبيعات"""
        query = """SELECT s.*, c.name as customer_name
                   FROM sales s
                   LEFT JOIN customers c ON s.customer_id = c.customer_id
                   ORDER BY s.date DESC"""
        return self.fetch_all(query)

    def get_sale_by_id(self, sale_id):
        """جلب بيع بالمعرف مع تفاصيله"""
        sale_query = """SELECT s.*, c.name as customer_name
                       FROM sales s
                       LEFT JOIN customers c ON s.customer_id = c.customer_id
                       WHERE s.sale_id = ?"""
        sale = self.fetch_one(sale_query, (sale_id,))

        if sale:
            details_query = """SELECT sd.*, p.name as product_name
                              FROM sale_details sd
                              JOIN products p ON sd.product_id = p.product_id
                              WHERE sd.sale_id = ?"""
            details = self.fetch_all(details_query, (sale_id,))
            return {'sale': sale, 'details': details}
        return None

    def get_sales_by_date_range(self, start_date, end_date):
        """جلب المبيعات في فترة زمنية محددة"""
        query = """SELECT s.*, c.name as customer_name
                   FROM sales s
                   LEFT JOIN customers c ON s.customer_id = c.customer_id
                   WHERE DATE(s.date) BETWEEN ? AND ?
                   ORDER BY s.date DESC"""
        return self.fetch_all(query, (start_date, end_date))

    def get_daily_sales_report(self, date):
        """تقرير المبيعات اليومية"""
        query = """SELECT
                       COUNT(*) as total_sales,
                       SUM(total_amount) as total_revenue,
                       SUM(profit) as total_profit,
                       SUM(final_amount) as total_final_amount
                   FROM sales
                   WHERE DATE(date) = ?"""
        return self.fetch_one(query, (date,))

class Expense(BaseModel):
    """نموذج المصروفات"""

    def add_expense(self, description, amount, date=None):
        """إضافة مصروف جديد"""
        if date is None:
            date = datetime.now().isoformat()
        query = "INSERT INTO expenses (description, amount, date) VALUES (?, ?, ?)"
        cursor = self.execute_query(query, (description, amount, date))
        return cursor.lastrowid if cursor else None

    def get_all_expenses(self):
        """جلب جميع المصروفات"""
        query = "SELECT * FROM expenses ORDER BY date DESC"
        return self.fetch_all(query)

    def get_expense_by_id(self, expense_id):
        """جلب مصروف بالمعرف"""
        query = "SELECT * FROM expenses WHERE expense_id = ?"
        return self.fetch_one(query, (expense_id,))

    def update_expense(self, expense_id, description, amount, date):
        """تحديث مصروف"""
        query = "UPDATE expenses SET description = ?, amount = ?, date = ? WHERE expense_id = ?"
        cursor = self.execute_query(query, (description, amount, date, expense_id))
        return cursor.rowcount > 0 if cursor else False

    def delete_expense(self, expense_id):
        """حذف مصروف"""
        query = "DELETE FROM expenses WHERE expense_id = ?"
        cursor = self.execute_query(query, (expense_id,))
        return cursor.rowcount > 0 if cursor else False

    def get_expenses_by_date_range(self, start_date, end_date):
        """جلب المصروفات في فترة زمنية محددة"""
        query = """SELECT * FROM expenses
                   WHERE DATE(date) BETWEEN ? AND ?
                   ORDER BY date DESC"""
        return self.fetch_all(query, (start_date, end_date))

    def get_total_expenses_by_date(self, date):
        """جلب إجمالي المصروفات في تاريخ محدد"""
        query = "SELECT SUM(amount) as total FROM expenses WHERE DATE(date) = ?"
        result = self.fetch_one(query, (date,))
        return result['total'] if result and result['total'] else 0

class ProductQuery(BaseModel):
    """نموذج استعلامات المنتجات"""

    def add_query(self, customer_id, product_name, price, quantity=1, notes=""):
        """إضافة استعلام منتج جديد"""
        query = """INSERT INTO product_queries
                   (customer_id, product_name, price, quantity, notes, query_date)
                   VALUES (?, ?, ?, ?, ?, ?)"""
        cursor = self.execute_query(query, (customer_id, product_name, price,
                                          quantity, notes, datetime.now().isoformat()))
        return cursor.lastrowid if cursor else None

    def get_all_queries(self, executed=None):
        """جلب جميع الاستعلامات"""
        if executed is None:
            query = """SELECT pq.*, c.name as customer_name
                       FROM product_queries pq
                       LEFT JOIN customers c ON pq.customer_id = c.customer_id
                       ORDER BY pq.query_date DESC"""
            return self.fetch_all(query)
        else:
            query = """SELECT pq.*, c.name as customer_name
                       FROM product_queries pq
                       LEFT JOIN customers c ON pq.customer_id = c.customer_id
                       WHERE pq.executed = ?
                       ORDER BY pq.query_date DESC"""
            return self.fetch_all(query, (executed,))

    def get_query_by_id(self, query_id):
        """جلب استعلام بالمعرف"""
        query = """SELECT pq.*, c.name as customer_name
                   FROM product_queries pq
                   LEFT JOIN customers c ON pq.customer_id = c.customer_id
                   WHERE pq.query_id = ?"""
        return self.fetch_one(query, (query_id,))

    def mark_as_executed(self, query_id):
        """تحديد الاستعلام كمنفذ"""
        query = "UPDATE product_queries SET executed = TRUE WHERE query_id = ?"
        cursor = self.execute_query(query, (query_id,))
        return cursor.rowcount > 0 if cursor else False

    def delete_query(self, query_id):
        """حذف استعلام"""
        query = "DELETE FROM product_queries WHERE query_id = ?"
        cursor = self.execute_query(query, (query_id,))
        return cursor.rowcount > 0 if cursor else False

    def search_products(self, search_term):
        """البحث عن المنتجات"""
        query = """SELECT p.*, c.category_name, s.supplier_name
                   FROM products p
                   LEFT JOIN categories c ON p.category_id = c.category_id
                   LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
                   WHERE p.name LIKE ? OR p.description LIKE ? OR c.category_name LIKE ?
                   ORDER BY p.name"""
        search_pattern = f"%{search_term}%"
        return self.fetch_all(query, (search_pattern, search_pattern, search_pattern))

class Invoice(BaseModel):
    """نموذج الفواتير"""

    def create_invoice(self, sale_id, customer_name="عميل عادي"):
        """إنشاء فاتورة جديدة"""
        # جلب بيانات البيع
        sale = Sale().get_sale_by_id(sale_id)
        if not sale:
            return None

        # إنشاء رقم فاتورة فريد
        invoice_number = f"INV-{datetime.now().strftime('%Y%m%d')}-{sale_id:04d}"

        query = """INSERT INTO invoices
                   (sale_id, invoice_number, customer_name, issue_date, total_amount)
                   VALUES (?, ?, ?, ?, ?)"""
        cursor = self.execute_query(query, (sale_id, invoice_number, customer_name,
                                          datetime.now().isoformat(), sale['sale']['final_amount']))
        return cursor.lastrowid if cursor else None

    def get_invoice_by_number(self, invoice_number):
        """جلب فاتورة برقم الفاتورة"""
        query = """SELECT i.*, s.date as sale_date, s.total_amount, s.profit, s.final_amount
                   FROM invoices i
                   JOIN sales s ON i.sale_id = s.sale_id
                   WHERE i.invoice_number = ?"""
        invoice = self.fetch_one(query, (invoice_number,))

        if invoice:
            # جلب تفاصيل الفاتورة
            details_query = """SELECT sd.*, p.name as product_name
                              FROM sale_details sd
                              JOIN products p ON sd.product_id = p.product_id
                              WHERE sd.sale_id = ?"""
            details = self.fetch_all(details_query, (invoice['sale_id'],))
            return {'invoice': invoice, 'details': details}
        return None

    def get_invoice_by_id(self, invoice_id):
        """جلب فاتورة بالمعرف"""
        query = """SELECT i.*, s.date as sale_date, s.total_amount, s.profit, s.final_amount
                   FROM invoices i
                   JOIN sales s ON i.sale_id = s.sale_id
                   WHERE i.invoice_id = ?"""
        invoice = self.fetch_one(query, (invoice_id,))

        if invoice:
            # جلب تفاصيل الفاتورة
            details_query = """SELECT sd.*, p.name as product_name
                              FROM sale_details sd
                              JOIN products p ON sd.product_id = p.product_id
                              WHERE sd.sale_id = ?"""
            details = self.fetch_all(details_query, (invoice['sale_id'],))
            return {'invoice': invoice, 'details': details}
        return None

    def get_all_invoices(self):
        """جلب جميع الفواتير"""
        query = """SELECT i.*, s.date as sale_date
                   FROM invoices i
                   JOIN sales s ON i.sale_id = s.sale_id
                   ORDER BY i.issue_date DESC"""
        return self.fetch_all(query)

    def update_invoice_status(self, invoice_id, status):
        """تحديث حالة الفاتورة"""
        query = "UPDATE invoices SET status = ? WHERE invoice_id = ?"
        cursor = self.execute_query(query, (status, invoice_id))
        return cursor.rowcount > 0 if cursor else False
