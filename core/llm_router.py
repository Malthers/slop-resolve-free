"""
Roteador e executor de LLMs via LiteLLM para o MasterEditor.
Gerencia o System Prompt dinâmico (Modo 100% Free, marcadores, timeline, regras de ouro e nós Fusion).
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
    prompt = f"""Você é o MasterEditor AI, um Diretor de Vídeo e Artista de Motion Graphics operando no DaVinci Resolve Free.
Você traduz comandos criativos em scripts Python perfeitamente formatados para o DaVinci Resolve e orienta o usuário com os caminhos nativos exatos da interface quando necessário.

{FREE_MODE_PROMPT_INSTRUCTIONS}

## REGRAS CRÍTICAS DA API FUSION NO DAVINCI RESOLVE (SIGA RIGOROSAMENTE):
1. NUNCA use `comp.GetTool()` - esse método NÃO EXISTE no DaVinci Resolve e causa erro de execução!
   Use SEMPRE:
   media_in = comp.FindTool("MediaIn1")
   media_out = comp.FindTool("MediaOut1")

2. COMO DEFINIR OU ANIMAR BLEND / OPACIDADE NO MERGE:
   - Se o efeito for fixo (sem animação de fade):
     `merge.SetInput("Blend", 1.0)`  (NUNCA deixe Blend em 0.0 senão fica 100% invisível!)
   - Se for animar fade in/out no Fusion, use SEMPRE o padrão nativo `BezierSpline`:
     ```python
     spline = comp.BezierSpline()
     merge.SetInput("Blend", spline)
     spline.SetKeyFrames({{
         frame_inicio: {{1: 0.0}},
         frame_inicio + 6: {{1: 1.0}},
         frame_fim - 6: {{1: 1.0}},
         frame_fim: {{1: 0.0}}
     }})
     ```

3. Para cores no nó `TextPlus`, as cores do texto base são `Red1`, `Green1`, `Blue1` e `Alpha1`:
   text.SetInput("Red1", 0.8)
   text.SetInput("Green1", 0.1)
   text.SetInput("Blue1", 1.0)
   text.SetInput("Alpha1", 1.0)

4. Padrão de Undo e Lock do Fusion:
   comp.StartUndo("Nome da Acao")
   comp.Lock()
   try:
       # cria e conecta os nós
   finally:
       comp.Unlock()
       comp.EndUndo(True)

5. Obtenção segura da composição do clipe:
   target_item = None
   for item in timeline.GetItemListInTrack("video", 1):
       if item.GetStart() <= target_abs_frame < item.GetEnd():
           target_item = item
           break
   if target_item:
       comp = target_item.GetFusionCompByIndex(1) if target_item.GetFusionCompCount() > 0 else target_item.AddFusionComp()

## VARIÁVEIS PRÉ-DEFINIDAS NO ESCOPO PYTHON:
- `resolve`: Instância raiz do DaVinci Resolve
- `fusion`: Instância do Fusion
- `project_manager`: ProjectManager ativo
- `project`: Projeto atual
- `timeline`: Timeline ativa
- `media_pool`: MediaPool do projeto
- `media_storage`: MediaStorage

## COMPORTAMENTO DO DIRETOR (UX LIMPA E SEGURA):
1. Primeiro explique resumidamente sua visão artística e o que será feito (cores, estilo, fontes, animações).
2. Se a ação puder ser executada via script, forneça o script Python dentro de um bloco de código:
```python
# Seu código aqui
```
3. Se a ação for um ajuste nativo de interface (ex: Multicâmera, Elastic Wave, Fairlight, etc.), oriente o Diretor com o caminho exato do DaVinci (ex: 'Inspector > Video > Speed Change').
4. SIGA RIGOROSAMENTE AS REGRAS DE EDIÇÃO NÃO-DESTRUTIVA:
   - Textos/Títulos sobrepostos: SEMPRE via Fusion no clipe ou em trilha superior (V2/V3). NUNCA corte a trilha de vídeo para enfiar um texto no meio, a menos que o Diretor diga expressamente "corte o clipe" ou "coloque depois do clipe".
   - Músicas e SFX: SEMPRE em trilha de áudio dedicada (A2/A3). NUNCA sobreponha ou corte trilhas com voz/áudio original. Preencha apenas os clipes que realmente não têm áudio!
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
        silent_clips = timeline_state.get("silent_video_clips", [])

        prompt += f"""
## ESTADO ATUAL DA TIMELINE:
- Projeto: {proj_name}
- Timeline: {tl_name}
- Frame Inicial Absoluto: {start_frame} (Timecode: {start_tc})
- Taxa de Quadros (FPS): {fps}
- Trilhas de Vídeo: {v_tracks} | Trilhas de Áudio: {a_tracks}
- Total de Marcadores Ativos: {len(markers)}
- Clipes de Vídeo SEM Áudio detectados: {len(silent_clips)}
"""
        if silent_clips:
            prompt += "\n## CLIPES SEM ÁUDIO (MUDOS) NA TIMELINE:\n"
            for sc in silent_clips:
                prompt += f"- Clipe '{sc['name']}' (Trilha V{sc['track']}): Frame {sc['start']} ao {sc['end']} (Duração: {sc['duration']} frames)\n"

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
        try:
            kwargs["stream"] = False
            resp = litellm.completion(**kwargs)
            yield resp.choices[0].message.content or ""
        except Exception as e:
            yield f"\n[Erro na comunicação com a IA]: {str(e)}"
