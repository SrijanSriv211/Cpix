@echo off

if "%1" == "clean" (
    if exist bin\ (
        rmdir bin /S /Q
    )
)

if not exist bin\ (
    mkdir bin
)

pip install pyinstaller
pyinstaller.exe --icon="web\static\img\icon.png" --add-data "web\templates;templates" --add-data "web\static;static" --add-data "web\static\img;img" --add-data "data;data" --distpath bin\app.exe --hidden-import=tqdm --hidden-import=Flask --hidden-import=transformers --hidden-import=numpy --onedir app.py

rmdir dist /S /Q
rmdir build /S /Q
rmdir __pycache__ /S /Q

del app.spec
