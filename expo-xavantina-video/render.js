/* Renderiza os frames do vídeo abrindo o design no Chromium e fotografando quadro a quadro. */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const args = process.argv.slice(2);
  const testMode = args.includes('--test');
  const tl = JSON.parse(fs.readFileSync('build/timeline.json', 'utf8'));
  const outDir = testMode ? 'build/test' : 'build/frames';
  fs.rmSync(outDir, { recursive: true, force: true });
  fs.mkdirSync(outDir, { recursive: true });

  const browser = await chromium.launch({
    args: ['--no-sandbox', '--force-color-profile=srgb', '--font-render-hinting=none',
           '--disable-lcd-text', '--hide-scrollbars']
  });
  const page = await browser.newPage({
    viewport: { width: tl.w, height: tl.h }, deviceScaleFactor: 1
  });
  page.on('console', m => { if (m.type() === 'error') console.log('  [console]', m.text()); });
  page.on('pageerror', e => console.log('  [pageerror]', e.message));

  await page.goto('file://' + path.resolve('design/frame.html'), { waitUntil: 'load' });
  await page.evaluate(() => window.fontsReady());
  const n = await page.evaluate(tl => window.initTimeline(tl), tl);
  console.log(`cenas montadas: ${n}`);

  let times;
  if (testMode) {
    // um instante representativo por cena + duas viradas
    times = [];
    for (const s of tl.scenes) times.push(+(s.start + Math.min(1.5, (s.end - s.start) * 0.55)).toFixed(2));
    times.push(+(tl.scenes[2].start + 0.12).toFixed(2));   // flash da cartela de dia
    times.push(+(tl.scenes[3].start + 0.18).toFixed(2));   // virada p/ artista
  } else {
    times = [];
    const total = Math.round(tl.duracao * tl.fps);
    for (let i = 0; i < total; i++) times.push(i / tl.fps);
  }

  const t0 = Date.now();
  for (let i = 0; i < times.length; i++) {
    const t = times[i];
    await page.evaluate(t => window.renderAt(t), t);
    const name = testMode
      ? `t${String(t).replace('.', '_')}.jpg`
      : `f${String(i).padStart(5, '0')}.jpg`;
    await page.screenshot({ path: path.join(outDir, name), type: 'jpeg', quality: 95 });
    if (!testMode && (i % 120 === 0 || i === times.length - 1)) {
      const el = (Date.now() - t0) / 1000, fps = (i + 1) / el;
      const eta = (times.length - i - 1) / fps;
      console.log(`  ${i + 1}/${times.length}  ${fps.toFixed(1)} fps  faltam ~${eta.toFixed(0)}s`);
    }
  }
  await browser.close();
  console.log(`pronto: ${times.length} frames em ${outDir} (${((Date.now()-t0)/1000).toFixed(1)}s)`);
})();
