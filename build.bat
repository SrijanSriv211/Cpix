@echo off

if "%1" == "clean" (
    if exist bin\ (
        rmdir bin /S /Q
    )
)

if not exist bin\ (
    mkdir bin\data bin\web
)

pyinstaller.exe --icon="web\static\img\icon.png" --add-data "web\templates;templates" --add-data "web\static;static" --add-data "web\static\img;img" --add-data "data;data" --distpath bin\app.exe --onefile app.py

copy data\* bin\data\*
copy web\* bin\web\*

rmdir dist /S /Q
rmdir build /S /Q
rmdir __pycache__ /S /Q

del app.spec
