@echo off
title Larka & Larki Comedy Studio
cd /d "%~dp0"
echo ========================================================
echo        STARTING LARKA ^& LARKI COMEDY STUDIO (LOCAL)
echo ========================================================
echo URL: http://localhost:8001
echo.
python -m uvicorn studio.server:app --host 127.0.0.1 --port 8001 --reload
pause
