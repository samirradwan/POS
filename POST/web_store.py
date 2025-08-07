#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام إدارة المتجر - إصدار ويب
"""

import http.server
import socketserver
import webbrowser
import threading
import time
import json
import urllib.parse
from database import Database

class StoreWebHandler(http.server.SimpleHTTPRequestHandler):
    """معالج طلبات الويب"""
    
    def __init__(self, *args, **kwargs):
        self.db = Database()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """معالجة طلبات GET"""
        if self.path == '/' or self.path == '/index.html':
            self.send_main_page()
        elif self.path == '/products':
            self.send_products_page()
        elif self.path == '/sales':
            self.send_sales_page()
        elif self.path == '/api/products':
            self.send_products_api()
        elif self.path == '/api/sales':
            self.send_sales_api()
        else:
            self.send_error(404)
    
    def do_POST(self):
        """معالجة طلبات POST"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        if self.path == '/api/add_product':
            self.add_product(post_data)
        elif self.path == '/api/add_sale':
            self.add_sale(post_data)
        else:
            self.send_error(404)
    
    def send_main_page(self):
        """إرسال الصفحة الرئيسية"""
        html = """
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏪 نظام إدارة المتجر</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
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
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .menu {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        .menu-item {
            background: rgba(255,255,255,0.2);
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }
        .menu-item:hover {
            background: rgba(255,255,255,0.3);
            border-color: white;
            transform: translateY(-5px);
        }
        .menu-item h3 {
            font-size: 1.5em;
            margin-bottom: 15px;
        }
        .menu-item p {
            opacity: 0.9;
        }
        .status {
            background: rgba(0,255,0,0.2);
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            margin-bottom: 20px;
            border: 1px solid rgba(0,255,0,0.5);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏪 نظام إدارة المتجر</h1>
        
        <div class="status">
            ✅ النظام يعمل بنجاح! - إصدار ويب
        </div>
        
        <div class="menu">
            <div class="menu-item" onclick="location.href='/products'">
                <h3>📦 إدارة المنتجات</h3>
                <p>إضافة وتعديل وحذف المنتجات</p>
            </div>
            
            <div class="menu-item" onclick="location.href='/sales'">
                <h3>💰 إدارة المبيعات</h3>
                <p>تسجيل المبيعات ومتابعة الأرباح</p>
            </div>
            
            <div class="menu-item" onclick="showReports()">
                <h3>📊 التقارير</h3>
                <p>تقارير المبيعات والأرباح</p>
            </div>
            
            <div class="menu-item" onclick="showExpenses()">
                <h3>💸 المصروفات</h3>
                <p>تسجيل ومتابعة المصروفات</p>
            </div>
            
            <div class="menu-item" onclick="showSuppliers()">
                <h3>🚚 الموردين</h3>
                <p>إدارة بيانات الموردين</p>
            </div>
            
            <div class="menu-item" onclick="showBackup()">
                <h3>💾 النسخ الاحتياطي</h3>
                <p>حفظ واستعادة البيانات</p>
            </div>
        </div>
    </div>
    
    <script>
        function showReports() {
            alert('📊 قريباً: صفحة التقارير');
        }
        
        function showExpenses() {
            alert('💸 قريباً: صفحة المصروفات');
        }
        
        function showSuppliers() {
            alert('🚚 قريباً: صفحة الموردين');
        }
        
        function showBackup() {
            alert('💾 قريباً: صفحة النسخ الاحتياطي');
        }
    </script>
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
        input, select { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
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
        // تحميل المنتجات
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
                });
        }
        
        // إضافة منتج
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
            });
        });
        
        // تحميل المنتجات عند فتح الصفحة
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
        """API للمنتجات"""
        try:
            products = self.db.get_all_products()
            self.send_json_response(products)
        except Exception as e:
            self.send_json_response({"error": str(e)}, 500)
    
    def add_product(self, post_data):
        """إضافة منتج جديد"""
        try:
            # تحليل البيانات
            data = urllib.parse.parse_qs(post_data.decode('utf-8'))
            
            name = data['name'][0]
            cost_price = float(data['cost_price'][0])
            sell_price = float(data['sell_price'][0])
            quantity = int(data['quantity'][0])
            
            # إضافة للقاعدة
            self.db.add_product(name, cost_price, sell_price, quantity)
            
            self.send_json_response({"success": True})
            
        except Exception as e:
            self.send_json_response({"success": False, "error": str(e)}, 400)
    
    def send_json_response(self, data, status=200):
        """إرسال استجابة JSON"""
        self.send_response(status)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

def start_web_server():
    """تشغيل الخادم"""
    PORT = 8080
    
    try:
        with socketserver.TCPServer(("", PORT), StoreWebHandler) as httpd:
            print(f"🌐 الخادم يعمل على: http://localhost:{PORT}")
            print("🚀 سيتم فتح المتصفح تلقائياً...")
            
            # فتح المتصفح بعد ثانية
            def open_browser():
                time.sleep(1)
                webbrowser.open(f'http://localhost:{PORT}')
            
            threading.Thread(target=open_browser, daemon=True).start()
            
            print("⏹️ اضغط Ctrl+C للإيقاف")
            httpd.serve_forever()
            
    except Exception as e:
        print(f"❌ خطأ في تشغيل الخادم: {e}")

if __name__ == "__main__":
    print("🏪 بدء تشغيل نظام إدارة المتجر - إصدار ويب")
    start_web_server()
