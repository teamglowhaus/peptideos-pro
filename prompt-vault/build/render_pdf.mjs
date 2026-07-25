// Render vault.html -> dist/Claude_Prompt_Vault.pdf via Chromium print.
// Also reports any .page whose content overflows its 8.5x11in box.
import path from 'path';
import { createRequire } from 'module';
import { fileURLToPath } from 'url';

// Use the globally installed playwright (ESM import ignores NODE_PATH).
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_PKG || '/opt/node22/lib/node_modules/playwright');

const here = path.dirname(fileURLToPath(import.meta.url));
const input = process.argv[2] || path.join(here, 'vault.html');
const output = process.argv[3] || path.join(here, '..', 'dist', 'Claude_Prompt_Vault_108_Prompts.pdf');

const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto('file://' + input, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);

const overflows = await page.evaluate(() => {
  const bad = [];
  document.querySelectorAll('.page').forEach((el, i) => {
    if (el.scrollHeight > el.clientHeight + 2 || el.scrollWidth > el.clientWidth + 2) {
      bad.push({ page: i + 1, sh: el.scrollHeight, ch: el.clientHeight });
    }
  });
  return bad;
});
if (overflows.length) {
  console.error('OVERFLOW on pages:', JSON.stringify(overflows));
} else {
  console.log('no page overflows');
}

// Overlap check: no two sibling content blocks on a page may intersect.
const overlaps = await page.evaluate(() => {
  const SEL = '.pbox, .featcard, .cheat-card, .mm-row, .mm-note, .pp-head, .pgfoot, ' +
    '.mm-secnum, .minimap h2, .light-head, .matter-head, .toc-row, .why-card, ' +
    '.how-step, .tier-sec, .protip, .bonusnote, .cheat-stack';
  const bad = [];
  document.querySelectorAll('.page').forEach((pg, pi) => {
    const els = [...pg.querySelectorAll(SEL)];
    for (let i = 0; i < els.length; i++) {
      for (let j = i + 1; j < els.length; j++) {
        const a = els[i], b = els[j];
        if (a.contains(b) || b.contains(a)) continue;
        const ra = a.getBoundingClientRect(), rb = b.getBoundingClientRect();
        const x = Math.min(ra.right, rb.right) - Math.max(ra.left, rb.left);
        const y = Math.min(ra.bottom, rb.bottom) - Math.max(ra.top, rb.top);
        if (x > 2 && y > 2) {
          bad.push({ page: pi + 1, a: a.className.toString().slice(0, 30), b: b.className.toString().slice(0, 30) });
        }
      }
    }
  });
  return bad;
});
if (overlaps.length) {
  console.error('OVERLAPS:', JSON.stringify(overlaps.slice(0, 20)));
} else {
  console.log('no element overlaps');
}

await page.pdf({
  path: output,
  preferCSSPageSize: true,
  printBackground: true,
});
await browser.close();
console.log('wrote', output);
