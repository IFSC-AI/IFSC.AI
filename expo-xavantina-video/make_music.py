#!/usr/bin/env python3
"""Cama musical instrumental 128 BPM, com acentos nas viradas das cartelas."""
import numpy as np, json, wave

SR, BPM = 48000, 128.0
BEAT = 60.0 / BPM
BAR  = BEAT * 4
tl   = json.load(open("build/timeline.json"))
DUR  = tl["duracao"] + 0.9
N    = int(DUR * SR)
T    = np.arange(N) / SR

mix = np.zeros(N)
def put(buf, t0):
    i = int(t0 * SR)
    if i >= N: return
    j = min(N, i + len(buf))
    mix[i:j] += buf[:j - i]

def env(n, a, d, s, r, sus=1.0):
    """envelope ADSR em amostras"""
    a, d, r = max(1, int(a*SR)), max(1, int(d*SR)), max(1, int(r*SR))
    s = max(0, n - a - d - r)
    e = np.concatenate([
        np.linspace(0, 1, a),
        np.linspace(1, sus, d),
        np.full(s, sus),
        np.linspace(sus, 0, r)])
    return e[:n] if len(e) >= n else np.pad(e, (0, n - len(e)))

def kick(amp=1.0):
    n = int(0.34 * SR); t = np.arange(n) / SR
    f = 118 * np.exp(-t * 30) + 44                       # pitch drop
    body = np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t*7.5)
    click = (np.random.RandomState(1).randn(n) * np.exp(-t*180)) * 0.16
    return (body + click) * 0.95 * amp

def clap(amp=1.0, seed=3):
    n = int(0.30 * SR); t = np.arange(n) / SR
    r = np.random.RandomState(seed).randn(n)
    # três batidinhas curtas + cauda: timbre de palma
    out = np.zeros(n)
    for k, off in enumerate((0.0, 0.010, 0.021)):
        i = int(off*SR); out[i:] += r[:n-i] * np.exp(-np.arange(n-i)/SR*150) * (0.8**k)
    out += r * np.exp(-t*19) * 0.5
    b, a = _hp(1100)
    return _filt(out, b, a) * 0.42 * amp

def hat(closed=True, amp=1.0, seed=5):
    n = int((0.07 if closed else 0.26) * SR); t = np.arange(n) / SR
    r = np.random.RandomState(seed).randn(n)
    d = 95 if closed else 16
    b, a = _hp(7200)
    return _filt(r * np.exp(-t*d), b, a) * 0.22 * amp

def _hp(fc):
    x = np.exp(-2*np.pi*fc/SR)
    return np.array([(1+x)/2, -(1+x)/2]), np.array([1.0, -x])
def _lp(fc):
    x = np.exp(-2*np.pi*fc/SR)
    return np.array([1-x]), np.array([1.0, -x])
def _filt(sig, b, a):
    from scipy.signal import lfilter  # type: ignore
    return lfilter(b, a, sig)

# scipy pode não existir: filtro IIR de 1 polo na mão
try:
    import scipy.signal  # noqa
except ImportError:
    def _filt(sig, b, a):
        out = np.zeros_like(sig); prev_y = 0.0; prev_x = 0.0
        b0 = b[0]; b1 = b[1] if len(b) > 1 else 0.0; a1 = a[1]
        for i, x in enumerate(sig):
            y = b0*x + b1*prev_x - a1*prev_y
            out[i] = y; prev_y = y; prev_x = x
        return out

def saw(freq, n, detune=0.0):
    t = np.arange(n) / SR
    out = np.zeros(n)
    for k in range(1, 14):                                # saw por série harmônica
        out += np.sin(2*np.pi*freq*(1+detune)*k*t) / k
    return out * (2/np.pi) * 0.5

