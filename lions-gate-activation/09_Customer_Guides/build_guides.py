# -*- coding: utf-8 -*-
"""Build the four customer guides: Read Me First, Printing Guide,
Planner Insert Guide, Digital Use Guide."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "02_Main_Workbook_Source"))
from lg import theme, engine

TM_NOTE = ("Franklin Planner and FranklinCovey are trademarks of their respective owners. This independently "
           "created digital product is not affiliated with, sponsored by, approved by or endorsed by Franklin "
           "Planner or FranklinCovey. Brand names are used only to help customers identify compatible page "
           "dimensions. Please measure your existing planner pages and binder before printing.")

LICENSE_SHORT = ("License summary: your purchase includes a single-user personal-use license. Print and use "
                 "everything for yourself as often as you like; please do not share, resell, redistribute, or use "
                 "the files with clients, students or groups without a separate license. The complete license is "
                 "inside the main workbook.")

# ================================================================ READ ME
READ_ME = [
{"kind": "cover", "title": "Read Me First", "subtitle": "Your map to everything inside The Lion's Gate 8/8 Activation",
 "tagline": "Start here · Two minutes"},
{
 "family": "front", "section": "Welcome", "title": "Welcome, and Thank You", "toc": False,
 "blocks": [
    ("p", "Thank you for bringing The Lion's Gate 8/8 Activation into your season. This short guide walks you through what you have downloaded, where to begin, and how to get help if anything misbehaves. Everything here is a digital download; no physical item will be shipped."),
    ("h2", "Where to begin"),
    ("kv", [
      ("If August 8 is close", "Open Lions_Gate_Quick_Start.pdf tonight. It is complete on its own."),
      ("If you have a week or more", "Open the main workbook in your preferred size and start with the Welcome pages."),
      ("If you live in a ring planner", "Read Lions_Gate_Planner_Insert_Guide.pdf before printing anything."),
      ("If you use a tablet", "Import a Digital edition; details live in Lions_Gate_Digital_Use_Guide.pdf."),
    ]),
    ("note", "Files are best opened in a real PDF reader (Adobe Acrobat Reader, Apple Books/Preview, Goodnotes) rather than a browser tab, which can hide links and print controls."),
 ],
},
{
 "family": "reference", "section": "What's Included", "title": "Everything in Your Download", "toc": False,
 "blocks": [
    ("table", ["File", "What it is"], [
      ["Lions_Gate_Activation_US_Letter.pdf", "Full workbook for 8.5 x 11 in printing"],
      ["Lions_Gate_Activation_A4.pdf", "Full workbook reflowed for A4 (210 x 297 mm)"],
      ["Digital editions (Letter + A4)", "Tablet versions: clickable contents, roomier writing lines"],
      ["Planner editions (4 sizes)", "Pocket 3.5 x 6, Compact 4.25 x 6.75, Classic 5.5 x 8.5, Monarch 8.5 x 11 in"],
      ["Print-and-trim files (6)", "Pocket, Compact and Classic inserts arranged on Letter or A4 sheets with cut marks"],
      ["Lions_Gate_Quick_Start.pdf", "The essentials for anyone starting close to August 8"],
      ["Affirmation cards (Letter + A4)", "32 cards, 3.5 x 2.5 in, with backs and cutting guide"],
      ["Planner tabs (Letter + A4)", "9 section tabs, color and printer-friendly, left and right sets"],
      ["Lions_Gate_Phone_Wallpapers.zip", "12 designs, dark and light versions, install notes inside"],
      ["Guides (this one + 3 more)", "Printing, planner inserts, and digital use, each a short read"],
    ], [0.42, 0.58]),
    ("note", "Tip: you do not need to print everything, and very few readers do. Choose one path (full workbook, planner, or tablet) and let the rest be a bonus shelf."),
 ],
},
{
 "family": "reference", "section": "Formats", "title": "Which Format Is Yours?", "toc": False,
 "blocks": [
    ("h2", "Printing versus digital"),
    ("p", "Print if handwriting helps you think; the light backgrounds are deliberately ink-friendly. Stay digital if you annotate on a tablet or want the experience with you everywhere. Mixing is normal: many readers print only the Eight-Day Activation and ritual pages."),
    ("h2", "Planner sizes at a glance"),
    ("table", ["Size", "Finished page", "Matches"], [
      ["Pocket", "3.5 x 6 in", "Small ring binders using pocket-size pages"],
      ["Compact", "4.25 x 6.75 in", "Compact ring binders"],
      ["Classic", "5.5 x 8.5 in", "The most common personal ring binder size"],
      ["Monarch", "8.5 x 11 in", "Full-letter ring binders"],
    ], [0.2, 0.3, 0.5]),
    ("note", TM_NOTE),
 ],
},
{
 "family": "reference", "section": "Help", "title": "Troubleshooting & Hello", "toc": False,
 "blocks": [
    ("kv", [
      ("A file will not open", "Download again over Wi-Fi and open in a dedicated PDF app; huge files sometimes arrive incomplete on a weak connection."),
      ("Printing looks cut off", "Set the printer dialog to 100 percent / Actual Size, never Fit to Page, and check the paper size matches the edition."),
      ("Links do not click", "Browser previews often disable links; open the Digital edition in Acrobat Reader, Goodnotes or Apple Books."),
      ("Wrong size for my binder", "Measure an existing page from your binder and match it to the table on the previous page before printing."),
      ("Anything else", "Message GlowHausDigital through Etsy (your Purchases page > this order > Contact shop). I answer, and I would rather fix a problem than have you shrug and move on."),
    ]),
    ("p", "One last thing: if this experience earns a place in your August, an honest review helps another reader decide whether it might support her too. Thank you for being here."),
    ("note", LICENSE_SHORT),
 ],
},
{"kind": "back", "quote": "Begin anywhere. Beginning is the ritual.", "brand": "GlowHausDigital"},
]

# ================================================================ PRINTING GUIDE
PRINTING = [
{"kind": "cover", "title": "The Printing Guide", "subtitle": "Beautiful pages from an ordinary home printer",
 "tagline": "US Letter · A4 · ink-friendly by design"},
{
 "family": "reference", "section": "Printing Guide", "title": "The Golden Rules", "toc": False,
 "blocks": [
    ("steps", [
      ("Match the file to your paper", "US Letter files for 8.5 x 11 in paper; A4 files for 210 x 297 mm. The A4 edition is reflowed, not shrunk, so nothing feels cramped."),
      ("Print at 100 percent", "In the print dialog choose Actual Size / Scale 100 percent. Fit to Page silently shrinks pages and ruins planner measurements."),
      ("Test one page first", "Print a single worksheet, check size and margins with a ruler, then commit to the full document."),
      ("Choose your page range", "Very few readers print all pages at once. Print the parts your week needs; the file is not going anywhere."),
    ]),
    ("h2", "Color or grayscale?"),
    ("p", "Both work. The palette was chosen so that gold rules and indigo headings degrade gracefully to grayscale; worksheets stay fully readable. If ink is precious, print the interior in grayscale and save color for the cover and dividers, or skip the dark pages entirely using your printer's page-range field."),
 ],
},
{
 "family": "reference", "section": "Printing Guide", "title": "Duplex, Paper & Ink", "toc": False,
 "blocks": [
    ("h2", "Double-sided printing"),
    ("p", "The main workbook is comfortable single- or double-sided; for duplex choose flip on long edge in your print dialog. Planner editions use mirrored margins, so duplex works beautifully there; the Planner Insert Guide covers the details, including the two-page alignment test."),
    ("h2", "Paper that flatters the design"),
    ("bullets", [
      "Everyday: any 20 lb / 80 gsm copy paper is fine for worksheets.",
      "Lovely: 24-28 lb / 90-105 gsm smooth white paper makes writing pages feel substantial.",
      "Cards and tabs: 65-80 lb / 176-216 gsm cardstock.",
      "Fountain-pen users: look for paper marked laser-guaranteed or with a smooth calendered finish to limit feathering.",
    ]),
    ("h2", "Professional printing"),
    ("p", "Any copy shop can print the PDFs; ask for 100 percent scale, single-sided or duplex long-edge, and paper from the list above. A spiral bind with a clear cover turns the workbook into a keepsake. Shops will print your personal copy; if one asks about copyright, show them the license page, which permits personal-use printing."),
    ("note", "Ink-saving summary: grayscale interior, skip dark divider pages (they are listed in the bookmarks panel), and never reprint what a page range could have avoided."),
 ],
},
{"kind": "back", "quote": "A test page today saves a ream tomorrow.", "brand": "GlowHausDigital"},
]

# ================================================================ PLANNER GUIDE
PLANNER_G = [
{"kind": "cover", "title": "The Planner Insert Guide", "subtitle": "Printing, trimming, punching and loving your ring-bound edition",
 "tagline": "Pocket · Compact · Classic · Monarch"},
{
 "family": "reference", "section": "Planner Guide", "title": "First, Measure", "toc": False,
 "blocks": [
    ("p", "Ring binders vary more than their labels suggest, so before printing anything, take one page you already use out of your binder and measure it. Match it to the table; if your pages differ by more than a couple of millimeters, choose the closer size and trim to match your existing pages."),
    ("table", ["Edition", "Finished page size", "File"], [
      ["Pocket", "3.5 x 6 in (89 x 152 mm)", "Lions_Gate_Planner_Pocket_3.5x6.pdf"],
      ["Compact", "4.25 x 6.75 in (108 x 171 mm)", "Lions_Gate_Planner_Compact_4.25x6.75.pdf"],
      ["Classic", "5.5 x 8.5 in (140 x 216 mm)", "Lions_Gate_Planner_Classic_5.5x8.5.pdf"],
      ["Monarch", "8.5 x 11 in (216 x 279 mm)", "Lions_Gate_Planner_Monarch_8.5x11.pdf"],
    ], [0.2, 0.42, 0.38]),
    ("note", TM_NOTE),
 ],
},
{
 "family": "reference", "section": "Planner Guide", "title": "Path A: Precut Paper", "toc": False,
 "blocks": [
    ("p", "If you own paper already cut to your planner size (or a stack of trimmed pages), print the sized PDF directly onto it."),
    ("steps", [
      ("Create the custom size", "In your printer settings, add a custom paper size matching the table (for example 3.5 x 6 in for Pocket). On many home printers this lives under Paper Size > Manage Custom Sizes."),
      ("Load carefully", "Small paper usually feeds from the manual or rear tray, centered or edge-aligned per your printer's diagram."),
      ("Print at 100 percent", "Actual Size, portrait orientation, no scaling, no centering adjustments."),
      ("Test two pages", "Print pages 2-3 double-sided first. Hold them to the light: the binding margins should mirror (wide edge on the ring side of both faces). If the back is upside down, switch between long-edge and short-edge flipping."),
      ("Print the rest", "Duplex with the flip setting your test proved, or single-sided if you prefer writing on one face."),
    ]),
    ("note", "Borderless caution: do not enable borderless/edge-to-edge modes; they scale the page slightly and shift the punch margin."),
 ],
},
{
 "family": "reference", "section": "Planner Guide", "title": "Path B: Print and Trim", "toc": False,
 "blocks": [
    ("p", "No precut paper? Use the print-and-trim files: inserts arranged on ordinary US Letter or A4 sheets with fine cut marks, centered to minimize waste."),
    ("table", ["File", "Layout"], [
      ["Pocket_Inserts_Print_on_US_Letter / _A4", "3 inserts per landscape sheet"],
      ["Compact_Inserts_Print_on_US_Letter / _A4", "2 inserts per landscape sheet"],
      ["Classic_Inserts_Print_on_US_Letter / _A4", "1 insert centered per portrait sheet"],
    ], [0.55, 0.45]),
    ("steps", [
      ("Print at 100 percent", "Actual Size; the footer on every sheet confirms the finished dimensions."),
      ("Duplex if you like", "Each sheet is labeled front or back and states its flip edge (short edge for landscape sheets, long edge for Classic). Run a one-sheet test; every cut stack then reads front/back like a bound page."),
      ("Cut on the marks", "A rotary trimmer or ruler-and-knife gives straighter edges than scissors. Cut inside the marks in single confident passes."),
      ("Keep order", "Sheets are numbered; cut one sheet at a time and stack as you go, and the inserts stay in page order."),
    ]),
 ],
},
{
 "family": "reference", "section": "Planner Guide", "title": "Punching & Living With It", "toc": False,
 "blocks": [
    ("h2", "Hole punching, honestly"),
    ("p", "Ring spacing varies between binder brands and generations, which is why these pages carry no printed hole marks: marks matching one binder would mislead every other. The reliable method takes one minute."),
    ("steps", [
      ("Borrow a template", "Take a punched page that already lives in your binder."),
      ("Align and mark", "Lay it over one printed insert, ring edge to ring edge (the wide margin), and mark through the existing holes with a pencil."),
      ("Test-punch one sheet", "Punch that single insert, try it in the binder, adjust, and only then punch in small batches."),
    ]),
    ("p", "The binding margin on every page is generous on purpose: Pocket 0.72 in, Compact 0.8 in, Classic 0.92 in, Monarch 1.15 in on the ring side, mirrored across page faces for duplex printing. Writing lines and page numbers stay clear of the punch zone."),
    ("h2", "Tabs"),
    ("p", "The planner's sections match the nine printable tabs in your download (Begin through Notes). Print, cut, fold and place them on each section's first page; full instructions ride along in the tabs file."),
    ("note", LICENSE_SHORT + " " + TM_NOTE),
 ],
},
{"kind": "back", "quote": "Measure once, punch twice-shy, and it will live happily in your rings for years.", "brand": "GlowHausDigital"},
]

# ================================================================ DIGITAL GUIDE
DIGITAL_G = [
{"kind": "cover", "title": "The Digital Use Guide", "subtitle": "Using your workbook on a tablet, phone or computer",
 "tagline": "Goodnotes · Notability · Xodo · Acrobat and friends"},
{
 "family": "reference", "section": "Digital Guide", "title": "Setting Up Your Tablet Edition", "toc": False,
 "blocks": [
    ("p", "Use the Digital editions (Letter or A4; pick whichever aspect ratio you like on screen). They share every page with the print editions but add roomier writing lines and a clickable table of contents, and every page carries a Contents link in the footer."),
    ("steps", [
      ("Move the file", "Send the PDF to your tablet: cloud drive, AirDrop, email to yourself, or a USB cable all work."),
      ("Import into your app", "In Goodnotes: New > Import; in Notability: the import arrow; in Xodo or Acrobat: simply open. Choose the option that keeps the file as a PDF with links intact."),
      ("Make a backup copy", "Duplicate the untouched file inside the app or your cloud drive before writing on it. Future you, restarting in January, will be grateful."),
      ("Write with your stylus", "Annotation layers sit on top of the page; the writing lines are spaced for a medium pen nib. Zoom in for the smaller planner-style elements."),
    ]),
    ("note", "Honest note: these PDFs are annotation editions, not form-fillable documents; there are no interactive text fields. Every mainstream annotation app writes on them beautifully, which is exactly how they were designed to be used."),
 ],
},
{
 "family": "reference", "section": "Digital Guide", "title": "Navigating, Repeating, Troubleshooting", "toc": False,
 "blocks": [
    ("h2", "Getting around"),
    ("bullets", [
      "The Contents pages are tap-targets: tap any line to jump to that page.",
      "The word Contents in every footer returns you to the table of contents.",
      "The PDF outline (bookmarks sidebar) mirrors the structure in most readers.",
      "In Goodnotes and Notability, remember the app's read-only toggle when links refuse to fire; links click when the pen tool is off.",
    ]),
    ("h2", "Repeating pages"),
    ("p", "Want a fresh Evidence of Movement tracker or another Open Script page? Use your app's duplicate page or copy page feature; duplicating pages inside your own copy for your own use is fully within your license."),
    ("h2", "When something misbehaves"),
    ("kv", [
      ("Links do nothing", "You are probably in a browser preview or an editing mode; open in a real PDF app and switch to reading/scroll mode."),
      ("File feels slow", "Close other large documents; 180-page PDFs like room to breathe on older tablets."),
      ("Handwriting looks jagged", "Turn off the app's zoom-snap or write in the zoomed writing box."),
      ("Still stuck", "Message GlowHausDigital through Etsy and I will help you personally."),
    ]),
    ("note", LICENSE_SHORT),
 ],
},
{"kind": "back", "quote": "The best edition is the one within arm's reach when the feeling strikes.", "brand": "GlowHausDigital"},
]

GUIDES = [
    (READ_ME, "Lions_Gate_Read_Me_First.pdf", "Read Me First"),
    (PRINTING, "Lions_Gate_Printing_Guide.pdf", "The Printing Guide"),
    (PLANNER_G, "Lions_Gate_Planner_Insert_Guide.pdf", "The Planner Insert Guide"),
    (DIGITAL_G, "Lions_Gate_Digital_Use_Guide.pdf", "The Digital Use Guide"),
]

if __name__ == "__main__":
    for pages, name, title in GUIDES:
        book = engine.Book(theme.spec("letter"), title=title, subtitle="The Lion's Gate 8/8 Activation")
        book.extend(pages)
        n = book.build(os.path.join(HERE, name))
        print("%-40s %d pages" % (name, n))
