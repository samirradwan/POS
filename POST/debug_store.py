#!/usr/bin/env python3
import sys
import os

# Force UTF-8 output
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

print("=== Store Management System Debug ===")
print(f"Python version: {sys.version}")
print(f"Working directory: {os.getcwd()}")

try:
    import http.server
    import socketserver
    import webbrowser
    import threading
    import time
    import json
    import urllib.parse
    import sqlite3
    print("✓ All modules imported successfully")
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)

class StoreDB:
    def __init__(self):
        self.db_name = "debug_store.db"
        print(f"Initializing database: {self.db_name}")
        self.init_db()
    
    def init_db(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    cost_price REAL NOT NULL,
                    sell_price REAL NOT NULL,
                    quantity INTEGER NOT NULL
                )
            ''')
            
            conn.commit()
            conn.close()
            print("✓ Database initialized successfully")
        except Exception as e:
            print(f"✗ Database error: {e}")
            raise
    
    def add_product(self, name, cost_price, sell_price, quantity):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO products (name, cost_price, sell_price, quantity) VALUES (?, ?, ?, ?)",
                (name, cost_price, sell_price, quantity)
            )
            conn.commit()
            conn.close()
            print(f"✓ Product added: {name}")
        except Exception as e:
            print(f"✗ Add product error: {e}")
            raise
    
    def get_products(self):
        try:
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
            print(f"✓ Retrieved {len(products)} products")
            return products
        except Exception as e:
            print(f"✗ Get products error: {e}")
            return []

class StoreHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def get_db(self):
        if not hasattr(self, '_db'):
            self._db = StoreDB()
        return self._db
    
    def log_message(self, format, *args):
        print(f"[{self.address_string()}] {format % args}")
    
    def do_GET(self):
        print(f"GET request: {self.path}")
        try:
            if self.path == '/' or self.path == '/index.html':
                self.send_main_page()
            elif self.path == '/products':
                self.send_products_page()
            elif self.path == '/api/products':
                self.send_products_api()
            else:
                self.send_error(404)
        except Exception as e:
            print(f"✗ GET error: {e}")
            self.send_error(500)
    
    def do_POST(self):
        print(f"POST request: {self.path}")
        try:
            if self.path == '/api/add_product':
                self.add_product()
            else:
                self.send_error(404)
        except Exception as e:
            print(f"✗ POST error: {e}")
            self.send_error(500)
    
    def send_main_page(self):
        html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Store Management System</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 50px; background: #f0f0f0; }
        .container { background: white; padding: 30px; border-radius: 10px; text-align: center; max-width: 600px; margin: 0 auto; }
        h1 { color: #333; margin-bottom: 30px; }
        .status { background: #d4edda; color: #155724; padding: 15px; border-radius: 5px; margin: 20px 0; }
        .menu { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 30px; }
        .menu-item { background: #007bff; color: white; padding: 20px; border-radius: 5px; cursor: pointer; transition: background 0.3s; }
        .menu-item:hover { background: #0056b3; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏪 Store Management System</h1>
        <div class="status">✅ System is running successfully!</div>
        <div class="menu">
            <div class="menu-item" onclick="location.href='/products'">
                <h3>📦 Products</h3>
                <p>Manage inventory</p>
            </div>
            <div class="menu-item" onclick="alert('Coming soon!')">
                <h3>💰 Sales</h3>
                <p>Record sales</p>
            </div>
        </div>
    </div>
</body>
</html>'''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
        print("✓ Main page sent")
    
    def send_products_page(self):
        html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Product Management</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }
        h1 { color: #333; text-align: center; }
        .form-group { margin: 15px 0; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; margin: 5px; }
        button:hover { background: #0056b3; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: center; }
        th { background: #f8f9fa; }
        .back-btn { background: #6c757d; }
    </style>
</head>
<body>
    <div class="container">
        <button class="back-btn" onclick="location.href='/'">🏠 Back to Home</button>
        
        <h1>📦 Product Management</h1>
        
        <form id="productForm">
            <div class="form-group">
                <label>Product Name:</label>
                <input type="text" id="name" required>
            </div>
            <div class="form-group">
                <label>Cost Price:</label>
                <input type="number" id="cost_price" step="0.01" required>
            </div>
            <div class="form-group">
                <label>Sell Price:</label>
                <input type="number" id="sell_price" step="0.01" required>
            </div>
            <div class="form-group">
                <label>Quantity:</label>
                <input type="number" id="quantity" required>
            </div>
            <button type="submit">➕ Add Product</button>
        </form>
        
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Product Name</th>
                    <th>Cost Price</th>
                    <th>Sell Price</th>
                    <th>Quantity</th>
                    <th>Expected Profit</th>
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
                                <td>$${product.cost_price}</td>
                                <td>$${product.sell_price}</td>
                                <td>${product.quantity}</td>
                                <td>$${profit.toFixed(2)}</td>
                            </tr>
                        `;
                    });
                })
                .catch(error => console.error('Error:', error));
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
                    alert('✅ Product added successfully!');
                    document.getElementById('productForm').reset();
                    loadProducts();
                } else {
                    alert('❌ Error: ' + result.error);
                }
            })
            .catch(error => console.error('Error:', error));
        });
        
        loadProducts();
    </script>
</body>
</html>'''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
        print("✓ Products page sent")
    
    def send_products_api(self):
        try:
            products = self.get_db().get_products()
            self.send_json(products)
        except Exception as e:
            print(f"✗ Products API error: {e}")
            self.send_json({"error": str(e)}, 500)
    
    def add_product(self):
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
            print(f"✗ Add product error: {e}")
            self.send_json({"success": False, "error": str(e)}, 400)
    
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

def start_server():
    PORT = 8080
    
    print(f"Starting server on port {PORT}...")
    
    try:
        # Test if port is available
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', PORT))
        sock.close()
        
        if result == 0:
            print(f"✗ Port {PORT} is already in use!")
            return False
        
        with socketserver.TCPServer(("", PORT), StoreHandler) as httpd:
            print(f"✓ Server started successfully on http://localhost:{PORT}")
            
            def open_browser():
                time.sleep(2)
                print("Opening browser...")
                try:
                    webbrowser.open(f'http://localhost:{PORT}')
                    print("✓ Browser opened")
                except Exception as e:
                    print(f"✗ Browser error: {e}")
            
            threading.Thread(target=open_browser, daemon=True).start()
            
            print("Server is running. Press Ctrl+C to stop.")
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n✓ Server stopped by user")
    except Exception as e:
        print(f"✗ Server error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = start_server()
    if not success:
        print("Failed to start server")
        input("Press Enter to exit...")
