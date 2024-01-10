@echo off
cd %~dp0

rem Add db.sqlite3 to the Git repository
git add db.sqlite3

rem Commit the change
git commit -m "Update db.sqlite3"

rem Push the change to the remote repository
git push

rem Fetch the code from GitHub, excluding db.sqlite3
git fetch origin master:master
git checkout master
git reset --hard origin/master
git rm -r --cached db.sqlite3

start cmd /k "python manage.py runserver"
start "" "http://localhost:8000"
