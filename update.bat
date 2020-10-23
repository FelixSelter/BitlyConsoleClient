@echo off
git add --all
git status
git commit -m '%date%_%time%'
git push
pause