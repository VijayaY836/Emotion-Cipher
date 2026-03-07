@echo off
echo Fixing large files in git repository...
echo.

REM Remove node_modules and venv from git tracking
echo Removing large files from git...
git rm -r --cached frontend/node_modules
git rm -r --cached backend/venv
git rm -r --cached backend/models

REM Add the updated gitignore
git add .gitignore

REM Commit the removal
echo Committing changes...
git commit -m "Remove node_modules, venv, and models from git tracking"

echo.
echo Done! Now you can push with: git push origin main
echo.
pause
