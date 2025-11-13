@echo off
REM demo.bat - Script demo tra cứu nhanh

echo ============================================
echo   DEMO LOOKUP TOOL - II.2
echo ============================================
echo.

cd /d "%~dp0"

echo [DEMO 1] Tra cuu cau thu: Mohamed Salah
echo.
python lookup.py --name "Mohamed Salah"
echo.
echo Nhan phim bat ky de tiep tuc...
pause > nul

echo.
echo ============================================
echo.
echo [DEMO 2] Tra cuu cau lac bo: Liverpool
echo.
python lookup.py --club Liverpool
echo.
echo Nhan phim bat ky de tiep tuc...
pause > nul

echo.
echo ============================================
echo.
echo [DEMO 3] Tra cuu cau thu: Erling Haaland
echo.
python lookup.py --name "Erling Haaland"
echo.
echo Nhan phim bat ky de ket thuc...
pause > nul

echo.
echo ============================================
echo   HOAN THANH DEMO!
echo ============================================
echo.
echo Kiem tra ket qua tai: ..\..\..\..\Output\Output_II\
echo.
pause
