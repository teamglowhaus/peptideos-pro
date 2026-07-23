// Build the Companion Doc (.docx) — upload this to Google Drive and "Open with
// Google Docs" to get the shareable click-to-copy bonus doc.
// Formatting goals (per handoff brief): clean and scannable, section headers,
// bold numbered prompt titles, plain-text bodies with NO manual line breaks so
// copy-paste works cleanly on desktop and mobile.
const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, BorderStyle,
} = require(path.join(__dirname, 'node_modules', 'docx'));

const data = JSON.parse(fs.readFileSync(path.join(__dirname, 'vault_data.json'), 'utf8'));

const INK = '0B0B11';
const GREY = '5C5C68';
const TIER_DARK = { beginner: '007C8F', intermediate: 'C40D69', advanced: '6F9400' };
const TIER_LABEL = { beginner: 'BEGINNER', intermediate: 'INTERMEDIATE', advanced: 'ADVANCED' };

const children = [];

children.push(new Paragraph({
  heading: HeadingLevel.TITLE,
  alignment: AlignmentType.CENTER,
  children: [new TextRun({ text: 'THE CLAUDE PROMPT VAULT — COMPANION DOC', bold: true, color: INK })],
}));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 240 },
  children: [new TextRun({ text: '108 Copy-Paste Prompts · Click to Copy · GlowHaus Digital', color: GREY })],
}));
children.push(new Paragraph({
  spacing: { after: 360 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: 'DDDDE4', space: 8 } },
  children: [new TextRun({
    italics: true, color: GREY,
    text: 'This is your bonus companion doc. Every prompt below is plain text, formatted to copy cleanly — no PDF line-break weirdness. Find your prompt, select the text, copy, paste into Claude, swap the [BRACKETS], go.',
  })],
}));

for (const section of data.sections) {
  const lo = (section.num - 1) * 9 + 1, hi = section.num * 9;
  children.push(new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 420, after: 60 },
    children: [new TextRun({
      text: `SECTION ${section.num}: ${section.title.toUpperCase()}`,
      bold: true, color: INK,
    })],
  }));
  children.push(new Paragraph({
    spacing: { after: 200 },
    children: [new TextRun({
      text: `${TIER_LABEL[section.tier]} · PROMPTS ${String(lo).padStart(3, '0')}–${String(hi).padStart(3, '0')}`,
      color: TIER_DARK[section.tier], size: 18, bold: true,
    })],
  }));

  for (const p of data.prompts.filter(p => p.n >= lo && p.n <= hi)) {
    children.push(new Paragraph({
      spacing: { before: 240, after: 40 },
      children: [
        new TextRun({ text: `${String(p.n).padStart(3, '0')} — ${p.title}`, bold: true, color: INK }),
      ],
    }));
    // Single paragraph, single run: guarantees clean one-block copy on any device.
    children.push(new Paragraph({
      spacing: { after: 120 },
      children: [new TextRun({ text: p.body, color: '1C1C26' })],
    }));
  }
}

children.push(new Paragraph({
  spacing: { before: 480 },
  alignment: AlignmentType.CENTER,
  children: [new TextRun({
    text: '© GlowHaus Digital. For personal use only. Not for resale or redistribution.',
    color: GREY, size: 18,
  })],
}));

const doc = new Document({
  styles: {
    default: {
      document: { run: { font: 'Arial', size: 22 }, paragraph: { spacing: { line: 300 } } },
      title: { run: { font: 'Arial', size: 40, bold: true } },
      heading1: { run: { font: 'Arial', size: 28, bold: true, color: INK } },
    },
  },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1080, bottom: 1080, left: 1260, right: 1260 } } },
    children,
  }],
});

const out = path.join(__dirname, '..', 'dist', 'Claude_Prompt_Vault_Companion_Doc.docx');
Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(out, buf);
  console.log('wrote', out, buf.length, 'bytes');
});
