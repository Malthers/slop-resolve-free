#!/usr/bin/env python3
"""
Script de instalacao e verificacao da ponte MasterEditorBridge no DaVinci Resolve.
Copia automaticamente o bridge_server.py para a pasta de Scripts/Utility do DaVinci.
"""

import os
import sys
import shutil
import platform
from pathlib import Path

# Configurar stdout para UTF-8 no Windows para suportar emojis sem erro de cp1252
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def get_utility_scripts_dir():
    """Detecta o diretorio de Scripts/Utility do DaVinci Resolve de acordo com o SO."""
    system = platform.system()
    if system == "Windows":
        appdata = os.environ.get("APPDATA")
        if not appdata:
            appdata = os.path.expanduser("~\\AppData\\Roaming")
        return Path(appdata) / "Blackmagic Design" / "DaVinci Resolve" / "Support" / "Fusion" / "Scripts" / "Utility"
    elif system == "Darwin": # macOS
        return Path.home() / "Library" / "Application Support" / "Blackmagic Design" / "DaVinci Resolve" / "Fusion" / "Scripts" / "Utility"
    else: # Linux
        return Path.home() / ".local" / "share" / "DaVinciResolve" / "Fusion" / "Scripts" / "Utility"

def install_bridge():
    src_file = Path(__file__).resolve().parent / "bridge" / "bridge_server.py"
    if not src_file.exists():
        print(f"[X] Erro: Arquivo fonte nao encontrado: {src_file}")
        return False

    dest_dir = get_utility_scripts_dir()
    try:
        dest_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"[X] Erro ao criar pasta de scripts do DaVinci ({dest_dir}): {e}")
        return False

    dest_file = dest_dir / "MasterEditorBridge.py"

    # Checar se ja existe e se o conteudo e identico
    is_updated = False
    if dest_file.exists():
        try:
            if dest_file.read_bytes() == src_file.read_bytes():
                print(f"[OK] Bridge ja esta instalado e atualizado em:\n   {dest_file}")
                return True
            else:
                is_updated = True
        except Exception:
            pass

    try:
        shutil.copy2(src_file, dest_file)
        action_verb = "atualizado" if is_updated else "instalado"
        print(f"[OK] MasterEditorBridge {action_verb} com sucesso no DaVinci Resolve!")
        print(f"Destino: {dest_file}")
        print(f"\nComo usar no DaVinci:")
        print(f"   Abra o DaVinci Resolve e acesse o menu:")
        print(f"   Workspace > Scripts > MasterEditorBridge\n")
        return True
    except Exception as e:
        print(f"[X] Falha ao copiar arquivo para {dest_file}: {e}")
        return False

if __name__ == "__main__":
    success = install_bridge()
    sys.exit(0 if success else 1)
