# -*- coding: utf-8 -*-
"""
Ukrainian digital editions:
  • Заповнюваний PDF  — typeable AcroForm fields on every write line
  • Планшетна версія  — same + full Ukrainian bookmark outline + taller fields

Ported from interior_digital.py, driving interior_uk_gen (Ukrainian builder).
"""

import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import interior_uk_gen as base

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas as rlc

W, H = letter
M    = 0.75 * inch
IW   = W - 2 * M

INK   = HexColor("#1a1410")
WTEXT = HexColor("#ede5cc")
LINEC = HexColor("#4a3f34")
LGOLD = HexColor("#e0c060")

_fld       = [0]
_bmn       = [0]
_tablet    = [False]
_dark_page = [False]
_canvas_ref = [None]


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
        name=_nf(), x=x, y=y_bottom, width=width, height=height,
        fontSize=11, fontName="Helvetica",
        fillColor=None, borderColor=None, textColor=_text_color(),
        borderWidth=0, fieldFlags=flags,
        maxlen=2000 if multiline else 300,
    )


def _set_tabs_on_last_page():
    try:
        doc = _canvas_ref[0]._doc
        pages_list = doc.Pages.pages
        if pages_list:
            from reportlab.pdfbase.pdfdoc import PDFName
            pages_list[-1].__dict__["Tabs"] = PDFName("S")
    except Exception:
        pass


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


_orig_energy_bar = base.energy_bar

def _patched_energy_bar(c, x, y):
    result = _orig_energy_bar(c, x, y)
    _add_text_field(c, x, y - 26, base.IW, 26)
    return result


_orig_moon_overview = base.build_moon_overview

def _patched_moon_overview(c, pn):
    _orig_moon_overview(c, pn)
    y_start = 140
    for i in range(4):
        _add_text_field(c, M, y_start - i * 28, IW, _field_height())


def _bm(c, title, level=0):
    if not _tablet[0]:
        return
    _bmn[0] += 1
    key = f"bm{_bmn[0]:05d}"
    c.bookmarkPage(key)
    c.addOutlineEntry(title, key, level=level)


def _showpage(c):
    c.showPage()
    _set_tabs_on_last_page()


