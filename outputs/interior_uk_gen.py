#!/usr/bin/env python3
"""
369 Portal Manifestation Journal — interior_v3.py
121-page print-ready 8.5×11 PDF built with ReportLab.
All text on cream pages uses dark ink #1a1410.
Gold (#c9a84c) is reserved exclusively for decorative elements.
"""

import os
import math
from reportlab.pdfgen import canvas as rlc
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, Color

# ── Paths ──────────────────────────────────────────────────────────────────────
FONT_DIR = "/mnt/skills/examples/canvas-design/canvas-fonts"
HERE     = os.path.dirname(os.path.abspath(__file__))

# ── Page geometry ──────────────────────────────────────────────────────────────
W, H  = letter           # 612 × 792 pt
M     = 0.75 * inch      # margin = 54 pt
IW    = W - 2 * M        # inner width = 504 pt
FY    = 26               # footer centre Y (pt from bottom)

# When True, pages that have write lines use cream backgrounds so handwriting
# shows up on printed paper. Digital editions leave this False.
PRINT_SAFE = False

# ── Colour palette ─────────────────────────────────────────────────────────────
INK     = HexColor("#1a1410")  # ALL readable text on cream pages
INK2    = HexColor("#2e2620")  # secondary body text
GOLD    = HexColor("#c9a84c")  # decorative only: rules, ornaments, borders, geometry
CREAM   = HexColor("#faf6f0")  # cream page background
DARKBG  = HexColor("#120e0b")  # dark page background
DARKBG2 = HexColor("#1c1610")  # dark page accent
WTEXT   = HexColor("#ede5cc")  # text on dark pages
LGOLD   = HexColor("#e0c060")  # brighter gold for dark pages
LINEC   = HexColor("#4a3f34")  # write-line stroke
BFILL   = HexColor("#ece7de")  # energy bar cell fill (subtle)
BGOLD   = HexColor("#dbb84a")  # energy bar border gold


# ── Font registration ──────────────────────────────────────────────────────────

def setup_fonts():
    # Ukrainian (Cyrillic) edition: map the same internal font names to
    # Cyrillic-complete faces so no drawing code changes.
    #   Italiana / Crimson / Gloock  -> Lora  (elegant serif, full Cyrillic)
    #   Arsenal (Ukrainian typeface) -> kept  (labels / small caps)
    #   Jura                         -> kept  (geometric accents)
    fonts = {
        "Italiana":      "Lora-Regular.ttf",
        "CrimsonPro":    "Lora-Regular.ttf",
        "CrimsonItal":   "Lora-Italic.ttf",
        "CrimsonBold":   "Lora-Bold.ttf",
        "Arsenal":       "ArsenalSC-Regular.ttf",
        "Jura":          "Jura-Light.ttf",
        "Gloock":        "Lora-Bold.ttf",
    }
    for name, fname in fonts.items():
        path = os.path.join(FONT_DIR, fname)
        pdfmetrics.registerFont(TTFont(name, path))
    # Symbol fallback for ornaments the Cyrillic faces lack (◆ ✶ moon glyphs)
    pdfmetrics.registerFont(
        TTFont("Sym", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))


# ── Background fills ───────────────────────────────────────────────────────────

def cream_bg(c):
    c.saveState()
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    c.restoreState()


def dark_bg(c):
    c.saveState()
    c.setFillColor(DARKBG)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    c.restoreState()


# ── Corner marks ───────────────────────────────────────────────────────────────

def corner_marks(c, color=GOLD):
    arm = 14
    pad = 26
    pts = [
        (pad,     H - pad,  1,  -1),
        (W - pad, H - pad, -1,  -1),
        (pad,     pad,      1,   1),
        (W - pad, pad,     -1,   1),
    ]
    c.saveState()
    c.setStrokeColor(color)
    c.setLineWidth(0.8)
    for (x, y, sx, sy) in pts:
        c.line(x, y, x + sx * arm, y)
        c.line(x, y, x, y + sy * arm)
    c.restoreState()


# ── Flower of Life sacred geometry ─────────────────────────────────────────────

def flower_of_life(c, cx, cy, r, rings=2, color=GOLD, alpha=0.30):
    sq3 = math.sqrt(3)
    # Hexagonal close-packed circle centers (circle-to-circle distance = r)
    centers = [(0.0, 0.0)]
    r1 = [
        (r, 0), (r/2, r*sq3/2), (-r/2, r*sq3/2),
        (-r, 0), (-r/2, -r*sq3/2), (r/2, -r*sq3/2),
    ]
    centers += r1
    if rings >= 2:
        r2_outer = [
            (2*r, 0), (r, r*sq3), (-r, r*sq3),
            (-2*r, 0), (-r, -r*sq3), (r, -r*sq3),
        ]
        r2_inner = [
            (3*r/2, r*sq3/2), (0, r*sq3), (-3*r/2, r*sq3/2),
            (-3*r/2, -r*sq3/2), (0, -r*sq3), (3*r/2, -r*sq3/2),
        ]
        centers += r2_outer + r2_inner

    c.saveState()
    c.setFillAlpha(0)
    c.setStrokeAlpha(alpha)
    c.setStrokeColor(color)
    c.setLineWidth(0.45)
    for (ox, oy) in centers:
        c.circle(cx + ox, cy + oy, r, stroke=1, fill=0)
    # Outer bounding circle
    outer_r = (2 * r + r * 0.05) if rings >= 2 else r * 1.05
    c.setLineWidth(0.75)
    c.setStrokeAlpha(min(alpha * 1.6, 1.0))
    c.circle(cx, cy, outer_r, stroke=1, fill=0)
    c.restoreState()


# ── Gold horizontal rule with optional diamond ornament ────────────────────────

def gold_rule(c, y, diamond=True):
    x0, x1 = M, W - M
    c.saveState()
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.75)
    if diamond:
        mid = W / 2
        gap = 10
        c.line(x0, y, mid - gap, y)
        c.line(mid + gap, y, x1, y)
        c.setFillColor(GOLD)
        c.setFont("Sym", 10)
        c.drawCentredString(mid, y - 4.5, "◆")  # ◆
    else:
        c.line(x0, y, x1, y)
    c.restoreState()


def dark_rule(c, y):
    c.saveState()
    c.setStrokeColor(LGOLD)
    c.setLineWidth(0.6)
    c.line(M + 20, y, W - M - 20, y)
    c.restoreState()


# ── Write lines ────────────────────────────────────────────────────────────────

def write_line(c, x, y, width):
    c.saveState()
    c.setStrokeColor(LINEC)
    c.setStrokeAlpha(0.65)
    c.setLineWidth(0.65)
    c.line(x, y, x + width, y)
    c.restoreState()


def write_lines_block(c, x, y, width, n, spacing):
    """Draw n write lines; return y after last line."""
    for i in range(n):
        write_line(c, x, y - i * spacing, width)
    return y - n * spacing


# ── Energy bar (10 shade cells) ────────────────────────────────────────────────

def energy_bar(c, x, y):
    """Draw 10 cells starting at top-left (x, y). Cell height = 26. Returns bottom y."""
    cell_w = IW / 10
    cell_h = 26
    c.saveState()
    for i in range(10):
        cx = x + i * cell_w
        # Subtle fill so buyers see they're meant to shade
        c.setFillColor(BFILL)
        c.setStrokeAlpha(1.0)
        c.setFillAlpha(1.0)
        c.rect(cx, y - cell_h, cell_w, cell_h, stroke=0, fill=1)
        # Gold border
        c.setStrokeColor(BGOLD)
        c.setLineWidth(0.9)
        c.rect(cx, y - cell_h, cell_w, cell_h, stroke=1, fill=0)
        # Number label — dark ink, fully readable
        c.setFillColor(INK)
        c.setFont("Arsenal", 8)
        c.drawCentredString(cx + cell_w / 2, y - cell_h + 6, str(i + 1))
    c.restoreState()
    return y - cell_h


# ── 3/6/9 Badge circle ─────────────────────────────────────────────────────────

def badge(c, cx, cy, num, title, subtitle=None, dark=False):
    """Badge circle: gold border, number in dark/light ink, title to the right."""
    R = 22
    ink  = WTEXT if dark else INK
    gclr = LGOLD if dark else GOLD

    c.saveState()
    c.setStrokeColor(gclr)
    c.setLineWidth(1.5)
    c.setFillAlpha(0)
    c.circle(cx, cy, R, stroke=1, fill=0)
    c.setFillAlpha(1.0)
    # Number inside circle
    c.setFillColor(ink)
    c.setFont("Italiana", 20)
    c.drawCentredString(cx, cy - 7, str(num))
    # Title to the right
    c.setFont("Arsenal", 11)
    tx = cx + R + 10
    if subtitle:
        c.drawString(tx, cy + 5, title)
        c.setFont("CrimsonItal", 12)
        c.drawString(tx, cy - 10, subtitle)
    else:
        c.drawString(tx, cy - 4, title)
    c.restoreState()


