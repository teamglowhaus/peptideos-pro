#!/usr/bin/env python3
"""
369 Portal — Digital Editions builder  (v2 — all fixes applied)

Produces three PDFs:
  369-portal-DIGITAL-FILLABLE.pdf      — typeable fields, all devices
  369-portal-TABLET-NAVIGATION.pdf     — same + PDF outline nav + taller fields
  369-portal-A4-PRINTABLE.pdf          — A4 Letter (international print)

Fixes applied:
  • Moon-note y-positions corrected (were 80pt too high)
  • Energy bar overlay text field added (digits 1-10 typeable)
  • GoodNotes claim removed — renamed to Tablet/PDF-reader navigation
  • Tab order: fields added top-to-bottom per page; /Tabs /S injected per page
  • Dark pages use WTEXT for field text colour
  • "Rewires subconscious" copy fixed in interior_v3.py separately
"""

import os, sys, struct, zlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import interior_v3 as base

from reportlab.lib.colors import HexColor, Color
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
FC_CLASSIC  = (5.5 * inch, 8.5 * inch)   # 396 × 612 pt
FC_COMPACT  = (4.25 * inch, 6.75 * inch)  # 306 × 486 pt
from reportlab.pdfgen import canvas as rlc

W, H = letter
M    = 0.75 * inch
IW   = W - 2 * M

INK   = HexColor("#1a1410")
WTEXT = HexColor("#ede5cc")
LINEC = HexColor("#4a3f34")
LGOLD = HexColor("#e0c060")
GOLD  = HexColor("#c9a84c")

# ── Shared state ───────────────────────────────────────────────────────────────
_fld       = [0]
_tablet    = [False]   # True → taller fields + outline nav
_dark_page = [False]


def _nf():
    _fld[0] += 1
    return f"f{_fld[0]:05d}"


def _field_height():
    return 20 if _tablet[0] else 14


def _text_color():
    return WTEXT if _dark_page[0] else INK


def _add_text_field(c, x, y_bottom, width, height, multiline=False):
    flags = "multiline" if multiline else ""
    c.acroForm.textfield(
        name=_nf(),
        x=x, y=y_bottom,
        width=width, height=height,
        fontSize=11, fontName="Helvetica",
        fillColor=None, borderColor=None,
        textColor=_text_color(),
        borderWidth=0,
        fieldFlags=flags,
        maxlen=2000 if multiline else 300,
    )


# ── Tab order: inject /Tabs /S into page dictionary after each showPage ────────
# ReportLab exposes the page dict via canvas._doc._pages[-1].pagedict after save.
# We wrap showPage to tag each finished page with structural tab order.

_canvas_ref = [None]

def _set_tabs_on_last_page():
    """Add /Tabs /S to the most-recently-finalised page dict."""
    try:
        doc = _canvas_ref[0]._doc
        # Pages are stored in doc.Pages.pages list
        pages_list = doc.Pages.pages
        if pages_list:
            last = pages_list[-1]
            # Inject /Tabs /S — tells PDF viewers to tab in structural order
            from reportlab.pdfbase.pdfdoc import PDFName
            last.__dict__["Tabs"] = PDFName("S")
    except Exception:
        pass  # non-fatal; tab order degrades gracefully


# ── Patched draw helpers ───────────────────────────────────────────────────────

def _write_line(c, x, y, width):
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


# ── Energy bar: overlay a transparent text field across the bar ────────────────
# Buyers click anywhere on the bar and type their level (1-10).

_orig_energy_bar = base.energy_bar

def _patched_energy_bar(c, x, y):
    result = _orig_energy_bar(c, x, y)
    # Bar occupies x..(x+IW), (y-26)..y  — overlay one transparent field
    _add_text_field(c, x, y - 26, base.IW, 26)
    return result


# ── Bookmark helper (tablet/navigation edition only) ──────────────────────────

def _bm(c, title, level=0):
    if not _tablet[0]:
        return
    key = f"bm{_fld[0]:05d}"
    c.bookmarkPage(key)
    c.addOutlineEntry(title, key, level=level)


# ── Moon overview: corrected y-positions for the 4 raw note lines ─────────────
# Traced from build_moon_overview layout (H=792, M=54):
#   y_start = 792-54-22 - 42 - 18 - 36 - (4*82+16) - 28 - 22 - 36 - 28 - 22 = 140
#   spacing = 28 pt

_orig_moon_overview = base.build_moon_overview

def _patched_moon_overview(c, pn):
    _orig_moon_overview(c, pn)
    y_start = 140   # y of first moon-note line (was wrongly 218)
    for i in range(4):
        _add_text_field(c, M, y_start - i * 28, IW, _field_height())


# ── Page sequence ──────────────────────────────────────────────────────────────

