@echo off
chcp 65001 >nul
title Pustaka Hadis - Pemasangan
cd /d "%~dp0"
setlocal EnableDelayedExpansion

echo.
echo   ==========================================
echo      PUSTAKA HADIS - Pemasangan
echo   ==========================================
echo.
echo   Folder: %~dp0
echo.

REM ===========================================================
REM  [1/4]  Cari Python
REM ===========================================================
set "PY="

for %%C in (py.exe python.exe) do (
    if not defined PY (
        for /f "delims=" %%P in ('where %%C 2^>nul') do (
            if not defined PY set "PY=%%P"
        )
    )
)

if not defined PY (
    echo   [X] PYTHON TIDAK DIJUMPAI
    echo.
    echo       1. Muat turun: https://python.org/downloads
    echo       2. Semasa pasang, TANDAKAN kotak:
    echo            [v] Add python.exe to PATH
    echo       3. Jalankan PASANG.bat ini semula
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%v in ('"%PY%" --version 2^>^&1') do set "PYVER=%%v"
echo   [1/4] Python !PYVER!
echo         !PY!
echo.

REM Pengesanan pythonw.exe dibuat dalam pintasan.ps1.
REM Versi lama guna:  for /f ... in ('... 'pythonw.exe' ...')
REM Petikan tunggal bersarang menamatkan perintah for /f awal
REM pada cmd.exe -> sintaks pecah, PYW kosong.


REM ===========================================================
REM  [2/4]  Pasang keperluan
REM ===========================================================
echo   [2/4] Memasang PyQt5, requests, pyperclip...
echo         (ambil masa 1-3 minit kali pertama)
echo.

"%PY%" -m pip install --upgrade pip
"%PY%" -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo   [X] PEMASANGAN GAGAL
    echo.
    echo       Cuba: klik kanan PASANG.bat - Run as administrator
    echo.
    pause
    exit /b 1
)
echo.


REM ===========================================================
REM  [3/4]  Sahkan PyQt5 betul-betul boleh diimport
REM ===========================================================
echo   [3/4] Menyemak pemasangan...

"%PY%" -c "import PyQt5.QtWidgets, requests, pyperclip" 2>nul
if errorlevel 1 (
    echo.
    echo   [X] PyQt5 dipasang tetapi TIDAK boleh diimport.
    echo.
    echo       Selalunya ada lebih satu Python dalam komputer.
    echo       Salin mesej di bawah dan tunjukkan kepada saya:
    echo.
    "%PY%" -c "import PyQt5.QtWidgets"
    echo.
    pause
    exit /b 1
)
echo         OK - semua modul berfungsi.
echo.


REM ===========================================================
REM  [4/4]  Cipta pintasan "Hadis"
REM ===========================================================
echo   [4/4] Mencipta pintasan "Hadis"...

REM Pintasan menunjuk TERUS ke pythonw.exe - tiada .vbs perantara.
REM Sebab: perkaitan fail .vbs sering dirampas program lain,
REM menyebabkan klik pintasan langsung tiada tindak balas.
REM
REM Logik pintasan diletak dalam pintasan.ps1, BUKAN sebaris di sini:
REM memetik laluan berruang merentas cmd.exe + PowerShell menyebabkan
REM ralat escape yang senyap.

set "OK_DESKTOP=tidak"

REM Laluan folder TIDAK dihantar sebagai argumen: %~dp0 sentiasa
REM tamat dengan '\', jadi cmd.exe menghantar  "D:\Folder Saya\"
REM dan PowerShell membaca \" sebagai petikan di-escape lalu menelan
REM argumen seterusnya. Skrip guna $PSScriptRoot sendiri.

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0pintasan.ps1"
set "PSKOD=%errorlevel%"

REM 9009 = powershell.exe langsung tidak dijumpai
if "%PSKOD%"=="9009" (
    echo         [!] PowerShell tidak dijumpai pada komputer ini.
)

if not "%PSKOD%"=="0" (
    echo.
    echo   [!] Pintasan gagal dicipta - tetapi apl TETAP boleh jalan.
    echo       Guna JALANKAN.bat dalam folder ini.
    echo.
) else (
    set "OK_DESKTOP=ya"
)

echo.
echo   ==========================================
echo      SIAP
echo   ==========================================
echo.
if "!OK_DESKTOP!"=="ya" (
    echo   Cari ikon "Hadis" di Desktop anda. Klik dua kali.
) else (
    echo   Klik dua kali JALANKAN.bat dalam folder ini.
)
echo.
echo   Kali pertama buka: klik ikon gear - Tetapan API
echo   dan masukkan kunci API hadis.my anda.
echo.
echo   Kalau ada masalah, jalankan NYAHPEPIJAT.bat
echo   dan hantar mesej yang keluar.
echo.
pause
