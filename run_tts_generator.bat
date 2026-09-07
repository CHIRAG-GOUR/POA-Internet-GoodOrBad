@echo off
title TTS Generator - Internet Smart Adventure
echo.
echo Starting TTS Generator...
echo.
python "%~dp0generate_tts.py"
if errorlevel 1 (
    echo.
    echo Python not found! Trying with 'py' launcher...
    py "%~dp0generate_tts.py"
)
if errorlevel 1 (
    echo.
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python from python.org or use Anaconda.
    pause
)
