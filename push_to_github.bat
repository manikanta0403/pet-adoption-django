@echo off
REM Batch script to initialize git and prepare for GitHub push
REM Run this script after installing Git

echo Initializing Git repository...
git init

echo Adding all files...
git add .

echo Creating initial commit...
git commit -m "Initial commit: Pet Adoption Django project with all critical fixes - Fixed cart functionality and URL patterns - Fixed admin logout - Fixed user registration/login redirects - Fixed user email field in admin - Fixed pet type filter"

echo.
echo Git repository initialized and committed!
echo.
echo Next steps:
echo 1. Create a new repository on GitHub (https://github.com/new)
echo 2. Copy the repository URL
echo 3. Run these commands:
echo    git remote add origin YOUR_REPO_URL
echo    git branch -M main
echo    git push -u origin main
pause

