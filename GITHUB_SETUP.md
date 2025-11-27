# GitHub Setup Instructions

## Quick Setup (After Installing Git)

### Option 1: Run the Script
1. Install Git from https://git-scm.com/download/win
2. Open PowerShell or Command Prompt in this directory
3. Run: `.\push_to_github.ps1` (PowerShell) or `push_to_github.bat` (CMD)

### Option 2: Manual Commands

```bash
# 1. Initialize git repository
git init

# 2. Add all files
git add .

# 3. Create initial commit
git commit -m "Initial commit: Pet Adoption Django project with all critical fixes"

# 4. Create repository on GitHub
# Go to https://github.com/new and create a new repository

# 5. Add remote (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# 6. Push to GitHub
git branch -M main
git push -u origin main
```

## What's Included

✅ All project files (excluding venv, db.sqlite3, __pycache__)
✅ All critical bug fixes:
- Cart functionality
- Admin logout
- User registration/login
- User email field in admin
- Pet type filter

## What's Excluded (.gitignore)

- `venv/` - Virtual environment
- `db.sqlite3` - Database file
- `__pycache__/` - Python cache
- `media/` - User uploaded files
- `.env` - Environment variables

## Need Help?

If Git is not installed:
1. Download from: https://git-scm.com/download/win
2. Install with default settings
3. Restart your terminal
4. Run the setup script again

