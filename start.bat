@echo off
chcp 65001 >nul 2>&1
title AZX TOOLS - SelfBot Backup & Clone (2026)

:: Taille de fenêtre (largeur/hauteur)
mode con: cols=100 lines=40

color 0e

cls
echo.
echo.
echo   [38;2;255;165;0m   █████╗ ███████╗██╗  ██╗     ████████╗ ██████╗  ██████╗ ██╗     ███████╗
echo      ██╔══██╗╚══███╔╝██║  ██║     ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
echo      ███████║  ███╔╝ ███████║        ██║   ██║   ██║██║   ██║██║     ███████╗
echo      ██╔══██║ ███╔╝  ██╔══██║        ██║   ██║   ██║██║   ██║██║     ╚════██║
echo      ██║  ██║███████╗██║  ██║        ██║   ╚██████╔╝╚██████╔╝███████╗███████║
echo      ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝        ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝[0m
echo.
echo.
echo   [38;2;255;100;100m               AZX TOOLS - SelfBot Backup ^& Clone Serveur Discord[0m
echo   [38;2;255;215;0m                     Version éducative 2026 - Usage à tes risques[0m
echo.
echo   [38;2;200;200;255m   Ce script utilise un compte utilisateur (selfbot) → CONTRE LES ToS Discord[0m
echo   [38;2;200;200;255m   Risque très élevé de ban permanent, même pour quelques secondes[0m
echo.
echo   [38;2;255;165;0m   Appuie sur une touche seulement si tu as bien compris le risque[0m
echo.
pause >nul

cls
echo.
echo   [38;2;100;255;100mLancement de main.py ...[0m
echo.
python main.py
if %errorlevel% neq 0 (
    echo.
    echo   [38;2;255;80;80mErreur lors du lancement de main.py[0m
    echo   Vérifie que Python est installé et que main.py est dans le même dossier
    echo.
)
echo.
pause