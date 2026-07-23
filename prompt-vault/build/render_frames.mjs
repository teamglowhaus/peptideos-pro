// Screenshot video_frames/*.html -> video_frames/*.png at 1440x1080.
import fs from 'fs';
import path from 'path';
import { createRequire } from 'module';
import { fileURLToPath } from 'url';

const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_PKG || '/opt/node22/lib/node_modules/playwright');

const here = path.dirname(fileURLToPath(import.meta.url));
const dir = path.join(here, 'video_frames');
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html')).sort();

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1440, height: 1080 } });
for (const f of files) {
  await page.goto('file://' + path.join(dir, f), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: path.join(dir, f.replace('.html', '.png')) });
}
console.log('shot', files.length, 'frames');
await browser.close();
