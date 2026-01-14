@echo off
echo.
echo ╔═══════════════════════════════════════════════════════════════════╗
echo ║                                                                   ║
echo ║    🌐 SCHEDULE CONFLICT DETECTION - WEB APPLICATION              ║
echo ║                                                                   ║
echo ╚═══════════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python not found. Please install Python first.
    pause
    exit /b 1
)
echo ✓ Python found

echo.
echo Checking Flask...
python -c "import flask; print('✓ Flask installed')" 2>nul
if errorlevel 1 (
    echo Installing Flask...
    pip install Flask==2.3.0 Werkzeug==2.3.0
)

echo.
echo ╔═══════════════════════════════════════════════════════════════════╗
echo ║                                                                   ║
echo ║  🚀 Starting Web Application...                                   ║
echo ║                                                                   ║
echo ║  📍 Open your browser and go to:                                 ║
echo ║                                                                   ║
echo ║     http://localhost:5000                                        ║
echo ║                                                                   ║
echo ║  Press CTRL+C to stop the server                                 ║
echo ║                                                                   ║
echo ╚═══════════════════════════════════════════════════════════════════╝
echo.

python app.py

pause
