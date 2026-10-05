"""
Biblioteca de Receitas, Regras e Mapeamento de Caminhos 100% Free para DaVinci Resolve.
Contem o catalogo de tecnicas, navegacao de interface e contornos de recursos Studio.
"""

# Mapeamento Completo de Caminhos e Acoes no DaVinci Resolve (100% Free)
DAVINCI_FREE_WORKFLOWS_MAP = {
    "Alterar Velocidade do Video": "Inspector > Video > Speed Change",
    "Exclusao por Propagacao / Apagar espaco vazio": "Edit > Ripple Delete",
    "Sincronizar Audios Automaticamente": "Select clips > Right-click > Auto Align Clips > Based on Waveform",
    "Criar Clipe Multicamera": "Select clips > Right-click > Create New Multicam Clip Using Selected Clips",
    "Trocar Camera no Clipe Multicamera": "Right-click on multicam clip > Switch Multicam Clip Angle",
    "Achatar/Mesclar Clipe Multicamera": "Right-click on multicam clip > Flatten Multicam Clip",
    "Transicao Cruzada de Video": "Effects > Toolbox > Video Transitions > Cross Dissolve",
    "Transicao Deslizante de Video": "Effects > Toolbox > Video Transitions > Edge Wipe",
    "Texto Basico": "Effects > Toolbox > Titles > Text",
    "Modos de Mesclagem / Overlay": "Inspector > Video > Composite > Composite Mode",
    "Ajuste de Posicao, Zoom e Rotacao": "Inspector > Video > Transform",
    "Ativar Animacao / Keyframes": "Inspector > Video > [Property] > Click the diamond icon (Keyframe)",
    "Preencher Fundo Preto (Barras Pretas)": "Effects > Resolve FX Stylize > Blanking Fill",
    "Alterar Duracao de Varios Clipes": "Edit Page > Select clips > Right-click > Change Clip Duration (Enable Trim Edit Mode to Ripple Delete gaps)",
    "Copiar e Colar Transicoes": "Edit Page > Select Transition > Ctrl+C / Cmd+C > Click on splice point > Ctrl+V / Cmd+V",
    "Copiar e Colar Espacos Vazios (Gaps)": "Edit Page > Select Space > Right-click > Copy > Go to desired point > Right-click > Paste",
    "Velocidade Variavel / Speed Ramp": "Edit Page > Right-click Compound Clip > Change Clip Speed (turn off Pitch Correction) > Right-click > Retime Controls > Add Speed Points > Adjust Keyframe splines",
    "Efeito Aparecer / Surgir para Texto": "Edit Page > Effects > Video Transitions > Cross Dissolve > Ease In and Out",
    "Salvar Fontes Favoritas": "Edit Page > Effects > Text+ > Inspector > Font Drop-down > Click Font Browser Icon > Click Star to Favorite",
    "Reverter Animacao / Efeito Undraw": "Edit Page > Inspector > Speed Change > Click Backwards Arrow (Reverse Speed)",
    "Rodas de Cores / Claros, Medios e Escuros": "Color Page > Color Wheels > Primaries",
    "Curvas de Cor Customizadas": "Color Page > Curves > Custom Curves",
    "Adicionar Novo No de Cor": "Color Page > Nodes > Right-click > Add Node > Add Serial",
    "Adicionar No Invertido / Selecao Externa": "Color Page > Nodes > Right-click > Add Node > Add Outside",
    "Copiar Cor de Referencia de Outro Video": "Color Page > Select target clip > Right-click on reference clip > Shot Match to this Clip",
    "Mascaras de Corte e Foco / Power Windows": "Color Page > Window > [Select shape: Circle, Polygon, etc.]",
    "Rastreamento Automatico de Mascara": "Color Page > Tracker > Track Forward / Track Reverse",
    "Isolamento de Cor Especifica / Chroma": "Color Page > Qualifier > HSL Qualifier",
    "Gerenciamento de Espaco de Cor do Projeto": "Project Settings > Color Management > Color Science > DaVinci YRGB Color Managed",
    "Transformacao de Espaco de Cor via No / CST": "Effects > Open FX > Filters > Resolve FX Color > Color Space Transform",
    "Atribuir Espaco de Cor Original ao Clipe": "Media Pool > Right-click on clip > Input Color Space",
    "Deixar Video em Preto e Branco": "Color Page > RGB Mixer > Monochrome",
    "Controles de Camera RAW": "Color Page > Camera RAW (First icon below viewer)",
    "Rodas de Cores de Alta Faixa Dinamica": "Color Page > HDR Wheels",
    "Distorcao Seletiva de Cor / Teia de Cor": "Color Page > Color Warper",
    "Borrar Rosto / Censurar com Mosaico": "Effects > Open FX > Filters > Resolve FX Blur > Mosaic Blur",
    "Salvar Preset de Cor / Grab Still": "Color Page > Viewer > Right-click > Grab Still",
    "Habilitar Mapeamento de Tons / Dolby Vision": "Project Settings > Color Management > Dolby Vision > Enable Dolby Vision",
    "Alterar Cor de Animacoes Prontas": "Color Page > Primary Wheels > Gain > Adjust Center Dot",
    "Normalizar Niveis de Audio": "Right-click on audio clip > Normalize Audio Levels",
    "Normalizar Volume dos Dialogos": "Right-click on audio clip > Normalize Audio Levels > Target Level (ex: -10 dBFS)",
    "Alterar Audio de Estereo para Mono": "Right-click on audio clip > Clip Attributes > Audio > Format: Mono",
    "Visualizar Faixas de Video na aba Audio": "Fairlight > Timeline Options (Icone no topo esquerdo) > Video Tracks",
    "Reproduzir Audio em Looping": "Playback > Play Around/To > Play In to Out (ou botao Loop)",
    "Desativar Clipe Individual de Audio": "Tecla M (Mute/Unmute) ou Inspector > Audio > Desmarcar Clip Enable",
    "Mover Audio para Faixa Abaixo": "Timeline > Move Audio Track Destination Down (Alt + Ctrl + Seta para Baixo)",
    "Cortar Clipe de Audio com a Navalha": "Barra de Ferramentas > Razor Tool (Tecla B)",
    "Testar Efeito de Audio sem Substituir (Audition)": "Fairlight > Sound Library > Right-click on sound > Audition",
    "Copiar Audio para Camadas (Layering)": "View > Show Audio Track Layers > Alt + Arrastar o audio",
    "Alterar Velocidade do Audio (Elastic Wave)": "Right-click on audio clip > Elastic Wave",
    "Alterar Afinacao (Voz Fina/Grossa)": "Inspector > Audio > Pitch",
    "Efeito Chorus (Voz de Robo/Modulador)": "Effects > FairlightFX > Chorus",
    "Efeito Reverb (Voz na Catedral/Sala)": "Effects > FairlightFX > Reverb",
    "Ouvir Audio Atras da Parede / Abafado (EQ)": "Mixer > EQ (Equalizer) > Ativar Banda 6 > Reduzir Agudos (High Cut)",
    "Reducao de Ruido Constante / Hiss": "Effects > FairlightFX > Noise Reduction",
    "Remover Ruido Eletrico / Hum": "Effects > FairlightFX > De-Hummer",
    "Gerar Cache do Efeito de Audio": "Right-click on track or clip > Cache Audio Effects",
    "Exportar Audio com Efeito Renderizado": "Right-click on track > Bounce Audio Effects",
    "Remover Fundo Verde / Chroma Key": "Effects > Open FX > Filters > Resolve FX Key > 3D Keyer (ou DeltaKeyer no Fusion)",
    "Remover Reflexo Verde do Fundo / Despill": "Inspector > Effects > Open FX > 3D Keyer > Despill",
    "Mosaico de Videos / Colagem": "Effects > Open FX > Filters > Resolve FX Transform > Video Collage",
    "Atrasar Movimento de Clipes / Time Offset": "Fusion Page > Shift + Spacebar > Add Duplicate Node > Time Offset",
    "Efeito Caminhar por Dentro de um Texto (Bypass Free)": "Fusion Page > TextPlus Node com Keyframe > Duplicar Video > Mascara Bezier/BSpline rastreada com Point Tracker (dispensa Magic Mask pago) > Merge",
    "Efeito Tilt-Shift Blur (Bypass Free)": "Fusion Page > No Blur/Defocus conectado a uma mascara Rectangle com Soft Edge maximo e invertida (dispensa Tilt-Shift OFX Studio)",
    "Gerar Arquivo Proxy pelo Programa": "Media Pool > Right-click on clip > Generate Proxy Media",
    "Ativar Reproducao via Proxy": "Playback > Proxy Handling > Prefer Proxies",
    "Diminuir Resolucao da Timeline": "Playback > Timeline Proxy Resolution > Half / Quarter",
    "Trocar Imagem de Capa do Projeto / Poster Frame": "Media Pool > Double-click clip > Playhead no frame desejado > Right-click > Clip Operations > Set Project Poster Frame",
    "Abrir Duas Pastas no Media Pool Simultaneamente": "Media Pool > Menu de tres pontos > Dual Pane Media Pool",
    "Configuracoes de Exportacao Customizadas": "Deliver Page > Render Settings > Custom",
    "Exportar Clipes Separados / Dailies": "Deliver Page > Render Settings > Video > Render: Individual clips",
    "Inserir Marca d'agua ou Timecode na Tela": "Workspace > Data Burn-In > Custom Text"
}