# ── Footer ─────────────────────────────────────────────────────────────────────

def footer(c, pn, dark=False):
    ink  = WTEXT if dark else INK
    gclr = LGOLD if dark else GOLD

    c.saveState()
    c.setStrokeColor(gclr)
    c.setLineWidth(0.5)
    c.line(M, FY + 10, W - M, FY + 10)

    c.setFillColor(ink)
    c.setFont("Arsenal", 9)
    c.drawCentredString(W / 2, FY - 2, "ПОРТАЛ  ·  ЩОДЕННИК МАНІФЕСТАЦІЇ 369")

    c.setFont("Jura", 9)
    c.drawRightString(W - M, FY - 2, str(pn))
    c.restoreState()


# ── Bordered writing box ───────────────────────────────────────────────────────

def bordered_box(c, x, y_top, w, h, label=None, label_size=10, dark=False):
    """Draw a gold-bordered box. y_top is the top edge. Returns bottom y."""
    ink  = WTEXT if dark else INK
    gclr = LGOLD if dark else GOLD

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


# ── Wrapped text helper ────────────────────────────────────────────────────────

_SPECIAL_GLYPHS = set("◆✶○◔◐◓●◒◑◕◇★✦♦✳❋✧")

def _mixed_runs(text, base_font):
    runs = []; cur = ""; curf = None
    for ch in text:
        f = "Sym" if ch in _SPECIAL_GLYPHS else base_font
        if curf is not None and f != curf:
            runs.append((cur, curf)); cur = ""
        cur += ch; curf = f
    if cur:
        runs.append((cur, curf))
    return runs

def draw_mixed_left(c, x, y, text, base_font, size):
    for seg, f in _mixed_runs(text, base_font):
        c.setFont(f, size); c.drawString(x, y, seg)
        x += c.stringWidth(seg, f, size)

def draw_mixed_centred(c, cx, y, text, base_font, size):
    runs = _mixed_runs(text, base_font)
    total = sum(c.stringWidth(seg, f, size) for seg, f in runs)
    x = cx - total / 2
    for seg, f in runs:
        c.setFont(f, size); c.drawString(x, y, seg)
        x += c.stringWidth(seg, f, size)


def draw_bullet_wrapped(c, x, y, text, base_font, size, max_w,
                        line_h=18, bullet="◆", gap=15, color=INK):
    """Gold diamond bullet + hanging-indent wrapped text. Returns last baseline y."""
    c.setFillColor(GOLD)
    c.setFont("Sym", size - 3)
    c.drawString(x, y, bullet)
    c.setFillColor(color)
    tx = x + gap
    avail = max_w - gap
    words = text.split()
    cur = ""
    yy = y
    for w in words:
        trial = (cur + " " + w).strip()
        if c.stringWidth(trial, base_font, size) <= avail or not cur:
            cur = trial
        else:
            c.setFont(base_font, size); c.drawString(tx, yy, cur)
            yy -= line_h; cur = w
    if cur:
        c.setFont(base_font, size); c.drawString(tx, yy, cur)
    return yy


def draw_wrapped(c, text, x, y, max_w, font, size, color=INK, line_h=None):
    """Simple word-wrap draw. Returns y after last line."""
    if line_h is None:
        line_h = size * 1.4
    c.setFont(font, size)
    c.setFillColor(color)
    words = text.split()
    line  = ""
    for word in words:
        test = (line + " " + word).strip()
        if c.stringWidth(test, font, size) <= max_w:
            line = test
        else:
            if line:
                c.drawString(x, y, line)
                y -= line_h
            line = word
    if line:
        c.drawString(x, y, line)
        y -= line_h
    return y


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE BUILDERS
# ══════════════════════════════════════════════════════════════════════════════

# ── Page 1: Cover ──────────────────────────────────────────────────────────────

def build_cover(c):
    dark_bg(c)
    corner_marks(c, LGOLD)

    # Large Flower of Life centred slightly above middle
    fol_cy = H * 0.50
    flower_of_life(c, W / 2, fol_cy, 40, rings=2, color=LGOLD, alpha=0.55)

    # Outer decorative halos
    c.saveState()
    c.setStrokeColor(LGOLD)
    c.setStrokeAlpha(0.18)
    c.setFillAlpha(0)
    c.setLineWidth(0.5)
    for r in (130, 148, 166):
        c.circle(W / 2, fol_cy, r, stroke=1, fill=0)
    c.restoreState()

    # Top thin rule
    c.saveState()
    c.setStrokeColor(LGOLD)
    c.setLineWidth(0.7)
    c.line(M + 20, H - M - 12, W - M - 20, H - M - 12)
    c.restoreState()

    # "СВЯЩЕННА ПРАКТИКА" supertitle
    y = H - M - 34
    c.setFillColor(LGOLD)
    c.setFont("Arsenal", 10)
    c.drawCentredString(W / 2, y, "∙ ∙ ∙   С В Я Щ Е Н Н А   П Р А К Т И К А   ∙ ∙ ∙")

    # Main title
    y -= 86
    c.setFillColor(WTEXT)
    c.setFont("Italiana", 72)
    c.drawCentredString(W / 2, y, "ПОРТАЛ")

    # Gold diamond separator
    y -= 28
    c.setFillColor(LGOLD)
    c.setFont("Italiana", 14)
    draw_mixed_centred(c, W / 2, y, "◆  3 · 6 · 9  ◆", "Italiana", 14)

    # Subtitle
    y -= 30
    c.setFillColor(WTEXT)
    c.setFont("Italiana", 22)
    c.drawCentredString(W / 2, y, "Щоденник маніфестації")

    # Tagline — positioned below the Flower of Life
    y = fol_cy - 120
    c.setFillColor(WTEXT)
    c.setFont("CrimsonItal", 15)
    c.drawCentredString(W / 2, y, "Впиши свою реальність у життя.")
    y -= 26
    c.setFillColor(LGOLD)
    c.setFont("Arsenal", 9)
    c.drawCentredString(W / 2, y,
        "28 ДНІВ  ·  РАНОК  ·  ОПІВДНІ  ·  ВЕЧІР  ·  СУГОЛОССЯ")

    # Bottom rule + brand
    c.saveState()
    c.setStrokeColor(LGOLD)
    c.setLineWidth(0.7)
    c.line(M + 20, M + 44, W - M - 20, M + 44)
    c.restoreState()
    c.setFillColor(LGOLD)
    c.setFont("Arsenal", 9)
    c.drawCentredString(W / 2, M + 28, "С Е Р І Я   « П О Р Т А Л »")


# ── Page 2: Title / Dedication ─────────────────────────────────────────────────

def build_title_page(c, pn):
    cream_bg(c)
    corner_marks(c)
    flower_of_life(c, W / 2, H / 2, 26, rings=2, color=GOLD, alpha=0.10)

    y = H - M
    gold_rule(c, y - 12, diamond=False)
    y -= 48

    c.setFillColor(INK)
    c.setFont("Arsenal", 11)
    c.drawCentredString(W / 2, y, "ЦЕЙ ЩОДЕННИК НАЛЕЖИТЬ")
    y -= 28
    write_line(c, M + 60, y + 6, IW - 120)
    y -= 44

    c.setFont("Arsenal", 11)
    c.drawCentredString(W / 2, y, "ДАТА АКТИВАЦІЇ ПОРТАЛУ")
    y -= 28
    write_line(c, M + 80, y + 6, IW - 160)
    y -= 52

    gold_rule(c, y, diamond=True)
    y -= 52

    c.setFont("Italiana", 32)
    c.drawCentredString(W / 2, y, "Мій намір у порталі")
    y -= 50

    c.setFont("CrimsonItal", 13)
    c.drawCentredString(W / 2, y, "Найважливіше бажання, яке я закликаю у своє життя:")
    y -= 48

    for _ in range(5):
        write_line(c, M, y, IW)
        y -= 36

    y -= 24
    gold_rule(c, y, diamond=True)
    y -= 46

    c.setFont("Arsenal", 11)
    c.drawCentredString(W / 2, y, "Я ГІДНА  ·  Я ГОТОВА  ·  Я ВІДКРИТА")

    footer(c, pn)


# ── Page 3: License & Terms of Use ────────────────────────────────────────────

