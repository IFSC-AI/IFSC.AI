#!/usr/bin/env python3
"""Monta a timeline das cenas a partir dos timestamps reais da locução."""
import json, os, pathlib

PAD_IN, PAD_OUT, LEAD, TAIL = 0.20, 1.00, 0.25, 1.00
SPEECH_END = 62.96

# início de cada parágrafo falado, medido na locução original
VOZ = [0.02, 4.64, 10.48, 12.60, 18.84, 28.40, 30.08,
       34.84, 40.84, 42.96, 49.56, 54.32, 58.16]

FOTOS = pathlib.Path("assets/fotos")
def foto(slug):
    """Usa a foto se o arquivo existir — o vídeo se reconstrói com fotos sem editar nada."""
    for ext in ("jpg", "jpeg", "png", "webp"):
        p = FOTOS / f"{slug}.{ext}"
        if p.exists():
            return f"../assets/fotos/{p.name}"
    return None

CENAS = [
    {"type": "intro"},
    {"type": "dates"},
    {"type": "day", "dia": "Sexta-feira", "num": "29", "data": "29 de janeiro de 2027"},
    {"type": "artist", "slug": "san-francisco", "nome": "Banda San Francisco",
     "tag": "Sexta · 29 de janeiro", "hora": "21H", "horaLabel": "A partir das",
     "durLabel": "Duração", "dur": "3 horas de show", "nomeSize": 112},
    {"type": "artist", "slug": "passarela", "nome": "Banda Passarela",
     "tag": "Sexta · madrugada", "hora": "00H30", "horaLabel": "A partir de",
     "durLabel": "ou 01h · duração", "dur": "3 horas de show", "nomeSize": 124, "flip": True},
    {"type": "day", "dia": "Sábado", "num": "30", "data": "30 de janeiro de 2027"},
    {"type": "artist", "slug": "felipe-e-murilo", "nome": "Felipe e Murilo",
     "tag": "Sábado · 30 de janeiro", "hora": "22H", "horaLabel": "A partir das",
     "durLabel": "Atração", "dur": "Grande show", "nomeSize": 124},
    {"type": "artist", "slug": "barbarella", "nome": "Banda Barbarella",
     "tag": "Sábado · meia-noite", "hora": "00H", "horaLabel": "À",
     "durLabel": "Duração", "dur": "3 horas de show", "nomeSize": 120, "flip": True},
    {"type": "day", "dia": "Domingo", "num": "31", "data": "31 de janeiro de 2027"},
    {"type": "artist", "slug": "som-do-sul", "nome": "Banda Som do Sul",
     "tag": "Domingo · 31 de janeiro", "hora": "20H", "horaLabel": "A partir das",
     "durLabel": "Encerramento", "dur": "2 a 3 horas de show", "nomeSize": 120},
    {"type": "big", "kicker": "São três dias de", "titulo": "Atrações imperdíveis",
     "sub": "Música boa e muita animação", "size": 136},
    {"type": "big", "kicker": "Marque os amigos", "titulo": "Venha fazer parte",
     "sub": "dessa festa", "size": 150},
    {"type": "final"},
]
assert len(CENAS) == len(VOZ), f"{len(CENAS)} cenas vs {len(VOZ)} parágrafos"

starts = [max(0.0, v + PAD_IN - LEAD) for v in VOZ]
total  = SPEECH_END + PAD_IN + TAIL
for i, c in enumerate(CENAS):
    c["start"] = round(starts[i], 3)
    c["end"]   = round(starts[i + 1] if i + 1 < len(starts) else total, 3)
    c["inD"], c["outD"] = 0.30, 0.22
    if c["type"] == "artist":
        c["foto"] = foto(c["slug"])

tl = {"fps": 30, "w": 1920, "h": 1080, "duracao": round(total, 3),
      "audio": {"pad_in": PAD_IN, "pad_out": PAD_OUT}, "scenes": CENAS}
json.dump(tl, open("build/timeline.json", "w"), ensure_ascii=False, indent=1)

print(f"duração do vídeo: {total:.2f}s  ({int(total*30)} frames @30fps)\n")
print(f"{'#':>2}  {'início':>7} {'fim':>7} {'dur':>6}  cena")
for i, c in enumerate(CENAS, 1):
    d = c["end"] - c["start"]
    rot = c.get("nome") or c.get("dia") or c.get("titulo") or c["type"]
    f = "" if c["type"] != "artist" else ("  [foto ✓]" if c.get("foto") else "  [sem foto]")
    print(f"{i:>2}  {c['start']:>7.2f} {c['end']:>7.2f} {d:>6.2f}  {c['type']:<7} {rot}{f}")
