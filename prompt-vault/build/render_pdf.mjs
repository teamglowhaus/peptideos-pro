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

await page.pdf({
  path: output,
  preferCSSPageSize: true,
  printBackground: true,
});
await browser.close();
console.log('wrote', output);
