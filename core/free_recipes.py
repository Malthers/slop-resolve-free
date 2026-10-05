"""
Biblioteca de Receitas e Regras 100% Free para DaVinci Resolve.
Projetada para contornar recursos exclusivos do DaVinci Studio (sem marcas d'agua)
e pronta para receber novas tecnicas e caminhos customizados do usuario.
"""

# Regras estritas Anti-Studio para injecao no System Prompt
FREE_MODE_PROMPT_INSTRUCTIONS = """
## DIRETRIZES ESTRITAS: MODO 100% DAVINCI RESOLVE FREE (ANTI-MARCA D'AGUA)
Voce esta operando em um ambiente DaVinci Resolve FREE.
E ABSOLUTAMENTE PROIBIDO gerar codigos que invoquem plugins ou recursos exclusivos do Studio que geram marcas d'agua ou erros de licenca.

Recursos Proibidos (Studio) vs. Contorno Obrigatorio (Free):
1. Granulacao (Film Grain OFX):
   - NUNCA use o plugin Film Grain OFX do Studio.
   - CONTORNO NO FUSION: Crie um no `FastNoise` monocromatico com `SeetheRate` animado (ex: 0.05), conectado a um no `Merge` em modo de mesclagem Soft Light ou Overlay com Blend reduzido (0.15 a 0.25).

2. Brilho / Glow Studio:
   - NUNCA use Aperture Glow ou Studio Glow OFX.
   - CONTORNO NO FUSION: Use os nos nativos `SoftGlow` ou `FastGlow` com ganho ajustado.

3. Desfoque de Movimento (Motion Blur OFX):
   - NUNCA use o plugin de Motion Blur OFX da timeline.
   - CONTORNO NO FUSION: Ative o Motion Blur nativo nos nos de movimento:
     `tool.SetInput("MotionBlur", 1)`
     `tool.SetInput("Quality", 4)`
     `tool.SetInput("ShutterAngle", 180.0)`
     (Disponivel nativamente na aba Settings de Transform e Merge no Free).

4. Isolamento de Objeto / Mascaras (Magic Mask Neural Engine):
   - NUNCA use Magic Mask.
   - CONTORNO: Use Power Windows com rastreador na pagina Color, ou no Fusion use `DeltaKeyer`, `Polygon` ou `BSpline` com o Point Tracker nativo.

5. Reducao de Ruido (Temporal/Spatial NR):
   - NUNCA use reducao de ruido da Color Page que requer licenca Studio.
   - CONTORNO: Faca no Fusion com `RemoveNoise` nativo ou na Color Page com mascaras HSL atenuando altas frequencias em sombras.

6. Sobreposicao de Titulos e Efeitos:
   - NUNCA use `timeline.InsertTitleIntoTimeline()` pois ela corta a timeline e abre buracos na trilha.
   - CONTORNO: Sempre crie composicoes no Fusion dentro do clipe com `TextPlus` sobreposto via `Merge`, ou insira clipes de Fusion Composition em trilha superior sem fatiar o video original.

7. Matematica de Marcadores:
   - Os marcadores da timeline (`timeline.GetMarkers()`) retornam frames RELATIVOS ao inicio da timeline.
   - O frame absoluto de timecode de cada clipe e: `abs_frame = timeline.GetStartFrame() + rel_frame`.
   - Sempre use `timeline.GetStartFrame()` para sincronizar com precisao cirurgica.
"""

# Registro de receitas de nos Fusion prontas para uso
FUSION_FREE_RECIPES = {
    "text_plus_overlay": """
# Adiciona titulo TextPlus sobreposto sem cortar clipe
comp.StartUndo("Add Overlay Title")
comp.Lock()
try:
    media_out = comp.FindTool("MediaOut1")
    media_in = comp.FindTool("MediaIn1")
    
    text = comp.AddTool("TextPlus", -32768, -32768)
    text.SetInput("StyledText", "{text_content}")
    text.SetInput("Size", {size})
    text.SetInput("Red1", {red})
    text.SetInput("Green1", {green})
    text.SetInput("Blue1", {blue})
    text.SetInput("Alpha1", 1.0)
    
    merge = comp.AddTool("Merge", -32768, -32768)
    if media_in:
        merge.ConnectInput("Background", media_in)
    merge.ConnectInput("Foreground", text)
    
    # Animacao de fade/blend opcional
    if {fade_frames} > 0:
        merge.SetInput("Blend", 1.0, 0)
        merge.SetInput("Blend", 1.0, {duration_frames} - {fade_frames})
        merge.SetInput("Blend", 0.0, {duration_frames})
        
    if media_out:
        media_out.ConnectInput("Input", merge)
finally:
    comp.Unlock()
    comp.EndUndo(True)
""",

    "free_film_grain": """
# Granulacao de Filme 100% Free com FastNoise no Fusion
comp.StartUndo("Add Free Film Grain")
comp.Lock()
try:
    media_out = comp.FindTool("MediaOut1")
    media_in = comp.FindTool("MediaIn1")
    
    noise = comp.AddTool("FastNoise", -32768, -32768)
    noise.SetInput("Detail", 5.0)
    noise.SetInput("Contrast", 2.5)
    noise.SetInput("Scale", 50.0)
    noise.SetInput("SeetheRate", 0.15)
    noise.SetInput("Color1Red", 0.0)
    noise.SetInput("Color1Green", 0.0)
    noise.SetInput("Color1Blue", 0.0)
    noise.SetInput("Color2Red", 1.0)
    noise.SetInput("Color2Green", 1.0)
    noise.SetInput("Color2Blue", 1.0)
    
    merge_grain = comp.AddTool("Merge", -32768, -32768)
    merge_grain.SetInput("ApplyMode", "SoftLight")
    merge_grain.SetInput("Blend", 0.20)
    
    if media_in:
        merge_grain.ConnectInput("Background", media_in)
    merge_grain.ConnectInput("Foreground", noise)
    
    if media_out:
        media_out.ConnectInput("Input", merge_grain)
finally:
    comp.Unlock()
    comp.EndUndo(True)
""",

    "free_soft_glow": """
# Efeito de Brilho / SoftGlow 100% Free
comp.StartUndo("Add Free SoftGlow")
comp.Lock()
try:
    media_out = comp.FindTool("MediaOut1")
    media_in = comp.FindTool("MediaIn1")
    
    glow = comp.AddTool("SoftGlow", -32768, -32768)
    glow.SetInput("Gain", 0.4)
    glow.SetInput("GlowSize", 15.0)
    
    if media_in:
        glow.ConnectInput("Input", media_in)
    if media_out:
        media_out.ConnectInput("Input", glow)
finally:
    comp.Unlock()
    comp.EndUndo(True)
"""
}

# Dicionario extensivel onde novos caminhos enviados pelo usuario serao registrados
CUSTOM_USER_FREE_PATHS = {}

def register_custom_path(name: str, description: str, steps: list, code_template: str = ""):
    """Registra uma nova tecnica ou caminho Free fornecido pelo usuario."""
    CUSTOM_USER_FREE_PATHS[name] = {
        "description": description,
        "steps": steps,
        "code_template": code_template
    }
