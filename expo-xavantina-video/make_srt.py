#!/usr/bin/env python3
"""Gera SRT e folha de tempos a partir dos limites reais da locução."""
import json, csv

PAD = 0.20   # silêncio acrescentado no início do áudio
FRASES = [
 (0.02, 4.52, "Prepare-se para três dias de muita música,\nalegria e grandes shows!"),
 (4.64, 10.32, "De 29 a 31 de janeiro de 2027,\numa programação especial espera por você!"),
 (10.48, 12.56, "SEXTA-FEIRA, 29 DE JANEIRO!"),
 (12.60, 18.80, "A partir das 21 horas, tem o show da Banda San Francisco,\ncom três horas de muita música e animação!"),
 (18.84, 24.00, "E a festa continua madrugada adentro!\nA partir da meia-noite e meia, ou uma hora da manhã,"),
 (24.04, 28.32, "é a vez da Banda Passarela subir ao palco\npara mais três horas de show!"),
 (28.40, 30.00, "SÁBADO, 30 DE JANEIRO!"),
 (30.08, 34.80, "A partir das 22 horas, Felipe e Murilo\ncomandam a noite com um grande show!"),
 (34.84, 40.80, "E à meia-noite, a Banda Barbarella assume o palco\npara mais três horas de muita música e diversão!"),
 (40.84, 42.88, "E NO DOMINGO, 31 DE JANEIRO!"),
 (42.96, 49.52, "A partir das 20 horas, a Banda Som do Sul encerra\na programação com um show especial de duas a três horas!"),
 (49.56, 54.24, "São três dias de atrações imperdíveis,\nmúsica boa e muita animação!"),
 (54.32, 58.08, "Marque os amigos, prepare-se\ne venha fazer parte dessa festa!"),
 (58.16, 62.96, "De 29 a 31 de janeiro de 2027.\nEsperamos por você!"),
]
def ts(s):
    h = int(s//3600); m = int(s%3600//60); sec = s%60
    return f"{h:02d}:{m:02d}:{sec:06.3f}".replace(".", ",")

with open("entrega/capcut/legendas.srt", "w", encoding="utf-8") as f:
    for i, (a, b, txt) in enumerate(FRASES, 1):
        f.write(f"{i}\n{ts(a+PAD)} --> {ts(b+PAD)}\n{txt}\n\n")
print(f"entrega/capcut/legendas.srt  ({len(FRASES)} legendas)")

tl = json.load(open("build/timeline.json"))
with open("entrega/capcut/folha-de-tempos.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["#", "entra (s)", "sai (s)", "duracao (s)", "cena", "titulo na tela",
                "horario", "duracao do show", "arquivo de overlay", "foto a inserir"])
    for i, s in enumerate(tl["scenes"], 1):
        rotulo = s.get("nome") or s.get("dia") or s.get("titulo") or (
            "Abertura" if s["type"] == "intro" else
            "Datas" if s["type"] == "dates" else "Encerramento")
        w.writerow([i, f'{s["start"]:.2f}', f'{s["end"]:.2f}', f'{s["end"]-s["start"]:.2f}',
                    s["type"], rotulo, s.get("hora", ""), s.get("dur", ""),
                    f'overlays/{i:02d}_{s["type"]}.png',
                    f'assets/fotos/{s["slug"]}.jpg' if s.get("slug") else ""])
print("entrega/capcut/folha-de-tempos.csv")
