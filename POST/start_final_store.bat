@echo off
chcp 65001 >nul
title نظام إدارة المتجر النهائي - Final Store Management System
color 0A
cls

echo.
echo ================================================================
echo                   نظام إدارة المتجر النهائي
echo                 Final Store Management System
echo ================================================================
echo.

echo 🔍 فحص النظام...
echo Checking system...
echo.

REM فحص Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python غير مثبت أو غير موجود في PATH
    echo ❌ Python is not installed or not in PATH
    echo.
    echo يرجى تثبيت Python من: https://python.org
    echo Please install Python from: https://python.org
    echo.
    pause
    exit /b 1
)

echo ✅ Python متوفر
echo ✅ Python available
echo.

REM فحص الملف الرئيسي
if not exist "final_working_store.py" (
    echo ❌ الملف الرئيسي مفقود: final_working_store.py
    echo ❌ Main file missing: final_working_store.py
    echo.
    pause
    exit /b 1
)

echo ✅ الملف الرئيسي موجود
echo ✅ Main file exists
echo.

REM إيقاف أي عمليات Python سابقة على المنفذ 8080
echo 🔄 إيقاف العمليات السابقة...
echo Stopping previous processes...
taskkill /f /im python.exe /fi "WINDOWTITLE eq *8080*" >nul 2>&1
timeout /t 2 /nobreak >nul

echo.
echo 🚀 بدء تشغيل نظام إدارة المتجر...
echo Starting Store Management System...
echo.
echo 📋 معلومات مهمة:
echo Important information:
echo.
echo • الرابط: http://localhost:8080
echo • Link: http://localhost:8080
echo.
echo • سيتم فتح المتصفح تلقائياً
echo • Browser will open automatically
echo.
echo • لإيقاف النظام: اضغط Ctrl+C
echo • To stop system: Press Ctrl+C
echo.
echo ================================================================
echo.

REM تشغيل النظام
python final_working_store.py

echo.
echo ================================================================
echo تم إيقاف النظام
echo System stopped
echo ================================================================
echo.
pause
