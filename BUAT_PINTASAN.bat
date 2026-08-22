@echo off
chcp 65001 >nul
title Hadis - Cipta Pintasan
cd /d "%~dp0"

echo.
echo   ==========================================
echo      CIPTA PINTASAN "Hadis"
echo   ==========================================
echo.
echo   Guna fail ini kalau PASANG.bat sudah selesai
echo   tetapi ikon tidak muncul di Desktop.
echo.

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0pintasan.ps1"
set "PSKOD=%errorlevel%"

if "%PSKOD%"=="9009" (
    echo   [X] PowerShell tidak dijumpai pada komputer ini.
    echo       Guna JALANKAN.bat untuk buka apl.
    echo.
    pause
    exit /b 1
)

if not "%PSKOD%"=="0" (
    echo.
    echo   [X] Pintasan gagal dicipta.
    echo.
    echo       Sebabnya tertera di atas. Salin dan hantar kepada saya.
    echo       Sementara itu, guna JALANKAN.bat untuk buka apl.
    echo.
    pause
    exit /b 1
)

echo   Selesai. Cari ikon "Hadis" di Desktop.
echo.
pause
