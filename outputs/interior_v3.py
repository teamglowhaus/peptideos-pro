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
    fonts = {
        "Italiana":      "Italiana-Regular.ttf",
        "CrimsonPro":    "CrimsonPro-Regular.ttf",
        "CrimsonItal":   "CrimsonPro-Italic.ttf",
        "CrimsonBold":   "CrimsonPro-Bold.ttf",
        "Arsenal":       "ArsenalSC-Regular.ttf",
        "Jura":          "Jura-Light.ttf",
        "Gloock":        "Gloock-Regular.ttf",
    }
    for name, fname in fonts.items():
        path = os.path.join(FONT_DIR, fname)
        pdfmetrics.registerFont(TTFont(name, path))


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
        c.setFont("Italiana", 12)
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
    c.drawCentredString(W / 2, FY - 2, "THE PORTAL  ·  369 MANIFESTATION JOURNAL")

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

    # "A SACRED PRACTICE" supertitle
    y = H - M - 34
    c.setFillColor(LGOLD)
    c.setFont("Arsenal", 10)
    c.drawCentredString(W / 2, y, "∙ ∙ ∙   A   S A C R E D   P R A C T I C E   ∙ ∙ ∙")

    # Main title
    y -= 52
    c.setFillColor(WTEXT)
    c.setFont("Italiana", 58)
    c.drawCentredString(W / 2, y, "THE")
    y -= 64
    c.drawCentredString(W / 2, y, "PORTAL")

    # Gold diamond separator
    y -= 28
    c.setFillColor(LGOLD)
    c.setFont("Italiana", 14)
    c.drawCentredString(W / 2, y, "◆  3 · 6 · 9  ◆")

    # Subtitle
    y -= 30
    c.setFillColor(WTEXT)
    c.setFont("Italiana", 22)
    c.drawCentredString(W / 2, y, "Manifestation Journal")

    # Tagline — positioned below the Flower of Life
    y = fol_cy - 120
    c.setFillColor(WTEXT)
    c.setFont("CrimsonItal", 15)
    c.drawCentredString(W / 2, y, "Write your reality into existence.")
    y -= 26
    c.setFillColor(LGOLD)
    c.setFont("Arsenal", 9)
    c.drawCentredString(W / 2, y,
        "28 DAYS  ·  MORNING  ·  MIDDAY  ·  EVENING  ·  ALIGNMENT")

    # Bottom rule + brand
    c.saveState()
    c.setStrokeColor(LGOLD)
    c.setLineWidth(0.7)
    c.line(M + 20, M + 44, W - M - 20, M + 44)
    c.restoreState()
    c.setFillColor(LGOLD)
    c.setFont("Arsenal", 9)
    c.drawCentredString(W / 2, M + 28, "T H E   P O R T A L   S E R I E S")


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
    c.drawCentredString(W / 2, y, "THIS JOURNAL BELONGS TO")
    y -= 28
    write_line(c, M + 60, y + 6, IW - 120)
    y -= 44

    c.setFont("Arsenal", 11)
    c.drawCentredString(W / 2, y, "PORTAL ACTIVATION DATE")
    y -= 28
    write_line(c, M + 80, y + 6, IW - 160)
    y -= 52

    gold_rule(c, y, diamond=True)
    y -= 52

    c.setFont("Italiana", 32)
    c.drawCentredString(W / 2, y, "My Portal Intention")
    y -= 50

    c.setFont("CrimsonItal", 13)
    c.drawCentredString(W / 2, y, "The single most important desire I am calling into form:")
    y -= 48

    for _ in range(5):
        write_line(c, M, y, IW)
        y -= 36

    y -= 24
    gold_rule(c, y, diamond=True)
    y -= 46

    c.setFont("Arsenal", 11)
    c.drawCentredString(W / 2, y, "I AM WORTHY  ·  I AM READY  ·  I AM OPEN")

    footer(c, pn)


# ── Page 3: Welcome (dark) ─────────────────────────────────────────────────────

