# Claude Prompt Vault — 2026 Relaunch Build

Conversion rebuild of the Etsy "Claude Prompt Vault" listing per the handoff brief:
72 → 108 prompts, continuous 001–108 numbering, USE-THIS-WHEN tags, tiered neon design
(Beginner = cyan · Intermediate = magenta · Advanced = lime), functional mini-map dividers,
companion copy-paste doc, and a full 10-image + video Etsy stack.

## What's in `dist/` (the deliverables)

| File | What it is |
|---|---|
| `Claude_Prompt_Vault_108_Prompts.pdf` | The rebuilt 48-page vault (US Letter, print-ready) |
| `Claude_Prompt_Vault_Companion_Doc.docx` | Companion doc — upload to Google Drive → "Open with Google Docs" |
| `Claude_Prompt_Vault_Companion_Doc.md` | Same content as markdown (backup/paste source) |
| `etsy/01…10_*.png` | The 10 listing images, 2700×2025, upload in numeric order |
| `etsy/video_flipthrough.mp4` | 14.4s silent flip-through video (1440×1080 h264) |
| `etsy/qa_hero_thumbnail_570px.png` | QA-only: hero at Etsy thumbnail size (do not upload) |
| `QA_REPORT.md` | Latest automated QA results |

`ETSY_LISTING_KIT.md` (repo root of this folder) has the copy-paste title, 13 tags,
description, pricing, sale schedule, and upload order.

## The one manual step left: the companion Google Doc link

I can't create a Google Doc from here, so the PDF currently carries a visible
`[ADD YOUR GOOGLE DOC LINK]` placeholder (page 4 + Section 1 mini-map) and QA
deliberately fails until it's replaced. To finish:

1. Upload `dist/Claude_Prompt_Vault_Companion_Doc.docx` to Google Drive, open with
   Google Docs (it converts cleanly — headers, bold titles, plain bodies).
2. Share → "Anyone with the link" → Viewer. Copy the link (shorten if you like).
3. Rebuild the PDF with the real link:

   ```bash
   cd prompt-vault/build
   python3 build_vault.py --companion-url "https://docs.google.com/your-link"
   node render_pdf.mjs
   python3 qa.py   # should now be all-green
   ```

## Regenerating everything

```bash
cd prompt-vault/build
python3 build_vault.py [--companion-url URL]   # -> vault.html
node render_pdf.mjs                            # -> dist/Claude_Prompt_Vault_108_Prompts.pdf
node build_companion.js                        # -> dist/...Companion_Doc.docx (needs: npm install docx --no-save)
python3 build_images.py && node render_images.mjs   # -> dist/etsy/*.png
python3 build_video.py && node render_frames.mjs && python3 build_video.py --encode  # -> video
python3 qa.py                                  # -> dist/QA_REPORT.md
```

Requirements: Python 3 + `pymupdf` `python-docx` `pillow` `imageio-ffmpeg`,
Node 22 + global `playwright` (Chromium), local `docx` package.
All content lives in `build/vault_data.py` — single source of truth for the
108 prompts, tags, section metadata, and front/back-matter copy.
Fonts are bundled in `assets/fonts/` (Fraunces, Jost, Space Mono — same set as career-os).

## Relaunch order of operations (from the Optimization Kit)

1. ~~Expand to 108 prompts + PDF architecture fixes~~ ✔ done (this build)
2. Companion Google Doc — upload the docx, set sharing, rebuild PDF with link (above)
3. Upload new image stack (minimum: 1, 2, 3, 5 — all 10 are ready)
4. Swap title, tags, description (`ETSY_LISTING_KIT.md`)
5. Upload video
6. Price to $12.99–$14.99 + schedule 25% sale for 14 days
