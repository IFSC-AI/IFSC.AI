#!/usr/bin/env bash
# Junta os frames renderizados com as trilhas de áudio e gera os MP4 finais.
set -euo pipefail
cd "$(dirname "$0")"
DUR=64.16
mkdir -p entrega entrega/audio entrega/capcut

enc() { # <dir de frames> <wav> <saida>
  ffmpeg -hide_banner -loglevel error -y \
    -framerate 30 -i "$1/f%05d.jpg" -i "$2" \
    -map 0:v -map 1:a \
    -c:v libx264 -preset slow -crf 19 -pix_fmt yuv420p \
    -profile:v high -level 4.1 -x264-params "keyint=60:min-keyint=30" \
    -c:a aac -b:a 192k -ar 48000 -ac 2 \
    -movflags +faststart -shortest -t "$DUR" "$3"
}

echo "1/3  vídeo com locução + música"
enc build/frames build/audio_mix.wav entrega/expo-xavantina-shows-1080p.mp4
echo "2/3  vídeo só com locução (para pôr música licenciada no CapCut)"
enc build/frames build/audio_voz.wav entrega/expo-xavantina-shows-SEM-MUSICA.mp4

echo "3/3  áudios separados"
ffmpeg -hide_banner -loglevel error -y -i build/audio_voz.wav \
  -c:a aac -b:a 192k entrega/audio/locucao.m4a
ffmpeg -hide_banner -loglevel error -y -i build/musica.wav \
  -c:a aac -b:a 192k -t "$DUR" entrega/audio/musica-instrumental.m4a
cp build/audio_voz.wav entrega/audio/locucao.wav

echo
for f in entrega/*.mp4 entrega/audio/*; do
  printf '%-58s %7s  ' "$f" "$(du -h "$f" | cut -f1)"
  ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$f"
done
