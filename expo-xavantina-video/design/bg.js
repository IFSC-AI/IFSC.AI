/* ---------- Fundo cinematográfico: brilhos, feixes de luz, bokeh e grão ---------- */
const W = 1920, H = 1080;

function mulberry(seed) {
  return function () {
    seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/* Partículas de bokeh (luzes de plateia) com parâmetros fixos por índice */
const BOKEH = (() => {
  const r = mulberry(7781), out = [];
  for (let i = 0; i < 90; i++) {
    out.push({
      x: r(), y: r(), rad: 3 + r() * 26, speed: 0.004 + r() * 0.022,
      drift: (r() - 0.5) * 0.05, phase: r() * Math.PI * 2,
      alpha: 0.10 + r() * 0.42, hue: r()
    });
  }
  return out;
})();

/* Tiles de grão pré-gerados — alternados por frame para dar textura de filme */
function makeGrain(n, size) {
  const tiles = [];
  for (let k = 0; k < n; k++) {
    const c = document.createElement('canvas');
    c.width = c.height = size;
    const x = c.getContext('2d'), img = x.createImageData(size, size), r = mulberry(1000 + k * 977);
    for (let i = 0; i < img.data.length; i += 4) {
      const v = 118 + (r() - 0.5) * 150;
      img.data[i] = img.data[i + 1] = img.data[i + 2] = v;
      img.data[i + 3] = 255;
    }
    x.putImageData(img, 0, 0);
    tiles.push(c);
  }
  return tiles;
}

const PALETTE = {
  pink:   [255,  46, 116],
  violet: [139,  61, 255],
  amber:  [255, 176,  31],
  gold:   [255, 210,  74],
  cyan:   [ 47, 224, 224]
};
const rgba = (c, a) => `rgba(${c[0]},${c[1]},${c[2]},${a})`;

/* O glow vai num canvas pequeno e sobe escalado: bloom suave e barato */
const GW = 480, GH = 270;

class Background {
  constructor(canvas) {
    this.ctx = canvas.getContext('2d', { alpha: false });
    this.glow = document.createElement('canvas');
    this.glow.width = GW; this.glow.height = GH;
    this.gctx = this.glow.getContext('2d');
    this.grain = makeGrain(6, 256);
  }

  /* feixes de palco varrendo a cena */
  beams(g, t, energy) {
    const beams = [
      { x: 0.20, base: -0.55, swing: 0.42, sp: 0.21, col: PALETTE.pink,   w: 0.085 },
      { x: 0.52, base:  0.10, swing: 0.50, sp: 0.16, col: PALETTE.violet, w: 0.105 },
      { x: 0.83, base:  0.55, swing: 0.40, sp: 0.25, col: PALETTE.amber,  w: 0.075 }
    ];
    g.globalCompositeOperation = 'lighter';
    for (const b of beams) {
      const ang = b.base + Math.sin(t * b.sp + b.x * 9) * b.swing;
      const ox = b.x * GW, oy = -GH * 0.16;
      const len = GH * 1.9, half = b.w * GW * (0.78 + energy * 0.5);
      const dx = Math.sin(ang), dy = Math.cos(ang);
      const px = -dy, py = dx;
      const tipx = ox + dx * len, tipy = oy + dy * len;
      const grd = g.createLinearGradient(ox, oy, tipx, tipy);
      const a = (0.30 + energy * 0.30);
      grd.addColorStop(0,    rgba(b.col, a));
      grd.addColorStop(0.45, rgba(b.col, a * 0.34));
      grd.addColorStop(1,    rgba(b.col, 0));
      g.fillStyle = grd;
      g.beginPath();
      g.moveTo(ox + px * half * 0.26, oy + py * half * 0.26);
      g.lineTo(ox - px * half * 0.26, oy - py * half * 0.26);
      g.lineTo(tipx - px * half, tipy - py * half);
      g.lineTo(tipx + px * half, tipy + py * half);
      g.closePath();
      g.fill();
    }
    g.globalCompositeOperation = 'source-over';
  }

  /* manchas de cor que respiram devagar atrás de tudo */
  blobs(g, t) {
    const spots = [
      { c: PALETTE.pink,   x: 0.18, y: 0.78, r: 0.62, sp: 0.071, a: 0.62 },
      { c: PALETTE.violet, x: 0.80, y: 0.26, r: 0.70, sp: 0.053, a: 0.56 },
      { c: PALETTE.amber,  x: 0.58, y: 0.90, r: 0.50, sp: 0.089, a: 0.40 },
      { c: PALETTE.cyan,   x: 0.92, y: 0.80, r: 0.34, sp: 0.101, a: 0.20 }
    ];
    g.globalCompositeOperation = 'lighter';
    for (let i = 0; i < spots.length; i++) {
      const s = spots[i];
      const cx = (s.x + Math.sin(t * s.sp + i * 2.1) * 0.06) * GW;
      const cy = (s.y + Math.cos(t * s.sp * 0.8 + i) * 0.05) * GH;
      const rr = s.r * GW * 0.5 * (1 + Math.sin(t * s.sp * 1.6 + i) * 0.08);
      const grd = g.createRadialGradient(cx, cy, 0, cx, cy, rr);
      grd.addColorStop(0,   rgba(s.c, s.a));
      grd.addColorStop(0.5, rgba(s.c, s.a * 0.26));
      grd.addColorStop(1,   rgba(s.c, 0));
      g.fillStyle = grd;
      g.fillRect(0, 0, GW, GH);
    }
    g.globalCompositeOperation = 'source-over';
  }

  draw(t, opts) {
    opts = opts || {};
    const dim = opts.dim == null ? 1 : opts.dim;      // escurece o fundo sob texto
    const flash = opts.flash || 0;                    // estouro de luz nas viradas
    // pulso no compasso (~128 BPM) para o fundo "respirar" junto com a música
    const beat = Math.pow(Math.max(0, Math.sin(t * Math.PI * 2 * (128 / 60) / 2)), 6);
    const energy = 0.22 + beat * 0.5;

    const g = this.gctx;
    g.globalCompositeOperation = 'source-over';
    g.fillStyle = '#07030E';
    g.fillRect(0, 0, GW, GH);
    this.blobs(g, t);
    this.beams(g, t, energy);

    const ctx = this.ctx;
    ctx.globalCompositeOperation = 'source-over';
    ctx.fillStyle = '#07030E';
    ctx.fillRect(0, 0, W, H);
    ctx.save();
    ctx.globalAlpha = 0.55 + 0.45 * dim;
    ctx.filter = 'blur(10px) saturate(1.18)';
    ctx.drawImage(this.glow, 0, 0, W, H);
    ctx.restore();

    /* bokeh nítido por cima do bloom */
    ctx.globalCompositeOperation = 'lighter';
    for (let i = 0; i < BOKEH.length; i++) {
      const b = BOKEH[i];
      let y = (b.y - t * b.speed) % 1; if (y < 0) y += 1;
      const x = (b.x + Math.sin(t * 0.3 + b.phase) * b.drift + 1) % 1;
      const cx = x * W, cy = y * H;
      const tw = 0.6 + 0.4 * Math.sin(t * 1.7 + b.phase * 3);
      const col = b.hue < 0.42 ? PALETTE.pink : (b.hue < 0.74 ? PALETTE.gold : PALETTE.cyan);
      const rr = b.rad * (1 + beat * 0.16);
      const grd = ctx.createRadialGradient(cx, cy, 0, cx, cy, rr);
      grd.addColorStop(0,   rgba(col, b.alpha * tw * dim));
      grd.addColorStop(0.4, rgba(col, b.alpha * tw * 0.3 * dim));
      grd.addColorStop(1,   rgba(col, 0));
      ctx.fillStyle = grd;
      ctx.beginPath(); ctx.arc(cx, cy, rr, 0, 6.2832); ctx.fill();
    }
    ctx.globalCompositeOperation = 'source-over';

    if (flash > 0) {
      ctx.fillStyle = `rgba(255,236,210,${0.52 * flash})`;
      ctx.fillRect(0, 0, W, H);
    }

    /* vinheta: fecha as bordas e joga o olho pro centro */
    const vg = ctx.createRadialGradient(W * 0.5, H * 0.48, H * 0.26, W * 0.5, H * 0.5, H * 1.02);
    vg.addColorStop(0, 'rgba(0,0,0,0)');
    vg.addColorStop(1, 'rgba(0,0,0,0.80)');
    ctx.fillStyle = vg;
    ctx.fillRect(0, 0, W, H);

    /* grão de filme: disfarça o banding dos gradientes */
    const tile = this.grain[Math.floor(t * 24) % this.grain.length];
    ctx.save();
    ctx.globalCompositeOperation = 'overlay';
    ctx.globalAlpha = 0.055;
    const off = (Math.floor(t * 24) * 37) % 256;
    for (let y = -off; y < H; y += 256) for (let x = -off; x < W; x += 256) ctx.drawImage(tile, x, y);
    ctx.restore();
  }
}
