@echo off
rem Botao "Capturar WhatsApp": sobe o Docker e o OpenWA se precisar e roda a captura.
rem O atalho da area de trabalho aponta para este arquivo. A logica toda mora no capturar.py.
chcp 65001 >nul
title Capturar WhatsApp (OpenWA)
set "OPENWA=%~dp0..\..\..\..\..\repos-externos\OpenWA"
set n=0

docker info >nul 2>&1
if not errorlevel 1 goto pronto
echo Abrindo o Docker Desktop...
start "" "%ProgramFiles%\Docker\Docker\Docker Desktop.exe"
:espera
timeout /t 3 /nobreak >nul
docker info >nul 2>&1
if not errorlevel 1 goto pronto
set /a n+=1
if %n% lss 40 goto espera
echo O Docker nao subiu em 2 minutos. Abra o Docker Desktop e tente de novo.
pause
exit /b 1

:pronto
pushd "%OPENWA%"
docker compose -f docker-compose.dev.yml up -d
popd

py "%~dp0capturar.py" %*
echo.
pause
