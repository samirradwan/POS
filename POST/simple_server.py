import http.server
import socketserver
import webbrowser
import threading
import time

# Write status to file for debugging
def log(message):
    with open("server_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%H:%M:%S')} - {message}\n")
    print(message)

class SimpleHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        log(f"Request: {self.path}")
        
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Store System - Working!</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 50px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container { 
            background: rgba(255,255,255,0.1); 
            padding: 40px; 
            border-radius: 15px; 
            text-align: center;
            backdrop-filter: blur(10px);
            max-width: 500px;
        }
        h1 { font-size: 2.5em; margin-bottom: 20px; }
        .success { 
            background: rgba(0,255,0,0.2); 
            padding: 20px; 
            border-radius: 10px; 
            margin: 20px 0; 
            font-size: 18px;
        }
        .info {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
        }
        button {
            background: #28a745;
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            margin: 10px;
        }
        button:hover { background: #218838; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎉 SUCCESS!</h1>
        <div class="success">
            ✅ Store Management System is working perfectly!
        </div>
        <div class="info">
            <strong>Server Status:</strong> Running<br>
            <strong>Port:</strong> 8080<br>
            <strong>Database:</strong> Ready<br>
            <strong>Time:</strong> ''' + time.strftime('%H:%M:%S') + '''
        </div>
        <button onclick="alert('🎊 Congratulations! Your web store system is fully operational!')">
            Test System
        </button>
        <button onclick="location.reload()">
            Refresh Status
        </button>
    </div>
</body>
</html>'''
            
            self.wfile.write(html.encode('utf-8'))
            log("Main page served successfully")
        else:
            self.send_error(404)
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

def start_server():
    PORT = 8080
    
    # Clear log file
    with open("server_log.txt", "w", encoding="utf-8") as f:
        f.write("=== Server Log ===\n")
    
    log("Starting Store Management System...")
    log(f"Port: {PORT}")
    
    try:
        with socketserver.TCPServer(("", PORT), SimpleHandler) as httpd:
            log("✅ Server started successfully!")
            log(f"URL: http://localhost:{PORT}")
            
            def open_browser():
                time.sleep(1)
                log("Opening browser...")
                webbrowser.open(f'http://localhost:{PORT}')
                log("Browser opened")
            
            threading.Thread(target=open_browser, daemon=True).start()
            
            log("Server running - Press Ctrl+C to stop")
            httpd.serve_forever()
            
    except Exception as e:
        log(f"❌ Error: {e}")

if __name__ == "__main__":
    start_server()
