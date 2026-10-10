@echo off
echo ============================================
echo   Building Omolecule to /dist folder
echo ============================================
echo.
echo Building... (this may take a minute)
call npm run build

if errorlevel 1 (
  echo.
  echo Build failed! Please check the error messages above.
  pause
  exit /b 1
)

echo.
echo ============================================
echo   Build Successful!
echo ============================================
echo Opening the "dist" folder for you...
echo Please drag and drop all files from this folder into GitHub.
echo.

:: Open the dist folder in Windows File Explorer
start "" "%~dp0dist"

pause
