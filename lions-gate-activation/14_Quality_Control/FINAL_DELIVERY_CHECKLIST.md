# FINAL DELIVERY CHECKLIST — The Lion's Gate 8/8 Activation

Status date: 2026-07-30. Every file below exists in this repository, was
rendered page-by-page to contact sheets (`14_Quality_Control/contact_sheets/`)
and visually inspected. Automated QC (`run_qc.py`) verified page sizes, page
counts, embedded fonts, link counts and near-blank-page detection; its raw
output is in `qc_report.txt`.

## Customer deliverables

| # | File | Status | Pages | Dimensions | Size |
|---|---|---|---|---|---|
| 1 | Lions_Gate_Activation_US_Letter.pdf | ✅ complete, inspected | 178 | 8.5 × 11 in | 848K |
| 2 | Lions_Gate_Activation_A4.pdf | ✅ complete, inspected | 176 | 210 × 297 mm | 860K |
| 3 | Lions_Gate_Activation_Digital_US_Letter.pdf | ✅ complete, inspected | 189 | 8.5 × 11 in | 916K |
| 4 | Lions_Gate_Activation_Digital_A4.pdf | ✅ complete, inspected | 176 | 210 × 297 mm | 920K |
| 5 | Lions_Gate_Planner_Pocket_3.5x6.pdf | ✅ complete, inspected | 69 | 3.5 × 6 in | 296K |
| 6 | Lions_Gate_Planner_Compact_4.25x6.75.pdf | ✅ complete, inspected | 63 | 4.25 × 6.75 in | 320K |
| 7 | Lions_Gate_Planner_Classic_5.5x8.5.pdf | ✅ complete, inspected | 52 | 5.5 × 8.5 in | 340K |
| 8 | Lions_Gate_Planner_Monarch_8.5x11.pdf | ✅ complete, inspected | 52 | 8.5 × 11 in | 400K |
| 9 | Pocket_Inserts_Print_on_US_Letter.pdf | ✅ complete, inspected | 24 sheets (3-up) | 11 × 8.5 in | 416K |
| 10 | Pocket_Inserts_Print_on_A4.pdf | ✅ complete, inspected | 24 sheets (3-up) | 297 × 210 mm | 424K |
| 11 | Compact_Inserts_Print_on_US_Letter.pdf | ✅ complete, inspected | 32 sheets (2-up) | 11 × 8.5 in | 428K |
| 12 | Compact_Inserts_Print_on_A4.pdf | ✅ complete, inspected | 32 sheets (2-up) | 297 × 210 mm | 436K |
| 13 | Classic_Inserts_Print_on_US_Letter.pdf | ✅ complete, inspected | 52 sheets (1-up) | 8.5 × 11 in | 432K |
| 14 | Classic_Inserts_Print_on_A4.pdf | ✅ complete, inspected | 52 sheets (1-up) | 210 × 297 mm | 440K |
| 15 | Lions_Gate_Quick_Start.pdf | ✅ complete, inspected | 10 | 8.5 × 11 in | 136K |
| 16 | Lions_Gate_Affirmation_Cards_US_Letter.pdf | ✅ complete, inspected | 10 (32 cards) | 8.5 × 11 in | 140K |
| 17 | Lions_Gate_Affirmation_Cards_A4.pdf | ✅ complete, inspected | 10 (32 cards) | 210 × 297 mm | 144K |
| 18 | Lions_Gate_Planner_Tabs_US_Letter.pdf | ✅ complete, inspected | 5 (9 tabs × 4 sets) | 8.5 × 11 in | 96K |
| 19 | Lions_Gate_Planner_Tabs_A4.pdf | ✅ complete, inspected | 5 (9 tabs × 4 sets) | 210 × 297 mm | 96K |
| 20 | Lions_Gate_Phone_Wallpapers.zip | ✅ complete, inspected | 24 PNG (12 designs × dark/light) + readme | 1170 × 2532 px | 892K |
| 21 | Lions_Gate_Printing_Guide.pdf | ✅ complete, inspected | 4 | 8.5 × 11 in | 116K |
| 22 | Lions_Gate_Planner_Insert_Guide.pdf | ✅ complete, inspected | 6 | 8.5 × 11 in | 124K |
| 23 | Lions_Gate_Digital_Use_Guide.pdf | ✅ complete, inspected | 4 | 8.5 × 11 in | 116K |
| 24 | Lions_Gate_Read_Me_First.pdf | ✅ complete, inspected | 6 | 8.5 × 11 in | 124K |

## Seller-facing files

| File | Status |
|---|---|
| 01_Research/MARKET_RESEARCH.md | ✅ complete (18 sections, web-researched 2026-07-30) |
| 01_Research/Etsy_SEO_Research.md | ✅ complete (verified 140-char title / 13×20-char tag limits) |
| 10_Etsy_Listing/Etsy_Listing_Copy.md | ✅ complete (title 136 chars; 13 tags verified; full FAQ) |
| 11_Listing_Images/Thumbnail_Copy_and_Art_Direction.md | ✅ complete (15-image strategy) |
| 11_Listing_Images/01–15 *.jpg | ✅ 15 images generated at 2000×1600 from real page renders |
| 12_Social_Launch/Pinterest_and_Social_Launch_Copy.md | ✅ complete |
| 13_License_and_Legal/PRODUCT_LICENSE_TEXT.md | ✅ complete |
| 14_Quality_Control/FINAL_DELIVERY_CHECKLIST.md | ✅ this file |

