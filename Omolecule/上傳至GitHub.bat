@echo off
echo ============================================
echo   Deploying Omolecule to GitHub Pages
echo ============================================
echo.

echo [1/3] Building the project (dist/)...
call npm run build
if errorlevel 1 (
  echo Build failed! Please check errors.
  pause
  exit /b 1
)

echo [2/3] Committing source code to main branch...
git add -A
git commit -m "update"
git push origin main

echo [3/3] Deploying to gh-pages branch...
set TMP_DEPLOY="%TEMP%\omolecule-deploy"
if exist %TMP_DEPLOY% rmdir /S /Q %TMP_DEPLOY%

git clone --branch gh-pages --single-branch . %TMP_DEPLOY% 2>nul || (
  mkdir %TMP_DEPLOY%
  cd /d %TMP_DEPLOY%
  git init
  git remote add origin https://github.com/julchung/Omolecule.git
  git fetch origin gh-pages
  git checkout gh-pages
)

cd /d %TMP_DEPLOY%
for /f "delims=" %%i in ('dir /b /a-d') do del "%%i" 2>nul
for /f "delims=" %%i in ('dir /b /ad /b ^| findstr /v "^\.git$"') do rmdir /S /Q "%%i" 2>nul

xcopy /E /Y /I "%~dp0dist\*" "." >nul
if errorlevel 1 (
  echo Copying files failed!
  cd /d "%~dp0"
  pause
  exit /b 1
)

git add -A
git commit -m "Deploy to gh-pages"
git push https://github.com/julchung/Omolecule.git HEAD:gh-pages --force
if errorlevel 1 (
  echo Push to gh-pages failed!
  cd /d "%~dp0"
  pause
  exit /b 1
)

cd /d "%~dp0"
rmdir /S /Q %TMP_DEPLOY% 2>nul

echo.
echo ============================================
echo   Successfully deployed to gh-pages!
echo ============================================
echo https://julchung.github.io/Omolecule/
echo.
pause