def _build_all(c):
    _canvas_ref[0] = c
    pn = 1

    _bm(c, "Обкладинка")
    _dark_page[0] = True;  base.build_cover(c);             _showpage(c); pn += 1

    _bm(c, "Титульна сторінка")
    _dark_page[0] = False; base.build_title_page(c, pn);    _showpage(c); pn += 1

    _bm(c, "Ліцензія та умови")
    _dark_page[0] = False; base.build_license_page(c, pn);  _showpage(c); pn += 1

    _bm(c, "Вітання")
    _dark_page[0] = True;  base.build_welcome(c, pn);       _showpage(c); pn += 1

    _bm(c, "Метод 369")
    _dark_page[0] = False; base.build_method(c, pn);        _showpage(c); pn += 1

    _bm(c, "Як користуватися")
    _dark_page[0] = False; base.build_how_to_use(c, pn);    _showpage(c); pn += 1

    _bm(c, "Формулювання бажання")
    _dark_page[0] = False; base.build_portal_intention(c, pn); _showpage(c); pn += 1

    _bm(c, "Мої обіцянки")
    _dark_page[0] = False; base.build_commitments(c, pn);   _showpage(c); pn += 1

    _bm(c, "Путівник фазами Місяця")
    _dark_page[0] = True;  base.build_moon_overview(c, pn); _showpage(c); pn += 1

    _bm(c, "Щоденна практика", level=0)
    for day in range(1, 29):
        week = (day - 1) // 7 + 1
        if day in (1, 8, 15, 22):
            _bm(c, f"  Тиждень {week}", level=1)
        _bm(c, f"    День {day} — Ранок та опівдні", level=2)
        _dark_page[0] = False
        base.build_morning_page(c, day, pn); _showpage(c); pn += 1

        _bm(c, f"    День {day} — Вечір", level=2)
        _dark_page[0] = False
        base.build_evening_page(c, day, pn); _showpage(c); pn += 1

    _bm(c, "Тижневі підсумки", level=0)
    for week in range(1, 5):
        _bm(c, f"  Підсумок тижня {week}", level=1)
        _dark_page[0] = False
        base.build_weekly_review(c, week, pn); _showpage(c); pn += 1

    _bm(c, "Місячний підсумок", level=0)
    month_labels = ["Огляд", "Докази та суголосся", "Інтеграція тіні", "Портал уперед"]
    for i in range(4):
        _bm(c, f"  {month_labels[i]}", level=1)
        _dark_page[0] = False
        base.build_monthly_review(c, i, pn); _showpage(c); pn += 1

    _bm(c, "Робота з тінню", level=0)
    for i in range(8):
        _bm(c, f"  {base.SHADOW_WORK[i][0]}", level=1)
        _dark_page[0] = False
        base.build_shadow_work(c, i, pn); _showpage(c); pn += 1

    _bm(c, "Журнал синхронічностей", level=0)
    for _ in range(16):
        _dark_page[0] = False
        base.build_sync_log(c, pn); _showpage(c); pn += 1

    _bm(c, "Місячний календар", level=0)
    for month_idx in range(4):
        _bm(c, f"  {base.MOON_MONTH_NAMES[month_idx]} місяць", level=1)
        for page_in_month in range(4):
            title, is_dark, _t = base.MOON_PAGE_INFO[page_in_month]
            _bm(c, f"    {title}", level=2)
            _dark_page[0] = is_dark
            base.build_moon_calendar(c, month_idx, page_in_month, pn)
            _showpage(c); pn += 1

    _bm(c, "Бонусні сторінки", level=0)
    for i in range(8):
        _bm(c, f"  {base.BONUS_TITLES[i]}", level=1)
        _dark_page[0] = False
        base.build_bonus_page(c, i, pn); _showpage(c); pn += 1

    _bm(c, "Завершення", level=0)
    _dark_page[0] = True
    base.build_closing(c, pn);  _showpage(c); pn += 1

    _bm(c, "Подяка", level=0)
    _dark_page[0] = True
    base.build_thank_you(c, pn)
    _showpage(c)

    return pn


def _install_patches():
    base.write_line          = _write_line
    base.write_lines_block   = _write_lines_block
    base.bordered_box        = _bordered_box
    base.energy_bar          = _patched_energy_bar
    base.build_moon_overview = _patched_moon_overview


def build_fillable(out_path):
    _install_patches()
    _tablet[0] = False; _fld[0] = 0; _dark_page[0] = False
    c = rlc.Canvas(out_path, pagesize=letter)
    pages = _build_all(c)
    c.save()
    print(f"Saved  {out_path}  ({pages} pages, {_fld[0]} fields, "
          f"{os.path.getsize(out_path)//1024} KB)  [FILLABLE]")


def build_tablet_nav(out_path):
    _install_patches()
    _tablet[0] = True; _fld[0] = 0; _bmn[0] = 0; _dark_page[0] = False
    c = rlc.Canvas(out_path, pagesize=letter)
    pages = _build_all(c)
    c.save()
    print(f"Saved  {out_path}  ({pages} pages, {_fld[0]} fields, "
          f"{os.path.getsize(out_path)//1024} KB)  [TABLET NAV]")


def main():
    base.PRINT_SAFE = False       # digital keeps the dark celestial aesthetic
    base.setup_fonts()
    build_fillable(os.path.join(HERE, "Портал 369 — Заповнюваний PDF.pdf"))
    build_tablet_nav(os.path.join(HERE, "Портал 369 — Планшетна версія (навігація).pdf"))
    print("\nDone.")


if __name__ == "__main__":
    main()
