import sqlite3
import os
from datetime import datetime
import shutil

class Database:
    def __init__(self, db_name="store_management.db"):
        self.db_name = db_name
        self.connection = None
        self.create_database()
    
    def connect(self):
        """إنشاء اتصال بقاعدة البيانات"""
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.connection.row_factory = sqlite3.Row  # للحصول على النتائج كقاموس
            return self.connection
        except sqlite3.Error as e:
            print(f"خطأ في الاتصال بقاعدة البيانات: {e}")
            return None
    
    def disconnect(self):
        """قطع الاتصال بقاعدة البيانات"""
        if self.connection:
            self.connection.close()
    
    def create_database(self):
        """إنشاء قاعدة البيانات والجداول"""
        conn = self.connect()
        if conn:
            try:
                cursor = conn.cursor()
                
                # إنشاء جدول الفئات
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS categories (
                        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        category_name TEXT NOT NULL UNIQUE,
                        description TEXT
                    )
                ''')
                
                # إنشاء جدول الموردين
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS suppliers (
                        supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        supplier_name TEXT NOT NULL,
                        contact_info TEXT
                    )
                ''')
                
                # إنشاء جدول العملاء
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS customers (
                        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        contact_info TEXT,
                        purchase_history TEXT
                    )
                ''')
                
                # إنشاء جدول المنتجات
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS products (
                        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        description TEXT,
                        selling_price REAL NOT NULL,
                        purchasing_price REAL NOT NULL,
                        stock_quantity INTEGER NOT NULL DEFAULT 0,
                        discount_percentage REAL DEFAULT 0,
                        manual_discount REAL DEFAULT 0,
                        category_id INTEGER,
                        supplier_id INTEGER,
                        invoice_number TEXT,
                        FOREIGN KEY (category_id) REFERENCES categories (category_id),
                        FOREIGN KEY (supplier_id) REFERENCES suppliers (supplier_id)
                    )
                ''')
                
                # إنشاء جدول المبيعات
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS sales (
                        sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        customer_id INTEGER,
                        date TEXT NOT NULL,
                        total_amount REAL NOT NULL,
                        profit REAL NOT NULL,
                        final_amount REAL NOT NULL,
                        FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
                    )
                ''')
                
                # إنشاء جدول تفاصيل البيع
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS sale_details (
                        sale_detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        sale_id INTEGER NOT NULL,
                        product_id INTEGER NOT NULL,
                        quantity INTEGER NOT NULL,
                        selling_price REAL NOT NULL,
                        purchasing_price REAL NOT NULL,
                        discount_applied REAL DEFAULT 0,
                        manual_discount REAL DEFAULT 0,
                        final_price REAL NOT NULL,
                        FOREIGN KEY (sale_id) REFERENCES sales (sale_id),
                        FOREIGN KEY (product_id) REFERENCES products (product_id)
                    )
                ''')
                
                # إنشاء جدول المصروفات
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS expenses (
                        expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        description TEXT NOT NULL,
                        amount REAL NOT NULL,
                        date TEXT NOT NULL
                    )
                ''')

                # إنشاء جدول استعلامات المنتجات
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS product_queries (
                        query_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        customer_id INTEGER,
                        product_name TEXT NOT NULL,
                        price REAL NOT NULL,
                        quantity INTEGER DEFAULT 1,
                        notes TEXT,
                        query_date TEXT NOT NULL,
                        executed BOOLEAN DEFAULT FALSE,
                        FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
                    )
                ''')

                # إنشاء جدول الفواتير (للاستعلام)
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS invoices (
                        invoice_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        sale_id INTEGER NOT NULL,
                        invoice_number TEXT UNIQUE NOT NULL,
                        customer_name TEXT,
                        issue_date TEXT NOT NULL,
                        total_amount REAL NOT NULL,
                        status TEXT DEFAULT 'active',
                        FOREIGN KEY (sale_id) REFERENCES sales (sale_id)
                    )
                ''')
                
                conn.commit()
                print("تم إنشاء قاعدة البيانات والجداول بنجاح")
                
                # إضافة بيانات تجريبية
                self.insert_sample_data(cursor)
                conn.commit()
                
            except sqlite3.Error as e:
                print(f"خطأ في إنشاء الجداول: {e}")
            finally:
                self.disconnect()
    
    def insert_sample_data(self, cursor):
        """إضافة بيانات تجريبية"""
        try:
            # إضافة فئات تجريبية
            categories = [
                ("إلكترونيات", "أجهزة إلكترونية ومعدات"),
                ("ملابس", "ملابس رجالية ونسائية"),
                ("طعام", "مواد غذائية ومشروبات")
            ]
            cursor.executemany("INSERT OR IGNORE INTO categories (category_name, description) VALUES (?, ?)", categories)
            
            # إضافة موردين تجريبيين
            suppliers = [
                ("شركة التقنية المتقدمة", "01234567890 - tech@example.com"),
                ("مصنع الملابس الحديث", "01234567891 - clothes@example.com"),
                ("مؤسسة الغذاء الطازج", "01234567892 - food@example.com")
            ]
            cursor.executemany("INSERT OR IGNORE INTO suppliers (supplier_name, contact_info) VALUES (?, ?)", suppliers)
            
            print("تم إضافة البيانات التجريبية بنجاح")
            
        except sqlite3.Error as e:
            print(f"خطأ في إضافة البيانات التجريبية: {e}")
    
    def backup_database(self, backup_path=None):
        """إنشاء نسخة احتياطية من قاعدة البيانات"""
        if backup_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"backup_{timestamp}_{self.db_name}"
        
        try:
            shutil.copy2(self.db_name, backup_path)
            print(f"تم إنشاء نسخة احتياطية: {backup_path}")
            return backup_path
        except Exception as e:
            print(f"خطأ في إنشاء النسخة الاحتياطية: {e}")
            return None
    
    def restore_database(self, backup_path):
        """استعادة قاعدة البيانات من نسخة احتياطية"""
        try:
            if os.path.exists(backup_path):
                shutil.copy2(backup_path, self.db_name)
                print(f"تم استعادة قاعدة البيانات من: {backup_path}")
                return True
            else:
                print("ملف النسخة الاحتياطية غير موجود")
                return False
        except Exception as e:
            print(f"خطأ في استعادة قاعدة البيانات: {e}")
            return False

    def add_product(self, name, cost_price, sell_price, quantity):
        """إضافة منتج جديد"""
        conn = self.connect()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO products (name, purchasing_price, selling_price, stock_quantity)
                    VALUES (?, ?, ?, ?)
                ''', (name, cost_price, sell_price, quantity))
                conn.commit()
                print(f"تم إضافة المنتج: {name}")
                return cursor.lastrowid
            except sqlite3.Error as e:
                print(f"خطأ في إضافة المنتج: {e}")
                return None
            finally:
                self.disconnect()

    def get_all_products(self):
        """الحصول على جميع المنتجات"""
        conn = self.connect()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT product_id as id, name, purchasing_price as cost_price,
                           selling_price as sell_price, stock_quantity as quantity
                    FROM products
                    ORDER BY name
                ''')
                products = []
                for row in cursor.fetchall():
                    products.append({
                        'id': row['id'],
                        'name': row['name'],
                        'cost_price': row['cost_price'],
                        'sell_price': row['sell_price'],
                        'quantity': row['quantity']
                    })
                return products
            except sqlite3.Error as e:
                print(f"خطأ في جلب المنتجات: {e}")
                return []
            finally:
                self.disconnect()
        return []

    def add_sale(self, customer_id, products_sold, total_amount, profit):
        """إضافة عملية بيع"""
        conn = self.connect()
        if conn:
            try:
                cursor = conn.cursor()

                # إضافة البيع الرئيسي
                cursor.execute('''
                    INSERT INTO sales (customer_id, date, total_amount, profit, final_amount)
                    VALUES (?, ?, ?, ?, ?)
                ''', (customer_id, datetime.now().isoformat(), total_amount, profit, total_amount))

                sale_id = cursor.lastrowid

                # إضافة تفاصيل البيع
                for product in products_sold:
                    cursor.execute('''
                        INSERT INTO sale_details (sale_id, product_id, quantity, selling_price,
                                                purchasing_price, final_price)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (sale_id, product['product_id'], product['quantity'],
                          product['selling_price'], product['purchasing_price'],
                          product['final_price']))

                    # تحديث المخزون
                    cursor.execute('''
                        UPDATE products
                        SET stock_quantity = stock_quantity - ?
                        WHERE product_id = ?
                    ''', (product['quantity'], product['product_id']))

                conn.commit()
                print(f"تم تسجيل البيع رقم: {sale_id}")
                return sale_id

            except sqlite3.Error as e:
                print(f"خطأ في تسجيل البيع: {e}")
                return None
            finally:
                self.disconnect()
        return None

# إنشاء مثيل من قاعدة البيانات
db = Database()
