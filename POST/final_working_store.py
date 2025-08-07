#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام إدارة المتجر النهائي - Final Store Management System
إصدار محسن ومبسط - Enhanced and Simplified Version
"""

import http.server
import socketserver
import webbrowser
import threading
import time
import json
import urllib.parse
import sqlite3
import os
import sys

# إعداد الترميز
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class StoreDatabase:
    """فئة إدارة قاعدة البيانات"""
    
    def __init__(self, db_name="store_final.db"):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """إنشاء قاعدة البيانات والجداول"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # جدول المنتجات
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    cost_price REAL NOT NULL,
                    sell_price REAL NOT NULL,
                    quantity INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            print("✓ Database initialized successfully")
            
        except Exception as e:
            print(f"✗ Database error: {e}")
            raise
    
    def add_product(self, name, cost_price, sell_price, quantity):
        """إضافة منتج جديد"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO products (name, cost_price, sell_price, quantity) VALUES (?, ?, ?, ?)",
                (name, float(cost_price), float(sell_price), int(quantity))
            )
            
            conn.commit()
            conn.close()
            print(f"✓ Product added: {name}")
            return True
            
        except Exception as e:
            print(f"✗ Add product error: {e}")
            return False
    
    def get_products(self):
        """الحصول على جميع المنتجات"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM products ORDER BY id DESC")
            products = []
            
            for row in cursor.fetchall():
                products.append({
                    'id': row[0],
                    'name': row[1],
                    'cost_price': row[2],
                    'sell_price': row[3],
                    'quantity': row[4],
                    'profit_per_unit': row[3] - row[2],
                    'total_profit': (row[3] - row[2]) * row[4]
                })
            
            conn.close()
            print(f"✓ Retrieved {len(products)} products")
            return products
            
        except Exception as e:
            print(f"✗ Get products error: {e}")
            return []

