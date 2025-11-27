# PowerShell script to initialize git and prepare for GitHub push
# Run this script after installing Git

Write-Host "Initializing Git repository..." -ForegroundColor Green
git init

Write-Host "Adding all files..." -ForegroundColor Green
git add .

Write-Host "Creating initial commit..." -ForegroundColor Green
git commit -m "Initial commit: Pet Adoption Django project with all critical fixes

- Fixed cart functionality and URL patterns
- Fixed admin logout (GET request support)
- Fixed user registration/login redirects
- Fixed user email field in admin
- Fixed pet type filter
- Added root-level cart URL
- Updated navigation links"

Write-Host "`n✅ Git repository initialized and committed!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "1. Create a new repository on GitHub (https://github.com/new)" -ForegroundColor Cyan
Write-Host "2. Copy the repository URL" -ForegroundColor Cyan
Write-Host "3. Run these commands:" -ForegroundColor Cyan
Write-Host "   git remote add origin YOUR_REPO_URL" -ForegroundColor White
Write-Host "   git branch -M main" -ForegroundColor White
Write-Host "   git push -u origin main" -ForegroundColor White