def build_license_page(c, pn):
    cream_bg(c)
    corner_marks(c)

    y = H - M - 22
    c.setFillColor(GOLD)
    c.setFont("Arsenal", 10)
    draw_mixed_centred(c, W / 2, y, "✶   Л І Ц Е Н З І Я   Т А   У М О В И   ✶", "Arsenal", 10)
    y -= 38

    c.setFillColor(INK)
    c.setFont("Italiana", 28)
    c.drawCentredString(W / 2, y, "Умови використання")
    y -= 18
    gold_rule(c, y, diamond=True)
    y -= 36

    terms = [
        ("ЛИШЕ ДЛЯ ОСОБИСТОГО ВИКОРИСТАННЯ",
         "Цей щоденник призначений лише для вашого особистого користування. Одна ліцензія на одного покупця. "
         "Ви можете друкувати цей файл для власної практики ведення щоденника скільки завгодно разів."),
        ("БЕЗ ПОШИРЕННЯ",
         "Забороняється ділитися, надсилати, завантажувати, перепродавати чи поширювати цей файл у будь-якій "
         "формі — цифровій чи друкованій — іншим особам або на будь-яких платформах."),
        ("БЕЗ КОМЕРЦІЙНОГО ВИКОРИСТАННЯ",
         "Забороняється використовувати цей щоденник або його вміст для створення товарів на продаж, "
         "наборів, курсів, коучингових програм чи будь-якої комерційної мети."),
        ("БЕЗ ЗМІН",
         "Забороняється змінювати, редагувати, ребрендувати чи видавати цю роботу за власну. "
         "Увесь текст, дизайн, верстка та вміст залишаються інтелектуальною власністю GlowHausDigital."),
        ("ДРУК",
         "Ви можете друкувати цей файл удома або в місцевій друкарні для власного "
         "особистого користування. Комерційний друк і перепродаж друкованих копій заборонені."),
    ]

    for heading, body in terms:
        c.setFillColor(GOLD)
        c.setFont("Arsenal", 10)
        c.drawString(M, y, heading)
        y -= 18
        draw_wrapped(c, body, M + 4, y, IW - 8, "CrimsonPro", 12, color=INK, line_h=18)
        lines_needed = len(body) // 62 + 1
        y -= lines_needed * 18 + 14

    y -= 8
    gold_rule(c, y, diamond=False)
    y -= 28

    c.setFillColor(INK)
    c.setFont("CrimsonItal", 12)
    c.drawCentredString(W / 2, y, "© 2026 GlowHausDigital  ·  Усі права захищено")
    y -= 20
    c.drawCentredString(W / 2, y, "Запитання? teamglowhaus@gmail.com")

    footer(c, pn)


# ── Page 4: Welcome (dark) ─────────────────────────────────────────────────────

def build_welcome(c, pn):
    dark_bg(c)
    corner_marks(c, LGOLD)
    flower_of_life(c, W / 2, H - M - 56, 20, rings=1, color=LGOLD, alpha=0.45)

    y = H - M - 130
    c.setFillColor(LGOLD)
    c.setFont("Arsenal", 10)
    draw_mixed_centred(c, W / 2, y, "✶   В І Т А Ю   ✶", "Arsenal", 10)
    y -= 42

    c.setFillColor(WTEXT)
    c.setFont("Italiana", 36)
    c.drawCentredString(W / 2, y, "Ви прибули.")
    y -= 14

    dark_rule(c, y)
    y -= 36

    paras = [
        "Портал 369 — це більше, ніж щоденник. Це щоденна священна практика,",
        "жива розмова між вами та безмежним полем усіх можливостей.",
        "",
        "Нікола Тесла вірив, що 3, 6 і 9 — це ключ до Всесвіту.",
        "Цей щоденник побудований на цьому священному коді:",
        "",
        "Пиши своє бажання 3 рази вранці, щоб закласти намір.",
        "Пиши його 6 разів опівдні, щоб закріпити його у своєму енергетичному полі.",
        "Пиши його 9 разів увечері, щоб надіслати його Всесвіту.",
        "",
        "Кожне повторення — це сигнал. Кожна сторінка — це акт віри.",
        "Кожен завершений день — це доказ, що ти прийшла заради своєї мрії.",
        "",
        "Це не список бажань. Це портал.",
        "Пройди крізь нього — щодня, віддано, впевнено.",
    ]

    c.setFont("CrimsonPro", 14)
    for line in paras:
        c.setFillColor(WTEXT)
        if line == "":
            y -= 10
        else:
            c.drawCentredString(W / 2, y, line)
            y -= 22

    y -= 24
    dark_rule(c, y)
    y -= 28

    c.setFillColor(LGOLD)
    c.setFont("Arsenal", 10)
    c.drawCentredString(W / 2, y, "3 · 6 · 9  ·  ПИШИ  ·  ВІР  ·  ОТРИМУЙ")

    footer(c, pn, dark=True)


# ── Page 4: The 369 Method ─────────────────────────────────────────────────────

def build_method(c, pn):
    cream_bg(c)
    corner_marks(c)

    y = H - M - 36
    c.setFillColor(INK)
    c.setFont("Italiana", 30)
    c.drawCentredString(W / 2, y, "Метод 369")
    y -= 22
    gold_rule(c, y, diamond=True)
    y -= 32

    sections = [
        ("3", "РАНКОВІ ТРАНСМІСІЇ",
         "Пиши своє бажання 3 рази одразу після пробудження. Вранці підсвідомість "
         "найбільш сприйнятлива, а завіса між світами найтонша. Ці "
         "три повторення садять зерно у родючий ґрунт нового дня."),
        ("6", "ОПІВДЕННА АКТИВАЦІЯ",
         "Пиши своє бажання 6 разів опівдні. Ця практика посеред дня підтримує твій "
         "намір живим попри денну метушню. Шість — це число "
         "гармонії: ти гармонізуєш свою вібрацію зі своїм бажанням."),
        ("9", "ВЕЧІРНЯ ІНТЕГРАЦІЯ",
         "Пиши своє бажання 9 разів перед сном. Дев'ять — це число завершення. "
         "Вечірній запис надсилає чіткий сигнал, коли свідомість поринає "
         "у квантове поле снів і глибокого творення."),
    ]

    for num, title, desc in sections:
        badge(c, M + 26, y - 20, num, title)
        y -= 50
        y = draw_wrapped(c, desc, M + 10, y, IW - 20, "CrimsonPro", 13,
                         color=INK, line_h=20)
        y -= 18
        gold_rule(c, y, diamond=False)
        y -= 28

    c.setFillColor(INK)
    c.setFont("Arsenal", 12)
    c.drawString(M, y, "ПОРАДИ ДЛЯ МАКСИМАЛЬНОЇ АКТИВАЦІЇ")
    y -= 22

    tips = [
        "Пиши від руки — фізична дія закодовує намір у твоєму тілі.",
        "Вживай теперішній час: «я є», «я маю», «я відчуваю».",
        "Відчувай емоцію володіння цим уже зараз із кожним повторенням.",
        "Будь послідовною — 28 днів практики змінюють твої переконання та щоденні звички.",
        "Довіряй процесу, навіть коли ще не бачиш, яким чином це станеться.",
    ]
    for tip in tips:
        y = draw_bullet_wrapped(c, M + 10, y, tip, "CrimsonPro", 13, IW - 20,
                                line_h=18)
        y -= 22

    footer(c, pn)


# ── Page 5: How to Use ─────────────────────────────────────────────────────────