def _showpage(c):
    """showPage wrapper: tag finished page with /Tabs /S then advance."""
    c.showPage()
    _set_tabs_on_last_page()


def _build_all(c):
    _canvas_ref[0] = c
    pn = 1

    _bm(c, "Cover")
    _dark_page[0] = True;  base.build_cover(c);             _showpage(c); pn += 1

    _bm(c, "Title Page")
    _dark_page[0] = False; base.build_title_page(c, pn);    _showpage(c); pn += 1

    _bm(c, "Welcome")
    _dark_page[0] = True;  base.build_welcome(c, pn);       _showpage(c); pn += 1

    _bm(c, "The 369 Method")
    _dark_page[0] = False; base.build_method(c, pn);        _showpage(c); pn += 1

    _bm(c, "How to Use")
    _dark_page[0] = False; base.build_how_to_use(c, pn);    _showpage(c); pn += 1

    _bm(c, "My Portal Desire Statement")
    _dark_page[0] = False; base.build_portal_intention(c, pn); _showpage(c); pn += 1

    _bm(c, "My Commitments")
    _dark_page[0] = False; base.build_commitments(c, pn);   _showpage(c); pn += 1

    _bm(c, "Moon Phase Guide")
    _dark_page[0] = True;  base.build_moon_overview(c, pn); _showpage(c); pn += 1

    _bm(c, "Daily Practice", level=0)
    for day in range(1, 29):
        week = (day - 1) // 7 + 1
        if day in (1, 8, 15, 22):
            _bm(c, f"  Week {week}", level=1)
        _bm(c, f"    Day {day} — Morning & Midday", level=2)
        _dark_page[0] = False
        base.build_morning_page(c, day, pn); _showpage(c); pn += 1

        _bm(c, f"    Day {day} — Evening", level=2)
        _dark_page[0] = False
        base.build_evening_page(c, day, pn); _showpage(c); pn += 1

    _bm(c, "Weekly Reviews", level=0)
    for week in range(1, 5):
        _bm(c, f"  Week {week} Review", level=1)
        _dark_page[0] = False
        base.build_weekly_review(c, week, pn); _showpage(c); pn += 1

    _bm(c, "Monthly Review", level=0)
    month_labels = ["Overview", "Evidence & Alignment", "Shadow Integration", "Portal Forward"]
    for i in range(4):
        _bm(c, f"  {month_labels[i]}", level=1)
        _dark_page[0] = False
        base.build_monthly_review(c, i, pn); _showpage(c); pn += 1

    _bm(c, "Shadow Work", level=0)
    for i in range(8):
        _bm(c, f"  {base.SHADOW_WORK[i][0]}", level=1)
        _dark_page[0] = False
        base.build_shadow_work(c, i, pn); _showpage(c); pn += 1

    _bm(c, "Synchronicity Log", level=0)
    for _ in range(16):
        _dark_page[0] = False
        base.build_sync_log(c, pn); _showpage(c); pn += 1

    _bm(c, "Moon Calendar", level=0)
    for month_idx in range(4):
        _bm(c, f"  {base.MOON_MONTH_NAMES[month_idx]} Month", level=1)
        for page_in_month in range(4):
            title, is_dark, _ = base.MOON_PAGE_INFO[page_in_month]
            _bm(c, f"    {title}", level=2)
            _dark_page[0] = is_dark
            base.build_moon_calendar(c, month_idx, page_in_month, pn)
            _showpage(c); pn += 1

    _bm(c, "Bonus Pages", level=0)
    for i in range(8):
        _bm(c, f"  {base.BONUS_TITLES[i]}", level=1)
        _dark_page[0] = False
        base.build_bonus_page(c, i, pn); _showpage(c); pn += 1

    _bm(c, "Closing", level=0)
    _dark_page[0] = True
    base.build_closing(c, pn)
    _showpage(c)

    return pn


def _install_patches():
    base.write_line        = _write_line
    base.write_lines_block = _write_lines_block
    base.bordered_box      = _bordered_box
    base.energy_bar        = _patched_energy_bar
    base.build_moon_overview = _patched_moon_overview


# ── Build: Digital Fillable ────────────────────────────────────────────────────

def build_fillable(out_path):
    _install_patches()
    _tablet[0]    = False
    _fld[0]       = 0
    _dark_page[0] = False

    c = rlc.Canvas(out_path, pagesize=letter)
    pages = _build_all(c)
    c.save()
    print(f"Saved  {out_path}  ({pages} pages, {os.path.getsize(out_path)//1024} KB)  [FILLABLE]")


# ── Build: Tablet/PDF-Reader Navigation Edition ────────────────────────────────

