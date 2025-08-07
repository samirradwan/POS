#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام التشخيص الشامل لمتجر الإدارة
System Comprehensive Diagnosis for Store Management
"""

import sys
import os
import platform
import subprocess

def write_log(message):
    """كتابة رسالة إلى ملف السجل والشاشة"""
    print(message)
    with open("diagnosis_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{message}\n")

def clear_log():
    """مسح ملف السجل"""
    try:
        with open("diagnosis_log.txt", "w", encoding="utf-8") as f:
            f.write("=== تشخيص النظام الشامل ===\n")
            f.write("=== System Comprehensive Diagnosis ===\n\n")
    except:
        pass

def check_python():
    """فحص Python"""
    write_log("🔍 فحص Python...")
    write_log(f"✓ إصدار Python: {sys.version}")
    write_log(f"✓ مسار Python: {sys.executable}")
    write_log(f"✓ نظام التشغيل: {platform.system()} {platform.release()}")
    write_log(f"✓ معمارية النظام: {platform.architecture()[0]}")
    return True

def check_modules():
    """فحص المكتبات المطلوبة"""
    write_log("\n🔍 فحص المكتبات المطلوبة...")
    
    required_modules = [
        'http.server',
        'socketserver', 
        'webbrowser',
        'threading',
        'time',
        'json',
        'urllib.parse',
        'sqlite3',
        'os',
        'sys'
    ]
    
    all_good = True
    for module in required_modules:
        try:
            __import__(module)
            write_log(f"✓ {module}")
        except ImportError as e:
            write_log(f"✗ {module} - خطأ: {e}")
            all_good = False
    
    return all_good

def check_port():
    """فحص المنفذ 8080"""
    write_log("\n🔍 فحص المنفذ 8080...")
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 8080))
        sock.close()
        
        if result == 0:
            write_log("⚠️ المنفذ 8080 مستخدم حالياً")
            return False
        else:
            write_log("✓ المنفذ 8080 متاح")
            return True
    except Exception as e:
        write_log(f"✗ خطأ في فحص المنفذ: {e}")
        return False

def test_database():
    """اختبار قاعدة البيانات"""
    write_log("\n🔍 اختبار قاعدة البيانات...")
    try:
        import sqlite3
        
        # إنشاء قاعدة بيانات اختبار
        conn = sqlite3.connect('test_db.db')
        cursor = conn.cursor()
        
        # إنشاء جدول اختبار
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_table (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        ''')
        
        # إدراج بيانات اختبار
        cursor.execute("INSERT INTO test_table (name) VALUES (?)", ("test",))
        
        # قراءة البيانات
        cursor.execute("SELECT * FROM test_table")
        result = cursor.fetchall()
        
        conn.commit()
        conn.close()
        
        # حذف قاعدة البيانات الاختبارية
        os.remove('test_db.db')
        
        write_log("✓ قاعدة البيانات تعمل بشكل صحيح")
        return True
        
    except Exception as e:
        write_log(f"✗ خطأ في قاعدة البيانات: {e}")
        return False

def test_web_server():
    """اختبار الخادم"""
    write_log("\n🔍 اختبار الخادم...")
    try:
        import http.server
        import socketserver
        import threading
        import time
        
        class TestHandler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'<html><body><h1>Test OK</h1></body></html>')
            
            def log_message(self, format, *args):
                pass
        
        # اختبار إنشاء الخادم
        PORT = 8081  # استخدام منفذ مختلف للاختبار
        with socketserver.TCPServer(("", PORT), TestHandler) as httpd:
            write_log(f"✓ الخادم يعمل على المنفذ {PORT}")
            
            # اختبار سريع
            def test_request():
                time.sleep(0.5)
                try:
                    import urllib.request
                    response = urllib.request.urlopen(f'http://localhost:{PORT}')
                    content = response.read().decode()
                    if 'Test OK' in content:
                        write_log("✓ اختبار الطلب نجح")
                    httpd.shutdown()
                except Exception as e:
                    write_log(f"⚠️ اختبار الطلب فشل: {e}")
                    httpd.shutdown()
            
            threading.Thread(target=test_request, daemon=True).start()
            httpd.serve_forever()
            
        return True
        
    except Exception as e:
        write_log(f"✗ خطأ في الخادم: {e}")
        return False

def check_files():
    """فحص الملفات المطلوبة"""
    write_log("\n🔍 فحص الملفات...")
    
    required_files = [
        'complete_store.py',
        'start_store.bat'
    ]
    
    all_good = True
    for file in required_files:
        if os.path.exists(file):
            write_log(f"✓ {file}")
        else:
            write_log(f"✗ {file} مفقود")
            all_good = False
    
    return all_good

def main():
    """الدالة الرئيسية"""
    clear_log()
    write_log("بدء التشخيص الشامل للنظام...")
    write_log("=" * 50)
    
    results = []
    
    # فحص Python
    results.append(("Python", check_python()))
    
    # فحص المكتبات
    results.append(("المكتبات", check_modules()))
    
    # فحص المنفذ
    results.append(("المنفذ", check_port()))
    
    # فحص قاعدة البيانات
    results.append(("قاعدة البيانات", test_database()))
    
    # فحص الخادم
    results.append(("الخادم", test_web_server()))
    
    # فحص الملفات
    results.append(("الملفات", check_files()))
    
    # النتائج النهائية
    write_log("\n" + "=" * 50)
    write_log("📊 ملخص النتائج:")
    
    all_passed = True
    for test_name, result in results:
        status = "✓ نجح" if result else "✗ فشل"
        write_log(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    write_log("\n" + "=" * 50)
    if all_passed:
        write_log("🎉 جميع الاختبارات نجحت! النظام جاهز للعمل.")
    else:
        write_log("⚠️ بعض الاختبارات فشلت. يرجى مراجعة الأخطاء أعلاه.")
    
    write_log(f"\nتم حفظ السجل في: diagnosis_log.txt")
    
    return all_passed

if __name__ == "__main__":
    try:
        success = main()
        input("\nاضغط Enter للخروج...")
    except KeyboardInterrupt:
        print("\nتم إيقاف التشخيص.")
    except Exception as e:
        print(f"خطأ غير متوقع: {e}")
        input("اضغط Enter للخروج...")
