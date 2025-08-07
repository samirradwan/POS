#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام إدارة المتجر - إصدار ويب مبسط
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

class SimpleStoreDB:
    """قاعدة بيانات مبسطة"""
    
    def __init__(self):
        self.db_name = "simple_store.db"
        self.init_db()
    
    def init_db(self):
        """إنشاء قاعدة البيانات"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # جدول المنتجات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                cost_price REAL NOT NULL,
                sell_price REAL NOT NULL,
                quantity INTEGER NOT NULL
            )
        ''')
        
        # جدول المبيعات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                profit REAL NOT NULL,
                date TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ تم إنشاء قاعدة البيانات")
    
    def add_product(self, name, cost_price, sell_price, quantity):
        """إضافة منتج"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products (name, cost_price, sell_price, quantity) VALUES (?, ?, ?, ?)",
            (name, cost_price, sell_price, quantity)
        )
        conn.commit()
        conn.close()
    
    def get_products(self):
        """جلب المنتجات"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        products = []
        for row in cursor.fetchall():
            products.append({
                'id': row[0],
                'name': row[1],
                'cost_price': row[2],
                'sell_price': row[3],
                'quantity': row[4]
            })
        conn.close()
        return products

class StoreHandler(http.server.SimpleHTTPRequestHandler):
    """معالج الطلبات"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_db(self):
        """الحصول على قاعدة البيانات"""
        if not hasattr(self, '_db'):
            self._db = SimpleStoreDB()
        return self._db
    
    def do_GET(self):
        """معالجة GET"""
        if self.path == '/' or self.path == '/index.html':
            self.send_main_page()
        elif self.path == '/products':
            self.send_products_page()
        elif self.path == '/api/products':
            self.send_products_api()
        else:
            self.send_error(404)
    
    def do_POST(self):
        """معالجة POST"""
        if self.path == '/api/add_product':
            self.add_product()
        else:
            self.send_error(404)
    
    def send_main_page(self):
        """الصفحة الرئيسية"""
        html = """
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <title>🏪 نظام إدارة المتجر</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: rgba(255,255,255,0.1);
            padding: 30px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        h1 {
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 30px;
        }
        .menu {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }
        .menu-item {
            background: rgba(255,255,255,0.2);
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .menu-item:hover {
            background: rgba(255,255,255,0.3);
            transform: translateY(-5px);
        }
        .status {
            background: rgba(0,255,0,0.2);
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏪 نظام إدارة المتجر</h1>
        
        <div class="status">
            ✅ النظام يعمل بنجاح! - إصدار ويب مبسط
        </div>
        
        <div class="menu">
            <div class="menu-item" onclick="location.href='/products'">
                <h3>📦 المنتجات</h3>
                <p>إدارة المنتجات والمخزون</p>
            </div>
            
            <div class="menu-item" onclick="alert('قريباً!')">
                <h3>💰 المبيعات</h3>
                <p>تسجيل المبيعات</p>
            </div>
            
            <div class="menu-item" onclick="alert('قريباً!')">
                <h3>📊 التقارير</h3>
                <p>تقارير الأرباح</p>
            </div>
        </div>
    </div>
</body>
</html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def send_products_page(self):
        """صفحة المنتجات"""
        html = """
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <title>📦 إدارة المنتجات</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1000px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }
        h1 { color: #333; text-align: center; }
        .form-group { margin: 15px 0; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #0056b3; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: center; }
        th { background: #f8f9fa; }
        .back-btn { background: #6c757d; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <button class="back-btn" onclick="location.href='/'">🏠 العودة للرئيسية</button>
        
        <h1>📦 إدارة المنتجات</h1>
        
        <form id="productForm">
            <div class="form-group">
                <label>اسم المنتج:</label>
                <input type="text" id="name" required>
            </div>
            <div class="form-group">
                <label>سعر الشراء:</label>
                <input type="number" id="cost_price" step="0.01" required>
            </div>
            <div class="form-group">
                <label>سعر البيع:</label>
                <input type="number" id="sell_price" step="0.01" required>
            </div>
            <div class="form-group">
                <label>الكمية:</label>
                <input type="number" id="quantity" required>
            </div>
            <button type="submit">➕ إضافة منتج</button>
        </form>
        
        <table id="productsTable">
            <thead>
                <tr>
                    <th>الرقم</th>
                    <th>اسم المنتج</th>
                    <th>سعر الشراء</th>
                    <th>سعر البيع</th>
                    <th>الكمية</th>
                    <th>الربح المتوقع</th>
                </tr>
            </thead>
            <tbody id="productsBody">
            </tbody>
        </table>
    </div>
    
    <script>
        function loadProducts() {
            fetch('/api/products')
                .then(response => response.json())
                .then(products => {
                    const tbody = document.getElementById('productsBody');
                    tbody.innerHTML = '';
                    products.forEach(product => {
                        const profit = (product.sell_price - product.cost_price) * product.quantity;
                        tbody.innerHTML += `
                            <tr>
                                <td>${product.id}</td>
                                <td>${product.name}</td>
                                <td>${product.cost_price}</td>
                                <td>${product.sell_price}</td>
                                <td>${product.quantity}</td>
                                <td>${profit.toFixed(2)}</td>
                            </tr>
                        `;
                    });
                })
                .catch(error => {
                    console.error('خطأ:', error);
                    alert('خطأ في تحميل المنتجات');
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
                    alert('✅ تم إضافة المنتج بنجاح!');
                    document.getElementById('productForm').reset();
                    loadProducts();
                } else {
                    alert('❌ خطأ: ' + result.error);
                }
            })
            .catch(error => {
                console.error('خطأ:', error);
                alert('خطأ في إضافة المنتج');
            });
        });
        
        loadProducts();
    </script>
</body>
</html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def send_products_api(self):
        """API المنتجات"""
        try:
            products = self.get_db().get_products()
            self.send_json(products)
        except Exception as e:
            self.send_json({"error": str(e)}, 500)
    
    def add_product(self):
        """إضافة منتج"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = urllib.parse.parse_qs(post_data.decode('utf-8'))
            
            name = data['name'][0]
            cost_price = float(data['cost_price'][0])
            sell_price = float(data['sell_price'][0])
            quantity = int(data['quantity'][0])
            
            self.get_db().add_product(name, cost_price, sell_price, quantity)
            self.send_json({"success": True})
            
        except Exception as e:
            self.send_json({"success": False, "error": str(e)}, 400)
    
    def send_json(self, data, status=200):
        """إرسال JSON"""
        self.send_response(status)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

def start_server():
    """تشغيل الخادم"""
    PORT = 8080
    
    try:
        with socketserver.TCPServer(("", PORT), StoreHandler) as httpd:
            print(f"🌐 الخادم يعمل على: http://localhost:{PORT}")
            print("🚀 سيتم فتح المتصفح...")
            
            def open_browser():
                time.sleep(1)
                webbrowser.open(f'http://localhost:{PORT}')
            
            threading.Thread(target=open_browser, daemon=True).start()
            
            print("⏹️ اضغط Ctrl+C للإيقاف")
            httpd.serve_forever()
            
    except Exception as e:
        print(f"❌ خطأ: {e}")

if __name__ == "__main__":
    print("🏪 بدء تشغيل نظام إدارة المتجر المبسط")
    start_server()
