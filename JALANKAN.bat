@echo off
REM PustakaHadith - pelancar sandaran.
REM Guna fail ini kalau pintasan "Hadis" tidak berfungsi.
chcp 65001 >nul
cd /d "%~dp0"

set "PYW="
for /f "delims=" %%W in ('where pythonw.exe 2^>nul') do (
    if not defined PYW set "PYW=%%W"
)

if not defined PYW (
    for /f "delims=" %%W in ('where python.exe 2^>nul') do (
        if not defined PYW set "PYW=%%W"
    )
)

if not defined PYW (
    echo Python tidak dijumpai. Jalankan PASANG.bat dahulu.
    pause
    exit /b 1
)

start "" "%PYW%" "%~dp0main.py"