def build_how_to_use(c, pn):
    cream_bg(c)
    corner_marks(c)

    y = H - M - 36
    c.setFillColor(INK)
    c.setFont("Italiana", 30)
    c.drawCentredString(W / 2, y, "Як користуватися цим щоденником")
    y -= 22
    gold_rule(c, y, diamond=True)
    y -= 32

    steps = [
        ("01", "ОБЕРИ СВОЄ БАЖАННЯ",
         "Обери одне конкретне, емоційно наповнене бажання, на якому зосередишся 28 днів. "
         "Запиши точне формулювання свого бажання на наступній сторінці перед початком."),
        ("02", "ПИШИ ЩОДНЯ — ВРАНЦІ, ОПІВДНІ ТА ВВЕЧЕРІ",
         "Кожен день має дві сторінки: ранок/опівдні та вечір. Заповнюй обидві "
         "щодня. Послідовність — це ключ, що відчиняє портал."),
        ("03", "ПЕРЕВІРКА ЕНЕРГІЇ",
         "Заштриховуй шкалу енергії щоранку та щовечора (1 — низька, 10 — висока). Відстеження "
         "твого вібраційного стану виявляє закономірності, що передвіщають прориви."),
        ("04", "ВДЯЧНІСТЬ І СИНХРОНІЧНОСТІ",
         "Занотовуй миті суголосся, несподівані знаки та все, за що ти "
         "вдячна. Що більше ти помічаєш — то більше Всесвіт посилає."),
        ("05", "ТИЖНЕВІ ТА МІСЯЧНІ ПІДСУМКИ",
         "Користуйся сторінками підсумків кожні 7 днів, щоб відстежувати докази своєї маніфестації, "
         "зміни в переконаннях і те, що варто підсилити в наступному циклі."),
        ("06", "РОБОТА З ТІННЮ ТА ЖУРНАЛ ЗНАКІВ",
         "Розділ роботи з тінню та журнал синхронічностей наприкінці підтримують глибшу "
         "трансформацію та збір доказів упродовж усієї твоєї практики."),
    ]

    for num, title, desc in steps:
        c.setFillColor(GOLD)
        c.setFont("Italiana", 20)
        c.drawString(M, y, num)
        c.setFillColor(INK)
        c.setFont("Arsenal", 12)
        c.drawString(M + 30, y + 2, title)
        y -= 20
        y = draw_wrapped(c, desc, M + 10, y, IW - 20, "CrimsonPro", 13,
                         color=INK, line_h=19)
        y -= 16

    footer(c, pn)


# ── Page 6: Portal Intention ───────────────────────────────────────────────────

def build_portal_intention(c, pn):
    cream_bg(c)
    corner_marks(c)
    flower_of_life(c, W / 2, H * 0.44, 28, rings=2, color=GOLD, alpha=0.12)

    y = H - M - 36
    c.setFillColor(INK)
    c.setFont("Italiana", 30)
    c.drawCentredString(W / 2, y, "Формулювання мого бажання")
    y -= 22
    gold_rule(c, y, diamond=True)
    y -= 24

    c.setFillColor(INK)
    c.setFont("CrimsonItal", 13)
    c.drawCentredString(W / 2, y, "Запиши точні слова, які використовуватимеш у щоденній практиці.")
    y -= 20
    c.drawCentredString(W / 2, y, "Теперішній час, особисто, стверджувально та емоційно живо.")
    y -= 38

    for _ in range(6):
        write_line(c, M, y, IW)
        y -= 36
    y -= 16

    gold_rule(c, y, diamond=False)
    y -= 28

    c.setFillColor(INK)
    c.setFont("Arsenal", 12)
    c.drawString(M, y, "ЯК ВІДЧУВАТИМЕТЬСЯ ЦЕ БАЖАННЯ, КОЛИ ЗДІЙСНИТЬСЯ")
    y -= 24
    for _ in range(3):
        write_line(c, M, y, IW)
        y -= 32
    y -= 14

    gold_rule(c, y, diamond=False)
    y -= 28

    c.setFillColor(INK)
    c.setFont("Arsenal", 12)
    c.drawString(M, y, "ЧОМУ Я ЗНАЮ, ЩО ГІДНА ЦЬОГО")
    y -= 24
    for _ in range(3):
        write_line(c, M, y, IW)
        y -= 32

    footer(c, pn)


# ── Page 7: My Commitments ─────────────────────────────────────────────────────

def build_commitments(c, pn):
    cream_bg(c)
    corner_marks(c)

    y = H - M - 36
    c.setFillColor(INK)
    c.setFont("Italiana", 30)
    c.drawCentredString(W / 2, y, "Мої обіцянки в порталі")
    y -= 22
    gold_rule(c, y, diamond=True)
    y -= 30

    c.setFillColor(INK)
    c.setFont("CrimsonItal", 13)
    c.drawCentredString(W / 2, y, "Я входжу в цей портал із повною відданістю своїй мрії.")
    y -= 20
    c.drawCentredString(W / 2, y, "Я підписуюся нижче як священна угода із самою собою.")
    y -= 38

    commits = [
        "Я зобов'язуюся писати своє бажання 3–6–9 разів щодня протягом 28 днів.",
        "Я зобов'язуюся приходити навіть у дні, коли не вірю, що це працює.",
        "Я зобов'язуюся помічати й записувати кожен знак суголосся, хай який маленький.",
        "Я зобов'язуюся ставитися до цього щоденника як до священного ритуалу, а не обов'язку.",
        "Я зобов'язуюся довіряти часу Всесвіту й відпускати результати.",
        "Я зобов'язуюся стати тією версією себе, яка вже має це бажання.",
        "Я зобов'язуюся пройти всі 28 днів, не пропускаючи й не здаючись.",
    ]

    c.setFillColor(INK)
    for line in commits:
        y = draw_bullet_wrapped(c, M + 5, y, line, "CrimsonPro", 13, IW - 5,
                                line_h=18)
        y -= 20
    y -= 16

    gold_rule(c, y, diamond=False)
    y -= 38

    c.setFillColor(INK)
    c.setFont("Arsenal", 11)
    c.drawString(M, y, "ПІДПИС")
    write_line(c, M + 60, y + 5, 200)
    c.drawString(M + 300, y, "ДАТА")
    write_line(c, M + 342, y + 5, 114)
    y -= 46

    c.setFillColor(INK)
    c.setFont("CrimsonItal", 14)
    c.drawCentredString(W / 2, y,
        "«Щойно ти наважуєшся — Всесвіт починає діяти на твою користь.»")
    y -= 22
    c.setFillColor(GOLD)
    c.setFont("Arsenal", 10)
    c.drawCentredString(W / 2, y, "— ЙОГАНН ГЕТЕ (АДАПТОВАНО)")
    y -= 44

    gold_rule(c, y, diamond=True)
    y -= 28

    c.setFillColor(INK)
    c.setFont("Arsenal", 12)
    c.drawString(M, y, "МОЯ АФІРМАЦІЯ ПОРТАЛУ")
    y -= 18
    c.setFont("CrimsonItal", 12)
    c.drawString(M + 8, y,
        "Запиши одну афірмацію, що закріплюватиме твою віру впродовж усього порталу:")
    y -= 26

    for _ in range(4):
        write_line(c, M, y, IW)
        y -= 28
    y -= 16

    c.setFillColor(INK)
    c.setFont("CrimsonItal", 13)
    c.drawCentredString(W / 2, y,
        "Я несу цю відданість на кожну сторінку цього порталу.")

    footer(c, pn)


# ── Page 8: Moon Phase Overview (dark) ─────────────────────────────────────────

def build_moon_overview(c, pn):
    # Print-safe: swap to cream so handwritten notes show on paper
    if PRINT_SAFE:
        cream_bg(c)
        corner_marks(c)
        hdr_color  = GOLD
        title_color = INK
        text_color  = INK
        rule_fn    = gold_rule
    else:
        dark_bg(c)
        corner_marks(c, LGOLD)
        hdr_color  = LGOLD
        title_color = WTEXT
        text_color  = WTEXT
        rule_fn    = dark_rule

    y = H - M - 22
    c.setFillColor(hdr_color)
    c.setFont("Arsenal", 10)
    draw_mixed_centred(c, W / 2, y, "✶   МІСЯЦЬ  ·  ТВІЙ КОСМІЧНИЙ ПАРТНЕР   ✶", "Arsenal", 10)
    y -= 42

    c.setFillColor(title_color)
    c.setFont("Italiana", 34)
    c.drawCentredString(W / 2, y, "Путівник фазами Місяця")
    y -= 18
    rule_fn(c, y)
    y -= 36

    phases = [
        ("○○", "МОЛОДИК",
         "Закладай наміри. Сій зерна. Ідеальний час, щоб відкрити свій портал."),
        ("◔", "МОЛОДИЙ СЕРП",
         "Дій натхненно. Набирай обертів. Покажи Всесвіту, що налаштована серйозно."),
        ("◐", "ПЕРША ЧВЕРТЬ",
         "Долай перешкоди. Подвоюй відданість. Продовжуй писати."),
        ("◓", "ПРИБУВАЮЧИЙ МІСЯЦЬ",
         "Уточнюй і вирівнюй. Твоя маніфестація формується в незримому."),
        ("●", "ПОВНЯ",
         "Святкуй докази. Відпускай блоки. Відчувай глибоку вдячність за те, що йде."),
        ("◒", "СПАДАЮЧИЙ МІСЯЦЬ",
         "Ділися своєю енергією та дарами. Дякуй полю всього творіння."),
        ("◑", "ОСТАННЯ ЧВЕРТЬ",
         "Відпусти те, що більше не служить. Звільни місце, щоб бажання втілилось."),
        ("◕", "СТАРИЙ СЕРП",
         "Відпочивай і приймай. Довіряй тиші. Готуйся до нового циклу."),
    ]

    col_w = IW / 2 - 10
    ROW_H = 82  # increased row height for better spacing
    for i, (sym, phase, desc) in enumerate(phases):
        col = i % 2
        row = i // 2
        x = M + col * (col_w + 20)
        row_y = y - row * ROW_H

        c.setFillColor(hdr_color)
        c.setFont("Arsenal", 11)
        c.drawString(x, row_y, phase)
        c.setFillColor(text_color)
        c.setFont("CrimsonPro", 12)
        draw_wrapped(c, desc, x + 5, row_y - 18, col_w - 10,
                     "CrimsonPro", 12, color=text_color, line_h=17)

    y -= (4 * ROW_H) + 16
    rule_fn(c, y)
    y -= 28

    c.setFillColor(text_color)
    c.setFont("CrimsonItal", 13)
    c.drawCentredString(W / 2, y, "Працюй з енергією Місяця, щоб підсилити свою практику 369.")
    y -= 22
    c.drawCentredString(W / 2, y, "Молодик — найпотужніший час, щоб відкрити новий портал.")
    y -= 36

    rule_fn(c, y)
    y -= 28

    c.setFillColor(hdr_color)
    c.setFont("Arsenal", 10)
    c.drawString(M, y, "МОЇ МІСЯЧНІ НОТАТКИ НА ЦЕЙ ЦИКЛ ПОРТАЛУ")
    y -= 22
    line_color = GOLD if PRINT_SAFE else LGOLD
    c.saveState()
    c.setStrokeColor(line_color)
    c.setStrokeAlpha(0.65 if PRINT_SAFE else 1.0)
    c.setLineWidth(0.65)
    for _ in range(4):
        c.line(M, y, W - M, y)
        y -= 28
    c.restoreState()

    footer(c, pn, dark=not PRINT_SAFE)


