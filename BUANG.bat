@echo off
chcp 437 >nul 2>&1
title Hadis - Buang dari komputer
cd /d "%~dp0"

echo.
echo   ==========================================
echo      BUANG PustakaHadith
echo   ==========================================
echo.
echo   Folder: %~dp0
echo.
echo   Apl ini tiada installer dan tiada registry.
echo   Ia hanya folder + ikon.
echo.
echo   AKAN dibuang:
echo      - ikon "Hadis" di Desktop
echo      - ikon "Hadis" di Start Menu
echo      - pin di taskbar (jika ada)
echo.
echo   ------------------------------------------
echo.

set "BUANGDATA=tidak"
set /p JWP1="   Buang juga data (hadis.db, tetapan)? Y/ENTER: "
if /i "%JWP1%"=="Y" set "BUANGDATA=ya"
echo.

set "BUANGPKG=tidak"
set /p JWP2="   Tanggal PyQt5 dari Python? Y/ENTER: "
if /i "%JWP2%"=="Y" set "BUANGPKG=ya"
echo.

set "PASTI="
set /p PASTI="   Taip BUANG untuk sahkan: "
if /i not "%PASTI%"=="BUANG" goto :batal

echo.
echo   ==========================================
echo.

REM ============================================================
REM  1. Pintasan
REM     cmd tulen - tiada PowerShell. Kurang titik kegagalan.
REM ============================================================
echo   [1] Membuang pintasan...

set "N=0"
call :buanglnk "%USERPROFILE%\Desktop"
call :buanglnk "%APPDATA%\Microsoft\Windows\Start Menu\Programs"
call :buanglnk "%PUBLIC%\Desktop"
call :buanglnk "%ProgramData%\Microsoft\Windows\Start Menu\Programs"
call :buanglnk "%APPDATA%\Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar"

if "%N%"=="0" echo         tiada pintasan dijumpai.
echo.

REM ============================================================
REM  2. Data pengguna
REM ============================================================
if "%BUANGDATA%"=="ya" (
    echo   [2] Membuang data pengguna...
    call :buangfail "hadis.db"
    call :buangfail "hadis.db-wal"
    call :buangfail "hadis.db-shm"
    call :buangfail "user_settings.json"
    call :buangfail "bookmarks.json"
    call :buangfail ".env"
) else (
    echo   [2] Data pengguna DIKEKALKAN
    echo         hadis.db + tetapan tidak disentuh.
)
echo.

REM ============================================================
REM  3. Pakej Python
REM     'requests' sengaja DIKEKALKAN - terlalu banyak
REM     program Python lain bergantung padanya.
REM ============================================================
if "%BUANGPKG%"=="ya" (
    echo   [3] Menanggalkan PyQt5...
    echo.
    set "PY="
    for /f "delims=" %%P in ('where python.exe 2^>nul') do if not defined PY set "PY=%%P"
    if not defined PY (
        for /f "delims=" %%P in ('where py.exe 2^>nul') do if not defined PY set "PY=%%P"
    )
    if defined PY (
        "%PY%" -m pip uninstall -y PyQt5 PyQt5-Qt5 PyQt5-sip pyperclip
        echo         requests dikekalkan - program lain mungkin guna.
    ) else (
        echo         Python tidak dijumpai - langkau.
    )
) else (
    echo   [3] Pakej Python DIKEKALKAN
)
echo.

echo   ==========================================
echo      SELESAI
echo   ==========================================
echo.
echo   Langkah terakhir - buat sendiri:
echo.
echo      Padam folder ini:
echo      %~dp0
echo.
echo   Skrip tidak boleh padam folder yang sedang
echo   dijalankannya. Tutup tetingkap ini, naik satu
echo   folder, dan padam folder tersebut.
echo.
pause
exit /b 0


REM ============================================================
REM  Subrutin
REM ============================================================

:buanglnk
REM %~1 = folder. Padam ikut NAMA TEPAT, bukan wildcard *.lnk,
REM supaya pintasan orang lain tidak tersentuh.
if not exist "%~1" goto :eof
call :satu "%~1\Hadis.lnk"
call :satu "%~1\PustakaHadith.lnk"
call :satu "%~1\PustakaHadith.lnk"
goto :eof

:satu
if not exist "%~1" goto :eof
del /f /q "%~1" >nul 2>&1
if exist "%~1" (
    echo         GAGAL   : %~1
) else (
    echo         dibuang : %~1
    set /a N+=1
)
goto :eof

:buangfail
if not exist "%~dp0%~1" goto :eof
del /f /q "%~dp0%~1" >nul 2>&1
if exist "%~dp0%~1" (
    echo         GAGAL   : %~1  - apl masih berjalan?
) else (
    echo         dibuang : %~1
)
goto :eof


:batal
echo.
echo   Dibatalkan. Tiada apa-apa disentuh.
echo.
pause
exit /b 0
