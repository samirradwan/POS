#!/usr/bin/env python3

print("Testing basic functionality...")

try:
    import http.server
    import socketserver
    print("✓ HTTP modules imported")
except Exception as e:
    print(f"✗ HTTP import error: {e}")
    exit(1)

try:
    import sqlite3
    print("✓ SQLite imported")
except Exception as e:
    print(f"✗ SQLite import error: {e}")
    exit(1)

try:
    import webbrowser
    print("✓ Webbrowser imported")
except Exception as e:
    print(f"✗ Webbrowser import error: {e}")
    exit(1)

# Test SQLite
try:
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE test (id INTEGER, name TEXT)")
    cursor.execute("INSERT INTO test VALUES (1, 'test')")
    result = cursor.fetchone()
    conn.close()
    print("✓ SQLite working")
except Exception as e:
    print(f"✗ SQLite error: {e}")
    exit(1)

# Test simple HTTP server
class SimpleHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<h1>Hello World!</h1>')
    
    def log_message(self, format, *args):
        pass  # Suppress log messages

def test_server():
    PORT = 8080
    try:
        with socketserver.TCPServer(("", PORT), SimpleHandler) as httpd:
            print(f"✓ Server started on port {PORT}")
            print(f"✓ Test URL: http://localhost:{PORT}")
            
            # Try to open browser
            try:
                import webbrowser
                import threading
                import time
                
                def open_browser():
                    time.sleep(1)
                    webbrowser.open(f'http://localhost:{PORT}')
                
                threading.Thread(target=open_browser, daemon=True).start()
                print("✓ Browser opening...")
                
            except Exception as e:
                print(f"✗ Browser error: {e}")
            
            print("Server running... Press Ctrl+C to stop")
            httpd.serve_forever()
            
    except Exception as e:
        print(f"✗ Server error: {e}")

if __name__ == "__main__":
    print("Starting minimal test...")
    test_server()