# ── Daily Pages ────────────────────────────────────────────────────────────────

EVENING_PROMPTS = [
    "Які докази моєї маніфестації я помітила сьогодні, хай які дрібні?",
    "Як я сьогодні втілювала відчуття, що вже маю своє бажання?",
    "Яке переконання про себе змінилося чи пом'якшилося сьогодні?",
    "Що я обираю відпустити перед сном сьогодні?",
    "Як Всесвіт підтримав мене сьогодні так, що я могла й не помітити?",
    "Що сказала б найвища версія мене про сьогоднішню практику?",
    "Що я хочу вимріяти в реальність, поки спатиму цієї ночі?",
]


def build_morning_page(c, day, pn):
    """Morning (3×) + Midday (6×) page."""
    cream_bg(c)
    corner_marks(c)
    flower_of_life(c, W - M - 36, H - M - 36, 18, rings=1, color=GOLD, alpha=0.10)

    week = (day - 1) // 7 + 1
    y = H - M - 14

    # Week label
    c.setFillColor(GOLD)
    c.setFont("Arsenal", 10)
    c.drawString(M, y, f"ТИЖДЕНЬ {week}")
    c.drawRightString(W - M, y, "РАНОК  ·  ОПІВДНІ")
    y -= 34

    # Day number
    c.setFillColor(INK)
    c.setFont("Italiana", 38)
    c.drawCentredString(W / 2, y, f"ДЕНЬ {day}")
    y -= 24

    # Date
    c.setFont("Arsenal", 11)
    c.drawCentredString(W / 2, y, "ДАТА  ______ / ______ / ______")
    y -= 22

    gold_rule(c, y, diamond=True)
    y -= 24

    # ── MORNING TRANSMISSIONS (3×) ─────────────────────────────────────────
    badge(c, M + 26, y - 20, "3", "РАНКОВІ ТРАНСМІСІЇ",
          subtitle="НАПИШИ СВОЄ БАЖАННЯ 3 РАЗИ")
    y -= 50

    for _ in range(3):
        write_line(c, M, y, IW)
        y -= 32
    y -= 8

    # Morning energy
    c.setFillColor(INK)
    c.setFont("Arsenal", 10)
    c.drawString(M, y, "РАНКОВА ЕНЕРГІЯ — ЗАШТРИХУЙ СВІЙ РІВЕНЬ  1 → 10")
    y -= 18
    energy_bar(c, M, y)
    y -= 38

    gold_rule(c, y, diamond=True)
    y -= 24

    # ── MIDDAY ACTIVATION (6×) ───────────────────────────────────────────────
    badge(c, M + 26, y - 20, "6", "ОПІВДЕННА АКТИВАЦІЯ",
          subtitle="НАПИШИ СВОЄ БАЖАННЯ 6 РАЗІВ")
    y -= 50

    for _ in range(6):
        write_line(c, M, y, IW)
        y -= 28
    y -= 8

    gold_rule(c, y, diamond=True)
    y -= 22

    # ── INTENTION ALIGNMENT ─────────────────────────────────────────────────────
    c.setFillColor(INK)
    c.setFont("Arsenal", 11)
    c.drawString(M, y, "СУГОЛОССЯ З НАМІРОМ")
    y -= 18
    c.setFont("CrimsonItal", 12)
    c.drawString(M + 8, y, "Яку суголосну дію я можу зробити сьогодні, щоб наблизитися до бажання?")
    y -= 24

    for _ in range(3):
        write_line(c, M, y, IW)
        y -= 26

    footer(c, pn)


def build_evening_page(c, day, pn):
    """Evening (9×) + Reflection page."""
    cream_bg(c)
    corner_marks(c)
    # Watermark in the blank space between write-lines section and energy bar
    flower_of_life(c, W / 2, H * 0.52, 18, rings=1, color=GOLD, alpha=0.04)

    week = (day - 1) // 7 + 1
    y = H - M - 14

    c.setFillColor(GOLD)
    c.setFont("Arsenal", 10)
    c.drawString(M, y, f"ТИЖДЕНЬ {week}")
    c.drawRightString(W - M, y, "ВЕЧІР  ·  ІНТЕГРАЦІЯ")
    y -= 30

    c.setFillColor(INK)
    c.setFont("Italiana", 28)
    c.drawCentredString(W / 2, y, f"День {day}  ·  Вечір")
    y -= 20

    gold_rule(c, y, diamond=True)
    y -= 24

    # ── EVENING INTEGRATION (9×) ───────────────────────────────────────────
    badge(c, M + 26, y - 20, "9", "ВЕЧІРНЯ ІНТЕГРАЦІЯ",
          subtitle="НАПИШИ СВОЄ БАЖАННЯ 9 РАЗІВ")
    y -= 50

    for _ in range(9):
        write_line(c, M, y, IW)
        y -= 22
    y -= 8

    gold_rule(c, y, diamond=True)
    y -= 16

    # Evening energy
    c.setFillColor(INK)
    c.setFont("Arsenal", 10)
    c.drawString(M, y, "ВЕЧІРНЯ ЕНЕРГІЯ — ЗАШТРИХУЙ СВІЙ РІВЕНЬ  1 → 10")
    y -= 18
    energy_bar(c, M, y)
    y -= 38

    # ── GRATITUDE SEED ──────────────────────────────────────────────────────────
    c.setFillColor(INK)
    c.setFont("Arsenal", 11)
    c.drawString(M, y, "ЗЕРНО ВДЯЧНОСТІ")
    y -= 16
    c.setFont("CrimsonItal", 12)
    c.drawString(M + 8, y, "Одне, за що я вдячна й що помітила сьогодні:")
    y -= 22
    write_line(c, M, y, IW)
    y -= 28
    write_line(c, M, y, IW)
    y -= 30

    # ── SYNCHRONICITIES & SIGNS ─────────────────────────────────────────────────
    c.setFillColor(INK)
    c.setFont("Arsenal", 11)
    c.drawString(M, y, "СИНХРОНІЧНОСТІ ТА ЗНАКИ")
    y -= 14
    c.setFont("CrimsonItal", 12)
    c.drawString(M + 8, y, "Які суголосні чи несподівані миті я помітила сьогодні?")
    y -= 6
    bordered_box(c, M, y, IW, 54)
    y -= 62

    # ── EVENING REFLECTION ──────────────────────────────────────────────────────
    c.setFillColor(INK)
    c.setFont("Arsenal", 11)
    c.drawString(M, y, "ВЕЧІРНЯ РЕФЛЕКСІЯ")
    y -= 16
    prompt = EVENING_PROMPTS[(day - 1) % 7]
    c.setFont("CrimsonItal", 12)
    c.drawString(M + 8, y, prompt)
    y -= 24
    write_line(c, M, y, IW)
    y -= 28
    write_line(c, M, y, IW)
    y -= 32

    # ── RELEASE STATEMENT (fixed above footer — never overlaps) ─────────────────
    release_y = FY + 30           # text baseline 30pt above footer centre
    gold_rule(c, release_y + 22, diamond=False)
    c.setFillColor(INK)
    c.setFont("CrimsonItal", 13)
    c.drawCentredString(
        W / 2, release_y,
        "Я віддаю це бажання Всесвіту з повною довірою та вдячністю."
    )

    footer(c, pn)


