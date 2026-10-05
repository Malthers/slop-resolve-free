"""
Detector online de modelos de IA com filtro estrito.
Consulta as APIs dos provedores em tempo real e retorna apenas modelos
de raciocinio e geracao de codigo, com suporte especial a toda linha Gemini 3.x Flash.
"""

import requests
import re

def fetch_available_models(provider_name: str, api_key: str = None, api_base: str = None) -> list:
    models = []

    # 1. Google Gemini
    if provider_name == "Google Gemini":
        if not api_key:
            # Modelos padrao recomendados da linha Gemini 3.x e 2.5
            return [
                "gemini/gemini-3.8-flash",
                "gemini/gemini-3.7-flash",
                "gemini/gemini-3.6-flash",
                "gemini/gemini-3.5-flash",
                "gemini/gemini-3.5-flash-lite",
                "gemini/gemini-3.1-flash-lite",
                "gemini/gemini-2.5-flash",
                "gemini/gemini-2.5-pro",
                "gemini/gemini-2.0-flash"
            ]

        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        try:
            r = requests.get(url, timeout=8)
            if r.status_code == 200:
                data = r.json()
                forbidden_tokens = [
                    "image", "live", "tts", "transcribe", "robotics",
                    "computer-use", "lyria", "banana", "clip", "vision-preview",
                    "preview-10-2025", "preview-12-2025"
                ]

                for m in data.get("models", []):
                    name = m.get("name", "").replace("models/", "")
                    methods = m.get("supportedGenerationMethods", [])

                    # Deve suportar geracao de texto/conteudo
                    if "generateContent" not in methods:
                        continue

                    # Ignorar versoes antigas obsoletas 1.0 e 1.5
                    if name.startswith("gemini-1."):
                        continue

                    # Descartar tokens proibidos (imagem, audio, robotics, etc.)
                    name_lower = name.lower()
                    if any(tok in name_lower for tok in forbidden_tokens):
                        continue

                    # FILTRO ESTRITO: Deve ser flash ou pro (incluindo 3.1, 3.5, 3.6, 3.7, 3.8, etc.)
                    if "flash" in name_lower or "pro" in name_lower:
                        models.append(f"gemini/{name}")

                if models:
                    # Ordenar priorizando modelos 3.x e depois versoes mais altas
                    def gemini_sort_key(m_str):
                        val = 0.0
                        match = re.search(r"gemini-(\d+(?:\.\d+)?)", m_str)
                        if match:
                            try:
                                val = float(match.group(1))
                            except Exception:
                                pass
                        is_flash = 1 if "flash" in m_str else 0
                        return (val, is_flash)

                    models = sorted(list(set(models)), key=gemini_sort_key, reverse=True)
                    return models
        except Exception:
            pass

        # Fallback se a requisicao falhar
        return [
            "gemini/gemini-3.8-flash",
            "gemini/gemini-3.7-flash",
            "gemini/gemini-3.6-flash",
            "gemini/gemini-3.5-flash",
            "gemini/gemini-3.5-flash-lite",
            "gemini/gemini-3.1-flash-lite",
            "gemini/gemini-2.5-flash",
            "gemini/gemini-2.5-pro"
        ]

    # 2. OpenAI
    elif provider_name in ["OpenAI (ChatGPT)", "OpenAI"]:
        if not api_key:
            return ["gpt-4o", "gpt-4o-mini", "o3-mini", "o1"]

        headers = {"Authorization": f"Bearer {api_key}"}
        try:
            r = requests.get("https://api.openai.com/v1/models", headers=headers, timeout=8)
            if r.status_code == 200:
                data = r.json()
                for m in data.get("data", []):
                    mid = m.get("id", "")
                    if mid.startswith("gpt-4o") or mid.startswith("o1") or mid.startswith("o3") or mid.startswith("gpt-5"):
                        if not any(x in mid for x in ["realtime", "audio", "transcribe"]):
                            models.append(mid)
                if models:
                    return sorted(list(set(models)), reverse=True)
        except Exception:
            pass
        return ["gpt-4o", "gpt-4o-mini", "o3-mini", "o1"]

    # 3. OpenRouter
    elif provider_name == "OpenRouter":
        headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
        try:
            r = requests.get("https://openrouter.ai/api/v1/models", headers=headers, timeout=8)
            if r.status_code == 200:
                data = r.json()
                for m in data.get("data", []):
                    mid = m.get("id", "")
                    # Pegar modelos recomendados
                    if any(k in mid for k in ["gemini", "claude", "gpt-4o", "qwen", "deepseek"]):
                        models.append(f"openrouter/{mid}")
                if models:
                    return sorted(list(set(models))[:50])
        except Exception:
            pass
        return ["openrouter/google/gemini-2.5-flash", "openrouter/anthropic/claude-3.5-sonnet", "openrouter/deepseek/deepseek-chat"]

    # 4. Ollama (Local)
    elif provider_name == "Ollama":
        base = api_base or "http://localhost:11434"
        try:
            r = requests.get(f"{base}/api/tags", timeout=5)
            if r.status_code == 200:
                data = r.json()
                for m in data.get("models", []):
                    models.append(f"ollama/{m.get('name', '')}")
                if models:
                    return sorted(list(set(models)))
        except Exception:
            pass
        return ["ollama/llama3.2", "ollama/qwen2.5-coder", "ollama/mistral"]

    # 5. LM Studio (Local)
    elif provider_name == "LM Studio":
        base = api_base or "http://localhost:1234/v1"
        try:
            r = requests.get(f"{base}/models", timeout=5)
            if r.status_code == 200:
                data = r.json()
                for m in data.get("data", []):
                    models.append(m.get("id", ""))
                if models:
                    return sorted(list(set(models)))
        except Exception:
            pass
        return ["local-model"]

    return models
