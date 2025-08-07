#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إعداد نظام إدارة متجر الأدوات الكهربائية
"""

from setuptools import setup, find_packages
import os

# قراءة ملف README
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# قراءة المتطلبات
def read_requirements():
    requirements = []
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line and not line.startswith("#"):
                    requirements.append(line)
    return requirements

setup(
    name="store-management-system",
    version="1.0.0",
    author="فريق التطوير",
    author_email="developer@example.com",
    description="نظام إدارة متجر الأدوات الكهربائية",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/example/store-management",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business :: Financial :: Point-Of-Sale",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Natural Language :: Arabic",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "charts": ["matplotlib>=3.5.0"],
        "calendar": ["tkcalendar>=1.6.0"],
        "images": ["Pillow>=8.0.0"],
        "encryption": ["cryptography>=3.4.0"],
        "dev": [
            "pytest>=6.0.0",
            "black>=21.0.0",
            "flake8>=3.9.0",
            "pyinstaller>=4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "store-management=run_system:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": [
            "*.md",
            "*.txt",
            "*.ico",
            "*.png",
            "*.jpg",
        ],
    },
    data_files=[
        ("docs", ["README.md", "دليل_المستخدم.md"]),
        ("config", ["requirements.txt"]),
    ],
    keywords=[
        "store management",
        "point of sale",
        "inventory",
        "electrical tools",
        "business software",
        "إدارة متجر",
        "نقطة بيع",
        "مخزون",
        "أدوات كهربائية",
    ],
    project_urls={
        "Bug Reports": "https://github.com/example/store-management/issues",
        "Source": "https://github.com/example/store-management",
        "Documentation": "https://github.com/example/store-management/wiki",
    },
)