def note(freq, dur, kind="bass", amp=1.0, detune=0.0):
    n = int(dur * SR)
    if kind == "bass":
        sig = saw(freq, n) * 0.6 + np.sin(2*np.pi*freq*np.arange(n)/SR) * 0.6
        sig = _filt(sig, *_lp(420))
        e = env(n, 0.004, 0.05, 0, 0.06, sus=0.78)
    else:
        sig = sum(saw(freq, n, d) for d in (-0.006, 0.0, 0.006)) / 3
        sig = _filt(sig, *_lp(2600))
        e = env(n, 0.012, 0.09, 0, 0.18, sus=0.62)
    return sig * e * amp

def riser(dur, amp=0.5, seed=11):
    n = int(dur*SR); t = np.arange(n)/SR
    r = np.random.RandomState(seed).randn(n)
    sweep = np.linspace(500, 9000, n)
    out = _filt(r, *_hp(900)) * (t/dur)**2
    out += np.sin(2*np.pi*np.cumsum(sweep)/SR) * (t/dur)**3 * 0.25
    return out * amp

def crash(amp=0.5, seed=13):
    n = int(1.7*SR); t = np.arange(n)/SR
    r = np.random.RandomState(seed).randn(n)
    return _filt(r * np.exp(-t*2.6), *_hp(4200)) * 0.5 * amp

NOTE = lambda s: 440.0 * 2**((s-69)/12)
# Am - F - C - G : progressão alegre e familiar
PROG = [(57, [57,60,64]), (53, [57,60,65]), (48, [52,55,60]), (55, [55,59,62])]

# quando cada seção do vídeo começa (para variar a intensidade)
sc = tl["scenes"]
DAYS  = [s["start"] for s in sc if s["type"] == "day"]
FINAL = [s["start"] for s in sc if s["type"] == "final"][0]
DATES = sc[1]["start"]

nbars = int(DUR / BAR) + 1
for bar in range(nbars):
    t0 = bar * BAR
    if t0 > DUR: break
    root, chord = PROG[bar % 4]
    full = t0 >= DATES - 0.5                    # groove completo depois da abertura
    fim  = t0 >= FINAL
    for b in range(4):
        tb = t0 + b*BEAT
        if tb > DUR: break
        if full and not fim:
            put(kick(1.0 if b % 2 == 0 else 0.85), tb)
        elif fim and b % 2 == 0:
            put(kick(1.0), tb)
        if full and b in (1, 3):
            put(clap(0.9 if not fim else 1.0), tb)
        for h in range(2):                       # chimbais em colcheias
            th = tb + h*BEAT/2
            if th > DUR: break
            a = 0.55 if h == 0 else 0.34
            put(hat(True, a * (0.6 if not full else 1.0), seed=5 + (b*2+h) % 4), th)
        if full:                                 # baixo em colcheias
            for h in range(2):
                put(note(NOTE(root-12), BEAT/2*0.92, "bass",
                         0.50 if h == 0 else 0.34), tb + h*BEAT/2)
    # acordes: pad no tempo 1 e 3
    for b in (0, 2):
        if t0 + b*BEAT > DUR: break
        for i, nt in enumerate(chord):
            put(note(NOTE(nt), BEAT*1.9, "pad", (0.17 if full else 0.12) * (1 - i*0.12)),
                t0 + b*BEAT)

# acentos nas viradas de cartela
for d in DAYS:
    put(crash(0.55), d)
    put(riser(min(1.5, 1.5), 0.30), max(0, d - 1.5))
put(crash(0.7), FINAL)
put(riser(1.8, 0.34), max(0, FINAL - 1.8))
put(crash(0.5), DATES)

# fade final e normalização
mix /= max(1e-9, np.abs(mix).max()) / 0.92
fade = int(1.6*SR)
mix[-fade:] *= np.linspace(1, 0, fade)
mix[:int(0.05*SR)] *= np.linspace(0, 1, int(0.05*SR))

st = np.stack([mix, mix], 1)                      # leve alargamento estéreo
st[:, 0] = np.roll(st[:, 0], 12) * 0.98
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
with wave.open("build/musica.wav", "w") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print(f"build/musica.wav  {DUR:.2f}s  {nbars} compassos @ {BPM:.0f} BPM")
