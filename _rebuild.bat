@echo off
cd /d "D:\Pustaka Quran Hadis\Pustaka\PustakaHadith"
".venv-build\Scripts\python.exe" -m PyInstaller PustakaHadith.spec --clean --noconfirm
echo EXITCODE=%ERRORLEVEL%
pause