# ── Weekly Review ──────────────────────────────────────────────────────────────

WEEKLY_SECTIONS = [
    ("ДОКАЗИ МАНІФЕСТАЦІЇ",
     "Які знаки, синхронічності чи відчутні зміни я помітила цього тижня?", 4),
    ("ЗМІНИ В ПЕРЕКОНАННЯХ",
     "Як зміцніла чи прояснилася моя віра в це бажання?", 3),
    ("ЕНЕРГЕТИЧНІ ЗАКОНОМІРНОСТІ",
     "Які дні відчувалися найсуголоснішими? Що живило, а що виснажувало мене?", 3),
    ("УРОЖАЙ ВДЯЧНОСТІ",
     "За що я найбільше вдячна з практики цього тижня?", 3),
    ("ПІДСИЛИТИ НАСТУПНОГО ТИЖНЯ",
     "Чого я робитиму більше наступного тижня, щоб поглибити маніфестацію?", 3),
]


def build_weekly_review(c, week, pn):
    cream_bg(c)
    corner_marks(c)
    flower_of_life(c, W / 2, H * 0.50, 18, rings=1, color=GOLD, alpha=0.04)

    y = H - M - 22
    c.setFillColor(GOLD)
    c.setFont("Arsenal", 10)
    c.drawCentredString(W / 2, y, "ТИЖНЕВИЙ ПІДСУМОК")
    y -= 36

    c.setFillColor(INK)
    c.setFont("Italiana", 32)
    c.drawCentredString(W / 2, y, f"Тиждень {week}  ·  Підсумок")
    y -= 22

    gold_rule(c, y, diamond=True)
    y -= 26

    for label, prompt, n_lines in WEEKLY_SECTIONS:
        c.setFillColor(INK)
        c.setFont("Arsenal", 11)
        c.drawString(M, y, label)
        y -= 18
        c.setFont("CrimsonItal", 12)
        c.drawString(M + 8, y, prompt)
        y -= 22
        for _ in range(n_lines):
            write_line(c, M, y, IW)
            y -= 26
        y -= 10

    footer(c, pn)


# ── Monthly Review (4 pages) ───────────────────────────────────────────────────

def build_monthly_review(c, page_idx, pn):
    """page_idx 0–3 = four review pages."""
    cream_bg(c)
    corner_marks(c)

    titles    = [
        "Місячний огляд",
        "Докази та суголосся",
        "Інтеграція тіні",
        "Портал уперед",
    ]
    subtitles = [
        "Роздуми про 28 днів священної практики",
        "Що подарував Всесвіт",
        "Що я відпустила й трансформувала",
        "Наміри на наступний цикл",
    ]

    y = H - M - 22
    c.setFillColor(GOLD)
    c.setFont("Arsenal", 10)
    c.drawCentredString(W / 2, y, "МІСЯЧНИЙ ПІДСУМОК")
    y -= 36

    c.setFillColor(INK)
    c.setFont("Italiana", 30)
    c.drawCentredString(W / 2, y, titles[page_idx])
    y -= 20

    c.setFont("CrimsonItal", 13)
    c.drawCentredString(W / 2, y, subtitles[page_idx])
    y -= 18

    gold_rule(c, y, diamond=True)
    y -= 28

    prompts_by_page = [
        # Page 0
        [
            ("ЗАВЕРШЕНО ДНІВ (із 28)", 1),
            ("НАЙПОТУЖНІША СИНХРОНІЧНІСТЬ", 3),
            ("НАЙБІЛЬША ЗМІНА В ПЕРЕКОНАННЯХ", 3),
            ("ЩО НАЙБІЛЬШЕ МЕНЕ ЗДИВУВАЛО", 3),
            ("ЗАГАЛЬНА ТЕНДЕНЦІЯ ЕНЕРГІЇ", 2),
        ],
        # Page 1
        [
            ("ДОКАЗИ МАНІФЕСТАЦІЇ — ПЕРЕЛІЧИ КОЖЕН ЗНАК", 5),
            ("НЕСПОДІВАНІ ДАРИ, ЩО З'ЯВИЛИСЯ", 4),
            ("ЯК ЗМІНИЛОСЯ МОЄ ЖИТТЯ ЗА 28 ДНІВ", 4),
        ],
        # Page 2
        [
            ("ЩО Я ВІДПУСТИЛА ЦЬОГО МІСЯЦЯ", 4),
            ("СКАРБИ ТІНІ, ЯКІ Я ВІДКРИЛА", 4),
            ("ЯК Я ПЕРЕТВОРИЛА ОПІР НА ЗРОСТАННЯ", 4),
        ],
        # Page 3
        [
            ("ФОРМУЛЮВАННЯ МОГО НАСТУПНОГО БАЖАННЯ", 3),
            ("ЯК МОЯ ВІБРАЦІЯ ЗМІНИЛАСЯ НАЗАВЖДИ", 4),
            ("МОЄ ПОСЛАННЯ ВДЯЧНОСТІ ВСЕСВІТУ", 4),
        ],
    ]

    for label, n_lines in prompts_by_page[page_idx]:
        c.setFillColor(INK)
        c.setFont("Arsenal", 11)
        c.drawString(M, y, label)
        y -= 22
        for _ in range(n_lines):
            write_line(c, M, y, IW)
            y -= 28
        y -= 10

    footer(c, pn)


# ── Shadow Work ────────────────────────────────────────────────────────────────

SHADOW_WORK = [
    (
        "Відпускаю страх бути поміченою",
        "Що станеться, якщо світ побачить тебе справжньою — повністю, потужно, автентично?",
        [
            "Чого я боюся, що подумають люди, якщо я справді здійсню це бажання?",
            "Де я вперше засвоїла, що бути помітною й сильною — небезпечно?",
            "Що б зробила інакше сьогодні найпомітніша, найвиразніша версія мене?",
        ],
    ),
    (
        "Що я готова відпустити",
        "Завершення — частина творення. Що має скінчитися, щоб бажання почалося?",
        [
            "Яка стара історія про мене займає місце, потрібне моєму бажанню?",
            "Яка звичка, стосунки чи переконання тихо блокують мій портал?",
            "Якби я знала, що відпустити це цілком безпечно, що б я відпустила просто зараз?",
        ],
    ),
    (
        "Історія, яку я розповідаю про себе",
        "Твоя підсвідомість виконує засвоєні програми. Які з них варто оновити?",
        [
            "Яке головне обмежувальне переконання я маю про те, чи заслуговую цього бажання?",
            "Коли я вперше вирішила, що недостатньо гідна чогось такого?",
            "Яке оновлене переконання я обираю встановити натомість?",
        ],
    ),
    (
        "Мої стосунки з отриманням",
        "Маніфестація потребує відкритості до отримання. Чи справді ти відкрита?",
        [
            "Коли трапляється хороше, чи я відхиляю, знецінюю чи сумніваюся? Чому?",
            "У що мені потрібно повірити про себе, щоб прийняти це бажання з легкістю?",
            "Як я можу практикувати повніше отримання цього тижня?",
        ],
    ),
    (
        "Родові патерни, які я розриваю",
        "Ти пишеш нову історію не лише для себе, а для всього свого роду.",
        [
            "Які патерни нестачі, боротьби чи негідності я успадкувала?",
            "Чиї голоси предків я чую, коли сумніваюся, що бажання можливе?",
            "Який новий патерн я свідомо обираю створити для тих, хто прийде після мене?",
        ],
    ),
    (
        "Мої тіньові бажання",
        "Іноді те, чого ми боїмося хотіти, — саме те, що нам найбільше треба прийняти.",
        [
            "Чого я потайки хочу, але боялася визнати навіть перед собою?",
            "Яке бажання я засуджую в інших, а насправді прагну його сама?",
            "Що б я проявила, якби була цілком вільна від сорому й осуду?",
        ],
    ),
    (
        "Прощення як портал",
        "Непрощення — це блок у твоєму енергетичному полі. Кого тобі треба відпустити?",
        [
            "На кого в житті я тримаю образу, що може блокувати мій потік?",
            "Чим непрощення служило мені й чого воно мені коштує?",
            "Як це — простити повністю: не заради них, а заради власної свободи?",
        ],
    ),
    (
        "Інтеграція — ким я стаю?",
        "Двадцять вісім днів практики змінили тебе. Засвідчимо цю трансформацію.",
        [
            "Чим я докорінно відрізняюся від тієї, хто відкрила цей щоденник першого дня?",
            "Які частини старої себе я нарешті готова відкласти назавжди?",
            "Ким я стаю — у що ця людина вірить, що відчуває і як діє?",
        ],
    ),
]


