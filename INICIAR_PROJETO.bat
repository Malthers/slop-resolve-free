@echo off
chcp 65001 >nul
title MasterEditor — DaVinci Resolve Free Edition

echo =======================================================
echo    🎬 MasterEditor — Inicializador do Assistente IA
echo =======================================================
echo.

:: 1. Verificar se Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao foi encontrado no sistema!
    echo Instale o Python 3.10 ou superior e marque "Add to PATH".
    pause
    exit /b 1
)

:: 2. Criar ambiente virtual .venv se nao existir
if not exist ".venv" (
    echo [1/4] Criando ambiente virtual Python (.venv)...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERRO] Falha ao criar o ambiente virtual .venv.
        pause
        exit /b 1
    )
)

:: 3. Ativar ambiente virtual
echo [2/4] Ativando ambiente virtual...
call .venv\Scripts\activate.bat

:: 4. Instalar ou validar dependencias
echo [3/4] Verificando dependencias necessarias...
python -c "import PyQt6, litellm, requests" >nul 2>&1
if errorlevel 1 (
    echo Instalando pacotes (PyQt6, litellm, requests)...
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERRO] Falha ao instalar dependencias do requirements.txt.
        pause
        exit /b 1
    )
) else (
    echo Dependencias ja estao instaladas.
)

:: 5. Verificar e auto-instalar a ponte no DaVinci Resolve se necessario
echo [4/4] Verificando integracao com o DaVinci Resolve...
python install.py
echo.

:: 6. Iniciar a interface grafica do MasterEditor
echo =======================================================
echo    🟢 Iniciando Interface Grafica Flutuante...
echo =======================================================
echo.
python main.py

if errorlevel 1 (
    echo.
    echo [AVISO] A aplicacao foi encerrada com erro.
    pause
)
