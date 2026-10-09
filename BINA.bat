@echo off
chcp 65001 >nul
cd /d "D:\Pustaka Quran Hadis\Pustaka\PustakaHadith"
title Bina PustakaHadith v1.1.0 (adaptif) - jangan tutup tetingkap ini
echo.
echo  ============================================================
echo   BINA PUSTAKAHADITH v1.1.0 (PyInstaller)
echo   Ambil masa 10-15 minit. JANGAN tutup tetingkap ini.
echo  ============================================================
echo.

".venv-build\Scripts\python.exe" -m PyInstaller PustakaHadith.spec --clean --noconfirm
set CODE=%ERRORLEVEL%

echo.
echo  ============================================================
if "%CODE%"=="0" (
    echo   SELESAI: exe baru siap.
) else (
    echo   GAGAL (exit code %CODE%). Lihat warning di atas.
)
echo  ============================================================
echo.
echo  Semak exe:
if exist "dist\PustakaHadith\PustakaHadith.exe" (
    echo   dist\PustakaHadith\PustakaHadith.exe
    for %%A in ("dist\PustakaHadith\PustakaHadith.exe") do echo   Tarikh: %%~tA   Saiz: %%~zA bytes
) else (
    echo   exe TIDAK wujud - build tak siap sepenuhnya.
)
echo.
pause
