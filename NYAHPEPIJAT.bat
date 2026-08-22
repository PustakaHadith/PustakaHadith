@echo off
chcp 65001 >nul
title Pustaka Hadis - Nyahpepijat
cd /d "%~dp0"

echo.
echo   ==========================================
echo      NYAHPEPIJAT - Pustaka Hadis
echo   ==========================================
echo.
echo   Tetingkap ini TIDAK akan tutup sendiri.
echo   Salin semua teks di bawah dan hantar kepada saya.
echo.
echo   ------------------------------------------
echo   Folder apl:
echo   %~dp0
echo.

echo   ------------------------------------------
echo   Python yang dijumpai Windows:
where python.exe 2>nul
where pythonw.exe 2>nul
where py.exe 2>nul
echo.

echo   ------------------------------------------
echo   Versi Python:
python --version 2>&1
echo.

echo   ------------------------------------------
echo   Modul yang diperlukan:
python -c "import PyQt5.QtWidgets; print('  PyQt5      : OK')" 2>&1
python -c "import requests;       print('  requests   : OK')" 2>&1
python -c "import pyperclip;      print('  pyperclip  : OK')" 2>&1
echo.

echo   ------------------------------------------
echo   Fail penting:
if exist "%~dp0main.py"          (echo   main.py          : ada) else (echo   main.py          : HILANG)
if exist "%~dp0ui\app_qt.py"     (echo   ui\app_qt.py     : ada) else (echo   ui\app_qt.py     : HILANG)
if exist "%~dp0requirements.txt" (echo   requirements.txt : ada) else (echo   requirements.txt : HILANG)
echo.

echo   ------------------------------------------
echo   CUBA JALANKAN APL (ralat penuh akan keluar):
echo   ------------------------------------------
echo.
python "%~dp0main.py"
echo.
echo   ------------------------------------------
echo   Apl tamat. Kod keluar: %errorlevel%
echo   ------------------------------------------
echo.
pause
