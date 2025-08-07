import http.server
import socketserver
import webbrowser
import threading
import time
import json
import urllib.parse
import sqlite3

class StoreDB:
    def __init__(self):
        self.db_name = "store_system.db"
        self.init_db()
    
    def init_db(self):
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
    
    def add_product(self, name, cost_price, sell_price, quantity):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products (name, cost_price, sell_price, quantity) VALUES (?, ?, ?, ?)",
            (name, cost_price, sell_price, quantity)
        )
        conn.commit()
        conn.close()
    
    def get_products(self):
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def get_db(self):
        if not hasattr(self, '_db'):
            self._db = StoreDB()
        return self._db
    
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_main_page()
        elif self.path == '/products':
            self.send_products_page()
        elif self.path == '/api/products':
            self.send_products_api()
        else:
            self.send_error(404)
    
    def do_POST(self):
        if self.path == '/api/add_product':
            self.add_product()
        else:
            self.send_error(404)
    
    def send_main_page(self):
        html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Store Management System</title>
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
        .status {
            background: rgba(0,255,0,0.2);
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            margin-bottom: 20px;
            font-size: 18px;
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
    </style>
</head>
<body>
    <div class="container">
        <h1>🏪 Store Management System</h1>
        
        <div class="status">
            ✅ System is running successfully!
        </div>
        
        <div class="menu">
            <div class="menu-item" onclick="location.href='/products'">
                <h3>📦 Products</h3>
                <p>Manage products and inventory</p>
            </div>
            
            <div class="menu-item" onclick="alert('Feature coming soon!')">
                <h3>💰 Sales</h3>
                <p>Record sales transactions</p>
            </div>
            
            <div class="menu-item" onclick="alert('Feature coming soon!')">
                <h3>📊 Reports</h3>
                <p>View profit and sales reports</p>
            </div>
        </div>
    </div>
</body>
</html>'''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def send_products_page(self):
        html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Product Management</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1000px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }
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
        .success { color: green; font-weight: bold; }
        .error { color: red; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <button class="back-btn" onclick="location.href='/'">🏠 Back to Home</button>
        
        <h1>📦 Product Management</h1>
        
        <div id="message"></div>
        
        <form id="productForm">
            <div class="form-group">
                <label>Product Name:</label>
                <input type="text" id="name" required>
            </div>
            <div class="form-group">
                <label>Cost Price ($):</label>
                <input type="number" id="cost_price" step="0.01" required>
            </div>
            <div class="form-group">
                <label>Sell Price ($):</label>
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
                <tr><td colspan="6">Loading products...</td></tr>
            </tbody>
        </table>
    </div>
    
    <script>
        function showMessage(text, isError = false) {
            const messageDiv = document.getElementById('message');
            messageDiv.innerHTML = `<div class="${isError ? 'error' : 'success'}">${text}</div>`;
            setTimeout(() => messageDiv.innerHTML = '', 3000);
        }
        
        function loadProducts() {
            fetch('/api/products')
                .then(response => response.json())
                .then(products => {
                    const tbody = document.getElementById('productsBody');
                    if (products.length === 0) {
                        tbody.innerHTML = '<tr><td colspan="6">No products found. Add some products!</td></tr>';
                    } else {
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
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    document.getElementById('productsBody').innerHTML = '<tr><td colspan="6">Error loading products</td></tr>';
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
                    showMessage('✅ Product added successfully!');
                    document.getElementById('productForm').reset();
                    loadProducts();
                } else {
                    showMessage('❌ Error: ' + result.error, true);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showMessage('❌ Error adding product', true);
            });
        });
        
        // Load products when page loads
        loadProducts();
    </script>
</body>
</html>'''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def send_products_api(self):
        try:
            products = self.get_db().get_products()
            self.send_json(products)
        except Exception as e:
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
            self.send_json({"success": False, "error": str(e)}, 400)
    
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def log_message(self, format, *args):
        pass  # Suppress log messages

def start_server():
    PORT = 8080
    
    try:
        with socketserver.TCPServer(("", PORT), StoreHandler) as httpd:
            def open_browser():
                time.sleep(1)
                webbrowser.open(f'http://localhost:{PORT}')
            
            threading.Thread(target=open_browser, daemon=True).start()
            httpd.serve_forever()
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    start_server()
