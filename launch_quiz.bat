@echo off
cd /d "%~dp0"
if exist "dist\QuizBacSVT.exe" (
  start "" "dist\QuizBacSVT.exe"
) else (
  echo EXE introuvable. Lancez d'abord build_exe.bat
  pause
)
