@echo off
copy "..\hip_main.dat" "public\hip_main.dat" /Y
if %errorlevel% equ 0 (
    echo ✓ Copied hip_main.dat to public folder
) else (
    echo ✗ Failed to copy hip_main.dat
    exit /b 1
)