def build_tablet_nav(out_path):
    _install_patches()
    _tablet[0]    = True
    _fld[0]       = 0
    _dark_page[0] = False

    c = rlc.Canvas(out_path, pagesize=letter)
    pages = _build_all(c)
    c.save()
    print(f"Saved  {out_path}  ({pages} pages, {os.path.getsize(out_path)//1024} KB)  [TABLET NAV]")


# ── Scaled canvas: draws Letter content scaled-to-fit on a smaller page ──────
# showPage() resets the canvas transform, so we reapply automatically.

class _ScaledCanvas(rlc.Canvas):
    """Canvas that transparently scales Letter-coordinate content to fit any page."""
    def __init__(self, filename, pagesize, src_size=letter):
        super().__init__(filename, pagesize=pagesize)
        pw, ph = pagesize
        sw, sh = src_size
        self._sc  = min(pw / sw, ph / sh)
        self._ox  = (pw - sw * self._sc) / 2
        self._oy  = (ph - sh * self._sc) / 2
        self._apply()

    def _apply(self):
        self.transform(self._sc, 0, 0, self._sc, self._ox, self._oy)

    def showPage(self):
        super().showPage()
        self._apply()


# ── Build: Franklin Covey print editions ─────────────────────────────────────

def _build_fc_print(out_path, pagesize, label):
    """Render the full journal scaled to fit a Franklin Covey page size."""
    base.PRINT_SAFE = True
    # Restore unpatched draw functions (print — no form fields)
    base.write_line          = base._orig_write_line  if hasattr(base, "_orig_write_line")  else _orig_write_line_draw
    base.write_lines_block   = base._orig_wlb         if hasattr(base, "_orig_wlb")         else _orig_wlb_draw
    base.bordered_box        = base._orig_bordered_box if hasattr(base, "_orig_bordered_box") else _orig_bb_draw
    base.energy_bar          = _orig_energy_bar
    base.build_moon_overview = _orig_moon_overview

    c = _ScaledCanvas(out_path, pagesize=pagesize)
    pn = 1
    base.build_cover(c);             c.showPage(); pn += 1
    base.build_title_page(c, pn);    c.showPage(); pn += 1
    base.build_welcome(c, pn);       c.showPage(); pn += 1
    base.build_method(c, pn);        c.showPage(); pn += 1
    base.build_how_to_use(c, pn);    c.showPage(); pn += 1
    base.build_portal_intention(c, pn); c.showPage(); pn += 1
    base.build_commitments(c, pn);   c.showPage(); pn += 1
    base.build_moon_overview(c, pn); c.showPage(); pn += 1
    for day in range(1, 29):
        base.build_morning_page(c, day, pn); c.showPage(); pn += 1
        base.build_evening_page(c, day, pn); c.showPage(); pn += 1
    for week in range(1, 5):
        base.build_weekly_review(c, week, pn); c.showPage(); pn += 1
    for i in range(4):
        base.build_monthly_review(c, i, pn); c.showPage(); pn += 1
    for i in range(8):
        base.build_shadow_work(c, i, pn); c.showPage(); pn += 1
    for _ in range(16):
        base.build_sync_log(c, pn); c.showPage(); pn += 1
    for month_idx in range(4):
        for page_in_month in range(4):
            base.build_moon_calendar(c, month_idx, page_in_month, pn)
            c.showPage(); pn += 1
    for i in range(8):
        base.build_bonus_page(c, i, pn); c.showPage(); pn += 1
    base.build_closing(c, pn); c.showPage()

    c.save()
    base.PRINT_SAFE = False
    scale_pct = int(min(pagesize[0]/letter[0], pagesize[1]/letter[1]) * 100)
    print(f"Saved  {out_path}  ({pn} pages, {os.path.getsize(out_path)//1024} KB)  [{label} — {scale_pct}% scale]")


# ── Build: A4 Printable ────────────────────────────────────────────────────────

