# Vídeo de divulgação — Expo Xavantina 2027

Vídeo comercial da programação de shows, **1920×1080 (horizontal), 30 fps, 64 s**,
com locução em português do Brasil e cama musical.

## Entrega

```
entrega/
├─ expo-xavantina-shows-1080p.mp4          ← pronto para postar (locução + música)
├─ expo-xavantina-shows-SEM-MUSICA.mp4     ← só locução, para pôr música licenciada
├─ audio/
│  ├─ locucao.m4a / .wav                   ← locução tratada
│  └─ musica-instrumental.m4a              ← cama 128 BPM
└─ capcut/
   ├─ COMO-MONTAR-NO-CAPCUT.md             ← passo a passo
   ├─ fundo-animado.mp4                    ← fundo sem texto
   ├─ overlays/01..13_*.png                ← grafismos com fundo transparente
   ├─ legendas.srt                         ← legendas sincronizadas
   └─ folha-de-tempos.csv                  ← entrada/saída exatas de cada cena
```

## Locução

Gerada no ElevenLabs com a voz **"Locução para Propaganda"** (`rpNe0HOx7heUulPiOEaG`),
masculina, grave, de locutor comercial brasileiro — modelo `eleven_v4`.
O texto é o roteiro original, com números escritos por extenso para a leitura sair certa.

A sincronia das cartelas **não** foi estimada no olho: o áudio foi transcrito com
timestamps por palavra (`eleven_scribe_v1`) e cada cena foi ancorada no início real
da frase correspondente, com 0,25 s de antecedência para o texto chegar junto com a voz.

## Fotos das bandas

As molduras estão **vazias de propósito**. A política de rede desta sessão bloqueia
todos os hosts de imagem (Instagram, Wikimedia, YouTube, Unsplash, Pexels), então não
foi possível buscar as fotos. Para preencher, há dois caminhos:

1. **No CapCut:** veja `entrega/capcut/COMO-MONTAR-NO-CAPCUT.md` — os overlays têm a
   janela da moldura vazada, basta pôr a foto numa faixa por baixo.
2. **Refazendo o vídeo:** coloque os arquivos em `assets/fotos/` com os nomes
   `san-francisco`, `passarela`, `felipe-e-murilo`, `barbarella`, `som-do-sul`
   (`.jpg`, `.png` ou `.webp`) e rode o pipeline — ele detecta as fotos sozinho.

## Como reconstruir

```bash
python3 build_timeline.py      # timeline das cenas (lê assets/fotos/)
python3 make_music.py          # cama musical sincronizada com as viradas
node render.js                 # 1925 frames em build/frames
./assemble.sh                  # MP4 finais com áudio
node render_layers.js --mode=overlay   # PNGs transparentes p/ CapCut
node render_layers.js --mode=bg        # fundo sem texto
python3 make_srt.py            # legendas + folha de tempos
```

O visual é HTML/CSS/Canvas renderizado quadro a quadro pelo Chromium (Playwright),
o que permite tipografia e composição de verdade em vez de filtros de vídeo.

- `design/frame.html` — cenas e animações (`renderAt(t)` desenha um instante exato)
- `design/bg.js` — fundo: feixes de palco, bokeh, pulso no compasso, grão de filme
- `design/scenes.css` — tipografia e layout dos cartões

## Observações

- **Marca:** o lockup "EXPO XAVANTINA" é tipográfico. Se houver logo oficial,
  substitua em `design/frame.html` (bloco `#lockup`).
- **Música:** a cama é sintetizada aqui, livre de licença. Para algo mais próximo do
  sertanejo/baile, troque pela biblioteca do CapCut usando o MP4 `SEM-MUSICA`.
- **Horário da Passarela:** o roteiro dizia "meia-noite e meia, ou uma hora".
  No vídeo aparece `00H30` com "ou 01h" ao lado, para não perder a informação.
