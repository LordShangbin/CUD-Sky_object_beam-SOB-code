#!/bin/bash

echo "========================================"
echo "Starting Sky Object Beam System"
echo "========================================"
echo ""

echo "[1/2] Starting Flask API Server..."
cd V.2.1
gnome-terminal -- bash -c "python3 Sky_object_beam_Main_V.2.1.py; exec bash" 2>/dev/null || \
xterm -e "python3 Sky_object_beam_Main_V.2.1.py; bash" 2>/dev/null || \
konsole -e bash -c "python3 Sky_object_beam_Main_V.2.1.py; exec bash" 2>/dev/null || \
x-terminal-emulator -e bash -c "python3 Sky_object_beam_Main_V.2.1.py; exec bash" 2>/dev/null || \
{
    echo "Could not open terminal. Starting API in background..."
    python3 Sky_object_beam_Main_V.2.1.py &
    API_PID=$!
    echo "API Server PID: $API_PID"
}
cd ..

echo "Waiting 3 seconds for API to initialize..."
sleep 3

echo "[2/2] Starting Starpointer Web App..."
cd Starpointer
gnome-terminal -- bash -c "npm run dev; exec bash" 2>/dev/null || \
xterm -e "npm run dev; bash" 2>/dev/null || \
konsole -e bash -c "npm run dev; exec bash" 2>/dev/null || \
x-terminal-emulator -e bash -c "npm run dev; exec bash" 2>/dev/null || \
{
    echo "Could not open terminal. Starting web app in background..."
    npm run dev &
    WEB_PID=$!
    echo "Web App PID: $WEB_PID"
}
cd ..

echo ""
echo "========================================"
echo "System Started!"
echo "========================================"
echo ""
echo "Two terminals opened:"
echo "  1. Sky Object Beam API (port 5000)"
echo "  2. Starpointer Web (port 5173)"
echo ""
echo "Open browser to: http://localhost:5173"
echo ""
echo "Press Ctrl+C to exit this script"
echo "(The services will keep running)"
echo ""

# Keep script running
wait