class StoreHandler(http.server.SimpleHTTPRequestHandler):
    """معالج طلبات HTTP"""
    
    def __init__(self, *args, **kwargs):
        self.db = StoreDatabase()
        super().__init__(*args, **kwargs)
    
    def log_message(self, format, *args):
        """تسجيل الطلبات"""
        print(f"[{self.address_string()}] {format % args}")
    
    def do_GET(self):
        """معالجة طلبات GET"""
        try:
            if self.path == '/' or self.path == '/index.html':
                self.send_main_page()
            elif self.path == '/products':
                self.send_products_page()
            elif self.path == '/api/products':
                self.send_products_api()
            else:
                self.send_error(404, "Page not found")
        except Exception as e:
            print(f"✗ GET error: {e}")
            self.send_error(500, f"Server error: {e}")
    
    def do_POST(self):
        """معالجة طلبات POST"""
        try:
            if self.path == '/api/add_product':
                self.handle_add_product()
            else:
                self.send_error(404, "Endpoint not found")
        except Exception as e:
            print(f"✗ POST error: {e}")
            self.send_error(500, f"Server error: {e}")
    
    def send_main_page(self):
        """إرسال الصفحة الرئيسية"""
        html = '''<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>نظام إدارة المتجر</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: rgba(255,255,255,0.1);
            padding: 40px;
            border-radius: 20px;
            backdrop-filter: blur(15px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
        h1 {
            text-align: center;
            font-size: 3em;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .status {
            background: rgba(0,255,0,0.2);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            margin: 30px 0;
            font-size: 1.2em;
            border: 2px solid rgba(0,255,0,0.3);
        }
        .menu {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 25px;
            margin-top: 40px;
        }
        .menu-item {
            background: rgba(255,255,255,0.15);
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 2px solid rgba(255,255,255,0.2);
            text-decoration: none;
            color: white;
        }
        .menu-item:hover {
            background: rgba(255,255,255,0.25);
            transform: translateY(-10px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        }
        .menu-item h3 {
            font-size: 1.5em;
            margin-bottom: 15px;
        }
        .menu-item p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        .footer {
            text-align: center;
            margin-top: 40px;
            opacity: 0.8;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏪 نظام إدارة المتجر</h1>
        
        <div class="status">
            ✅ النظام يعمل بنجاح!
            <br>
            <small>System is running successfully!</small>
        </div>
        
        <div class="menu">
            <a href="/products" class="menu-item">
                <h3>📦 إدارة المنتجات</h3>
                <p>إضافة وعرض المنتجات والمخزون</p>
            </a>
            
            <div class="menu-item" onclick="alert('هذه الميزة قيد التطوير!')">
                <h3>💰 إدارة المبيعات</h3>
                <p>تسجيل المبيعات والفواتير</p>
            </div>
            
            <div class="menu-item" onclick="alert('هذه الميزة قيد التطوير!')">
                <h3>📊 التقارير</h3>
                <p>تقارير الأرباح والمبيعات</p>
            </div>
            
            <div class="menu-item" onclick="alert('هذه الميزة قيد التطوير!')">
                <h3>⚙️ الإعدادات</h3>
                <p>إعدادات النظام والمتجر</p>
            </div>
        </div>
        
        <div class="footer">
            <p>نظام إدارة المتجر - الإصدار النهائي</p>
            <p>Store Management System - Final Version</p>
        </div>
    </div>
</body>
</html>'''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
        print("✓ Main page sent")
    
    def send_products_page(self):
        """إرسال صفحة إدارة المنتجات"""
        html = '''<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>إدارة المنتجات</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f8f9fa;
            padding: 20px;
            line-height: 1.6;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #e9ecef;
        }
        h1 {
            color: #333;
            font-size: 2.5em;
        }
        .back-btn {
            background: #6c757d;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            text-decoration: none;
            transition: background 0.3s;
        }
        .back-btn:hover { background: #5a6268; }
        
        .form-section {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #333;
        }
        input {
            width: 100%;
            padding: 12px;
            border: 2px solid #dee2e6;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input:focus {
            outline: none;
            border-color: #007bff;
        }
        .btn {
            background: #007bff;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            transition: background 0.3s;
        }
        .btn:hover { background: #0056b3; }
        
        .message {
            padding: 15px;
            margin: 15px 0;
            border-radius: 8px;
            font-weight: bold;
        }
        .success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .table-section {
            margin-top: 30px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        th, td {
            padding: 15px;
            text-align: center;
            border-bottom: 1px solid #dee2e6;
        }
        th {
            background: #007bff;
            color: white;
            font-weight: bold;
        }
        tr:hover {
            background: #f8f9fa;
        }
        .profit-positive { color: #28a745; font-weight: bold; }
        .profit-negative { color: #dc3545; font-weight: bold; }
        
        @media (max-width: 768px) {
            .container { padding: 15px; }
            h1 { font-size: 2em; }
            table { font-size: 14px; }
            th, td { padding: 10px 5px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📦 إدارة المنتجات</h1>
            <a href="/" class="back-btn">🏠 العودة للرئيسية</a>
        </div>
        
        <div id="message"></div>
        
        <div class="form-section">
            <h3 style="margin-bottom: 20px; color: #333;">➕ إضافة منتج جديد</h3>
            <form id="productForm">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;">
                    <div class="form-group">
                        <label>اسم المنتج:</label>
                        <input type="text" id="name" required placeholder="أدخل اسم المنتج">
                    </div>
                    <div class="form-group">
                        <label>سعر التكلفة (ريال):</label>
                        <input type="number" id="cost_price" step="0.01" required placeholder="0.00">
                    </div>
                    <div class="form-group">
                        <label>سعر البيع (ريال):</label>
                        <input type="number" id="sell_price" step="0.01" required placeholder="0.00">
                    </div>
                    <div class="form-group">
                        <label>الكمية:</label>
                        <input type="number" id="quantity" required placeholder="0">
                    </div>
                </div>
                <button type="submit" class="btn">➕ إضافة المنتج</button>
            </form>
        </div>
        
        <div class="table-section">
            <h3 style="margin-bottom: 20px; color: #333;">📋 قائمة المنتجات</h3>
            <table>
                <thead>
                    <tr>
                        <th>الرقم</th>
                        <th>اسم المنتج</th>
                        <th>سعر التكلفة</th>
                        <th>سعر البيع</th>
                        <th>الكمية</th>
                        <th>ربح الوحدة</th>
                        <th>إجمالي الربح</th>
                    </tr>
                </thead>
                <tbody id="productsBody">
                    <tr><td colspan="7">جاري تحميل المنتجات...</td></tr>
                </tbody>
            </table>
        </div>
    </div>
    
    <script>
        function showMessage(text, isError = false) {
            const messageDiv = document.getElementById('message');
            messageDiv.innerHTML = `<div class="message ${isError ? 'error' : 'success'}">${text}</div>`;
            setTimeout(() => messageDiv.innerHTML = '', 4000);
        }
        
        function loadProducts() {
            fetch('/api/products')
                .then(response => response.json())
                .then(products => {
                    const tbody = document.getElementById('productsBody');
                    if (products.length === 0) {
                        tbody.innerHTML = '<tr><td colspan="7">لا توجد منتجات. أضف منتجات جديدة!</td></tr>';
                    } else {
                        tbody.innerHTML = '';
                        products.forEach(product => {
                            const profitClass = product.profit_per_unit >= 0 ? 'profit-positive' : 'profit-negative';
                            tbody.innerHTML += `
                                <tr>
                                    <td>${product.id}</td>
                                    <td><strong>${product.name}</strong></td>
                                    <td>${product.cost_price.toFixed(2)} ريال</td>
                                    <td>${product.sell_price.toFixed(2)} ريال</td>
                                    <td>${product.quantity}</td>
                                    <td class="${profitClass}">${product.profit_per_unit.toFixed(2)} ريال</td>
                                    <td class="${profitClass}">${product.total_profit.toFixed(2)} ريال</td>
                                </tr>
                            `;
                        });
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    document.getElementById('productsBody').innerHTML = '<tr><td colspan="7">خطأ في تحميل المنتجات</td></tr>';
                });
        }
        
        document.getElementById('productForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData();
            formData.append('name', document.getElementById('name').value);
            formData.append('cost_price', document.getElementById('cost_price').value);
            formData.append('sell_price', document.getElementById('sell_price').value);
            formData.append('quantity', document.getElementById('quantity').value);
            
            fetch('/api/add_product', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                    showMessage('✅ تم إضافة المنتج بنجاح!');
                    document.getElementById('productForm').reset();
                    loadProducts();
                } else {
                    showMessage('❌ خطأ: ' + result.error, true);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showMessage('❌ خطأ في إضافة المنتج', true);
            });
        });
        
        // تحميل المنتجات عند تحميل الصفحة
        loadProducts();
    </script>
</body>
</html>'''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
        print("✓ Products page sent")
    
    def send_products_api(self):
        """إرسال بيانات المنتجات كـ JSON"""
        try:
            products = self.db.get_products()
            self.send_json(products)
        except Exception as e:
            print(f"✗ Products API error: {e}")
            self.send_json({"error": str(e)}, 500)
    
    def handle_add_product(self):
        """معالجة إضافة منتج جديد"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = urllib.parse.parse_qs(post_data.decode('utf-8'))
            
            name = data['name'][0].strip()
            cost_price = float(data['cost_price'][0])
            sell_price = float(data['sell_price'][0])
            quantity = int(data['quantity'][0])
            
            # التحقق من صحة البيانات
            if not name:
                raise ValueError("اسم المنتج مطلوب")
            if cost_price < 0:
                raise ValueError("سعر التكلفة لا يمكن أن يكون سالباً")
            if sell_price < 0:
                raise ValueError("سعر البيع لا يمكن أن يكون سالباً")
            if quantity < 0:
                raise ValueError("الكمية لا يمكن أن تكون سالبة")
            
            success = self.db.add_product(name, cost_price, sell_price, quantity)
            
            if success:
                self.send_json({"success": True, "message": "تم إضافة المنتج بنجاح"})
            else:
                self.send_json({"success": False, "error": "فشل في إضافة المنتج"}, 400)
            
        except ValueError as e:
            self.send_json({"success": False, "error": str(e)}, 400)
        except Exception as e:
            print(f"✗ Add product error: {e}")
            self.send_json({"success": False, "error": f"خطأ في الخادم: {e}"}, 500)
    
    def send_json(self, data, status=200):
        """إرسال استجابة JSON"""
        self.send_response(status)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8'))

def start_server():
    """بدء تشغيل الخادم"""
    PORT = 8080
    
    print("=" * 60)
    print("🏪 نظام إدارة المتجر النهائي")
    print("Final Store Management System")
    print("=" * 60)
    
    try:
        # التحقق من توفر المنفذ
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', PORT))
        sock.close()
        
        if result == 0:
            print(f"⚠️ المنفذ {PORT} مستخدم حالياً!")
            print("يرجى إغلاق أي تطبيقات أخرى تستخدم هذا المنفذ.")
            input("اضغط Enter للمحاولة مرة أخرى...")
            return False
        
        # بدء الخادم
        with socketserver.TCPServer(("", PORT), StoreHandler) as httpd:
            print(f"✅ تم بدء الخادم بنجاح!")
            print(f"🌐 الرابط: http://localhost:{PORT}")
            print(f"📱 يمكنك الوصول من أي جهاز في الشبكة المحلية")
            print("🔄 سيتم فتح المتصفح تلقائياً...")
            print("⏹️ اضغط Ctrl+C لإيقاف الخادم")
            print("=" * 60)
            
            # فتح المتصفح تلقائياً
            def open_browser():
                time.sleep(2)
                try:
                    webbrowser.open(f'http://localhost:{PORT}')
                    print("✅ تم فتح المتصفح")
                except Exception as e:
                    print(f"⚠️ لم يتم فتح المتصفح تلقائياً: {e}")
                    print(f"يرجى فتح المتصفح والذهاب إلى: http://localhost:{PORT}")
            
            threading.Thread(target=open_browser, daemon=True).start()
            
            # تشغيل الخادم
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n✅ تم إيقاف الخادم بواسطة المستخدم")
        return True
    except Exception as e:
        print(f"❌ خطأ في الخادم: {e}")
        return False

if __name__ == "__main__":
    try:
        success = start_server()
        if not success:
            print("فشل في بدء الخادم")
    except Exception as e:
        print(f"خطأ غير متوقع: {e}")
    finally:
        input("اضغط Enter للخروج...")
