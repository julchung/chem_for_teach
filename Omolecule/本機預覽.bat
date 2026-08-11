@echo off
chcp 65001 >nul
title Omolecule 本機預覽

cd /d "%~dp0"

echo ============================================
echo   Omolecule 本機預覽伺服器
echo ============================================
echo.
echo 正在啟動開發伺服器...
echo 伺服器就緒後請開啟: http://localhost:5173/Omolecule/
echo.
echo 關閉此視窗即可停止伺服器。
echo ============================================
echo.

:: 等待 2 秒後自動開啟瀏覽器
start "" cmd /c "timeout /t 2 >nul && start http://localhost:5173/Omolecule/"

:: 啟動 Vite 開發伺服器（前景執行，Ctrl+C 停止）
npm run dev

pause
