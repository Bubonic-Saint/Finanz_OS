@echo off
setlocal enabledelayedexpansion
title Finanz-OS Setup - OneClick Edition

echo ======================================================
echo    FINANZ-OS: AUTOMATISCHE INSTALLATION
echo ======================================================
echo.

:: 1. PRÜFEN OB PYTHON INSTALLIERT IST
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python wurde nicht gefunden.
    echo [!] Lade Python Installer herunter...

    :: Nutzt PowerShell um den offiziellen Installer zu ziehen
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe' -OutFile 'python_installer.exe'"

    echo [!] Starte Installation...
    echo [WICHTIG] Bitte im Installer unbedingt "Add Python to PATH" anklicken!
    start /wait python_installer.exe

    del python_installer.exe
    echo [+] Python Setup beendet.
    echo [INFO] Bitte starte diese Batch-Datei jetzt noch einmal neu.
    pause
    exit
)

:: 2. VIRTUELLE UMGEBUNG (.venv) ERSTELLEN
if not exist ".venv" (
    echo [+] Erstelle virtuelle Umgebung... Dies kann einen Moment dauern...
    python -m venv .venv
)

:: 3. BIBLIOTHEKEN INSTALLIEREN
echo [+] Installiere/Aktualisiere Pakete (Pandas, psutil, etc.)...
.venv\Scripts\python.exe -m pip install --upgrade pip >nul
.venv\Scripts\pip install -r requirements.txt

:: 4. ORDNERSTRUKTUR SICHERSTELLEN
echo [+] Erstelle notwendige Datenordner...
for %%d in (data\input data\output data\archiv data\rules) do (
    if not exist "%%d" mkdir "%%d"
)

:: 5. DESKTOP-VERKNÜPFUNG ERSTELLEN
echo [+] Erstelle Verknuepfung auf dem Desktop...
set "TARGET_PATH=%~dp0Finanzen_Template.xlsm"
set "SHORTCUT_PATH=%userprofile%\Desktop\Finanz-OS.lnk"

powershell -Command "$s=(New-Object -COM WScript.Shell).CreateShortcut('%SHORTCUT_PATH%');$s.TargetPath='%TARGET_PATH%';$s.IconLocation='%TARGET_PATH%';$s.Save()"

echo.
echo ======================================================
echo    FERTIG! Setup erfolgreich abgeschlossen.
echo ======================================================
echo.
echo Du findest jetzt eine Verknuepfung namens "Finanz-OS"
echo auf deinem Desktop. Viel Erfolg beim Tracken!
echo.
pause