#!/usr/bin/env python3
"""
369 Portal — Digital Editions builder
Monkey-patches interior_v3 draw helpers to inject AcroForm text fields,
then re-runs every page-builder to produce two PDFs:

  369-portal-DIGITAL-FILLABLE.pdf   — typeable fields, desktop/mobile/browser
  369-portal-GOODNOTES.pdf          — same + PDF outline nav, taller fields for stylus
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import interior_v3 as base

from reportlab.lib.colors import HexColor, Color
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas as rlc

W, H = letter
M = 0.75 * inch
IW = W - 2 * M

INK   = HexColor("#1a1410")
WTEXT = HexColor("#ede5cc")
LINEC = HexColor("#4a3f34")
LGOLD = HexColor("#e0c060")
GOLD  = HexColor("#c9a84c")

TRANSPARENT = Color(0, 0, 0, 0)

# ── State shared across patches ────────────────────────────────────────────────
_fld        = [0]          # field counter
_goodnotes  = [False]      # True when building GoodNotes edition
_dark_page  = [False]      # True when current page has dark background


def _nf():
    _fld[0] += 1
    return f"f{_fld[0]:05d}"


def _field_height():
    return 18 if _goodnotes[0] else 14


def _text_color():
    return WTEXT if _dark_page[0] else INK


def _add_text_field(c, x, y_bottom, width, height, multiline=False):
    """Insert a transparent AcroForm text field."""
    flags = 'multiline' if multiline else ''
    c.acroForm.textfield(
        name=_nf(),
        x=x,
        y=y_bottom,
        width=width,
        height=height,
        fontSize=11,
        fontName="Helvetica",
        fillColor=None,
        borderColor=None,
        textColor=_text_color(),
        borderWidth=0,
        fieldFlags=flags,
        maxlen=2000 if multiline else 300,
    )


# ── Patched draw helpers ───────────────────────────────────────────────────────

def _write_line(c, x, y, width):
    """Draw visual underline + transparent text field above it."""
    c.saveState()
    c.setStrokeColor(LGOLD if _dark_page[0] else LINEC)
    c.setStrokeAlpha(1.0 if _dark_page[0] else 0.65)
    c.setLineWidth(0.65)
    c.line(x, y, x + width, y)
    c.restoreState()
    _add_text_field(c, x, y, width, _field_height())


def _write_lines_block(c, x, y, width, n, spacing):
    for i in range(n):
        _write_line(c, x, y - i * spacing, width)
    return y - n * spacing


def _bordered_box(c, x, y_top, w, h, label=None, label_size=10, dark=False):
    """Draw gold border + multiline text field inside."""
    ink  = base.WTEXT if dark else base.INK
    gclr = base.LGOLD if dark else base.GOLD
    c.saveState()
    c.setStrokeColor(gclr)
    c.setLineWidth(0.85)
    c.rect(x, y_top - h, w, h, stroke=1, fill=0)
    if label:
        c.setFillColor(ink)
        c.setFont("Arsenal", label_size)
        c.drawString(x + 7, y_top - 14, label)
    c.restoreState()
    label_offset = 18 if label else 4
    _add_text_field(c, x + 4, y_top - h + 4, w - 8, h - label_offset - 4,
                    multiline=True)
    return y_top - h


# ── Wrap page builders to set dark-page flag ───────────────────────────────────

def _cream_page(fn, *args, **kwargs):
    _dark_page[0] = False
    fn(*args, **kwargs)


def _dark_page_fn(fn, *args, **kwargs):
    _dark_page[0] = True
    fn(*args, **kwargs)


# ── Bookmark helper (GoodNotes only) ──────────────────────────────────────────

def _bm(c, title, level=0):
    if not _goodnotes[0]:
        return
    key = f"bm{_fld[0]:05d}"
    c.bookmarkPage(key)
    c.addOutlineEntry(title, key, level=level)


# ── Page sequence (shared for both editions) ──────────────────────────────────

def _build_all(c):
    pn = 1

    # ── Front matter ─────────────────────────────────────────────────────────
    _bm(c, "Cover")
    _dark_page[0] = True;  base.build_cover(c);            c.showPage(); pn += 1

    _bm(c, "Title Page")
    _dark_page[0] = False; base.build_title_page(c, pn);   c.showPage(); pn += 1

    _bm(c, "Welcome")
    _dark_page[0] = True;  base.build_welcome(c, pn);      c.showPage(); pn += 1

    _bm(c, "The 369 Method")
    _dark_page[0] = False; base.build_method(c, pn);       c.showPage(); pn += 1

    _bm(c, "How to Use")
    _dark_page[0] = False; base.build_how_to_use(c, pn);   c.showPage(); pn += 1

    _bm(c, "My Portal Desire Statement")
    _dark_page[0] = False; base.build_portal_intention(c, pn); c.showPage(); pn += 1

    _bm(c, "My Commitments")
    _dark_page[0] = False; base.build_commitments(c, pn);  c.showPage(); pn += 1

    _bm(c, "Moon Phase Guide")
    _dark_page[0] = True;  base.build_moon_overview(c, pn); c.showPage(); pn += 1

    # ── Daily pages ───────────────────────────────────────────────────────────
    _bm(c, "Daily Practice", level=0)
    for day in range(1, 29):
        week = (day - 1) // 7 + 1
        if day in (1, 8, 15, 22):
            _bm(c, f"  Week {week}", level=1)
        _bm(c, f"    Day {day} — Morning & Midday", level=2)
        _dark_page[0] = False
        base.build_morning_page(c, day, pn); c.showPage(); pn += 1

        _bm(c, f"    Day {day} — Evening", level=2)
        _dark_page[0] = False
        base.build_evening_page(c, day, pn); c.showPage(); pn += 1

    # ── Weekly Reviews ────────────────────────────────────────────────────────
    _bm(c, "Weekly Reviews", level=0)
    for week in range(1, 5):
        _bm(c, f"  Week {week} Review", level=1)
        _dark_page[0] = False
        base.build_weekly_review(c, week, pn); c.showPage(); pn += 1

    # ── Monthly Review ────────────────────────────────────────────────────────
    _bm(c, "Monthly Review", level=0)
    month_labels = ["Overview", "Evidence & Alignment", "Shadow Integration", "Portal Forward"]
    for i in range(4):
        _bm(c, f"  {month_labels[i]}", level=1)
        _dark_page[0] = False
        base.build_monthly_review(c, i, pn); c.showPage(); pn += 1

    # ── Shadow Work ───────────────────────────────────────────────────────────
    _bm(c, "Shadow Work", level=0)
    for i in range(8):
        _bm(c, f"  {base.SHADOW_WORK[i][0]}", level=1)
        _dark_page[0] = False
        base.build_shadow_work(c, i, pn); c.showPage(); pn += 1

    # ── Synchronicity Log ─────────────────────────────────────────────────────
    _bm(c, "Synchronicity Log", level=0)
    for _ in range(16):
        _dark_page[0] = False
        base.build_sync_log(c, pn); c.showPage(); pn += 1

    # ── Moon Calendar ─────────────────────────────────────────────────────────
    _bm(c, "Moon Calendar", level=0)
    for month_idx in range(4):
        _bm(c, f"  {base.MOON_MONTH_NAMES[month_idx]} Month", level=1)
        for page_in_month in range(4):
            title, is_dark, _ = base.MOON_PAGE_INFO[page_in_month]
            _bm(c, f"    {title}", level=2)
            _dark_page[0] = is_dark
            base.build_moon_calendar(c, month_idx, page_in_month, pn)
            c.showPage(); pn += 1

    # ── Bonus Pages ───────────────────────────────────────────────────────────
    _bm(c, "Bonus Pages", level=0)
    for i in range(8):
        _bm(c, f"  {base.BONUS_TITLES[i]}", level=1)
        _dark_page[0] = False
        base.build_bonus_page(c, i, pn); c.showPage(); pn += 1

    # ── Closing ───────────────────────────────────────────────────────────────
    _bm(c, "Closing", level=0)
    _dark_page[0] = True
    base.build_closing(c, pn)
    c.showPage()

    return pn


# ── Install patches ────────────────────────────────────────────────────────────

def _install_patches():
    base.write_line         = _write_line
    base.write_lines_block  = _write_lines_block
    base.bordered_box       = _bordered_box


# ── Moon overview dark-page note lines ────────────────────────────────────────
# The 4 "MY MOON NOTES" lines in build_moon_overview use raw canvas.line() calls
# (not write_line) so we need a small wrapper that also injects fields.

_orig_moon_overview = base.build_moon_overview

def _patched_moon_overview(c, pn):
    """Run original builder then overlay text fields on the 4 moon note lines."""
    _orig_moon_overview(c, pn)
    # The 4 gold note lines sit at y positions starting at ~135 pt from bottom
    # (computed from build_moon_overview layout: footer at FY=26, lines spaced 28pt)
    # We lay fields over them conservatively.
    y_start = 134 + 28 * 3  # top of first note line ≈ 218
    for i in range(4):
        y = y_start - i * 28
        _add_text_field(c, M, y, IW, _field_height())


# ── Build functions ────────────────────────────────────────────────────────────

def build_fillable(out_path):
    _install_patches()
    _goodnotes[0] = False
    _fld[0] = 0

    c = rlc.Canvas(out_path, pagesize=letter)
    base.build_moon_overview = _patched_moon_overview
    pages = _build_all(c)
    c.save()
    size_kb = os.path.getsize(out_path) // 1024
    print(f"Saved  {out_path}  ({pages} pages, {size_kb} KB)  [FILLABLE]")


def build_goodnotes(out_path):
    _install_patches()
    _goodnotes[0] = True
    _fld[0] = 0

    c = rlc.Canvas(out_path, pagesize=letter)
    base.build_moon_overview = _patched_moon_overview
    pages = _build_all(c)
    c.save()
    size_kb = os.path.getsize(out_path) // 1024
    print(f"Saved  {out_path}  ({pages} pages, {size_kb} KB)  [GOODNOTES]")


def main():
    base.setup_fonts()

    fillable_path  = os.path.join(HERE, "369-portal-DIGITAL-FILLABLE.pdf")
    goodnotes_path = os.path.join(HERE, "369-portal-GOODNOTES.pdf")

    print("Building fillable edition...")
    build_fillable(fillable_path)

    print("Building GoodNotes edition...")
    build_goodnotes(goodnotes_path)

    print("\nDone. Files written to outputs/")


if __name__ == "__main__":
    main()
