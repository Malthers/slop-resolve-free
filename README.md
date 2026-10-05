# 🎬 slop-resolve-free

> **Assistente de Direção de IA para DaVinci Resolve focado 100% no Modo Gratuito (Free), com interface gráfica flutuante, escaneamento dinâmico de marcadores e receitas nativas sem marca d\'água.**

Desenvolvido por **[Malthers](https://github.com/Malthers)**.

---

## 🤝 Créditos e Agradecimento ao Projeto Original

Este projeto é um fork evolutivo e especializado construído a partir do excelente trabalho de **[meigo](https://github.com/meigo)** no repositório original [slop-resolve](https://github.com/meigo/slop-resolve).

Enquanto o projeto original estabeleceu o conceito inovador de controlar o DaVinci Resolve via CLI em linguagem natural, o **slop-resolve-free** foi reestruturado para superar as limitações do **DaVinci Resolve Free** no Windows, transformar o terminal em uma **interface gráfica moderna flutuante**, e garantir que qualquer efeito solicitado seja construído **sem marcas d\'água da versão Studio**.

---

## 🚀 Principais Melhorias Implementadas nesta Edição

### 1. 🛡️ 100% Focado no DaVinci Resolve Free (Sem Bloqueios de API)
- No Windows, a versão Free do DaVinci Resolve bloqueia conexões externas diretas via script.
- **A Solução:** Criamos uma **Ponte HTTP Interna** (MasterEditorBridge.py) que roda dentro do próprio DaVinci (Workspace > Scripts > MasterEditorBridge). Ela executa no processo nativo com permissões totais e expõe uma API local ultrarrápida em 127.0.0.1:8955.

### 2. 🎨 Política Anti-Studio (Zero Marcas d\'Água)
- Se uma IA comum tentar aplicar efeitos Studio (como *Film Grain OFX*, *Face Refinement*, *Voice Isolation*, *Magic Mask* ou *Temporal Noise Reduction*), o DaVinci estampa a marca d\'água de compra e trava a renderização.
- O **slop-resolve-free** possui um conjunto de regras e receitas em nós do **Fusion** e da **Color Page** que contornam os recursos pagos:
  - **Granulação:** FastNoise monocromático animado via Merge (Soft Light / Overlay) sem marca d\'água.
  - **Glow Cinematográfico:** Nós nativos SoftGlow / FastGlow.
  - **Motion Blur:** Ativação na aba Settings -> Motion Blur nativa de qualquer nó Transform ou Merge.
  - **Títulos e Overlays:** Inserção não-destrutiva sem fatiar clipes nem abrir buracos na timeline.

### 3. 🎯 Varredura Inteligente de Marcadores (🎯 Varrer Marcadores)
- Leitura dinâmica do início da timeline com 	imeline.GetStartFrame().
- Converte os frames relativos dos marcadores em frames absolutos de timecode, identificando exatamente qual clipe de vídeo está sob cada marcador e aplicando títulos ou efeitos com precisão cirúrgica de frames.

### 4. 🪟 Interface Gráfica Flutuante Always-on-Top (PyQt6)
- Substitui o uso exclusivo por linha de comando por uma janela elegante que flutua sobre a interface do DaVinci Resolve.
- Paleta de cores oficial do DaVinci Resolve (Dark Theme #181818, acentos em laranja #f05a28 e azul #4a90e2).

### 5. 🎬 Clean UX (O Usuário é o Diretor)
- O chat não exibe centenas de linhas de código técnico Python para poluir a tela.
- A IA responde como um Diretor Artístico, explicando o plano e as escolhas criativas.
- O código é capturado em segundo plano e executado apenas após a confirmação no botão **[✅ Aprovar e Executar no DaVinci]**.

### 6. 🧠 Suporte Completo à Família Gemini 3.x Flash e Modelos Modernos
- Suporte nativo e detector com filtro estrito para os novos modelos:
  - **Gemini 3.8 Flash**
  - **Gemini 3.7 Flash**
  - **Gemini 3.6 Flash**
  - **Gemini 3.5 Flash** e **3.5 Flash Lite**
  - **Gemini 3.1 Flash Lite**
  - Modelos Pro da linha 3.x e 2.5
  - Suporte adicional a **OpenAI** (GPT-4o, o1, o3-mini), **OpenRouter**, **Ollama** e **LM Studio**.
  - Filtro rigoroso: descarta automaticamente endpoints de imagem, TTS, robotics e transcrição.

### 7. ⚡ Inicializador de 1 Clique (INICIAR_PROJETO.bat)
- Cria o ambiente virtual .venv automaticamente se não existir.
- Instala todas as dependências necessárias.
- Verifica e instala/atualiza automaticamente o script da ponte na pasta de utilitários do DaVinci:
  %APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Utility\MasterEditorBridge.py
- Inicia a interface gráfica pronta para uso.

---

## 🛠️ Como Usar

### 1. Pré-requisitos
- **Windows 10 ou 11**
- **Python 3.10 ou superior** instalado e adicionado ao PATH.
- **DaVinci Resolve** (versão Free 18, 19 ou superior) aberto.

### 2. Inicialização Rápida
Dê dois cliques no arquivo:
`cmd
INICIAR_PROJETO.bat
`

### 3. Conectando ao DaVinci Resolve
1. No DaVinci Resolve, acesse o menu superior:
   **Workspace > Scripts > MasterEditorBridge**
2. A janela do **MasterEditor** mostrará instantaneamente:
   🟢 DaVinci Resolve Conectado com o nome do seu projeto e timeline ativos.
3. Clique em **⚙️ Configurar IA** para informar sua chave de API (Gemini, OpenAI, etc.) e escolher o seu modelo favorito.
4. Comece a interagir! Use comandos livres como:
   - *'Crie uma vinheta com fade nos primeiros 3 segundos'*
   - *'Aplique granulação de cinema no clipe selecionado'*
   - *'Clique em 🎯 Varrer Marcadores para analisar os pontos da sua timeline'*

---

## 📄 Licença

Este projeto é distribuído sob os termos da licença **MIT**, preservando os direitos e créditos originais de **meigo** (2025) e as melhorias e adaptações desenvolvidas por **Malthers** (2026). Consulte o arquivo LICENSE para mais detalhes.
