# Montar o vídeo no CapCut (projeto editável)

Tudo aqui está em **1920×1080, 30 fps, 64,16 s**. As camadas vêm separadas
justamente para você trocar/editar qualquer parte sem refazer nada.

## O que tem nesta pasta

| Arquivo | O que é |
|---|---|
| `fundo-animado.mp4` | O fundo em movimento (luzes, feixes, partículas), **sem nenhum texto** |
| `overlays/01..13_*.png` | Os grafismos de cada cena, **com fundo transparente** |
| `../audio/locucao.wav` | A locução tratada (equalizada e comprimida) |
| `../audio/musica-instrumental.m4a` | A cama musical 128 BPM |
| `legendas.srt` | Legendas sincronizadas — o CapCut importa direto |
| `folha-de-tempos.csv` | Entrada e saída exatas de cada cena |

## Montagem (5 passos)

1. **Novo projeto** → proporção **16:9**, 1080p, 30 fps.
2. **Faixa 1 (base):** arraste `fundo-animado.mp4`. Ele já tem os 64,16 s.
3. **Faixa 2 (fotos):** arraste a foto de cada banda e posicione nos tempos da
   `folha-de-tempos.csv` (coluna *entra/sai*). Deixe a foto **por baixo** do overlay.
4. **Faixa 3 (grafismos):** arraste os PNGs de `overlays/` na ordem, cada um no
   tempo da folha. A moldura da foto nos cards de artista é **vazada**, então a
   foto da faixa 2 aparece dentro dela.
5. **Áudio:** `locucao.wav` numa faixa e a música noutra. Se trocar por uma música
   da biblioteca do CapCut, deixe-a em torno de **−18 dB** e ative
   *Reduzir ruído/Ducking* para ela abaixar sob a voz.

> As legendas são opcionais: **Texto → Importar legendas → `legendas.srt`**.
> Vale a pena, porque a maioria assiste sem som nas redes.

## Onde entram as fotos das bandas

Na faixa 2, nestes trechos:

| Banda | Entra | Sai |
|---|---|---|
| Banda San Francisco | 12,55 s | 18,79 s |
| Banda Passarela | 18,79 s | 28,35 s |
| Felipe e Murilo | 30,03 s | 34,79 s |
| Banda Barbarella | 34,79 s | 40,79 s |
| Banda Som do Sul | 42,91 s | 49,51 s |

Enquadre em **retrato (3:4)**, porque a moldura é vertical. Nos cards 2 e 4
(Passarela e Barbarella) a moldura fica **à esquerda**; nos outros, à direita.

A janela mede **560 × 730 px**. Posição na tela (canto superior esquerdo da foto):

- moldura à direita (cards 1, 3 e 5): **x = 1242, y = 175**
- moldura à esquerda (cards 2 e 4): **x = 118, y = 175**

> Detalhe de acabamento: a moldura tem cantos arredondados e a foto é retangular,
> então sobra um fiapo de canto. Se quiser 100% limpo, aplique na foto
> **Máscara → Retângulo arredondado** com raio pequeno. São 5 segundos e some.

## Para refazer o vídeo inteiro com as fotos

Se preferir não montar à mão: coloque as fotos em `assets/fotos/` com os nomes
`san-francisco.jpg`, `passarela.jpg`, `felipe-e-murilo.jpg`, `barbarella.jpg`,
`som-do-sul.jpg` e rode de novo:

```bash
python3 build_timeline.py && node render.js && ./assemble.sh
```

O pipeline detecta as fotos sozinho e regenera os MP4 já com elas no lugar,
com Ken Burns (zoom lento) aplicado.
