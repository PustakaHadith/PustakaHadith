@echo off
REM ============================================
REM PustakaHadith - MSIX Packaging Script
REM ============================================

echo.
echo [1/4] Rebuild .exe dengan PyInstaller...
echo.

cd /d "%~dp0\.."
pyinstaller PustakaHadith.spec --clean --noconfirm
if errorlevel 1 (
    echo ERROR: PyInstaller gagal!
    pause
    exit /b 1
)

echo.
echo [2/4] Salin .exe ke folder MSIX...
echo.

if not exist "msix\PustakaHadith" mkdir "msix\PustakaHadith"
xcopy /E /I /Y "dist\PustakaHadith\*" "msix\PustakaHadith\"
if errorlevel 1 (
    echo ERROR: Salin fail gagal!
    pause
    exit /b 1
)

echo.
echo [3/4] Package MSIX dengan MakeAppx...
echo.

set MAKEAPPX=%ProgramFiles(x86)%\Windows Kits\10\bin\%SDK_VERSION%\x64\MakeAppx.exe
if not exist "%MAKEAPPX%" (
    REM Try latest SDK
    for /f "tokens=*" %%i in ('dir /b /s "%ProgramFiles(x86)%\Windows Kits\10\bin\*\x64\MakeAppx.exe" 2^>nul ^| sort /r') do (
        set MAKEAPPX=%%i
        goto :found_makeappx
    )
    echo ERROR: MakeAppx.exe tidak ditemui! Pasang Windows SDK.
    pause
    exit /b 1
)
:found_makeappx

"%MAKEAPPX%" pack /d "msix" /p "PustakaHadith.msix" /o
if errorlevel 1 (
    echo ERROR: MakeAppx gagal!
    pause
    exit /b 1
)

echo.
echo [4/4] Selesai!
echo.
echo Fail MSIX: %~dp0\PustakaHadith.msix
echo.
echo Langkah seterusnya:
echo   1. Sign MSIX dengan signtool
echo   2. Upload ke Microsoft Partner Center
echo.
pause
