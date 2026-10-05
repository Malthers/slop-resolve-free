"""
Roteador e executor de LLMs via LiteLLM para o MasterEditor.
Gerencia o System Prompt dinamico (Modo 100% Free, marcadores, timeline, caminhos de interface e nos Fusion).
"""

import os
import re
import json
from pathlib import Path
from core.free_recipes import FREE_MODE_PROMPT_INSTRUCTIONS, DAVINCI_FREE_WORKFLOWS_MAP

CONFIG_DIR = Path.home() / ".resolve-agent"
CONFIG_FILE = CONFIG_DIR / "config.json"

def get_config():
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "provider": "Google Gemini",
        "model": "gemini/gemini-3.8-flash",
        "api_key": os.environ.get("GEMINI_API_KEY", "")
    }

def save_config(cfg: dict):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2), encoding="utf-8")

def build_system_prompt(timeline_state: dict = None) -> str:
    prompt = f"""Você é o MasterEditor AI, um Diretor de Vídeo e Artista de Motion Graphics operando no DaVinci Resolve.
Você traduz comandos criativos em scripts Python perfeitamente formatados para o DaVinci Resolve e orienta o usuário com os caminhos nativos exatos da interface quando necessário.

{FREE_MODE_PROMPT_INSTRUCTIONS}

## VARIÁVEIS PRÉ-DEFINIDAS NO ESCOPO PYTHON:
- `resolve`: Instância raiz do DaVinci Resolve
- `fusion`: Instância do Fusion
- `project_manager`: ProjectManager ativo
- `project`: Projeto atual
- `timeline`: Timeline ativa
- `media_pool`: MediaPool do projeto
- `media_storage`: MediaStorage

## COMPORTAMENTO DO DIRETOR (UX LIMPA):
1. Primeiro explique resumidamente sua visão artística e o que será feito (cores, estilo, fontes, animações).
2. Se a ação puder ser executada via script, forneça o script Python dentro de um bloco de código:
```python
# Seu código aqui
```
3. Se a ação for um ajuste nativo de interface (ex: Multicâmera, Elastic Wave, Fairlight, etc.), oriente o Diretor com o caminho exato do DaVinci (ex: 'Inspector > Video > Speed Change').
4. NUNCA faça cortes destrutivos na timeline com InsertTitleIntoTimeline(). Para títulos e efeitos sobrepostos, use sempre nós do Fusion (TextPlus, Merge, Blend, Transform) ou Fusion Composition em faixa superior.
5. Mantenha os prints informativos para confirmar cada ação no console.
"""

    if timeline_state and timeline_state.get("connected"):
        tl_name = timeline_state.get("timeline_name") or "Sem Timeline"
        proj_name = timeline_state.get("project_name") or "Sem Projeto"
        start_frame = timeline_state.get("timeline_start_frame", 0)
        start_tc = timeline_state.get("timeline_start_timecode", "01:00:00:00")
        fps = timeline_state.get("frame_rate", 24.0)
        v_tracks = timeline_state.get("video_tracks", 0)
        a_tracks = timeline_state.get("audio_tracks", 0)
        markers = timeline_state.get("markers", [])

        prompt += f"""
## ESTADO ATUAL DA TIMELINE:
- Projeto: {proj_name}
- Timeline: {tl_name}
- Frame Inicial Absoluto: {start_frame} (Timecode: {start_tc})
- Taxa de Quadros (FPS): {fps}
- Trilhas de Vídeo: {v_tracks} | Áudio: {a_tracks}
- Total de Marcadores Ativos: {len(markers)}
"""
        if markers:
            prompt += "\n## MARCADORES MAPEADOS NA TIMELINE:\n"
            for m in markers:
                rel_f = m.get("relative_frame")
                abs_f = m.get("absolute_frame")
                name = m.get("name") or "Sem nome"
                note = m.get("note") or ""
                color = m.get("color")
                matched = m.get("matched_clip")
                clip_info = f" -> Clipe: '{matched['name']}' (Trilha V{matched['track']})" if matched else " -> Sem clipe embaixo"
                prompt += f"- [Frame Rel: {rel_f} | Frame Abs: {abs_f}] Cor: {color} | '{name}': {note}{clip_info}\n"

    return prompt

def extract_code_blocks(text: str) -> str:
    """Extrai blocos de código python da resposta do modelo."""
    matches = re.findall(r"```(?:python)?\s*\n(.*?)```", text, re.DOTALL)
    if matches:
        return "\n\n".join(matches).strip()
    return ""

def call_llm_stream(messages: list, config: dict = None, timeline_state: dict = None):
    """
    Chama litellm com streaming.
    Se o streaming falhar por socket ou timeout, faz fallback automático para non-streaming.
    """
    import litellm

    cfg = config or get_config()
    model = cfg.get("model", "gemini/gemini-3.8-flash")
    api_key = cfg.get("api_key")
    api_base = cfg.get("api_base")

    # Injetar api_key no ambiente se necessário
    if api_key:
        if "gemini" in model.lower():
            os.environ["GEMINI_API_KEY"] = api_key
        elif "gpt" in model.lower() or "o1" in model.lower() or "o3" in model.lower():
            os.environ["OPENAI_API_KEY"] = api_key
        elif "openrouter" in model.lower():
            os.environ["OPENROUTER_API_KEY"] = api_key

    sys_prompt = build_system_prompt(timeline_state)
    full_messages = [{"role": "system", "content": sys_prompt}] + messages

    kwargs = {
        "model": model,
        "messages": full_messages,
        "stream": True,
        "timeout": 45
    }
    if api_base:
        kwargs["api_base"] = api_base
    if api_key:
        kwargs["api_key"] = api_key

    try:
        response = litellm.completion(**kwargs)
        for chunk in response:
            content = chunk.choices[0].delta.content or ""
            if content:
                yield content
    except Exception as stream_err:
        # Fallback transparente sem streaming
        try:
            kwargs["stream"] = False
            resp = litellm.completion(**kwargs)
            yield resp.choices[0].message.content or ""
        except Exception as e:
            yield f"\n[Erro na comunicação com a IA]: {str(e)}"
