@echo off
title Emergency Store System Fix
cls
echo.
echo ========================================
echo    EMERGENCY STORE SYSTEM FIX
echo ========================================
echo.

echo Step 1: Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python first.
    pause
    exit
)

echo.
echo Step 2: Killing any existing servers...
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Step 3: Creating emergency server...

echo import http.server > emergency_server.py
echo import socketserver >> emergency_server.py
echo import webbrowser >> emergency_server.py
echo import threading >> emergency_server.py
echo import time >> emergency_server.py
echo. >> emergency_server.py
echo class Handler(http.server.SimpleHTTPRequestHandler): >> emergency_server.py
echo     def do_GET(self): >> emergency_server.py
echo         self.send_response(200) >> emergency_server.py
echo         self.send_header('Content-type', 'text/html') >> emergency_server.py
echo         self.end_headers() >> emergency_server.py
echo         html = '''^^<!DOCTYPE html^^>^^<html^^>^^<head^^>^^<title^^>WORKING!^^</title^^>^^<style^^>body{background:#4CAF50;color:white;text-align:center;padding:50px;font-size:30px;}^^</style^^>^^</head^^>^^<body^^>^^<h1^^>SUCCESS! SYSTEM WORKING!^^</h1^^>^^<p^^>Store system is now operational!^^</p^^>^^</body^^>^^</html^^>''' >> emergency_server.py
echo         self.wfile.write(html.encode()) >> emergency_server.py
echo. >> emergency_server.py
echo PORT = 8080 >> emergency_server.py
echo with socketserver.TCPServer(("", PORT), Handler) as httpd: >> emergency_server.py
echo     def open_browser(): >> emergency_server.py
echo         time.sleep(1) >> emergency_server.py
echo         webbrowser.open(f'http://localhost:{PORT}') >> emergency_server.py
echo     threading.Thread(target=open_browser, daemon=True).start() >> emergency_server.py
echo     print(f"Server running on http://localhost:{PORT}") >> emergency_server.py
echo     httpd.serve_forever() >> emergency_server.py

echo.
echo Step 4: Starting emergency server...
echo.
echo The browser should open automatically.
echo If not, go to: http://localhost:8080
echo.
echo Press Ctrl+C to stop the server.
echo.

python emergency_server.py

echo.
echo Server stopped.
pause
