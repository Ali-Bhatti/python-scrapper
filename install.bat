@echo off
echo Amazon Review Scraper - Windows Setup
echo ======================================

echo Installing Python dependencies...
pip install -r requirements.txt

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Dependencies installed successfully!
    echo.
    echo You can now use the scraper:
    echo   python amazon_review_scraper.py B08N5WRWNW
    echo   python amazon_review_scraper.py --help
    echo.
    echo Or run the test script:
    echo   python test_scraper.py
) else (
    echo.
    echo ❌ Failed to install dependencies.
    echo Please make sure Python and pip are installed correctly.
    echo.
    echo Manual installation:
    echo   pip install requests beautifulsoup4 lxml pandas fake-useragent python-dotenv
)

pause 