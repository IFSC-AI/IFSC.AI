/* Exporta as camadas separadas para edição: fundo animado e overlays com alpha. */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const mode = (process.argv.find(a => a.startsWith('--mode=')) || '').split('=')[1] || 'overlay';
  const tl = JSON.parse(fs.readFileSync('build/timeline.json', 'utf8'));
  const outDir = mode === 'bg' ? 'build/bgframes' : 'entrega/capcut/overlays';
  fs.mkdirSync(outDir, { recursive: true });

  const browser = await chromium.launch({
    args: ['--no-sandbox', '--force-color-profile=srgb', '--font-render-hinting=none',
           '--disable-lcd-text', '--hide-scrollbars']
  });
  const page = await browser.newPage({ viewport: { width: tl.w, height: tl.h }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.resolve('design/frame.html'), { waitUntil: 'load' });
  await page.evaluate(() => window.fontsReady());
  await page.evaluate(tl => window.initTimeline(tl), tl);
  await page.evaluate(m => window.setExportMode(m), mode);

  if (mode === 'bg') {
    const total = Math.round(tl.duracao * tl.fps);
    const t0 = Date.now();
    for (let i = 0; i < total; i++) {
      await page.evaluate(t => window.renderAt(t), i / tl.fps);
      await page.screenshot({ path: path.join(outDir, `f${String(i).padStart(5, '0')}.jpg`),
                              type: 'jpeg', quality: 93 });
      if (i % 300 === 0) console.log(`  fundo ${i}/${total}`);
    }
    console.log(`fundo: ${total} frames (${((Date.now()-t0)/1000).toFixed(0)}s)`);
  } else {
    // um PNG por cena, no instante em que a animação já assentou
    for (let i = 0; i < tl.scenes.length; i++) {
      const s = tl.scenes[i];
      const t = Math.min(s.start + 1.9, s.start + (s.end - s.start) * 0.85);
      await page.evaluate(t => window.renderAt(t), t);
      const name = `${String(i + 1).padStart(2, '0')}_${s.type}.png`;
      await page.screenshot({ path: path.join(outDir, name), type: 'png', omitBackground: true });
      console.log(`  ${name}  (t=${t.toFixed(2)}s)`);
    }
  }
  await browser.close();
})();
