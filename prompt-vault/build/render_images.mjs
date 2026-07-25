// Screenshot the 10 listing-image HTML files -> dist/etsy/*.png (2700x2025),
// plus a 570x428 thumbnail of the hero for the Etsy-thumbnail readability QA check.
import fs from 'fs';
import path from 'path';
import { createRequire } from 'module';
import { fileURLToPath } from 'url';

const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_PKG || '/opt/node22/lib/node_modules/playwright');

const here = path.dirname(fileURLToPath(import.meta.url));
const srcDir = path.join(here, 'images_html');
const outDir = path.join(here, '..', 'dist', 'etsy');
fs.mkdirSync(outDir, { recursive: true });

const files = fs.readdirSync(srcDir).filter(f => f.endsWith('.html')).sort();
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 2700, height: 2025 } });

for (const f of files) {
  await page.goto('file://' + path.join(srcDir, f), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  const out = path.join(outDir, f.replace('.html', '.png').replace(/^img/, ''));
  await page.screenshot({ path: out });
  console.log('shot', path.basename(out));
}

// Thumbnail readability check for the hero (Etsy search-grid size).
const thumb = await browser.newPage({ viewport: { width: 570, height: 428 } });
await thumb.goto('file://' + path.join(srcDir, 'img01_hero.html'), { waitUntil: 'networkidle' });
await thumb.evaluate(() => {
  document.body.style.transform = 'scale(' + 570 / 2700 + ')';
  document.body.style.transformOrigin = 'top left';
});
await thumb.screenshot({ path: path.join(outDir, 'qa_hero_thumbnail_570px.png') });
console.log('shot qa_hero_thumbnail_570px.png');

await browser.close();