## Verification status

- **Link testing:** Digital US Letter 308 working internal links; Digital A4
  295 (clickable contents + a Contents return link in every footer). Verified
  programmatically; spot-clicked in rendered inspection. Print editions carry
  PDF outline bookmarks instead of links (intended).
- **Visual inspection:** all covers, license pages, thank-you pages, all 12
  part dividers, representative worksheets from every section, all four
  planner sizes, print-and-trim sheets, affirmation cards, planner tabs and
  all guides reviewed on contact sheets; issues found during QC (license
  overflow page, pocket column-header collision, imposition duplex pairing,
  glyph coverage, tab contrast, wallpaper arch) were fixed and re-rendered.
- **Printing test:** no physical printer in the build environment; sizes,
  margins and 100%-scale geometry verified programmatically. Recommend one
  physical test print of: a workbook worksheet, one print-and-trim sheet
  (duplex), and one card sheet before launch.
- **Digital navigation:** outline/bookmarks present in all engine-built PDFs.
- **Planner margins:** binding margins Pocket 0.72" / Compact 0.80" /
  Classic 0.92" / Monarch 1.15", mirrored per page face; page numbers at the
  outer edge; no content in punch zones (inspected).
- **License / thank-you / disclaimer:** present in both main and planner
  editions (full and shortened versions respectively); license summaries in
  all guides, card sheet and wallpaper readme.
- **Franklin trademark disclaimer:** present in the workbook copyright page,
  planner "About This Edition" page, Planner Insert Guide, Read Me First,
  Etsy listing copy, and listing image #13.
- **Bonus counts verified:** 32 cards (4 sheets × 8), 9 tab labels × 4 set
  variants, 12 wallpaper designs × 2 variants, 88 affirmations (8 families ×
  11), 3 full rituals + 6 adaptations, 8 day sequences × 3 pages.
- **Fonts:** Cormorant Garamond, Marcellus, Lato — all SIL OFL (commercial-safe),
  embedded. The only Helvetica references are unused default resources plus
  the tiny technical footer on print-and-trim sheets (base-14, renders
  everywhere); no visible content depends on a non-embedded font.

## Known limitations (stated honestly)

1. **No interactive form fields.** The digital editions are annotation
   editions (stylus/annotation apps), deliberately not marketed as
   "fillable"; listing copy and guides say so explicitly.
2. **Main workbook exceeds the 110–150-page target** (178 pages at Letter).
   The overage is content, not padding: the spec'd 19 sections with generous
   writing space did not fit 150 pages. Every page was individually reviewed
   against the no-filler rules; the two ritual pages that flow onto labeled
   "continued" pages are intentional long-form sequences.
3. **No printed punch-hole marks** on planner pages (deliberate; ring spacing
   varies by binder; the guide teaches the template method).
4. **Print-and-trim duplex** depends on the buyer's printer flip setting; each
   sheet is labeled front/back with its flip edge, and the guide mandates a
   one-sheet test.
5. **Physical print test pending** (see above).

## Manual seller steps before publishing

1. Replace placeholders (in `02_Main_Workbook_Source/content_front.py`, then
   rerun `build_main.py`, or edit externally):
   - `[INSERT WEBSITE OR ETSY SHOP URL]` (copyright page)
   - `[INSERT CONTACT EMAIL]` (copyright page)
   - `[INSERT YOUR FIRST NAME]` (thank-you page)
   - `[INSERT SOCIAL HANDLE, OPTIONAL]` (thank-you page)
2. Replace `[SHOP LINK]` in the social launch copy with the live listing URL.
3. Do one physical test print (worksheet + trim sheet + card sheet).
4. Decide launch pricing (recommended $16.88 launch / $24 regular; see
   listing copy) and set the sale end date (Aug 12).
5. Optional: legal review of license text if practitioner licenses will be
   sold (see PRODUCT_LICENSE_TEXT.md).

## Recommended Etsy upload order (media)

Images 01–15 from `11_Listing_Images/` in numeric order (hero first; Etsy
shows the first image in search). Etsy digital listings allow up to 5 files ×
20MB, so upload the five ZIPs described below.

## Recommended ZIP organization (5 download files ≤20MB each)

1. `LionsGate_1_START_HERE.zip` — Read Me First, Quick Start, all 4 guides
2. `LionsGate_2_Workbook_Print.zip` — US Letter + A4 main workbooks
3. `LionsGate_3_Workbook_Digital.zip` — both digital editions
4. `LionsGate_4_Planner_Inserts.zip` — 4 sized editions + 6 print-and-trim files
5. `LionsGate_5_Bonuses.zip` — cards (2), tabs (2), Lions_Gate_Phone_Wallpapers.zip

## Suggested customer download instructions (for the listing / receipt message)

"Download all five ZIP files from your Etsy purchases page on a computer or
tablet (phones sometimes struggle with large ZIPs). Open
LionsGate_1_START_HERE first and read Lions_Gate_Read_Me_First.pdf; it maps
everything else in two minutes. If any file gives you trouble, message me
through Etsy and I'll help you personally."