# Diretrizes Estritas para o System Prompt
FREE_MODE_PROMPT_INSTRUCTIONS = """
## DIRETRIZES ESTRITAS: MODO 100% DAVINCI RESOLVE FREE (ANTI-MARCA D'AGUA)
Voce opera estritamente no DaVinci Resolve FREE.
E PROIBIDO sugerir ou injetar plugins exclusivos do Studio que gerem marcas d'agua ou erros de licenca.

Tabela de Equivalencias e Contornos Obrigatorios:
1. Tilt-Shift Blur:
   - O plugin OFX Tilt-Shift e Studio (pago).
   - CONTORNO NO FREE: No Fusion, use um no `Blur` ou `Defocus` associado a uma mascara de gradiente linear suave invertida, mantendo o meio nitido e as bordas desfocadas.
2. Isolamento de Pessoas / Text Walk-Through:
   - O Magic Mask e recurso pago do Studio.
   - CONTORNO NO FREE: No Fusion, crie uma mascara `Polygon` ou `BSpline` conectada a um `Point Tracker` ou use o `DeltaKeyer` se houver contraste suficiente.
3. Granulacao (Film Grain OFX Studio):
   - CONTORNO NO FREE: No Fusion, use `FastNoise` monocromatico animado com `SeetheRate` conectado a um `Merge` em modo Soft Light com blend suave (0.15 - 0.25).
4. Brilho / Glow Studio:
   - CONTORNO NO FREE: Use os nos nativos `SoftGlow` ou `FastGlow`.
5. Motion Blur OFX Studio:
   - CONTORNO NO FREE: Ative a aba nativa `Settings -> Motion Blur` em nos `Transform` ou `Merge` no Fusion.
6. Reducao de Ruido na Color Page (NR Studio):
   - CONTORNO NO FREE: Use o no `RemoveNoise` no Fusion ou o plugin nativo `FairlightFX > Noise Reduction` para audio.

======================================================================
## REGRAS DE OURO DA EDICAO SEGURA E NAO-DESTRUTIVA (OBRIGATORIO SEGUIR):
======================================================================

1. REGRA SUPREMA DE TEXTOS E TITULOS (SOBREPOSICAO LIMPA):
   - Quando o Diretor pedir para adicionar texto, titulo ou legenda em determinado tempo ou sobre um clipe:
     * REGRA 1A (FUSION - RECOMENDADO): Crie a sobreposicao no Fusion do proprio clipe usando `TextPlus` conectado a um `Merge` com entrada `MediaIn1` no Background. O tempo e controlado por keyframes em `Merge.Blend` sem mexer na duracao do clipe!
     * REGRA 1B (TRILHA SUPERIOR): Se for inserir um elemento de texto na timeline, adicione-o SEMPRE em uma TRILHA SUPERIOR (ex: V2, V3 acima do video).
     * NUNCA use InsertTitleIntoTimeline() fatiando a trilha V1 onde esta o video (isso quebra o clipe no meio, desloca o restante e cria buracos pretos!).
   - QUANDO E PERMITIDO CORTAR OU INSERIR NA MESMA TRILHA:
     * APENAS quando o Diretor disser explicitamente: "corte o video", "coloque um texto DEPOIS do clipe", "divida o clipe no segundo X", "fatie a timeline". Nesses casos expressos, e somente neles, a divisao e permitida.

2. REGRA SUPREMA DE AUDIO E MUSICA (PRESERVACAO TOTAL DE DIALOGOS):
   - Quando o Diretor pedir para adicionar musica de fundo ou efeitos sonoros (SFX):
     * NUNCA insira musica na trilha A1 onde estao os dialogos ou o som original da gravacao.
     * Crie ou utilize SEMPRE uma NOVA TRILHA DEDICADA de audio (ex: Trilha A2 ou A3, rotulada para Musica).
     * Se o pedido for "adicionar musica nos clipes que estao sem audio":
       A IA DEVE inspecionar a timeline, mapear os intervalos EXATOS de frames onde nao ha audio correspondente na trilha A1, e preencher APENAS esses espacos vazios na trilha de musica, JAMAIS fatiando, silenciando ou sobrescrevendo os clipes que ja contem voz/audio!
     * NUNCA aplique ripple delete ou delete automatico de audio que faca a timeline perder a sincronia entre imagem e som.

3. MATEMATICA PRECISA DE MARCADORES:
   - Calcule sempre o frame absoluto com `abs_frame = timeline.GetStartFrame() + rel_marker_frame`.
   - Se for aplicar efeito ou texto no ponto do marcador, sincronize o tempo exato com `abs_frame`.

Voce tambem conhece todos os 72+ atalhos e caminhos nativos da interface do DaVinci Resolve (Inspector, Color Page, Fairlight, Fusion, Deliver) e orienta o usuario com precisao passo a passo quando a acao for manual.
"""

# Receitas de Nos Fusion Prontas
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

    "free_tilt_shift": """
comp.StartUndo("Add Free Tilt-Shift")
comp.Lock()
try:
    media_out = comp.FindTool("MediaOut1")
    media_in = comp.FindTool("MediaIn1")
    
    blur = comp.AddTool("Blur", -32768, -32768)
    blur.SetInput("XBlurSize", 12.0)
    blur.SetInput("YBlurSize", 12.0)
    
    mask = comp.AddTool("RectangleMask", -32768, -32768)
    mask.SetInput("Width", 1.0)
    mask.SetInput("Height", 0.25)
    mask.SetInput("SoftEdge", 0.20)
    mask.SetInput("Invert", 1)
    
    blur.ConnectInput("EffectMask", mask)
    if media_in:
        blur.ConnectInput("Input", media_in)
    if media_out:
        media_out.ConnectInput("Input", blur)
finally:
    comp.Unlock()
    comp.EndUndo(True)
"""
}

def get_workflow_path(action_name: str) -> str:
    """Retorna o caminho exato de menus no DaVinci para uma determinada acao."""
    return DAVINCI_FREE_WORKFLOWS_MAP.get(action_name, "")
