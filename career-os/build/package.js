#!/usr/bin/env node
/* =========================================================================
   CAREER OS — BUYER PACKAGE BUILD
   -------------------------------------------------------------------------
   Runs build-single-file.js, then zips exactly THREE flat files (no nested
   folders) into dist/Career-OS.zip:
     - Career OS — Open This File.html   (the whole app, self-contained)
     - Quick Start.txt
     - License.txt

   This is the file uploaded to Etsy. A buyer downloads one zip, extracts
   it (one click on Mac/Windows), sees three plainly-named files sitting
   flat — not a folder tree — and double-clicks the .html file. No relative
   paths to break, no "which of these 23 files do I open."

   Usage: node build/package.js
   ========================================================================= */

const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const ROOT = path.join(__dirname, '..');
const DIST = path.join(ROOT, 'dist');
const STAGE = path.join(DIST, '_package_stage');
const ZIP_PATH = path.join(DIST, 'Career-OS.zip');

execFileSync('node', [path.join(__dirname, 'build-single-file.js')], { stdio: 'inherit' });

fs.rmSync(STAGE, { recursive: true, force: true });
fs.mkdirSync(STAGE, { recursive: true });

fs.copyFileSync(
  path.join(DIST, 'Career OS — Open This File.html'),
  path.join(STAGE, 'Career OS — Open This File.html')
);
fs.copyFileSync(
  path.join(__dirname, 'package-assets', 'Quick Start.txt'),
  path.join(STAGE, 'Quick Start.txt')
);
fs.copyFileSync(
  path.join(ROOT, 'LICENSE.txt'),
  path.join(STAGE, 'License.txt')
);

fs.rmSync(ZIP_PATH, { force: true });
// -j: junk paths (flat, no folder entries) — this is what keeps the zip's
// root free of any subfolder for the buyer to navigate into.
execFileSync('zip', ['-j', '-X', ZIP_PATH,
  path.join(STAGE, 'Career OS — Open This File.html'),
  path.join(STAGE, 'Quick Start.txt'),
  path.join(STAGE, 'License.txt'),
], { stdio: 'inherit' });

fs.rmSync(STAGE, { recursive: true, force: true });

const sizeKB = Math.round(fs.statSync(ZIP_PATH).size / 1024);
console.log(`\nPackaged: ${ZIP_PATH} (${sizeKB} KB) — this is the file to upload to Etsy.`);
