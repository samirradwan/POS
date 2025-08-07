@echo off
echo Testing Python...
python --version
echo.
echo Testing simple Python command...
python -c "print('Python works!')"
echo.
echo Testing tkinter...
python -c "import tkinter; print('tkinter works!')"
echo.
pause
