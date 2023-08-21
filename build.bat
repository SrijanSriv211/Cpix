@echo off

if "%1" == "clean" (
    if exist bin (
        rmdir bin /S /Q
    )
)

if not exist bin/ (
    mkdir bin
)

pyinstaller.exe --icon="web/static/img/icon.ico" --add-data "web/templates;templates" --add-data "web/static;static" --add-data "data;data" --distpath bin/app.exe --onefile app.py

copy data\* bin\data\*
copy web\* bin\web\*

rem rmdir /s /q dist
rem rmdir /s /q build
rem rmdir /s /q __pycache__

rem del app.spec