def build_a4(out_path):
    """Rebuild journal at A4 page size for international buyers."""
    base.PRINT_SAFE = True
    # Patch base module geometry to A4
    orig_W, orig_H, orig_IW = base.W, base.H, base.IW
    base.W, base.H = A4          # 595.27 × 841.89 pt
    base.IW = base.W - 2 * base.M   # 595.27 - 108 = 487.27

    # Restore original draw helpers (no form fields for print version)
    base.write_line        = base._orig_write_line  if hasattr(base, "_orig_write_line")  else _orig_write_line_draw
    base.write_lines_block = base._orig_wlb         if hasattr(base, "_orig_wlb")         else _orig_wlb_draw
    base.bordered_box      = base._orig_bordered_box if hasattr(base, "_orig_bordered_box") else _orig_bb_draw
    base.energy_bar        = _orig_energy_bar
    base.build_moon_overview = _orig_moon_overview

    c = rlc.Canvas(out_path, pagesize=A4)
    pn = 1
    base.build_cover(c);             c.showPage(); pn += 1
    base.build_title_page(c, pn);    c.showPage(); pn += 1
    base.build_welcome(c, pn);       c.showPage(); pn += 1
    base.build_method(c, pn);        c.showPage(); pn += 1
    base.build_how_to_use(c, pn);    c.showPage(); pn += 1
    base.build_portal_intention(c, pn); c.showPage(); pn += 1
    base.build_commitments(c, pn);   c.showPage(); pn += 1
    base.build_moon_overview(c, pn); c.showPage(); pn += 1
    for day in range(1, 29):
        base.build_morning_page(c, day, pn); c.showPage(); pn += 1
        base.build_evening_page(c, day, pn); c.showPage(); pn += 1
    for week in range(1, 5):
        base.build_weekly_review(c, week, pn); c.showPage(); pn += 1
    for i in range(4):
        base.build_monthly_review(c, i, pn); c.showPage(); pn += 1
    for i in range(8):
        base.build_shadow_work(c, i, pn); c.showPage(); pn += 1
    for _ in range(16):
        base.build_sync_log(c, pn); c.showPage(); pn += 1
    for month_idx in range(4):
        for page_in_month in range(4):
            base.build_moon_calendar(c, month_idx, page_in_month, pn)
            c.showPage(); pn += 1
    for i in range(8):
        base.build_bonus_page(c, i, pn); c.showPage(); pn += 1
    base.build_closing(c, pn); c.showPage()

    c.save()
    print(f"Saved  {out_path}  ({pn} pages, {os.path.getsize(out_path)//1024} KB)  [A4 PRINT]")

    base.PRINT_SAFE = False
    # Restore geometry
    base.W, base.H, base.IW = orig_W, orig_H, orig_IW


# Store unpatched draw functions for the A4 builder to restore
import importlib, types

def _make_orig_draw_fns():
    """Capture the clean draw functions before any patching."""
    import interior_v3 as _b
    _b._orig_write_line   = _b.write_line
    _b._orig_wlb          = _b.write_lines_block
    _b._orig_bordered_box = _b.bordered_box

# ── Helper stubs (used by build_a4 before capture) ────────────────────────────

def _orig_write_line_draw(c, x, y, width):
    from reportlab.lib.colors import HexColor
    LINEC = HexColor("#4a3f34")
    c.saveState()
    c.setStrokeColor(LINEC)
    c.setStrokeAlpha(0.65)
    c.setLineWidth(0.65)
    c.line(x, y, x + width, y)
    c.restoreState()

def _orig_wlb_draw(c, x, y, width, n, spacing):
    for i in range(n):
        _orig_write_line_draw(c, x, y - i * spacing, width)
    return y - n * spacing

def _orig_bb_draw(c, x, y_top, w, h, label=None, label_size=10, dark=False):
    from reportlab.lib.colors import HexColor
    ink  = HexColor("#ede5cc") if dark else HexColor("#1a1410")
    gclr = HexColor("#e0c060") if dark else HexColor("#c9a84c")
    c.saveState()
    c.setStrokeColor(gclr)
    c.setLineWidth(0.85)
    c.rect(x, y_top - h, w, h, stroke=1, fill=0)
    if label:
        c.setFillColor(ink)
        c.setFont("Arsenal", label_size)
        c.drawString(x + 7, y_top - 14, label)
    c.restoreState()
    return y_top - h


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    base.setup_fonts()
    _make_orig_draw_fns()

    fillable_path = os.path.join(HERE, "369-portal-DIGITAL-FILLABLE.pdf")
    tablet_path   = os.path.join(HERE, "369-portal-TABLET-NAVIGATION.pdf")
    a4_path       = os.path.join(HERE, "369-portal-A4-PRINTABLE.pdf")
    fc_classic_path = os.path.join(HERE, "369-portal-FC-CLASSIC-PRINTABLE.pdf")
    fc_compact_path = os.path.join(HERE, "369-portal-FC-COMPACT-PRINTABLE.pdf")

    print("Building A4 print edition...")
    build_a4(a4_path)

    print("Building Franklin Covey Classic (5.5×8.5) print edition...")
    _build_fc_print(fc_classic_path, FC_CLASSIC, "FC CLASSIC")

    print("Building Franklin Covey Compact (4.25×6.75) print edition...")
    _build_fc_print(fc_compact_path, FC_COMPACT, "FC COMPACT")

    base.PRINT_SAFE = False
    print("Building fillable edition...")
    build_fillable(fillable_path)

    print("Building tablet navigation edition...")
    build_tablet_nav(tablet_path)

    print("\nDone.")


if __name__ == "__main__":
    main()
