@echo off
title Pakistani Sitcom Studio
cd /d "%~dp0"
echo ========================================================
echo        STARTING PAKISTANI SITCOM STUDIO (LOCAL)
echo ========================================================
echo URL: http://localhost:8000
echo.
python -m uvicorn studio.server:app --host 127.0.0.1 --port 8000 --reload
pause
