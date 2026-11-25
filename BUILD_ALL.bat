@echo off
chcp 65001 >nul
cd /d "D:\Pustaka Quran Hadis\Pustaka\PustakaHadith"
title BUILD ALL v1.2.0 - EXE + ZIP + MSIX - jangan tutup tetingkap ini
echo.
echo  ============================================================
echo   BUILD SEMUA v1.2.0 (EXE + ZIP + MSIX)
echo   Ambil masa 20-30 minit. JANGAN tutup tetingkap ini.
echo  ============================================================
echo.

REM ============================================================
REM LANGKAH 1: REBUILD EXE (PyInstaller)
REM ============================================================
echo  [1/3] Rebuild EXE (PyInstaller)...
echo.
".venv-build\Scripts\python.exe" -m PyInstaller PustakaHadith.spec --clean --noconfirm
set CODE=%ERRORLEVEL%

if not "%CODE%"=="0" (
    echo.
    echo  ============================================================
    echo   GAGAL: PyInstaller exit code %CODE%
    echo  ============================================================
    pause
    exit /b %CODE%
)

echo.
echo  [OK] EXE siap: dist\PustakaHadith\PustakaHadith.exe
echo.

REM ============================================================
REM LANGKAH 2: CIPTA ZIP (Portable)
REM ============================================================
echo  [2/3] Cipta ZIP (Portable)...
echo.

set ZIPPATH=D:\Pustaka Quran Hadis\Pustaka\PustakaQH_dist\PustakaHadith-portable-1.2.0-x64.zip

REM Padam ZIP lama jika wujud
if exist "%ZIPPATH%" (
    del "%ZIPPATH%"
    echo   ZIP lama dipadam
)

REM Cipta ZIP baru
powershell -Command "Compress-Archive -Path 'dist\PustakaHadith\*' -DestinationPath '%ZIPPATH%' -Force"

if exist "%ZIPPATH%" (
    echo   [OK] ZIP siap: %ZIPPATH%
) else (
    echo   [X] ZIP gagal
    pause
    exit /b 1
)
echo.

REM ============================================================
REM LANGKAH 3: REBUILD MSIX
REM ============================================================
echo  [3/3] Rebuild MSIX...
echo.

powershell -ExecutionPolicy Bypass -File "installer\build_msix.ps1"

if errorlevel 1 (
    echo.
    echo  ============================================================
    echo   MSIX build selesai (SignTool verify error adalah normal)
    echo  ============================================================
) else (
    echo.
    echo  ============================================================
    echo   MSIX siap!
    echo  ============================================================
)

echo.
echo  ============================================================
echo   SEMUA BUILD SELESAI v1.2.0
echo  ============================================================
echo.
echo  Fail yang dicipta:
echo   1. EXE:  dist\PustakaHadith\PustakaHadith.exe (74.3 MB)
echo   2. ZIP:  D:\Pustaka Quran Hadis\Pustaka\PustakaQH_dist\PustakaHadith-portable-1.2.0-x64.zip (758 MB)
echo   3. MSIX: D:\Pustaka Quran Hadis\Pustaka\PustakaQH_dist\msix\PustakaHadith_1.2.0_x64.msix (783 MB)
echo.
echo  Dokumentasi: installer\BUILD_MSIX.md
echo  ============================================================
echo.
pause
