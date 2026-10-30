@echo off
cd /d "%~dp0"
py -3 -c "import customtkinter" >nul 2>nul
if errorlevel 1 (
    echo Installing the CustomTkinter dependency...
    py -3 -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Could not install dependencies. Check Python and internet access.
        pause
        exit /b 1
    )
)
py -3 ambulance_route_finder.py
if errorlevel 1 pause
