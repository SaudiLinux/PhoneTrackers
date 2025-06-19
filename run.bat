@echo off
chcp 65001 >nul
color 0B
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    📱 Phone Lookup Tool 📱                    ║
echo ║                      Quick Launcher                          ║
echo ║                                                              ║
echo ║  Developer: Saudi Linux                                      ║
echo ║  Email: SaudiLinux7@gmail.com                                ║
echo ║                                                              ║
echo ║  ⚠️  FOR EDUCATIONAL PURPOSES ONLY ⚠️                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 🚀 Phone Lookup Tool Launcher
echo ═══════════════════════════════
echo.
echo Please select an option:
echo.
echo [1] 🖥️  Run Command Line Version
echo [2] 🖼️  Run GUI Version
echo [3] 📖 View Documentation (README.md)
echo [4] 📁 Open Results Folder
echo [5] 🔧 Run Installation Script
echo [6] 📋 Show System Information
echo [7] 🧪 Test Installation
echo [8] ❌ Exit
echo.
set /p choice="Enter your choice (1-8): "

if "%choice%"=="1" goto run_cli
if "%choice%"=="2" goto run_gui
if "%choice%"=="3" goto view_readme
if "%choice%"=="4" goto open_results
if "%choice%"=="5" goto run_install
if "%choice%"=="6" goto show_info
if "%choice%"=="7" goto test_install
if "%choice%"=="8" goto exit

echo ❌ Invalid choice. Please try again.
pause
goto start

:run_cli
echo.
echo 🖥️  Starting Command Line Version...
echo ═══════════════════════════════════
echo.
if not exist "phone_lookup.py" (
    echo ❌ phone_lookup.py not found!
    echo 💡 Please make sure all files are in the correct directory
    pause
    goto start
)
python phone_lookup.py
if %errorlevel% neq 0 (
    echo.
    echo ❌ Error occurred while running the tool
    echo 💡 Check if Python and required packages are installed
    pause
)
goto start

:run_gui
echo.
echo 🖼️  Starting GUI Version...
echo ═══════════════════════════
echo.
if not exist "gui_version.py" (
    echo ❌ gui_version.py not found!
    echo 💡 Please make sure all files are in the correct directory
    pause
    goto start
)
python gui_version.py
if %errorlevel% neq 0 (
    echo.
    echo ❌ Error occurred while running the GUI
    echo 💡 Check if Python and tkinter are installed
    pause
)
goto start

:view_readme
echo.
echo 📖 Opening Documentation...
echo ═══════════════════════════
if exist "README.md" (
    start notepad README.md
) else (
    echo ❌ README.md not found!
    pause
)
goto start

:open_results
echo.
echo 📁 Opening Results Folder...
echo ═══════════════════════════
if not exist "results" mkdir results
start explorer results
goto start

:run_install
echo.
echo 🔧 Running Installation Script...
echo ═══════════════════════════════
if exist "install.bat" (
    call install.bat
) else (
    echo ❌ install.bat not found!
    pause
)
goto start

:show_info
echo.
echo 📋 System Information
echo ═══════════════════
echo.
echo 🖥️  Operating System:
systeminfo | findstr /C:"OS Name" /C:"OS Version"
echo.
echo 🐍 Python Information:
python --version 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python not found or not in PATH
) else (
    echo ✅ Python is available
    python -c "import sys; print(f'Python Path: {sys.executable}')"
)
echo.
echo 📦 Pip Information:
pip --version 2>nul
if %errorlevel% neq 0 (
    echo ❌ Pip not found
) else (
    echo ✅ Pip is available
)
echo.
echo 📁 Current Directory:
echo %CD%
echo.
echo 📄 Available Files:
dir /B *.py *.bat *.md *.txt 2>nul
echo.
echo 📂 Directories:
dir /AD /B 2>nul
echo.
pause
goto start

:test_install
echo.
echo 🧪 Testing Installation...
echo ═══════════════════════
echo.
echo 🔍 Testing Python modules...
python -c "import requests, json, re, os, time, logging; print('✅ Core modules OK')"
if %errorlevel% neq 0 (
    echo ❌ Core modules test failed
    pause
    goto start
)

echo 🔍 Testing configuration...
python -c "from config import DEVELOPER_INFO; print('✅ Configuration OK')"
if %errorlevel% neq 0 (
    echo ❌ Configuration test failed
    pause
    goto start
)

echo 🔍 Testing phone lookup tool...
python -c "from phone_lookup import PhoneLookupTool; print('✅ Phone lookup tool OK')"
if %errorlevel% neq 0 (
    echo ❌ Phone lookup tool test failed
    pause
    goto start
)

echo 🔍 Testing GUI components...
python -c "import tkinter; print('✅ GUI components OK')"
if %errorlevel% neq 0 (
    echo ❌ GUI components test failed
    pause
    goto start
)

echo.
echo ✅ All tests passed successfully!
echo 🎉 Your installation is working correctly!
echo.
pause
goto start

:exit
echo.
echo 👋 Thank you for using Phone Lookup Tool!
echo.
echo 👨‍💻 Developer: Saudi Linux
echo 📧 Email: SaudiLinux7@gmail.com
echo.
echo 🔒 Remember: Use responsibly and ethically!
echo.
echo Press any key to exit...
pause >nul
exit

:start
cls
color 0B
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    📱 Phone Lookup Tool 📱                    ║
echo ║                      Quick Launcher                          ║
echo ║                                                              ║
echo ║  Developer: Saudi Linux                                      ║
echo ║  Email: SaudiLinux7@gmail.com                                ║
echo ║                                                              ║
echo ║  ⚠️  FOR EDUCATIONAL PURPOSES ONLY ⚠️                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 🚀 Phone Lookup Tool Launcher
echo ═══════════════════════════════
echo.
echo Please select an option:
echo.
echo [1] 🖥️  Run Command Line Version
echo [2] 🖼️  Run GUI Version
echo [3] 📖 View Documentation (README.md)
echo [4] 📁 Open Results Folder
echo [5] 🔧 Run Installation Script
echo [6] 📋 Show System Information
echo [7] 🧪 Test Installation
echo [8] ❌ Exit
echo.
set /p choice="Enter your choice (1-8): "

if "%choice%"=="1" goto run_cli
if "%choice%"=="2" goto run_gui
if "%choice%"=="3" goto view_readme
if "%choice%"=="4" goto open_results
if "%choice%"=="5" goto run_install
if "%choice%"=="6" goto show_info
if "%choice%"=="7" goto test_install
if "%choice%"=="8" goto exit

echo ❌ Invalid choice. Please try again.
pause
goto start