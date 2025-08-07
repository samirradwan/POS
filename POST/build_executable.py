#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تجميع نظام إدارة المتجر إلى ملف تنفيذي

هذا الملف يستخدم PyInstaller لتجميع النظام
إلى ملف .exe يمكن تشغيله بدون Python
"""

import os
import sys
import subprocess
import shutil

def check_pyinstaller():
    """التحقق من وجود PyInstaller"""
    try:
        import PyInstaller
        print("✅ PyInstaller متاح")
        return True
    except ImportError:
        print("❌ PyInstaller غير مثبت")
        print("لتثبيته: pip install pyinstaller")
        return False

def create_spec_file():
    """إنشاء ملف .spec للتجميع"""
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['run_system.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('README.md', '.'),
        ('دليل_المستخدم.md', '.'),
        ('requirements.txt', '.'),
    ],
    hiddenimports=[
        'tkinter',
        'sqlite3',
        'matplotlib.backends.backend_tkagg',
        'PIL._tkinter_finder'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='نظام_إدارة_المتجر',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)
'''
    
    with open('store_system.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ تم إنشاء ملف store_system.spec")

def build_executable():
    """تجميع الملف التنفيذي"""
    print("🔨 بدء عملية التجميع...")
    
    try:
        # تشغيل PyInstaller
        cmd = [
            'pyinstaller',
            '--onefile',
            '--windowed',
            '--name=نظام_إدارة_المتجر',
            '--add-data=README.md;.',
            '--add-data=دليل_المستخدم.md;.',
            '--add-data=requirements.txt;.',
            '--hidden-import=tkinter',
            '--hidden-import=sqlite3',
            'run_system.py'
        ]
        
        # إضافة أيقونة إذا كانت متوفرة
        if os.path.exists('icon.ico'):
            cmd.extend(['--icon=icon.ico'])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ تم التجميع بنجاح!")
            return True
        else:
            print("❌ فشل التجميع:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ خطأ في التجميع: {e}")
        return False

def create_distribution():
    """إنشاء حزمة التوزيع"""
    print("📦 إنشاء حزمة التوزيع...")
    
    dist_dir = "نظام_إدارة_المتجر_v1.0"
    
    # إنشاء مجلد التوزيع
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    os.makedirs(dist_dir)
    
    # نسخ الملف التنفيذي
    exe_file = "dist/نظام_إدارة_المتجر.exe"
    if os.path.exists(exe_file):
        shutil.copy2(exe_file, dist_dir)
        print(f"✅ تم نسخ {exe_file}")
    
    # نسخ الملفات المهمة
    important_files = [
        'README.md',
        'دليل_المستخدم.md',
        'requirements.txt'
    ]
    
    for file in important_files:
        if os.path.exists(file):
            shutil.copy2(file, dist_dir)
            print(f"✅ تم نسخ {file}")
    
    # إنشاء ملف تشغيل سريع
    quick_run_content = '''@echo off
echo تشغيل نظام إدارة المتجر...
echo.
"نظام_إدارة_المتجر.exe"
pause
'''
    
    with open(f"{dist_dir}/تشغيل_النظام.bat", 'w', encoding='utf-8') as f:
        f.write(quick_run_content)
    
    print(f"✅ تم إنشاء حزمة التوزيع في: {dist_dir}")
    
    return dist_dir

def cleanup():
    """تنظيف الملفات المؤقتة"""
    print("🧹 تنظيف الملفات المؤقتة...")
    
    temp_dirs = ['build', '__pycache__']
    temp_files = ['store_system.spec']
    
    for dir_name in temp_dirs:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✅ تم حذف {dir_name}")
    
    for file_name in temp_files:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"✅ تم حذف {file_name}")

def main():
    """الدالة الرئيسية"""
    print("🏗️ تجميع نظام إدارة متجر الأدوات الكهربائية")
    print("=" * 60)
    
    # التحقق من المتطلبات
    if not check_pyinstaller():
        print("\nلتثبيت PyInstaller:")
        print("pip install pyinstaller")
        return
    
    # التحقق من وجود الملفات المطلوبة
    required_files = [
        'run_system.py',
        'main_application.py',
        'database.py',
        'models.py',
        'utils.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ ملفات مفقودة: {', '.join(missing_files)}")
        return
    
    print("✅ جميع الملفات المطلوبة متوفرة")
    
    # بدء عملية التجميع
    if build_executable():
        # إنشاء حزمة التوزيع
        dist_dir = create_distribution()
        
        # تنظيف الملفات المؤقتة
        cleanup()
        
        print("\n🎉 تم التجميع بنجاح!")
        print(f"📁 حزمة التوزيع: {dist_dir}")
        print("📋 محتويات الحزمة:")
        
        for item in os.listdir(dist_dir):
            print(f"   - {item}")
        
        print("\n📝 تعليمات التوزيع:")
        print("1. انسخ مجلد التوزيع إلى الجهاز المطلوب")
        print("2. شغل 'تشغيل_النظام.bat' أو الملف التنفيذي مباشرة")
        print("3. لا يحتاج Python على الجهاز المستهدف")
        
    else:
        print("\n❌ فشل في التجميع")

if __name__ == "__main__":
    main()
