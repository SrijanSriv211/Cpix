@echo off

if "%1" == "clean" (
    if exist bin (
        rmdir bin /S /Q
    )
)

if not exist bin/ (
    mkdir bin
)

pyinstaller.exe --icon="web/static/img/icon.ico" --add-data "web/templates;templates" --add-data "web/static;static" --add-data "data;data" --distpath bin --onefile app.py

rem rmdir /s /q dist
rmdir /s /q build
rmdir /s /q __pycache__

del main.spec
