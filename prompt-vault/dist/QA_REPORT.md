# QA Report — Claude Prompt Vault Relaunch

Overall: FAILURES PRESENT — see below

- [x] PASS — PDF page count is 48 (got 48)
- [x] PASS — PDF page size is US Letter
- [x] PASS — 108 numbered prompt boxes (#001–#108) (found 108 unique, min 1, max 108)
- [x] PASS — USE THIS WHEN tag on every prompt box (108) (found 108 occurrences)
- [x] PASS — All 12 sections have exactly 9 prompts
- [ ] FAIL — Companion-doc link is set (no placeholder) (placeholder still present — rebuild with: python3 build_vault.py --companion-url <link> && node render_pdf.mjs)
- [x] PASS — All 108 prompt bodies present verbatim
- [x] PASS — Companion doc has 108 numbered prompts (got 108)
- [x] PASS — Companion doc has 12 section headers
- [x] PASS — Companion doc has no manual line breaks in prompts
- [x] PASS — 10 listing images present at 2700x2025
- [x] PASS — Hero thumbnail QA preview exists
- [x] PASS — Flip-through video exists (645 KB)

Manual checks that cannot be automated:
- Companion Google Doc created, shared as 'anyone with link can view', copy-paste tested on mobile
- PDF rebuilt with the real companion link before uploading to Etsy
- Title/description proofread on the live listing
- Images previewed at Etsy thumbnail size (see dist/etsy/qa_hero_thumbnail_570px.png)
