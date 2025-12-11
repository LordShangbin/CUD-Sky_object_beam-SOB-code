@echo off
echo ========================================
echo Starting Sky Object Beam System
echo ========================================
echo.

echo [1/2] Starting Flask API Server...
start "Sky Object Beam API" cmd /k "cd V.2.1 && py .\Sky_object_beam_Main_V.2.1.py"

echo Waiting 3 seconds for API to initialize...
timeout /t 3 /nobreak > nul

echo [2/2] Starting Starpointer Web App...
start "Starpointer Web" cmd /k "cd Starpointer && npm run dev"

echo.
echo ========================================
echo System Started!
echo ========================================
echo.
echo Two windows opened:
echo   1. Sky Object Beam API (port 5000)
echo   2. Starpointer Web (port 5173)
echo.
echo Open browser to: http://localhost:5173
echo.
echo Press any key to close this window...
echo (The services will keep running)
pause > nul
