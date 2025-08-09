@echo off
echo Vérification de Python...

where python >nul 2>&1
if errorlevel 1 (
    echo Python n'est pas installé ou pas dans le PATH !
    pause
    exit /b 1
)

echo Installation des modules nécessaires...
python -m pip install --upgrade pip
python -m pip install pywin32 pynput

echo Modules installés, t'es ready pour lancer ton script !
pause
