"""
Cliente HTTP para comunicacao com o MasterEditorBridge dentro do DaVinci Resolve.
Conecta em 127.0.0.1:8955.
"""

import requests
import json

BRIDGE_URL = "http://127.0.0.1:8955"

class ResolveBridgeClient:
    def __init__(self, base_url=BRIDGE_URL, timeout=4):
        self.base_url = base_url
        self.timeout = timeout

    def ping(self):
        """Verifica se a ponte interna no DaVinci Resolve esta ativa."""
        try:
            r = requests.get(f"{self.base_url}/ping", timeout=self.timeout)
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
        return None

    def get_state(self):
        """Obtem o estado completo da timeline, trilhas e marcadores resolvidos."""
        try:
            r = requests.get(f"{self.base_url}/state", timeout=self.timeout + 2)
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            return {"connected": False, "error": str(e)}
        return None

    def execute_code(self, code_str: str):
        """Envia codigo Python para ser executado no ambiente nativo do DaVinci Resolve."""
        try:
            payload = {"code": code_str}
            r = requests.post(
                f"{self.base_url}/execute",
                json=payload,
                timeout=30
            )
            if r.status_code == 200:
                return r.json()
            else:
                return {
                    "success": False,
                    "stdout": "",
                    "stderr": f"Erro HTTP {r.status_code}: {r.text}"
                }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Erro de comunicacao com a ponte: {str(e)}"
            }
