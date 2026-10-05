@echo off
title MasterEditor - DaVinci Resolve Free Edition

echo =======================================================
echo    MasterEditor - Inicializador do Assistente IA
echo =======================================================
echo.

:: 1. Detectar comando Python funcional
set "PY_CMD="

where python >nul 2>&1
if %errorlevel% equ 0 set "PY_CMD=python"

if "%PY_CMD%"=="" (
    where py >nul 2>&1
    if %errorlevel% equ 0 set "PY_CMD=py -3"
)

if "%PY_CMD%"=="" (
    if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" set "PY_CMD=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
)
if "%PY_CMD%"=="" (
    if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" set "PY_CMD=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
)
if "%PY_CMD%"=="" (
    if exist "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" set "PY_CMD=%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
)

if "%PY_CMD%"=="" (
    echo [ERRO] Python nao foi encontrado no sistema!
    echo Certifique-se de que o Python 3.10+ esta instalado e marcado Add to PATH.
    pause
    exit /b 1
)

echo [OK] Python detectado: %PY_CMD%

:: 2. Criar ambiente virtual se nao existir
if not exist ".venv\Scripts\python.exe" (
    echo [1/4] Criando ambiente virtual Python .venv...
    %PY_CMD% -m venv .venv
)

:: 3. Definir Python do ambiente virtual
set "VENV_PY=.venv\Scripts\python.exe"
echo [2/4] Usando ambiente virtual .venv...

:: 4. Instalar ou validar dependencias
echo [3/4] Verificando dependencias necessarias...
%VENV_PY% -c "import PyQt6, litellm, requests" >nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando pacotes necessarios: PyQt6, litellm, requests...
    %VENV_PY% -m pip install --upgrade pip
    %VENV_PY% -m pip install -r requirements.txt
) else (
    echo [OK] Dependencias ja estao prontas.
)

:: 5. Verificar e auto-instalar a ponte no DaVinci Resolve
echo [4/4] Verificando integracao com o DaVinci Resolve...
%VENV_PY% install.py
echo.

:: 6. Iniciar a interface grafica do MasterEditor
echo =======================================================
echo    Iniciando Interface Grafica Flutuante...
echo =======================================================
echo.
%VENV_PY% main.py

if %errorlevel% neq 0 (
    echo.
    echo [AVISO] A aplicacao foi encerrada.
    pause
)
