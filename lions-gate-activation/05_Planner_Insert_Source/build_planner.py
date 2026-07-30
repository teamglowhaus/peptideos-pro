# -*- coding: utf-8 -*-
"""Build the four planner insert editions + the six print-and-trim files."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "02_Main_Workbook_Source"))
sys.path.insert(0, HERE)
from lg import theme, engine
import planner_content

TITLE = "The Lion's Gate 8/8 Activation · Planner Edition"
SUBTITLE = "Printable ring-bound planner inserts"

SIZES = [
    ("pocket",  "Lions_Gate_Planner_Pocket_3.5x6.pdf"),
    ("compact", "Lions_Gate_Planner_Compact_4.25x6.75.pdf"),
    ("classic", "Lions_Gate_Planner_Classic_5.5x8.5.pdf"),
    ("monarch", "Lions_Gate_Planner_Monarch_8.5x11.pdf"),
]

def build_sizes():
    out = {}
    for key, name in SIZES:
        path = os.path.join(ROOT, "06_Planner_Insert_PDFs", name)
        book = engine.Book(theme.spec(key), title=TITLE, subtitle=SUBTITLE)
        book.extend(planner_content.PAGES)
        n = book.build(path)
        out[key] = path
        print("%-8s %3d pages  %s" % (key, n, name))
    return out

# ---------------------------------------------------------------- imposition
import fitz

IN = 72.0
MM = 72.0 / 25.4
SHEETS = {"letter": (8.5 * IN, 11 * IN), "a4": (210 * MM, 297 * MM)}

# (source_size, sheet, n_across, landscape)
IMPOSE = [
    ("pocket",  "letter", 3, True,  "Pocket_Inserts_Print_on_US_Letter.pdf"),
    ("pocket",  "a4",     3, True,  "Pocket_Inserts_Print_on_A4.pdf"),
    ("compact", "letter", 2, True,  "Compact_Inserts_Print_on_US_Letter.pdf"),
    ("compact", "a4",     2, True,  "Compact_Inserts_Print_on_A4.pdf"),
    ("classic", "letter", 1, False, "Classic_Inserts_Print_on_US_Letter.pdf"),
    ("classic", "a4",     1, False, "Classic_Inserts_Print_on_A4.pdf"),
]

SIZE_LABEL = {"pocket": '3.5 x 6 in', "compact": '4.25 x 6.75 in', "classic": '5.5 x 8.5 in'}

def trim_marks(page, x0, y0, w, h, length=14, gap=4):
    """Corner trim marks outside the trim box."""
    for cx, cy, dx, dy in [(x0, y0, -1, -1), (x0 + w, y0, 1, -1),
                            (x0, y0 + h, -1, 1), (x0 + w, y0 + h, 1, 1)]:
        page.draw_line(fitz.Point(cx + dx * gap, cy), fitz.Point(cx + dx * (gap + length), cy),
                       color=(0.45, 0.42, 0.5), width=0.5)
        page.draw_line(fitz.Point(cx, cy + dy * gap), fitz.Point(cx, cy + dy * (gap + length)),
                       color=(0.45, 0.42, 0.5), width=0.5)

def impose(src_path, sheet_key, n_across, landscape, out_name):
    src = fitz.open(src_path)
    sw, sh = SHEETS[sheet_key]
    if landscape:
        sw, sh = sh, sw
    pw = src[0].rect.width
    ph = src[0].rect.height
    doc = fitz.open()
    n = n_across
    total_w = n * pw
    left = (sw - total_w) / 2.0
    top = (sh - ph) / 2.0
    # Duplex-correct pairing: physical sheet p carries source pages
    #   front slots (left to right):  p*2n, p*2n+2, p*2n+4, ...
    #   back  slots (reversed):       p*2n+1, p*2n+3, ...
    # so each cut stack reads front/back like a bound page. Landscape sheets
    # flip on the SHORT edge, portrait 1-up sheets on the LONG edge (the
    # Planner Insert Guide says so, and recommends a two-sheet test first).
    n_phys = (len(src) + 2 * n - 1) // (2 * n)
    flip = "short edge" if landscape else "long edge"
    for p in range(n_phys):
        for side in (0, 1):
            base = p * 2 * n + side
            pages = [base + 2 * s for s in range(n) if base + 2 * s < len(src)]
            if side == 1 and not pages:
                continue
            page = doc.new_page(width=sw, height=sh)
            slots = list(range(n)) if side == 0 else [n - 1 - s for s in range(n)]
            for slot, pno in zip(slots, pages):
                x0 = left + slot * pw
                y0 = top
                rect = fitz.Rect(x0, y0, x0 + pw, y0 + ph)
                page.show_pdf_page(rect, src, pno)
                trim_marks(page, x0, y0, pw, ph)
            for slot in range(1, n):
                x = left + slot * pw
                page.draw_line(fitz.Point(x, top - 18), fitz.Point(x, top - 6), color=(0.45, 0.42, 0.5), width=0.5)
                page.draw_line(fitz.Point(x, top + ph + 6), fitz.Point(x, top + ph + 18), color=(0.45, 0.42, 0.5), width=0.5)
            label = "Lion's Gate planner inserts · finished size %s · sheet %d %s · duplex: flip on %s · print at 100%% · cut on the marks" % (
                SIZE_LABEL[key_of(src_path)], p + 1, "front" if side == 0 else "back", flip)
            page.insert_text(fitz.Point(left, sh - 14), label, fontsize=7.5, color=(0.35, 0.33, 0.42),
                             fontname="lato", fontfile=os.path.join(ROOT, "02_Main_Workbook_Source", "assets", "fonts", "Lato-400.ttf"))
    out = os.path.join(ROOT, "07_Print_and_Trim_Files", out_name)
    doc.set_metadata({"title": out_name.replace(".pdf", ""), "author": "GlowHausDigital"})
    doc.save(out, deflate=True)
    print("imposed  %3d sheets %s" % (len(doc), out_name))

def key_of(src_path):
    b = os.path.basename(src_path)
    for k in ("pocket", "compact", "classic"):
        if k in b.lower():
            return k
    return "classic"

if __name__ == "__main__":
    paths = build_sizes()
    for src_key, sheet, n, land, out_name in IMPOSE:
        impose(paths[src_key], sheet, n, land, out_name)
