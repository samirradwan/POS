@echo off
chcp 65001 >nul
title فتح نظام إدارة المتجر - HTML Version
color 0B
cls

echo.
echo ================================================================
echo                    نظام إدارة المتجر - HTML
echo                 Store Management System - HTML
echo ================================================================
echo.

echo 🌐 فتح النسخة البسيطة من نظام إدارة المتجر...
echo Opening simple version of Store Management System...
echo.

REM التحقق من وجود ملف index.html
if not exist "index.html" (
    echo ❌ ملف index.html غير موجود!
    echo ❌ index.html file not found!
    echo.
    echo يرجى التأكد من وجود الملف في نفس المجلد
    echo Please make sure the file exists in the same folder
    echo.
    pause
    exit /b 1
)

echo ✅ تم العثور على ملف index.html
echo ✅ index.html file found
echo.

echo 📋 معلومات مهمة:
echo Important information:
echo.
echo • هذه نسخة بسيطة تعمل في المتصفح مباشرة
echo • This is a simple version that works directly in browser
echo.
echo • البيانات محفوظة في المتصفح فقط
echo • Data is saved in browser only
echo.
echo • للنسخة الكاملة: شغل start_final_store.bat
echo • For full version: run start_final_store.bat
echo.
echo ================================================================
echo.

echo 🚀 فتح المتصفح...
echo Opening browser...
echo.

REM فتح الملف في المتصفح الافتراضي
start "" "index.html"

echo ✅ تم فتح النظام في المتصفح
echo ✅ System opened in browser
echo.

echo 💡 نصائح:
echo Tips:
echo.
echo • إذا لم يفتح المتصفح، اضغط مرتين على index.html
echo • If browser doesn't open, double-click index.html
echo.
echo • لحفظ البيانات بشكل دائم، استخدم النسخة الكاملة
echo • For permanent data saving, use the full version
echo.

echo ================================================================
echo.
pause
