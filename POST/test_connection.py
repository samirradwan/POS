#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print("Testing Python and modules...")

try:
    import socket
    print("✓ Socket module OK")
    
    # Test if port 8080 is free
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', 8080))
    sock.close()
    
    if result == 0:
        print("✗ Port 8080 is BUSY!")
    else:
        print("✓ Port 8080 is FREE")
        
except Exception as e:
    print(f"✗ Socket error: {e}")

try:
    import http.server
    print("✓ HTTP server module OK")
except Exception as e:
    print(f"✗ HTTP server error: {e}")

try:
    import socketserver
    print("✓ Socket server module OK")
except Exception as e:
    print(f"✗ Socket server error: {e}")

try:
    import webbrowser
    print("✓ Web browser module OK")
except Exception as e:
    print(f"✗ Web browser error: {e}")

print("\nStarting ULTRA SIMPLE server...")

class TestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print(f"Request received: {self.path}")
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>TEST SUCCESS</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background: #4CAF50;
            color: white;
            padding: 50px;
            font-size: 24px;
        }
        .success {
            background: rgba(255,255,255,0.2);
            padding: 30px;
            border-radius: 15px;
            margin: 20px auto;
            max-width: 500px;
        }
    </style>
</head>
<body>
    <div class="success">
        <h1>🎉 SUCCESS!</h1>
        <p>✅ Server is working!</p>
        <p>✅ Connection established!</p>
        <p>✅ Python HTTP server OK!</p>
        <button onclick="alert('System is working perfectly!')">Test Alert</button>
    </div>
</body>
</html>'''
        
        self.wfile.write(html.encode('utf-8'))
        print("Response sent successfully!")

try:
    PORT = 8080
    print(f"Starting server on port {PORT}...")
    
    with socketserver.TCPServer(("", PORT), TestHandler) as httpd:
        print(f"✓ Server started successfully!")
        print(f"✓ URL: http://localhost:{PORT}")
        print("✓ Server is running...")
        print("Press Ctrl+C to stop")
        
        # Open browser
        import webbrowser
        import threading
        import time
        
        def open_browser():
            time.sleep(1)
            print("Opening browser...")
            webbrowser.open(f'http://localhost:{PORT}')
        
        threading.Thread(target=open_browser, daemon=True).start()
        
        httpd.serve_forever()
        
except KeyboardInterrupt:
    print("\n✓ Server stopped")
except Exception as e:
    print(f"✗ Server error: {e}")
    input("Press Enter to exit...")
