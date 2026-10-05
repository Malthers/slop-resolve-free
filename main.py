#!/usr/bin/env python3
"""
Ponto de entrada principal do MasterEditor DaVinci Resolve.
Inicia a interface grafica flutuante PyQt6.
"""

import sys
import os

# Adicionar diretorio raiz ao PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from ui.app import run_app

if __name__ == "__main__":
    run_app()
