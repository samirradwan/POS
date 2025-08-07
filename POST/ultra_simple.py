import http.server
import socketserver
import webbrowser
import threading
import time

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Store System</title>
    <style>
        body { font-family: Arial; margin: 50px; background: #f0f0f0; }
        .container { background: white; padding: 30px; border-radius: 10px; text-align: center; }
        h1 { color: #333; }
        .success { color: green; font-size: 18px; margin: 20px 0; }
        button { background: #007bff; color: white; padding: 15px 30px; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; }
        button:hover { background: #0056b3; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏪 Store Management System</h1>
        <div class="success">✅ System is working successfully!</div>
        <p>The web-based store management system is now running.</p>
        <button onclick="alert('System is working! You can now add more features.')">Test Button</button>
    </div>
</body>
</html>
            '''
            self.wfile.write(html.encode())
        else:
            self.send_error(404)

def start():
    PORT = 8080
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Server running at http://localhost:{PORT}")
        
        def open_browser():
            time.sleep(1)
            webbrowser.open(f'http://localhost:{PORT}')
        
        threading.Thread(target=open_browser, daemon=True).start()
        print("Press Ctrl+C to stop")
        httpd.serve_forever()

if __name__ == "__main__":
    start()
