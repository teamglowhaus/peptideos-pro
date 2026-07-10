#!/usr/bin/env node
/* =========================================================================
   CAREER OS — SINGLE-FILE BUILD
   -------------------------------------------------------------------------
   Buyers on Etsy shouldn't have to unzip a folder and hunt for index.html
   among 23 files across 5 subfolders. This script inlines the whole app —
   both stylesheets (fonts.css's five .woff2 files as base64 data URIs,
   style.css as-is) and all nine JS files, in their original load order —
   into ONE self-contained .html file. Double-click it, it opens in the
   browser, done. No server, no relative paths, no unzip-and-hunt.

   Source files are untouched; this only ever WRITES to dist/. Re-run after
   any change to index.html/css/js so the shipped file stays in sync.

   Usage: node build/build-single-file.js
   ========================================================================= */

const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const DIST = path.join(ROOT, 'dist');
const OUT_FILE = path.join(DIST, 'Career OS — Open This File.html');

function readText(rel){ return fs.readFileSync(path.join(ROOT, rel), 'utf8'); }
function readBase64(rel){ return fs.readFileSync(path.join(ROOT, rel)).toString('base64'); }

const FONT_MIME = { '.woff2': 'font/woff2' };

// Inline every url('./xxx.woff2') in fonts.css as a base64 data URI, resolved
// relative to the fonts/ folder the file itself lives in.
function inlineFontsCss(){
  const cssPath = 'fonts/fonts.css';
  let css = readText(cssPath);
  css = css.replace(/url\(['"]?\.\/([^'")]+)['"]?\)/g, (match, fname) => {
    const ext = path.extname(fname);
    const mime = FONT_MIME[ext];
    if(!mime) throw new Error(`Unhandled font asset type in fonts.css: ${fname}`);
    const b64 = readBase64(path.join('fonts', fname));
    return `url('data:${mime};base64,${b64}')`;
  });
  return css;
}

function build(){
  let html = readText('index.html');

  const fontsCss = inlineFontsCss();
  const styleCss = readText('css/style.css');

  // Replace the two <link rel="stylesheet"> tags with one inlined <style> block.
  html = html.replace(
    /<link rel="stylesheet" href="fonts\/fonts\.css" \/>\s*<link rel="stylesheet" href="css\/style\.css" \/>/,
    `<style>\n${fontsCss}\n</style>\n<style>\n${styleCss}\n</style>`
  );

  const scriptFiles = [
    'js/occupations.js', 'js/modules.js', 'js/resume.js', 'js/coverletter.js',
    'js/flashcards.js', 'js/offercalc.js', 'js/atscheck.js', 'js/tracker.js',
    'js/extras.js', 'js/app.js',
  ];
  const scriptRegex = /<script src="js\/[a-z]+\.js"><\/script>\s*/g;
  let firstScriptSeen = false;
  html = html.replace(scriptRegex, () => {
    if(firstScriptSeen) return '';   // collapse all matches into a single insertion point
    firstScriptSeen = true;
    return scriptFiles.map(f => `<script>\n${readText(f)}\n</script>`).join('\n');
  });

  // Sanity check: nothing referencing an external/relative file path should remain.
  const leftoverRefs = html.match(/(?:src|href)="(?!#)[^"]*\.(?:js|css)"/g);
  if(leftoverRefs) throw new Error('Un-inlined external references remain: ' + leftoverRefs.join(', '));

  fs.mkdirSync(DIST, { recursive: true });
  fs.writeFileSync(OUT_FILE, html);

  const sizeKB = Math.round(fs.statSync(OUT_FILE).size / 1024);
  console.log(`Built: ${OUT_FILE} (${sizeKB} KB)`);
}

build();
