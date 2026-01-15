@echo off
echo Starting Flask Backend Server...
echo.
echo Installing dependencies if needed...
pip install -r requirements.txt
echo.
echo Starting server on http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python backend_api.py
pause