def build_shadow_work(c, idx, pn):
    cream_bg(c)
    corner_marks(c)

    title, intro, prompts = SHADOW_WORK[idx]

    y = H - M - 16
    c.setFillColor(GOLD)
    c.setFont("Arsenal", 10)
    c.drawCentredString(W / 2, y, "РОБОТА З ТІННЮ")
    y -= 36

    c.setFillColor(INK)
    c.setFont("Italiana", 26)
    c.drawCentredString(W / 2, y, title)
    y -= 20

    gold_rule(c, y, diamond=True)
    y -= 22

    c.setFont("CrimsonItal", 13)
    y = draw_wrapped(c, intro, M + 20, y, IW - 40, "CrimsonItal", 13,
                     color=INK, line_h=20)
    y -= 28

    for i, prompt in enumerate(prompts):
        c.setFillColor(GOLD)
        c.setFont("Arsenal", 10)
        c.drawString(M, y, f"ПИТАННЯ {i + 1}")
        y -= 18
        c.setFillColor(INK)
        y = draw_wrapped(c, prompt, M + 8, y, IW - 16, "CrimsonItal", 13,
                         color=INK, line_h=20)
        y -= 22
        lines = 6 if i == 0 else 5
        for _ in range(lines):
            write_line(c, M, y, IW)
            y -= 26
        y -= 14

    footer(c, pn)


# ── Synchronicity Log ──────────────────────────────────────────────────────────

def build_sync_log(c, pn):
    cream_bg(c)
    corner_marks(c)

    # Header (only on first page of section, but we put a mini header on each)
    y = H - M - 22
    c.setFillColor(GOLD)
    c.setFont("Arsenal", 10)
    c.drawCentredString(W / 2, y, "ЖУРНАЛ СИНХРОНІЧНОСТЕЙ")
    y -= 36

    c.setFillColor(INK)
    c.setFont("Italiana", 26)
    c.drawCentredString(W / 2, y, "Знаки та суголосся")
    y -= 22
    gold_rule(c, y, diamond=True)
    y -= 22

    # 3 entries per page
    for entry_idx in range(3):
        # Entry header row
        c.setFillColor(INK)
        c.setFont("Arsenal", 10)
        c.drawString(M, y, "ЗАПИС  №_____")
        c.drawString(M + 180, y, "ДАТА _____ / _____ / _____")
        y -= 20

        c.setFont("Arsenal", 10)
        c.drawString(M, y, "ЩО СТАЛОСЯ")
        y -= 16
        for _ in range(2):
            write_line(c, M, y, IW)
            y -= 22

        c.drawString(M, y, "ПОСЛАННЯ АБО ЗНАЧЕННЯ")
        y -= 16
        write_line(c, M, y, IW)
        y -= 22

        c.drawString(M, y, "ЯК Я ВІДРЕАГУВАЛА ЧИ ВІДЗНАЧИЛА ЦЕ")
        y -= 16
        write_line(c, M, y, IW)
        y -= 26

        if entry_idx < 2:
            gold_rule(c, y, diamond=False)
            y -= 20

    footer(c, pn)


# ── Moon Calendar ──────────────────────────────────────────────────────────────

MOON_MONTH_NAMES = ["Перший", "Другий", "Третій", "Четвертий"]

MOON_PAGE_INFO = [
    # (title, dark_page, content_type)
    ("Наміри на молодик",      True,  "intentions"),
    ("Зростаючий Місяць — Дія",     False, "action"),
    ("Повня — Відпускання",      False, "release"),
    ("Спадний Місяць — Інтеграція",  False, "integrate"),
]


def build_moon_calendar(c, month_idx, page_in_month, pn):
    """month_idx 0–3, page_in_month 0–3."""
    title, is_dark, ctype = MOON_PAGE_INFO[page_in_month]
    month_name = MOON_MONTH_NAMES[month_idx]

    if is_dark and not PRINT_SAFE:
        dark_bg(c)
        corner_marks(c, LGOLD)
        ink  = WTEXT
        gclr = LGOLD
        dark = True
        flower_of_life(c, W / 2, H / 2, 34, rings=1, color=LGOLD, alpha=0.06)
    else:
        cream_bg(c)
        corner_marks(c)
        ink  = INK
        gclr = GOLD
        dark = False

    y = H - M - 20
    c.setFillColor(gclr)
    c.setFont("Arsenal", 10)
    c.drawCentredString(W / 2, y, f"МІСЯЧНИЙ ЦИКЛ  ·  {month_name.upper()} МІСЯЦЬ")
    y -= 38

    c.setFillColor(ink)
    c.setFont("Italiana", 28)
    c.drawCentredString(W / 2, y, title)
    y -= 20

    if dark:
        dark_rule(c, y)
    else:
        gold_rule(c, y, diamond=True)
    y -= 30

    content_map = {
        "intentions": [
            ("МОЄ БАЖАННЯ НА МОЛОДИК ЦЬОГО ЦИКЛУ",
             "Що я закликаю у своє життя цього місячного циклу?", 5),
            ("РИТУАЛ, ЯКИЙ Я ПРОВЕДУ НА МОЛОДИК",
             "Як я відзначу цей священний поріг?", 4),
            ("ЩО Я САДЖУ",
             "Зерна, які я свідомо сію цього циклу:", 4),
        ],
        "action": [
            ("НАТХНЕННІ ДІЇ, ЯКІ Я РОБЛЮ",
             "Конкретні кроки до мого бажання цього тижня:", 6),
            ("ЩО ПОКАЗУЄ МЕНІ ВСЕСВІТ",
             "Знаки та сигнали, що з'являються в моїй зростаючій енергії:", 5),
            ("НОТАТКИ ПРО ІМПУЛЬС",
             "Як відчувається моє бажання, наближаючись до повні?", 4),
        ],
        "release": [
            ("ЩО Я ВІДПУСКАЮ НА ПОВНЮ",
             "Переконання, звички чи патерни енергії, які я свідомо відпускаю:", 5),
            ("ЩО Я СВЯТКУЮ",
             "Докази, зростання та перемоги цього місячного циклу:", 5),
            ("МОЯ ВДЯЧНІСТЬ НА ПОВНЮ",
             "Що повня освітлює в моєму серці:", 4),
        ],
        "integrate": [
            ("ЩО Я ІНТЕГРУЮ",
             "Уроки та дари цього завершеного місячного циклу:", 5),
            ("ЯК Я ЗРОСЛА",
             "Ким я є тепер, якою не була на молодик:", 4),
            ("ГОТУЮСЯ ДО НАСТУПНОГО ЦИКЛУ",
             "Що я хочу понести далі, до наступного молодика:", 4),
        ],
    }

    for label, prompt, n_lines in content_map[ctype]:
        c.setFillColor(ink)
        c.setFont("Arsenal", 11)
        c.drawString(M, y, label)
        y -= 18
        c.setFont("CrimsonItal", 12)
        c.drawString(M + 8, y, prompt)
        y -= 22
        for _ in range(n_lines):
            write_line(c, M, y, IW)
            y -= 26
        y -= 12

    footer(c, pn, dark=dark)


# ── Bonus / Extra Journaling Pages ─────────────────────────────────────────────

BONUS_TITLES = [
    "Простір — додаткове місце для письма",
    "Нотатки порталу",
    "Майданчик афірмацій",
    "Щоденник снів",
    "Листи до Всесвіту",
    "Візуалізація квантового стрибка",
    "Промовляє моя найвища сутність",
    "Завершення — фінальна рефлексія",
]

BONUS_PROMPTS = [
    "Використовуй цю сторінку для будь-яких записів, що не вмістилися в щоденну практику.",
    "Нотатки, осяяння, послання та ідеї, зібрані під час практики порталу.",
    "Пиши афірмації в усіх напрямках — заповни сторінку твердженнями «я є».",
    "Записуй свої сни, символи та нічні послання від Всесвіту.",
    "Напиши лист Всесвіту, майбутній собі або самому своєму бажанню.",
    "Опиши в яскравих чуттєвих деталях день, коли твоє бажання повністю здійснилося.",
    "Що твоя найвища сутність хоче, щоб ти знала просто зараз?",
    "Ти завершила 28 днів. Ким ти є тепер? Що змінилося назавжди?",
]


