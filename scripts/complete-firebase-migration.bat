@echo off
REM Firebase Migration Completion Script for Windows
REM This script helps complete the remaining UUID to String conversions

echo.
echo Firebase Migration - Completion Helper
echo ==========================================
echo.

REM Check if we're in the project root
if not exist "backend" (
    echo Error: Please run this script from the project root directory
    exit /b 1
)

echo Checking for UUID references in DTOs and Controllers...
echo.

REM Check for UUID imports
findstr /S /M "import java.util.UUID" backend\src\main\java\com\contentgen\dto\*.java backend\src\main\java\com\contentgen\controllers\*.java 2>nul
if %ERRORLEVEL% EQU 0 (
    echo WARNING: Found UUID imports in DTOs or Controllers
    echo These files need to be updated:
    echo 1. Change 'import java.util.UUID;' - Remove this import
    echo 2. Change 'private UUID id;' - 'private String id;'
    echo 3. Change 'private UUID userId;' - 'private String userId;'
    echo 4. Change 'private UUID sessionId;' - 'private String sessionId;'
    echo 5. Change '@PathVariable UUID' - '@PathVariable String'
    echo.
) else (
    echo OK: No UUID imports found in DTOs and Controllers!
    echo.
)

echo Checking Firebase configuration...
echo.

REM Check if firebase-credentials.json exists
if exist "backend\firebase-credentials.json" (
    echo OK: Firebase credentials file found
) else (
    echo WARNING: Firebase credentials file not found
    echo    Please download from Firebase Console and save as:
    echo    backend\firebase-credentials.json
    echo.
)

REM Check if .env exists
if exist "backend\.env" (
    echo OK: Backend .env file found
) else (
    echo WARNING: Backend .env file not found
    if exist "backend\.env.example" (
        echo    Creating from .env.example...
        copy backend\.env.example backend\.env >nul
        echo OK: Created backend\.env from example
        echo    Please edit backend\.env with your Firebase project ID
    )
    echo.
)

REM Check .gitignore
findstr /C:"firebase-credentials.json" .gitignore >nul
if %ERRORLEVEL% EQU 0 (
    echo OK: .gitignore includes Firebase credentials
) else (
    echo WARNING: .gitignore doesn't include Firebase credentials
    echo    This should be added to .gitignore
)

echo.
echo Next Steps:
echo.
echo 1. Update DTOs and Controllers (if needed):
echo    - Open each file listed above
echo    - Replace UUID with String for id fields
echo.
echo 2. Set up Firebase:
echo    - Create project at https://firebase.google.com
echo    - Enable Firestore Database
echo    - Download credentials - backend\firebase-credentials.json
echo    - Update backend\.env with your project ID
echo.
echo 3. Build and test:
echo    cd backend
echo    mvnw.cmd clean install
echo    mvnw.cmd spring-boot:run
echo.
echo 4. Create Firestore indexes (after first run)
echo.
echo Documentation:
echo    - FIREBASE_SETUP.md - Complete setup guide
echo    - FIREBASE_MIGRATION_COMPLETE.md - Migration summary
echo    - FIREBASE_REMAINING_TASKS.md - Detailed task list
echo.
echo You're almost done! Estimated time remaining: 1 hour
echo.
pause
