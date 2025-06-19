@echo off
chcp 65001 >nul
color 0A
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    📱 Phone Lookup Tool 📱                    ║
echo ║                     Installation Script                      ║
echo ║                                                              ║
echo ║  Developer: Saudi Linux                                      ║
echo ║  Email: SaudiLinux7@gmail.com                                ║
echo ║                                                              ║
echo ║  ⚠️  FOR EDUCATIONAL PURPOSES ONLY ⚠️                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 🔧 Starting installation process...
echo.

REM Check if Python is installed
echo 🐍 Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo 📥 Please install Python from https://python.org
    echo 💡 Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo ✅ Python is installed
python --version
echo.

REM Check if pip is available
echo 📦 Checking pip installation...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is not available
    echo 📥 Installing pip...
    python -m ensurepip --upgrade
    if %errorlevel% neq 0 (
        echo ❌ Failed to install pip
        pause
        exit /b 1
    )
)

echo ✅ pip is available
pip --version
echo.

REM Upgrade pip
echo 🔄 Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install required packages
echo 📚 Installing required packages...
echo.

REM Core packages
echo 🔧 Installing core packages...
pip install requests>=2.28.0
if %errorlevel% neq 0 (
    echo ❌ Failed to install requests
    pause
    exit /b 1
)
echo ✅ requests installed

REM Optional packages for enhanced functionality
echo 🎨 Installing optional packages for enhanced functionality...

echo   📡 Installing httpx...
pip install httpx>=0.24.0
if %errorlevel% neq 0 (
    echo ⚠️  Warning: Failed to install httpx (optional)
) else (
    echo ✅ httpx installed
)

echo   🎨 Installing colorama...
pip install colorama>=0.4.6
if %errorlevel% neq 0 (
    echo ⚠️  Warning: Failed to install colorama (optional)
) else (
    echo ✅ colorama installed
)

echo   ✨ Installing rich...
pip install rich>=13.0.0
if %errorlevel% neq 0 (
    echo ⚠️  Warning: Failed to install rich (optional)
) else (
    echo ✅ rich installed
)

echo   🖱️  Installing click...
pip install click>=8.1.0
if %errorlevel% neq 0 (
    echo ⚠️  Warning: Failed to install click (optional)
) else (
    echo ✅ click installed
)

echo   📊 Installing pandas...
pip install pandas>=1.5.0
if %errorlevel% neq 0 (
    echo ⚠️  Warning: Failed to install pandas (optional)
) else (
    echo ✅ pandas installed
)

echo   📞 Installing phonenumbers...
pip install phonenumbers>=8.13.0
if %errorlevel% neq 0 (
    echo ⚠️  Warning: Failed to install phonenumbers (optional)
) else (
    echo ✅ phonenumbers installed
)

echo   🌍 Installing country-converter...
pip install country-converter>=0.7.7
if %errorlevel% neq 0 (
    echo ⚠️  Warning: Failed to install country-converter (optional)
) else (
    echo ✅ country-converter installed
)

echo   🕵️  Installing fake-useragent...
pip install fake-useragent>=1.4.0
if %errorlevel% neq 0 (
    echo ⚠️  Warning: Failed to install fake-useragent (optional)
) else (
    echo ✅ fake-useragent installed
)

echo   🌐 Installing beautifulsoup4...
pip install beautifulsoup4>=4.11.0
if %errorlevel% neq 0 (
    echo ⚠️  Warning: Failed to install beautifulsoup4 (optional)
) else (
    echo ✅ beautifulsoup4 installed
)

echo   📝 Installing pyyaml...
pip install pyyaml>=6.0
if %errorlevel% neq 0 (
    echo ⚠️  Warning: Failed to install pyyaml (optional)
) else (
    echo ✅ pyyaml installed
)

echo   📋 Installing loguru...
pip install loguru>=0.6.0
if %errorlevel% neq 0 (
    echo ⚠️  Warning: Failed to install loguru (optional)
) else (
    echo ✅ loguru installed
)

echo.
echo 📁 Creating necessary directories...
if not exist "results" mkdir results
if not exist "logs" mkdir logs
echo ✅ Directories created

echo.
echo 🧪 Testing installation...
echo.
echo 🔍 Testing core functionality...
python -c "import requests, json, re, os, time, logging; print('✅ Core modules imported successfully')"
if %errorlevel% neq 0 (
    echo ❌ Core modules test failed
    pause
    exit /b 1
)

echo 🔍 Testing configuration...
python -c "from config import DEVELOPER_INFO, APP_SETTINGS; print('✅ Configuration loaded successfully')"
if %errorlevel% neq 0 (
    echo ❌ Configuration test failed
    pause
    exit /b 1
)

echo 🔍 Testing phone lookup tool...
python -c "from phone_lookup import PhoneLookupTool; tool = PhoneLookupTool(); print('✅ Phone lookup tool initialized successfully')"
if %errorlevel% neq 0 (
    echo ❌ Phone lookup tool test failed
    pause
    exit /b 1
)

echo.
echo ✅ Installation completed successfully!
echo.
echo 📋 Usage Instructions:
echo ═══════════════════════
echo.
echo 🖥️  Command Line Version:
echo    python phone_lookup.py
echo.
echo 🖼️  GUI Version:
echo    python gui_version.py
echo.
echo 📁 Files Created:
echo    • phone_lookup.py     - Main command line tool
echo    • gui_version.py      - GUI version
echo    • config.py           - Configuration file
echo    • requirements.txt    - Package requirements
echo    • README.md           - Documentation
echo    • results/            - Results directory
echo    • logs/               - Logs directory
echo.
echo 📖 Documentation:
echo    Read README.md for detailed usage instructions
echo.
echo ⚠️  Important Reminders:
echo    • This tool is for educational purposes only
echo    • Respect privacy and legal boundaries
echo    • Use only for legitimate research
echo    • Contact developer for support
echo.
echo 👨‍💻 Developer: Saudi Linux
echo 📧 Email: SaudiLinux7@gmail.com
echo.
echo 🎉 Ready to use! Press any key to exit...
pause >nul