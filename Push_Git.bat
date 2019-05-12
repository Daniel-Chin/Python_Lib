@echo off
echo Pushing...
git add -A
git commit -m "Auto upload"
git push https://github.com/Daniel-Chin/Python_Lib master
pause
