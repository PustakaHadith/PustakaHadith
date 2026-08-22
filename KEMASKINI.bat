@echo off
setlocal
REM Pasang kemas kini Pustaka Hadis dari ZIP.
REM Guna -Force: Expand-Archive TANPA -Force GAGAL pada fail sedia ada
REM dan meninggalkan kod LAMA tanpa amaran.

set "ZIP=%~1"
if "%ZIP%"=="" set "ZIP=%USERPROFILE%\Downloads\PustakaHadis.zip"

if not exist "%ZIP%" (
  echo.
  echo   ZIP tidak dijumpai: %ZIP%
  echo.
  echo   Seret ZIP ke atas fail ini, atau:
  echo     KEMASKINI.bat "C:\laluan\ke\PustakaHadis.zip"
  echo.
  pause
  exit /b 1
)

echo.
echo   Sumber : %ZIP%
echo   Sasaran: %~dp0
echo.

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "Expand-Archive -LiteralPath \"%ZIP%\" -DestinationPath \"%~dp0.\" -Force"

if errorlevel 1 (
  echo.
  echo   EKSTRAK GAGAL. Tutup aplikasi yang mungkin mengunci fail.
  pause
  exit /b 1
)

if exist "%~dp0hadis\config.py" (
  echo.
  echo   AMARAN: folder "hadis" bersarang dijumpai ^(dari ZIP lama^).
  echo   Skrip berjalan dari folder INI, jadi fail di dalamnya
  echo   DIABAIKAN. Padamkan folder itu untuk mengelak keliru.
)

echo.
python "%~dp0semak_versi.py"
pause
