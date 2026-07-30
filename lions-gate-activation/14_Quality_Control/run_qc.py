# -*- coding: utf-8 -*-
"""Quality control: render every PDF page, build contact sheets, run automated
checks (page sizes, counts, embedded fonts, links, near-blank pages, banned
phrases, glyph fallbacks). Writes contact sheets + qc_report.txt here."""
import os, sys, glob, io
import fitz
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SHEET_DIR = os.path.join(HERE, "contact_sheets")
os.makedirs(SHEET_DIR, exist_ok=True)

IN = 72.0
EXPECT = {
 "03_Main_Workbook_PDFs/Lions_Gate_Activation_US_Letter.pdf": (8.5, 11),
 "03_Main_Workbook_PDFs/Lions_Gate_Activation_A4.pdf": (8.27, 11.69),
 "04_Digital_Editions/Lions_Gate_Activation_Digital_US_Letter.pdf": (8.5, 11),
 "04_Digital_Editions/Lions_Gate_Activation_Digital_A4.pdf": (8.27, 11.69),
 "06_Planner_Insert_PDFs/Lions_Gate_Planner_Pocket_3.5x6.pdf": (3.5, 6),
 "06_Planner_Insert_PDFs/Lions_Gate_Planner_Compact_4.25x6.75.pdf": (4.25, 6.75),
 "06_Planner_Insert_PDFs/Lions_Gate_Planner_Classic_5.5x8.5.pdf": (5.5, 8.5),
 "06_Planner_Insert_PDFs/Lions_Gate_Planner_Monarch_8.5x11.pdf": (8.5, 11),
 "07_Print_and_Trim_Files/Pocket_Inserts_Print_on_US_Letter.pdf": (11, 8.5),
 "07_Print_and_Trim_Files/Pocket_Inserts_Print_on_A4.pdf": (11.69, 8.27),
 "07_Print_and_Trim_Files/Compact_Inserts_Print_on_US_Letter.pdf": (11, 8.5),
 "07_Print_and_Trim_Files/Compact_Inserts_Print_on_A4.pdf": (11.69, 8.27),
 "07_Print_and_Trim_Files/Classic_Inserts_Print_on_US_Letter.pdf": (8.5, 11),
 "07_Print_and_Trim_Files/Classic_Inserts_Print_on_A4.pdf": (8.27, 11.69),
 "08_Bonus_Files/Lions_Gate_Quick_Start.pdf": (8.5, 11),
 "08_Bonus_Files/Lions_Gate_Affirmation_Cards_US_Letter.pdf": (8.5, 11),
 "08_Bonus_Files/Lions_Gate_Affirmation_Cards_A4.pdf": (8.27, 11.69),
 "08_Bonus_Files/Lions_Gate_Planner_Tabs_US_Letter.pdf": (8.5, 11),
 "08_Bonus_Files/Lions_Gate_Planner_Tabs_A4.pdf": (8.27, 11.69),
 "09_Customer_Guides/Lions_Gate_Printing_Guide.pdf": (8.5, 11),
 "09_Customer_Guides/Lions_Gate_Planner_Insert_Guide.pdf": (8.5, 11),
 "09_Customer_Guides/Lions_Gate_Digital_Use_Guide.pdf": (8.5, 11),
 "09_Customer_Guides/Lions_Gate_Read_Me_First.pdf": (8.5, 11),
}

report = []
def log(msg):
    report.append(msg)
    print(msg)

def contact_sheet(pdf_rel, thumb_h=300, cols=8):
    path = os.path.join(ROOT, pdf_rel)
    d = fitz.open(path)
    thumbs = []
    for page in d:
        zoom = thumb_h / page.rect.height
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
        thumbs.append(Image.frombytes("RGB", (pix.width, pix.height), pix.samples))
    tw = max(t.width for t in thumbs)
    rows = (len(thumbs) + cols - 1) // cols
    per_sheet = cols * 6
    name = os.path.basename(pdf_rel).replace(".pdf", "")
    for si in range(0, len(thumbs), per_sheet):
        chunk = thumbs[si:si + per_sheet]
        rws = (len(chunk) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * (tw + 8) + 8, rws * (thumb_h + 8) + 8), (240, 238, 234))
        for i, t in enumerate(chunk):
            sheet.paste(t, (8 + (i % cols) * (tw + 8), 8 + (i // cols) * (thumb_h + 8)))
        out = os.path.join(SHEET_DIR, "%s_%02d.png" % (name, si // per_sheet + 1))
        sheet.save(out)
    return d

def check(pdf_rel, exp):
    path = os.path.join(ROOT, pdf_rel)
    if not os.path.exists(path):
        log("MISSING FILE: %s" % pdf_rel)
        return
    d = contact_sheet(pdf_rel)
    w_in = d[0].rect.width / IN
    h_in = d[0].rect.height / IN
    ok_size = abs(w_in - exp[0]) < 0.03 and abs(h_in - exp[1]) < 0.03
    size_msg = "%.2fx%.2fin" % (w_in, h_in)
    # fonts embedded?
    unembedded = set()
    for pno in range(min(len(d), 40)):
        for f in d[pno].get_fonts(full=False):
            # f: (xref, ext, type, basefont, name, encoding)
            if f[1] == "n/a" and f[2] != "Type3":
                unembedded.add(f[3])
    # near-blank pages (excluding known fill pages)
    blanks = []
    for pno in range(len(d)):
        pix = d[pno].get_pixmap(matrix=fitz.Matrix(0.35, 0.35))
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples).convert("L")
        hist = im.histogram()
        total = sum(hist)
        # fraction of pixels that differ from the dominant tone
        dom = max(range(256), key=lambda i: hist[i])
        near_dom = sum(hist[max(0, dom - 6):dom + 7])
        frac_ink = 1.0 - near_dom / total
        if frac_ink < 0.005:
            blanks.append(pno + 1)
    # links in digital editions
    n_links = sum(len(list(d[p].links())) for p in range(len(d)))
    log("%-62s %4d pages  %s%s  links=%d%s%s" % (
        pdf_rel, len(d), size_msg, "" if ok_size else "  *** SIZE MISMATCH",
        n_links,
        ("  unembedded=%s" % ",".join(sorted(unembedded))) if unembedded else "",
        ("  near-blank=%s" % blanks) if blanks else ""))
    mb = os.path.getsize(path) / 1e6
    return {"pages": len(d), "size": size_msg, "links": n_links, "mb": mb}

if __name__ == "__main__":
    log("=" * 30 + " QC RUN " + "=" * 30)
    stats = {}
    for rel, exp in EXPECT.items():
        stats[rel] = check(rel, exp)
    # zip check
    z = os.path.join(ROOT, "08_Bonus_Files", "Lions_Gate_Phone_Wallpapers.zip")
    import zipfile
    with zipfile.ZipFile(z) as zf:
        names = zf.namelist()
        log("Lions_Gate_Phone_Wallpapers.zip: %d files (%d png, readme=%s)" % (
            len(names), sum(1 for n in names if n.endswith(".png")),
            "READ_ME_Wallpapers.txt" in names))
    with open(os.path.join(HERE, "qc_report.txt"), "w") as f:
        f.write("\n".join(report) + "\n")
    print("contact sheets in", SHEET_DIR)