def build_bonus_page(c, idx, pn):
    cream_bg(c)
    corner_marks(c)
    flower_of_life(c, W / 2, H * 0.50, 18, rings=1, color=GOLD, alpha=0.04)

    y = H - M - 22
    c.setFillColor(GOLD)
    c.setFont("Arsenal", 10)
    c.drawCentredString(W / 2, y, "ДОДАТКОВИЙ ПРОСТІР")
    y -= 36

    c.setFillColor(INK)
    c.setFont("Italiana", 26)
    c.drawCentredString(W / 2, y, BONUS_TITLES[idx])
    y -= 20

    gold_rule(c, y, diamond=True)
    y -= 24

    c.setFont("CrimsonItal", 13)
    c.setFillColor(INK)
    # Wrap the prompt so long Ukrainian lines never approach the page edge
    words = BONUS_PROMPTS[idx].split()
    plines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if c.stringWidth(trial, "CrimsonItal", 13) <= IW - 60 or not cur:
            cur = trial
        else:
            plines.append(cur); cur = w
    if cur:
        plines.append(cur)
    for pl in plines:
        c.drawCentredString(W / 2, y, pl)
        y -= 20
    y -= 18

    n_lines = 18 - (len(plines) - 1)   # keep the writing block from reaching the footer
    for _ in range(n_lines):
        write_line(c, M, y, IW)
        y -= 30

    footer(c, pn)


# ── Closing Page (dark) ─────────────────────────────────────────────────────────

def build_closing(c, pn):
    dark_bg(c)
    corner_marks(c, LGOLD)
    flower_of_life(c, W / 2, H * 0.50, 40, rings=2, color=LGOLD, alpha=0.22)

    # Outer halos
    c.saveState()
    c.setStrokeColor(LGOLD)
    c.setStrokeAlpha(0.10)
    c.setFillAlpha(0)
    c.setLineWidth(0.5)
    for r in (140, 158):
        c.circle(W / 2, H * 0.50, r, stroke=1, fill=0)
    c.restoreState()

    y = H - M - 36
    c.setFillColor(LGOLD)
    c.setFont("Arsenal", 10)
    draw_mixed_centred(c, W / 2, y, "✶   Т И   З М О Г Л А   ✶", "Arsenal", 10)

    y = H * 0.50 + 100
    c.setFillColor(WTEXT)
    c.setFont("Italiana", 42)
    c.drawCentredString(W / 2, y, "Портал відчинено.")
    y -= 18

    dark_rule(c, y)
    y -= 36

    c.setFont("CrimsonPro", 14)
    lines_closing = [
        "Двадцять вісім днів священної відданості.",
        "П'ятсот чотири повторення твого бажання.",
        "Кожне — нитка, вплетена в тканину того, що стає реальним.",
        "",
        "Ти не просто писала в щоденнику.",
        "Ти змінила свої переконання й підняла свою вібрацію,",
        "і надіслала сигнал такий чіткий, що Всесвіт не міг його оминути.",
        "",
        "Портал не позаду тебе. Він у тебе під ногами.",
        "Продовжуй іти крізь нього.",
    ]
    for line in lines_closing:
        c.setFillColor(WTEXT)
        if line == "":
            y -= 10
        else:
            c.drawCentredString(W / 2, y, line)
            y -= 22

    y -= 28
    dark_rule(c, y)
    y -= 30

    c.setFillColor(LGOLD)
    c.setFont("Arsenal", 11)
    c.drawCentredString(W / 2, y, "3 · 6 · 9  ·  Я НАПИСАЛА  ·  Я ПОВІРИЛА  ·  Я ОТРИМАЛА")

    footer(c, pn, dark=True)


# ── Thank You Page (dark) ──────────────────────────────────────────────────────

def build_thank_you(c, pn):
    dark_bg(c)
    corner_marks(c, LGOLD)
    flower_of_life(c, W / 2, H * 0.50, 34, rings=1, color=LGOLD, alpha=0.08)

    y = H - M - 36
    c.setFillColor(LGOLD)
    c.setFont("Arsenal", 10)
    draw_mixed_centred(c, W / 2, y, "✶   Д Я К У Ю   ✶", "Arsenal", 10)

    y = H * 0.50 + 110
    c.setFillColor(WTEXT)
    c.setFont("Italiana", 42)
    c.drawCentredString(W / 2, y, "З вдячністю")
    y -= 16
    dark_rule(c, y)
    y -= 34

    lines = [
        "Дякую, що обрала Щоденник маніфестації «Портал 369».",
        "Його створено з наміром, любов'ю та глибокою вірою",
        "в силу твоїх бажань.",
        "",
        "Твоя покупка підтримує незалежну авторку, яка вкладає",
        "усе, щоб створювати інструменти, які справді змінюють життя.",
        "",
        "Якщо цей щоденник зворушив тебе, будь ласка, залиш відгук",
        "на Etsy — це безцінно й допомагає іншим знайти свій портал.",
        "",
        "Ти гідна всього, що закликаєш у своє життя.",
        "Довіряй процесу. Продовжуй писати. Всесвіт слухає.",
    ]

    c.setFont("CrimsonPro", 13)
    for line in lines:
        if line == "":
            y -= 8
        else:
            c.setFillColor(WTEXT)
            c.drawCentredString(W / 2, y, line)
            y -= 22

    y -= 20
    dark_rule(c, y)
    y -= 28

    c.setFillColor(LGOLD)
    c.setFont("Arsenal", 11)
    c.drawCentredString(W / 2, y, "GlowHausDigital  ·  teamglowhaus@gmail.com")

    footer(c, pn, dark=True)


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN BUILD
# ══════════════════════════════════════════════════════════════════════════════

def main():
    global PRINT_SAFE
    PRINT_SAFE = True
    setup_fonts()

    out_path = os.path.join(HERE, "369-portal-FINAL.pdf")
    c = rlc.Canvas(out_path, pagesize=letter)

    pn = 1  # running page counter

    # ── Front matter (pages 1-9) ─────────────────────────────────────────────
    build_cover(c);              c.showPage(); pn += 1   # 1
    build_title_page(c, pn);     c.showPage(); pn += 1   # 2
    build_license_page(c, pn);   c.showPage(); pn += 1   # 3
    build_welcome(c, pn);        c.showPage(); pn += 1   # 4
    build_method(c, pn);         c.showPage(); pn += 1   # 5
    build_how_to_use(c, pn);     c.showPage(); pn += 1   # 6
    build_portal_intention(c, pn); c.showPage(); pn += 1 # 7
    build_commitments(c, pn);    c.showPage(); pn += 1   # 8
    build_moon_overview(c, pn);  c.showPage(); pn += 1   # 9

    # ── Daily pages (pages 9-64: 28 days × 2 pages) ──────────────────────────
    for day in range(1, 29):
        build_morning_page(c, day, pn); c.showPage(); pn += 1
        build_evening_page(c, day, pn); c.showPage(); pn += 1
    # now pn = 65

    # ── Weekly Reviews (pages 65-68) ─────────────────────────────────────────
    for week in range(1, 5):
        build_weekly_review(c, week, pn); c.showPage(); pn += 1
    # now pn = 69

    # ── Monthly Review (pages 69-72) ─────────────────────────────────────────
    for i in range(4):
        build_monthly_review(c, i, pn); c.showPage(); pn += 1
    # now pn = 73

    # ── Shadow Work (pages 73-80) ─────────────────────────────────────────────
    for i in range(8):
        build_shadow_work(c, i, pn); c.showPage(); pn += 1
    # now pn = 81

    # ── Synchronicity Log (pages 81-96) ──────────────────────────────────────
    for _ in range(16):
        build_sync_log(c, pn); c.showPage(); pn += 1
    # now pn = 97

    # ── Moon Calendar (pages 97-112: 4 months × 4 pages) ────────────────────
    for month_idx in range(4):
        for page_in_month in range(4):
            build_moon_calendar(c, month_idx, page_in_month, pn)
            c.showPage(); pn += 1
    # now pn = 113

    # ── Bonus Pages (pages 113-120) ───────────────────────────────────────────
    for i in range(8):
        build_bonus_page(c, i, pn); c.showPage(); pn += 1
    # now pn = 121

    # ── Closing & Thank You (pages 122-123) ─────────────────────────────────
    build_closing(c, pn);   c.showPage(); pn += 1
    build_thank_you(c, pn); c.showPage()

    c.save()
    print(f"Saved {out_path}  ({pn} pages)")
    return out_path


if __name__ == "__main__":
    main()
