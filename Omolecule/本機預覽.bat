@echo off
echo ============================================
echo   Omolecule Local Preview Server
echo ============================================
echo.
echo Starting development server...
echo The browser will open shortly at: http://localhost:5173/Omolecule/
echo.
echo Close this window to stop the server.
echo ============================================
echo.

:: Wait 2 seconds then open browser
start "" cmd /c "timeout /t 2 >nul && start http://localhost:5173/Omolecule/"

:: Start Vite dev server in this window
call npm run dev

pause
