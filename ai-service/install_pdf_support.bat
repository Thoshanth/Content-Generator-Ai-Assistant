@echo off
echo ============================================================
echo PDF Export Support Installation for Windows
echo ============================================================
echo.

echo Step 1: Installing ReportLab (fallback PDF library)...
echo --------------------------------------------------------
pip install reportlab
if %errorlevel% neq 0 (
    echo ERROR: Failed to install ReportLab
    pause
    exit /b 1
)
echo ✓ ReportLab installed successfully
echo.

echo Step 2: Testing ReportLab...
echo --------------------------------------------------------
python -c "from reportlab.pdfgen import canvas; print('✓ ReportLab working')"
if %errorlevel% neq 0 (
    echo ERROR: ReportLab test failed
    pause
    exit /b 1
)
echo.

echo Step 3: Checking WeasyPrint (optional, requires GTK3)...
echo --------------------------------------------------------
python -c "from weasyprint import HTML; print('✓ WeasyPrint working')" 2>nul
if %errorlevel% neq 0 (
    echo ⚠ WeasyPrint not available (requires GTK3 runtime)
    echo.
    echo To install GTK3 for better PDF quality:
    echo 1. Download: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
    echo 2. Run the installer and check "Add to PATH"
    echo 3. Restart your terminal
    echo.
    echo For now, PDF export will use ReportLab (works fine!)
) else (
    echo ✓ WeasyPrint is available
)
echo.

echo ============================================================
echo Installation Complete!
echo ============================================================
echo.
echo PDF export is now available using:
if %errorlevel% neq 0 (
    echo - ReportLab ^(fallback, pure Python^)
) else (
    echo - WeasyPrint ^(preferred, better quality^)
    echo - ReportLab ^(fallback^)
)
echo.
echo You can now start the AI service:
echo   python main.py
echo.
pause
