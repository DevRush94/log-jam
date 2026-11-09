@echo off
cd /d "%~dp0"
title Log Jam Server
echo ===================================================
echo   LOG JAM: CLOUD SAVE SERVER (PORT 8000)
echo ===================================================
python server.py
pause
