@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
  set PY_CMD=py
) else (
  set PY_CMD=python
)

%PY_CMD% -m pip install --upgrade pip
%PY_CMD% -m pip install reportlab pyinstaller

%PY_CMD% -m PyInstaller --noconfirm --onefile --windowed --name QuizBacSVT --add-data "data;data" main.py

echo.
echo Build termine. EXE disponible dans: dist\QuizBacSVT.exe
pause