def build_welcome(c, pn):
    dark_bg(c)
    corner_marks(c, LGOLD)
    flower_of_life(c, W / 2, H - M - 56, 20, rings=1, color=LGOLD, alpha=0.45)

    y = H - M - 130
    c.setFillColor(LGOLD)
    c.setFont("Arsenal", 10)
    c.drawCentredString(W / 2, y, "✶   W E L C O M E   ✶")
    y -= 42

    c.setFillColor(WTEXT)
    c.setFont("Italiana", 36)
    c.drawCentredString(W / 2, y, "You Have Arrived.")
    y -= 14

    dark_rule(c, y)
    y -= 36

    paras = [
        "The 369 Portal is more than a journal — it is a daily sacred practice,",
        "a living conversation between you and the infinite field of all possibility.",
        "",
        "Nikola Tesla believed 3, 6, and 9 hold the key to the universe.",
        "This journal is built on that sacred code:",
        "",
        "Write your desire 3 times in the morning to set the intention.",
        "Write it 6 times at midday to anchor it in your energy field.",
        "Write it 9 times in the evening to send it to the universe.",
        "",
        "Each repetition is a signal. Each page is an act of faith.",
        "Each completed day is proof that you showed up for your vision.",
        "",
        "This is not a wish list. This is a portal.",
        "Step through it — daily, devotedly, powerfully.",
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
    c.drawCentredString(W / 2, y, "3 · 6 · 9  ·  WRITE  ·  BELIEVE  ·  RECEIVE")

    footer(c, pn, dark=True)


# ── Page 4: The 369 Method ─────────────────────────────────────────────────────

def build_method(c, pn):
    cream_bg(c)
    corner_marks(c)

    y = H - M - 36
    c.setFillColor(INK)
    c.setFont("Italiana", 30)
    c.drawCentredString(W / 2, y, "The 369 Method")
    y -= 22
    gold_rule(c, y, diamond=True)
    y -= 32

    sections = [
        ("3", "MORNING TRANSMISSIONS",
         "Write your desire 3 times upon waking. Morning is when the subconscious "
         "mind is most receptive and the veil between worlds is thinnest. These "
         "three repetitions plant the seed in the fertile soil of a new day."),
        ("6", "MIDDAY ACTIVATION",
         "Write your desire 6 times at midday. This mid-point practice keeps your "
         "intention alive through the distractions of the day. Six is the number "
         "of harmony — you are harmonizing your vibration with your desire."),
        ("9", "EVENING INTEGRATION",
         "Write your desire 9 times before sleep. Nine is the number of completion. "
         "Your evening writing sends a clear signal as your conscious mind releases "
         "into the quantum field of dreams and deep creation."),
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
    c.drawString(M, y, "TIPS FOR MAXIMUM ACTIVATION")
    y -= 22

    tips = [
        "◆  Write by hand — the physical act encodes the intention in your body.",
        '◆  Use present tense: "I am," "I have," "I experience."',
        "◆  Feel the emotion of already having it as you write each repetition.",
        "◆  Stay consistent — 28 days of practice rewires your subconscious mind.",
        "◆  Trust the process even when you cannot yet see the how.",
    ]
    c.setFont("CrimsonPro", 13)
    c.setFillColor(INK)
    for tip in tips:
        c.drawString(M + 10, y, tip)
        y -= 22

    footer(c, pn)


# ── Page 5: How to Use ─────────────────────────────────────────────────────────

def build_how_to_use(c, pn):
    cream_bg(c)
    corner_marks(c)

    y = H - M - 36
    c.setFillColor(INK)
    c.setFont("Italiana", 30)
    c.drawCentredString(W / 2, y, "How to Use This Journal")
    y -= 22
    gold_rule(c, y, diamond=True)
    y -= 32

    steps = [
        ("01", "CHOOSE YOUR DESIRE",
         "Select one specific, emotionally charged desire to focus on for 28 days. "
         "Write your exact desire statement on the next page before beginning."),
        ("02", "WRITE DAILY — MORNING, MIDDAY & EVENING",
         "Each day has two pages: morning/midday and evening. Complete both every "
         "day. Consistency is the key that opens the portal."),
        ("03", "ENERGY CHECK-INS",
         "Shade the energy bar each morning and evening (1=low, 10=high). Tracking "
         "your vibrational state reveals patterns that predict breakthroughs."),
        ("04", "GRATITUDE & SYNCHRONICITIES",
         "Log moments of alignment, unexpected signs, and things you are grateful "
         "for. The more you notice, the more the universe sends."),
        ("05", "WEEKLY & MONTHLY REVIEWS",
         "Use the review pages every 7 days to track evidence of your manifestation, "
         "shifts in belief, and what to amplify in the next cycle."),
        ("06", "SHADOW WORK & SYNC LOG",
         "The shadow work section and synchronicity log at the back support deeper "
         "transformation and evidence collection throughout your practice."),
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
    c.drawCentredString(W / 2, y, "My Portal Desire Statement")
    y -= 22
    gold_rule(c, y, diamond=True)
    y -= 24

    c.setFillColor(INK)
    c.setFont("CrimsonItal", 13)
    c.drawCentredString(W / 2, y, "Write the exact words you will use in your daily practice.")
    y -= 20
    c.drawCentredString(W / 2, y, "Present tense, personal, positive, and emotionally alive.")
    y -= 38

    for _ in range(6):
        write_line(c, M, y, IW)
        y -= 36
    y -= 16

    gold_rule(c, y, diamond=False)
    y -= 28

    c.setFillColor(INK)
    c.setFont("Arsenal", 12)
    c.drawString(M, y, "HOW THIS DESIRE WILL FEEL WHEN IT ARRIVES")
    y -= 24
    for _ in range(3):
        write_line(c, M, y, IW)
        y -= 32
    y -= 14

    gold_rule(c, y, diamond=False)
    y -= 28

    c.setFillColor(INK)
    c.setFont("Arsenal", 12)
    c.drawString(M, y, "WHY I KNOW I AM WORTHY OF THIS")
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
    c.drawCentredString(W / 2, y, "My Portal Commitments")
    y -= 22
    gold_rule(c, y, diamond=True)
    y -= 30

    c.setFillColor(INK)
    c.setFont("CrimsonItal", 13)
    c.drawCentredString(W / 2, y, "I enter this portal with full commitment to my vision.")
    y -= 20
    c.drawCentredString(W / 2, y, "I sign my name below as a sacred contract with myself.")
    y -= 38

    commits = [
        "I commit to writing my desire 3–6–9 times every single day for 28 days.",
        "I commit to showing up even on days when I don’t believe it’s working.",
        "I commit to noticing and recording every sign of alignment, however small.",
        "I commit to treating this journal as a sacred ritual, not a chore.",
        "I commit to trusting the timing of the universe and releasing outcomes.",
        "I commit to becoming the version of myself who already has this desire.",
        "I commit to completing all 28 days without skipping or giving up.",
    ]

    c.setFont("CrimsonPro", 13)
    c.setFillColor(INK)
    for line in commits:
        c.drawString(M + 5, y, f"◆   {line}")
        y -= 26
    y -= 18

    gold_rule(c, y, diamond=False)
    y -= 38

    c.setFillColor(INK)
    c.setFont("Arsenal", 11)
    c.drawString(M, y, "SIGNED")
    write_line(c, M + 60, y + 5, 200)
    c.drawString(M + 300, y, "DATE")
    write_line(c, M + 342, y + 5, 114)
    y -= 46

    c.setFillColor(INK)
    c.setFont("CrimsonItal", 14)
    c.drawCentredString(W / 2, y,
        '"The moment you commit, the universe conspires in your favor."')
    y -= 22
    c.setFillColor(GOLD)
    c.setFont("Arsenal", 10)
    c.drawCentredString(W / 2, y, "— GOETHE (ADAPTED)")
    y -= 44

    gold_rule(c, y, diamond=True)
    y -= 28

    c.setFillColor(INK)
    c.setFont("Arsenal", 12)
    c.drawString(M, y, "MY PORTAL AFFIRMATION")
    y -= 18
    c.setFont("CrimsonItal", 12)
    c.drawString(M + 8, y,
        "Write the single affirmation that will anchor your belief throughout this portal:")
    y -= 26

    for _ in range(4):
        write_line(c, M, y, IW)
        y -= 28
    y -= 16

    c.setFillColor(INK)
    c.setFont("CrimsonItal", 13)
    c.drawCentredString(W / 2, y,
        "I carry this commitment into every page of this portal.")

    footer(c, pn)


# ── Page 8: Moon Phase Overview (dark) ─────────────────────────────────────────

def build_moon_overview(c, pn):
    dark_bg(c)
    corner_marks(c, LGOLD)

    y = H - M - 22
    c.setFillColor(LGOLD)
    c.setFont("Arsenal", 10)
    c.drawCentredString(W / 2, y, "✶   THE MOON  ·  YOUR COSMIC PARTNER   ✶")
    y -= 42

    c.setFillColor(WTEXT)
    c.setFont("Italiana", 34)
    c.drawCentredString(W / 2, y, "Moon Phase Guide")
    y -= 18
    dark_rule(c, y)
    y -= 36

    phases = [
        ("○○", "NEW MOON",
         "Set intentions. Plant seeds. The ideal time to begin your portal."),
        ("◔", "WAXING CRESCENT",
         "Take inspired action. Build momentum. Show the universe you’re serious."),
        ("◐", "FIRST QUARTER",
         "Push through obstacles. Double your commitment. Keep writing."),
        ("◓", "WAXING GIBBOUS",
         "Refine and align. Your manifestation is forming in the unseen."),
        ("●", "FULL MOON",
         "Celebrate evidence. Release blocks. Feel deep gratitude for what’s coming."),
        ("◒", "WANING GIBBOUS",
         "Share your energy and gifts. Express thanks to the field of all creation."),
        ("◑", "LAST QUARTER",
         "Let go of what no longer serves. Clear space for your desire to land."),
        ("◕", "WANING CRESCENT",
         "Rest and receive. Trust the silence. Prepare for the next new cycle."),
    ]

    col_w = IW / 2 - 10
    ROW_H = 82  # increased row height for better spacing
    for i, (sym, phase, desc) in enumerate(phases):
        col = i % 2
        row = i // 2
        x = M + col * (col_w + 20)
        row_y = y - row * ROW_H

        c.setFillColor(LGOLD)
        c.setFont("Arsenal", 11)
        c.drawString(x, row_y, phase)
        c.setFillColor(WTEXT)
        c.setFont("CrimsonPro", 12)
        draw_wrapped(c, desc, x + 5, row_y - 18, col_w - 10,
                     "CrimsonPro", 12, color=WTEXT, line_h=17)

    y -= (4 * ROW_H) + 16
    dark_rule(c, y)
    y -= 28

    c.setFillColor(WTEXT)
    c.setFont("CrimsonItal", 13)
    c.drawCentredString(W / 2, y, "Work with the moon’s energy to amplify your 369 practice.")
    y -= 22
    c.drawCentredString(W / 2, y, "New moons are the most potent time to begin a new portal.")
    y -= 36

    dark_rule(c, y)
    y -= 28

    c.setFillColor(LGOLD)
    c.setFont("Arsenal", 10)
    c.drawString(M, y, "MY MOON NOTES FOR THIS PORTAL CYCLE")
    y -= 22
    # Gold lines — fully visible against the dark background
    c.saveState()
    c.setStrokeColor(LGOLD)
    c.setStrokeAlpha(1.0)
    c.setFillAlpha(1.0)
    c.setLineWidth(0.65)
    for _ in range(4):
        c.line(M, y, W - M, y)
        y -= 28
    c.restoreState()

    footer(c, pn, dark=True)


# ── Daily Pages ────────────────────────────────────────────────────────────────

EVENING_PROMPTS = [
    "What evidence of my manifestation did I notice today, however small?",
    "How did I embody the feeling of already having my desire today?",
    "What belief about myself shifted or softened today?",
    "What am I choosing to release before I sleep tonight?",
    "How did the universe support me today in ways I might have missed?",
    "What would the highest version of me say about today’s practice?",
    "What do I want to dream into being as I sleep tonight?",
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
    c.drawString(M, y, f"WEEK {week}")
    c.drawRightString(W - M, y, "MORNING  ·  MIDDAY")
    y -= 34

    # Day number
    c.setFillColor(INK)
    c.setFont("Italiana", 38)
    c.drawCentredString(W / 2, y, f"DAY {day}")
    y -= 24

    # Date
    c.setFont("Arsenal", 11)
    c.drawCentredString(W / 2, y, "DATE  ______ / ______ / ______")
    y -= 22

    gold_rule(c, y, diamond=True)
    y -= 24

    # ── MORNING TRANSMISSIONS (3×) ─────────────────────────────────────────
    badge(c, M + 26, y - 20, "3", "MORNING TRANSMISSIONS",
          subtitle="WRITE YOUR DESIRE 3 TIMES")
    y -= 50

    for _ in range(3):
        write_line(c, M, y, IW)
        y -= 32
    y -= 8

    # Morning energy
    c.setFillColor(INK)
    c.setFont("Arsenal", 10)
    c.drawString(M, y, "MORNING ENERGY — SHADE YOUR LEVEL  1 → 10")
    y -= 18
    energy_bar(c, M, y)
    y -= 38

    gold_rule(c, y, diamond=True)
    y -= 24

    # ── MIDDAY ACTIVATION (6×) ───────────────────────────────────────────────
    badge(c, M + 26, y - 20, "6", "MIDDAY ACTIVATION",
          subtitle="WRITE YOUR DESIRE 6 TIMES")
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
    c.drawString(M, y, "INTENTION ALIGNMENT")
    y -= 18
    c.setFont("CrimsonItal", 12)
    c.drawString(M + 8, y, "What aligned action can I take today that moves me toward this desire?")
    y -= 24

    for _ in range(3):
        write_line(c, M, y, IW)
        y -= 26

    footer(c, pn)


def build_evening_page(c, day, pn):
    """Evening (9×) + Reflection page."""
    cream_bg(c)
    corner_marks(c)
    # Subtle watermark centred in the 9-write-lines area — well clear of release statement
    flower_of_life(c, W / 2, H * 0.65, 22, rings=2, color=GOLD, alpha=0.06)

    week = (day - 1) // 7 + 1
    y = H - M - 14

    c.setFillColor(GOLD)
    c.setFont("Arsenal", 10)
    c.drawString(M, y, f"WEEK {week}")
    c.drawRightString(W - M, y, "EVENING  ·  INTEGRATION")
    y -= 30

    c.setFillColor(INK)
    c.setFont("Italiana", 28)
    c.drawCentredString(W / 2, y, f"Day {day}  ·  Evening")
    y -= 20

    gold_rule(c, y, diamond=True)
    y -= 24

    # ── EVENING INTEGRATION (9×) ───────────────────────────────────────────
    badge(c, M + 26, y - 20, "9", "EVENING INTEGRATION",
          subtitle="WRITE YOUR DESIRE 9 TIMES")
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
    c.drawString(M, y, "EVENING ENERGY — SHADE YOUR LEVEL  1 → 10")
    y -= 18
    energy_bar(c, M, y)
    y -= 38

    # ── GRATITUDE SEED ──────────────────────────────────────────────────────────
    c.setFillColor(INK)
    c.setFont("Arsenal", 11)
    c.drawString(M, y, "GRATITUDE SEED")
    y -= 16
    c.setFont("CrimsonItal", 12)
    c.drawString(M + 8, y, "One thing I’m grateful for that I noticed today:")
    y -= 22
    write_line(c, M, y, IW)
    y -= 28
    write_line(c, M, y, IW)
    y -= 30

    # ── SYNCHRONICITIES & SIGNS ─────────────────────────────────────────────────
    c.setFillColor(INK)
    c.setFont("Arsenal", 11)
    c.drawString(M, y, "SYNCHRONICITIES  &  SIGNS")
    y -= 14
    c.setFont("CrimsonItal", 12)
    c.drawString(M + 8, y, "What aligned or unexpected moments did I notice today?")
    y -= 6
    bordered_box(c, M, y, IW, 54)
    y -= 62

    # ── EVENING REFLECTION ──────────────────────────────────────────────────────
    c.setFillColor(INK)
    c.setFont("Arsenal", 11)
    c.drawString(M, y, "EVENING REFLECTION")
    y -= 16
    prompt = EVENING_PROMPTS[(day - 1) % 7]
    c.setFont("CrimsonItal", 12)
    c.drawString(M + 8, y, prompt)
    y -= 24
    write_line(c, M, y, IW)
    y -= 28
    write_line(c, M, y, IW)
    y -= 32

    # ── RELEASE STATEMENT ───────────────────────────────────────────────────────
    gold_rule(c, y, diamond=False)
    y -= 20
    c.setFillColor(INK)
    c.setFont("CrimsonItal", 13)
    c.drawCentredString(
        W / 2, y,
        "I release this desire to the universe with full trust and gratitude."
    )

    footer(c, pn)


# ── Weekly Review ──────────────────────────────────────────────────────────────

WEEKLY_SECTIONS = [
    ("EVIDENCE OF MANIFESTATION",
     "What signs, synchronicities, or physical shifts did I notice this week?", 4),
    ("BELIEF SHIFTS",
     "How has my belief in this desire strengthened or clarified?", 3),
    ("ENERGY PATTERNS",
     "Which days felt most aligned? What supported or drained my energy?", 3),
    ("GRATITUDE HARVEST",
     "What am I most grateful for from this week’s practice?", 3),
    ("AMPLIFY NEXT WEEK",
     "What will I do more of in the coming week to deepen my manifestation?", 3),
]


def build_weekly_review(c, week, pn):
    cream_bg(c)
    corner_marks(c)
    flower_of_life(c, W / 2, H * 0.50, 24, rings=2, color=GOLD, alpha=0.08)

    y = H - M - 22
    c.setFillColor(GOLD)
    c.setFont("Arsenal", 10)
    c.drawCentredString(W / 2, y, "WEEKLY REVIEW")
    y -= 36

    c.setFillColor(INK)
    c.setFont("Italiana", 32)
    c.drawCentredString(W / 2, y, f"Week {week}  ·  Reflection")
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
        "Monthly Overview",
        "Evidence & Alignment",
        "Shadow Integration",
        "Portal Forward",
    ]
    subtitles = [
        "Reflecting on 28 days of sacred practice",
        "What the universe has delivered",
        "What I’ve released and transformed",
        "Setting intentions for the next cycle",
    ]

    y = H - M - 22
    c.setFillColor(GOLD)
    c.setFont("Arsenal", 10)
    c.drawCentredString(W / 2, y, "MONTHLY REVIEW")
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
            ("DAYS COMPLETED (out of 28)", 1),
            ("MOST POWERFUL SYNCHRONICITY", 3),
            ("BIGGEST BELIEF SHIFT", 3),
            ("WHAT SURPRISED ME MOST", 3),
            ("OVERALL ENERGY TREND", 2),
        ],
        # Page 1
        [
            ("MANIFESTATION EVIDENCE — LIST EVERY SIGN", 5),
            ("UNEXPECTED GIFTS THAT ARRIVED", 4),
            ("HOW MY LIFE HAS SHIFTED IN 28 DAYS", 4),
        ],
        # Page 2
        [
            ("WHAT I RELEASED THIS MONTH", 4),
            ("SHADOW TREASURES I DISCOVERED", 4),
            ("HOW I INTEGRATED RESISTANCE INTO GROWTH", 4),
        ],
        # Page 3
        [
            ("MY NEXT DESIRE STATEMENT", 3),
            ("HOW MY VIBRATION HAS PERMANENTLY SHIFTED", 4),
            ("MY MESSAGE OF GRATITUDE TO THE UNIVERSE", 4),
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
        "Releasing the Fear of Being Seen",
        "What would happen if the world truly saw you — fully, powerfully, authentically?",
        [
            "What am I afraid people will think if I actually achieve this desire?",
            "Where did I first learn that it wasn’t safe to be fully visible and powerful?",
            "What would the most seen, most expressed version of me do differently today?",
        ],
    ),
    (
        "What I’m Ready to Let Go Of",
        "Completion is part of creation. What must end for your desire to begin?",
        [
            "What old story about myself is taking up space that my desire needs?",
            "What habit, relationship, or belief is quietly blocking my portal?",
            "If I knew letting this go was completely safe, what would I release right now?",
        ],
    ),
    (
        "The Story I Tell About Myself",
        "Your subconscious runs the programs it learned. Which ones need upgrading?",
        [
            "What is the core limiting belief I hold about whether I deserve this desire?",
            "When was the first time I decided I wasn’t enough for something like this?",
            "What is the upgraded belief I am choosing to install in its place?",
        ],
    ),
    (
        "My Relationship with Receiving",
        "Manifestation requires openness to receive. Are you truly open?",
        [
            "When good things happen, do I deflect, minimize, or doubt? Why?",
            "What would I need to believe about myself to receive this desire gracefully?",
            "What’s one way I can practice receiving more fully this week?",
        ],
    ),
    (
        "Ancestral Patterns I’m Breaking",
        "You are writing a new story not just for yourself, but for your entire lineage.",
        [
            "What patterns of lack, struggle, or unworthiness have I inherited?",
            "Which ancestors’ voices do I hear when I doubt my desire is possible?",
            "What new pattern am I consciously choosing to create for those who come after?",
        ],
    ),
    (
        "My Shadow Desires",
        "Sometimes what we resist wanting is exactly what we most need to claim.",
        [
            "What do I secretly want but have been afraid to admit, even to myself?",
            "What desire do I judge in others that I am actually longing for myself?",
            "What would I manifest if I were completely free of shame and judgment?",
        ],
    ),
    (
        "Forgiveness as a Portal",
        "Unforgiveness is a block in your energy field. Who do you need to release?",
        [
            "Who in my life am I holding grievances against that might be blocking my flow?",
            "How has staying in unforgiveness served me, and what is it costing me?",
            "What would it feel like to forgive fully — not for them, but for my own freedom?",
        ],
    ),
    (
        "Integration — Who Am I Becoming?",
        "Twenty-eight days of practice has changed you. Let’s witness that transformation.",
        [
            "How am I fundamentally different from the person who opened this journal on day 1?",
            "What parts of my old identity am I finally ready to lay down permanently?",
            "Who is the person I am stepping into — what do they believe, feel, and do?",
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
    c.drawCentredString(W / 2, y, "SHADOW WORK")
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
        c.drawString(M, y, f"PROMPT {i + 1}")
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
    c.drawCentredString(W / 2, y, "SYNCHRONICITY LOG")
    y -= 36

    c.setFillColor(INK)
    c.setFont("Italiana", 26)
    c.drawCentredString(W / 2, y, "Signs & Alignments")
    y -= 22
    gold_rule(c, y, diamond=True)
    y -= 22

    # 3 entries per page
    for entry_idx in range(3):
        # Entry header row
        c.setFillColor(INK)
        c.setFont("Arsenal", 10)
        c.drawString(M, y, "ENTRY  #_____")
        c.drawString(M + 180, y, "DATE _____ / _____ / _____")
        y -= 20

        c.setFont("Arsenal", 10)
        c.drawString(M, y, "WHAT HAPPENED")
        y -= 16
        for _ in range(2):
            write_line(c, M, y, IW)
            y -= 22

        c.drawString(M, y, "MESSAGE OR MEANING")
        y -= 16
        write_line(c, M, y, IW)
        y -= 22

        c.drawString(M, y, "HOW I RESPONDED OR ACKNOWLEDGED IT")
        y -= 16
        write_line(c, M, y, IW)
        y -= 26

        if entry_idx < 2:
            gold_rule(c, y, diamond=False)
            y -= 20

    footer(c, pn)


# ── Moon Calendar ──────────────────────────────────────────────────────────────

MOON_MONTH_NAMES = ["First", "Second", "Third", "Fourth"]

MOON_PAGE_INFO = [
    # (title, dark_page, content_type)
    ("New Moon Intentions",      True,  "intentions"),
    ("Waxing Moon — Action",     False, "action"),
    ("Full Moon — Release",      False, "release"),
    ("Waning Moon — Integrate",  False, "integrate"),
]


def build_moon_calendar(c, month_idx, page_in_month, pn):
    """month_idx 0–3, page_in_month 0–3."""
    title, is_dark, ctype = MOON_PAGE_INFO[page_in_month]
    month_name = MOON_MONTH_NAMES[month_idx]

    if is_dark:
        dark_bg(c)
        corner_marks(c, LGOLD)
        ink  = WTEXT
        gclr = LGOLD
        dark = True
    else:
        cream_bg(c)
        corner_marks(c)
        ink  = INK
        gclr = GOLD
        dark = False

    if is_dark:
        flower_of_life(c, W / 2, H / 2, 34, rings=2, color=LGOLD, alpha=0.40)

    y = H - M - 20
    c.setFillColor(gclr)
    c.setFont("Arsenal", 10)
    c.drawCentredString(W / 2, y, f"MOON CYCLE  ·  {month_name.upper()} MONTH")
    y -= 38

    c.setFillColor(ink)
    c.setFont("Italiana", 28)
    c.drawCentredString(W / 2, y, title)
    y -= 20

    if is_dark:
        dark_rule(c, y)
    else:
        gold_rule(c, y, diamond=True)
    y -= 30

    content_map = {
        "intentions": [
            ("MY NEW MOON DESIRE FOR THIS CYCLE",
             "What am I calling in during this lunar month?", 5),
            ("RITUAL I WILL PERFORM AT NEW MOON",
             "How will I mark this sacred threshold?", 4),
            ("WHAT I AM PLANTING",
             "Seeds I am consciously sowing in this cycle:", 4),
        ],
        "action": [
            ("INSPIRED ACTIONS I’M TAKING",
             "Concrete steps I’m taking toward my desire this week:", 6),
            ("WHAT THE UNIVERSE IS SHOWING ME",
             "Signs and signals appearing in my waxing energy:", 5),
            ("MOMENTUM NOTES",
             "How does my desire feel as it builds toward the full moon?", 4),
        ],
        "release": [
            ("WHAT I AM RELEASING AT THE FULL MOON",
             "Beliefs, habits, or energy patterns I am consciously letting go:", 5),
            ("WHAT I AM CELEBRATING",
             "Evidence, growth, and wins from this lunar cycle:", 5),
            ("MY FULL MOON GRATITUDE",
             "What the full moon illuminates in my heart:", 4),
        ],
        "integrate": [
            ("WHAT I AM INTEGRATING",
             "Lessons and gifts from this completed lunar cycle:", 5),
            ("HOW I HAVE GROWN",
             "Who I am now that I wasn’t at the new moon:", 4),
            ("PREPARING FOR THE NEXT CYCLE",
             "What I want to carry forward into the next new moon:", 4),
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
    "Overflow — Extra Writing Space",
    "Portal Notes",
    "Affirmation Playground",
    "Dream Journal",
    "Letters to the Universe",
    "Quantum Leap Visualization",
    "My Highest Self Speaks",
    "Completion — Final Reflection",
]

BONUS_PROMPTS = [
    "Use this page for any writing that overflows from your daily practice.",
    "Notes, insights, downloads, and ideas captured from your portal practice.",
    "Write affirmations in every direction — fill the page with I AM statements.",
    "Record your dreams, symbols, and nighttime downloads from the universe.",
    "Write a letter to the universe, your future self, or your desire itself.",
    "Describe in vivid sensory detail the day your desire has fully manifested.",
    "What does your highest self want you to know right now?",
    "You have completed 28 days. Who are you now? What has changed forever?",
]


def build_bonus_page(c, idx, pn):
    cream_bg(c)
    corner_marks(c)
    flower_of_life(c, W / 2, H * 0.50, 26, rings=2, color=GOLD, alpha=0.09)

    y = H - M - 22
    c.setFillColor(GOLD)
    c.setFont("Arsenal", 10)
    c.drawCentredString(W / 2, y, "EXTRA SPACE")
    y -= 36

    c.setFillColor(INK)
    c.setFont("Italiana", 26)
    c.drawCentredString(W / 2, y, BONUS_TITLES[idx])
    y -= 20

    gold_rule(c, y, diamond=True)
    y -= 24

    c.setFont("CrimsonItal", 13)
    c.setFillColor(INK)
    c.drawCentredString(W / 2, y, BONUS_PROMPTS[idx])
    y -= 38

    n_lines = 18
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
    c.drawCentredString(W / 2, y, "✶   Y O U   D I D   I T   ✶")

    y = H * 0.50 + 100
    c.setFillColor(WTEXT)
    c.setFont("Italiana", 42)
    c.drawCentredString(W / 2, y, "The Portal is Open.")
    y -= 18

    dark_rule(c, y)
    y -= 36

    c.setFont("CrimsonPro", 14)
    lines_closing = [
        "Twenty-eight days of sacred commitment.",
        "Five hundred and four repetitions of your desire.",
        "Each one a thread woven into the fabric of what is becoming real.",
        "",
        "You did not just write in a journal.",
        "You rewired your subconscious, raised your vibration,",
        "and sent a signal so clear the universe could not ignore it.",
        "",
        "The portal is not behind you. It is beneath your feet.",
        "Keep walking through it.",
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
    c.drawCentredString(W / 2, y, "3 · 6 · 9  ·  I WROTE IT  ·  I BELIEVED IT  ·  I RECEIVED IT")

    footer(c, pn, dark=True)


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN BUILD
# ══════════════════════════════════════════════════════════════════════════════

def main():
    setup_fonts()

    out_path = os.path.join(HERE, "369-portal-FINAL.pdf")
    c = rlc.Canvas(out_path, pagesize=letter)

    pn = 1  # running page counter

    # ── Front matter (pages 1-8) ─────────────────────────────────────────────
    build_cover(c);           c.showPage(); pn += 1   # 1
    build_title_page(c, pn);  c.showPage(); pn += 1   # 2
    build_welcome(c, pn);     c.showPage(); pn += 1   # 3
    build_method(c, pn);      c.showPage(); pn += 1   # 4
    build_how_to_use(c, pn);  c.showPage(); pn += 1   # 5
    build_portal_intention(c, pn); c.showPage(); pn += 1  # 6
    build_commitments(c, pn); c.showPage(); pn += 1   # 7
    build_moon_overview(c, pn); c.showPage(); pn += 1 # 8

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

    # ── Closing (page 121) ───────────────────────────────────────────────────
    build_closing(c, pn)
    c.showPage()

    c.save()
    print(f"Saved {out_path}  ({pn} pages)")
    return out_path


if __name__ == "__main__":
    main()
