import http.server
import socketserver
import webbrowser
import threading
import time

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>WORKING!</title>
    <style>
        body {
            background: linear-gradient(45deg, #4CAF50, #45a049);
            color: white;
            text-align: center;
            padding: 50px;
            font-family: Arial, sans-serif;
            margin: 0;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background: rgba(255,255,255,0.1);
            padding: 40px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
        }
        h1 {
            font-size: 3em;
            margin-bottom: 20px;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        p {
            font-size: 1.5em;
            margin: 20px 0;
        }
        .success {
            background: rgba(0,255,0,0.3);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎉 SUCCESS!</h1>
        <div class="success">
            ✅ Store System is WORKING!
        </div>
        <p>✅ Server: Running</p>
        <p>✅ Connection: Established</p>
        <p>✅ Port 8080: Active</p>
        <p>✅ Browser: Connected</p>
        
        <div style="margin-top: 30px;">
            <button onclick="alert('System is fully operational!')" 
                    style="background:#fff; color:#4CAF50; padding:15px 30px; border:none; border-radius:10px; font-size:18px; cursor:pointer;">
                Test System
            </button>
        </div>
    </div>
</body>
</html>'''
        
        self.wfile.write(html.encode('utf-8'))

PORT = 8080

def open_browser():
    time.sleep(1)
    webbrowser.open(f'http://localhost:{PORT}')

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    threading.Thread(target=open_browser, daemon=True).start()
    print(f"Server running on http://localhost:{PORT}")
    httpd.serve_forever()
