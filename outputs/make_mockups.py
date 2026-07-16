#!/usr/bin/env python3
"""
Create 15 Etsy listing mockup images for 369 Portal Manifestation Journal.
Output: outputs/etsy-mockups/  (JPG, 2000×2000 or 2000×1500)
"""

import os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE     = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/mnt/skills/examples/canvas-design/canvas-fonts"
MOCK_DIR = os.path.join(HERE, "etsy-mockups")
os.makedirs(MOCK_DIR, exist_ok=True)

# ── Brand palette (RGB) ────────────────────────────────────────────────────────
DARKBG = (18,  14,  11)
CREAM  = (250, 246, 240)
GOLD   = (201, 168, 76)
LGOLD  = (224, 192, 96)
DGOLD  = (160, 128, 52)
INK    = (26,  20,  16)
WTEXT  = (237, 229, 204)
LINEC  = (74,  63,  52)
WHITE  = (255, 255, 255)
BGRAY  = (38,  32,  28)   # slightly lighter dark for panels

SQ = 2000   # square canvas
LS = (2000, 1500)  # landscape canvas

# ── Font loader ────────────────────────────────────────────────────────────────
_font_cache = {}
def F(name, size):
    key = (name, size)
    if key not in _font_cache:
        try:
            _font_cache[key] = ImageFont.truetype(os.path.join(FONT_DIR, name), size)
        except Exception:
            _font_cache[key] = ImageFont.load_default()
    return _font_cache[key]

IT  = "Italiana-Regular.ttf"
AR  = "ArsenalSC-Regular.ttf"
CR  = "CrimsonPro-Regular.ttf"
CI  = "CrimsonPro-Italic.ttf"
JU  = "Jura-Light.ttf"

# ── Page image loader ──────────────────────────────────────────────────────────
_page_cache = {}
def P(page_num):
    if page_num not in _page_cache:
        path = os.path.join(HERE, f"preview-page{page_num:03d}-{page_num:03d}.png")
        _page_cache[page_num] = Image.open(path).convert("RGB")
    return _page_cache[page_num]

# ── Drawing helpers ────────────────────────────────────────────────────────────

def canvas(size=SQ, bg=DARKBG):
    if isinstance(size, int):
        size = (size, size)
    return Image.new("RGB", size, bg)

def centred_text(draw, text, y, font, fill, img_w=SQ):
    bbox = draw.textbbox((0, 0), text, font=font)
    x = (img_w - (bbox[2] - bbox[0])) // 2
    draw.text((x, y), text, font=font, fill=fill)
    return bbox[3] - bbox[1]  # return line height

def paste_page(img, page_img, x, y, w, h, border_color=None, shadow=True):
    """Resize page and paste with drop-shadow."""
    page_r = page_img.resize((w, h), Image.LANCZOS)
    if shadow:
        sh_size = (w + 40, h + 40)
        sh = Image.new("RGBA", sh_size, (0, 0, 0, 0))
        shd = ImageDraw.Draw(sh)
        shd.rectangle([12, 12, w + 12, h + 12], fill=(0, 0, 0, 140))
        sh = sh.filter(ImageFilter.GaussianBlur(14))
        img.paste(sh.convert("RGB"), (x - 16, y - 8), sh.split()[3])
    if border_color:
        border = Image.new("RGB", (w + 4, h + 4), border_color)
        border.paste(page_r, (2, 2))
        img.paste(border, (x - 2, y - 2))
    else:
        img.paste(page_r, (x, y))

def gold_rule(draw, y, x0, x1, w=2):
    draw.line([(x0, y), (x1, y)], fill=GOLD, width=w)
    draw.line([(x0 + 20, y + 5), (x1 - 20, y + 5)], fill=GOLD, width=1)

def badge_box(draw, x, y, w, h, text1, text2, text3=None, img_w=None):
    """Gold-bordered badge with 2-3 lines of text."""
    r = 14
    draw.rounded_rectangle([x, y, x + w, y + h], radius=r,
                            outline=GOLD, width=2, fill=BGRAY)
    ty = y + 18
    draw.text((x + w//2, ty), text1,
              font=F(AR, 38), fill=LGOLD,
              anchor="mt")
    draw.text((x + w//2, ty + 52), text2,
              font=F(IT, 30), fill=WTEXT,
              anchor="mt")
    if text3:
        draw.text((x + w//2, ty + 90), text3,
                  font=F(CI, 26), fill=GOLD,
                  anchor="mt")

def save(img, name, quality=93):
    path = os.path.join(MOCK_DIR, name)
    img.save(path, "JPEG", quality=quality)
    kb = os.path.getsize(path) // 1024
    print(f"  {name}  ({kb} KB)")
    return path

# ══════════════════════════════════════════════════════════════════════════════
# IMAGE 00 — THUMBNAIL (show-stopper 2000×2000)
# ══════════════════════════════════════════════════════════════════════════════
def make_thumbnail():
    img = canvas(SQ, DARKBG)
    draw = ImageDraw.Draw(img)

    # Subtle radial gold rings
    cx, cy = SQ//2, SQ//2
    for r in range(300, 1100, 70):
        alpha = max(8, 20 - r // 55)
        c = tuple(max(0, min(255, int(DARKBG[i] + alpha))) for i in range(3))
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=c, width=1)

    # ── Top text block ────────────────────────────────────────────────────────
    draw.line([(100, 90), (SQ-100, 90)], fill=GOLD, width=3)
    draw.line([(140, 100), (SQ-140, 100)], fill=DGOLD, width=1)

    draw.text((SQ//2, 122), "∙  ∙  ∙   A  S A C R E D  P R A C T I C E   ∙  ∙  ∙",
              font=F(AR, 34), fill=LGOLD, anchor="mt")

    draw.text((SQ//2, 168), "THE PORTAL",
              font=F(IT, 210), fill=WTEXT, anchor="mt")

    draw.text((SQ//2, 390), "3  ·  6  ·  9   Manifestation Journal",
              font=F(IT, 70), fill=LGOLD, anchor="mt")

    draw.line([(200, 480), (SQ-200, 480)], fill=GOLD, width=2)

    # ── 6-page grid ──────────────────────────────────────────────────────────
    show_pages = [1, 3, 9, 10, 8, 121]
    pw, ph = 520, int(520 * 11 / 8.5)   # ≈ 520 × 674
    cols, rows = 3, 2
    gap = 28
    total_w = cols * pw + (cols - 1) * gap
    total_h = rows * ph + (rows - 1) * gap
    gx0 = (SQ - total_w) // 2
    gy0 = 510

    for i, pn in enumerate(show_pages):
        col = i % cols
        row = i // cols
        x = gx0 + col * (pw + gap)
        y = gy0 + row * (ph + gap)
        paste_page(img, P(pn), x, y, pw, ph, border_color=GOLD, shadow=True)

    # ── Bottom badge strip ────────────────────────────────────────────────────
    strip_y = gy0 + total_h + 48
    draw.line([(100, strip_y - 10), (SQ-100, strip_y - 10)], fill=GOLD, width=2)

    badges = [
        ("PRINTABLE PDF",    "Print at home"),
        ("DIGITAL FILLABLE", "Type on any device"),
        ("TABLET NAVIGATION", "iPad & any PDF app"),
    ]
    bw, bh = 560, 115
    bx_starts = [70, (SQ - bw) // 2, SQ - 70 - bw]
    for (t1, t2), bx in zip(badges, bx_starts):
        draw.rounded_rectangle([bx, strip_y, bx+bw, strip_y+bh],
                               radius=12, outline=GOLD, width=2, fill=BGRAY)
        draw.text((bx + bw//2, strip_y + 14), t1, font=F(AR, 38),
                  fill=LGOLD, anchor="mt")
        draw.text((bx + bw//2, strip_y + 62), t2, font=F(CI, 30),
                  fill=WTEXT, anchor="mt")

    # Bottom bar
    footer_y = strip_y + bh + 30
    draw.line([(100, footer_y), (SQ-100, footer_y)], fill=GOLD, width=1)
    draw.text((SQ//2, footer_y + 14),
              "121 PAGES  ·  28 DAYS  ·  4 FILE FORMATS  ·  INSTANT DOWNLOAD",
              font=F(AR, 30), fill=DGOLD, anchor="mt")

    save(img, "00-THUMBNAIL.jpg")


# ══════════════════════════════════════════════════════════════════════════════
# IMAGE 01 — What's In the Bundle (3 formats side by side)
# ══════════════════════════════════════════════════════════════════════════════
def make_bundle_overview():
    img = canvas(SQ, DARKBG)
    draw = ImageDraw.Draw(img)

    draw.line([(100, 80), (SQ-100, 80)], fill=GOLD, width=2)
    draw.text((SQ//2, 106), "WHAT YOU GET — THREE COMPLETE FILES",
              font=F(AR, 44), fill=LGOLD, anchor="mt")
    draw.line([(100, 168), (SQ-100, 168)], fill=GOLD, width=2)

    # 3 columns
    cols_data = [
        (1,   "01  PRINTABLE PDF",   "369-portal-FINAL.pdf",
               "Print at home on any\nstandard printer.\n8.5×11 Letter size.\nBlack & white friendly."),
        (9,   "02  DIGITAL FILLABLE", "369-portal-DIGITAL-FILLABLE.pdf",
               "Type directly into\nevery field.\nWorks in Adobe Reader,\nbrowser, iPhone & Android."),
        (97,  "03  TABLET NAVIGATION", "369-portal-TABLET-NAVIGATION.pdf",
               "Clickable navigation\noutline panel.\nPerfect for iPad,\nGoodNotes & Notability."),
    ]

    pw, ph = 480, int(480 * 11 / 8.5)
    col_w = (SQ - 160) // 3
    y_page = 210

    for i, (pn, label, fname, desc) in enumerate(cols_data):
        cx = 80 + i * col_w + col_w // 2
        x_page = cx - pw // 2

        paste_page(img, P(pn), x_page, y_page, pw, ph,
                   border_color=GOLD, shadow=True)

        ty = y_page + ph + 36
        draw.text((cx, ty), label, font=F(AR, 36), fill=LGOLD, anchor="mt")
        ty += 54

        for line in desc.split("\n"):
            draw.text((cx, ty), line, font=F(CR, 28), fill=WTEXT, anchor="mt")
            ty += 40

    draw.line([(100, SQ-100), (SQ-100, SQ-100)], fill=GOLD, width=2)
    draw.text((SQ//2, SQ - 80),
              "ALL THREE FILES INCLUDED IN ONE DOWNLOAD",
              font=F(AR, 36), fill=GOLD, anchor="mt")

    save(img, "01-bundle-three-formats.jpg")


# ══════════════════════════════════════════════════════════════════════════════
# IMAGE 02 — Cover page full bleed
# ══════════════════════════════════════════════════════════════════════════════
def make_cover_full():
    # Just the cover page enlarged with a thin gold mat
    cover = P(1).resize((1700, int(1700 * 11/8.5)), Image.LANCZOS)
    cw, ch = cover.size
    img = canvas(SQ, DARKBG)
    x = (SQ - cw) // 2
    y = (SQ - ch) // 2
    paste_page(img, P(1), x, y, cw, ch, border_color=GOLD, shadow=True)
    save(img, "02-cover-page.jpg")


# ══════════════════════════════════════════════════════════════════════════════
# IMAGE 03 — Daily Practice spread (Morning + Evening side by side)
# ══════════════════════════════════════════════════════════════════════════════
def make_daily_spread():
    img = canvas(SQ, CREAM)
    draw = ImageDraw.Draw(img)

    # Cream background header
    draw.rectangle([0, 0, SQ, 160], fill=INK)
    draw.text((SQ//2, 20), "THE DAILY PRACTICE",
              font=F(AR, 56), fill=LGOLD, anchor="mt")
    draw.text((SQ//2, 92), "Morning · Midday · Evening — every single day for 28 days",
              font=F(CI, 34), fill=WTEXT, anchor="mt")

    pw, ph = 880, int(880 * 11/8.5)
    gap = 40
    y = 185
    x1 = (SQ // 2) - pw - gap // 2
    x2 = (SQ // 2) + gap // 2

    paste_page(img, P(9),  x1, y, pw, ph, border_color=DGOLD, shadow=True)
    paste_page(img, P(10), x2, y, pw, ph, border_color=DGOLD, shadow=True)

    # Labels below pages
    ty = y + ph + 24
    draw.text((x1 + pw//2, ty), "MORNING & MIDDAY PAGE",
              font=F(AR, 32), fill=INK, anchor="mt")
    draw.text((x1 + pw//2, ty + 44), "Write 3 times at dawn · 6 times at noon",
              font=F(CI, 28), fill=LINEC, anchor="mt")
    draw.text((x2 + pw//2, ty), "EVENING PAGE",
              font=F(AR, 32), fill=INK, anchor="mt")
    draw.text((x2 + pw//2, ty + 44), "Write 9 times · Reflect · Release",
              font=F(CI, 28), fill=LINEC, anchor="mt")

    save(img, "03-daily-practice-spread.jpg")


# ══════════════════════════════════════════════════════════════════════════════
# IMAGE 04 — 121 pages breakdown (4-page preview grid)
# ══════════════════════════════════════════════════════════════════════════════
def make_pages_overview():
    img = canvas(SQ, DARKBG)
    draw = ImageDraw.Draw(img)

    draw.line([(100, 70), (SQ-100, 70)], fill=GOLD, width=2)
    draw.text((SQ//2, 96), "121 PAGES OF SACRED PRACTICE",
              font=F(IT, 76), fill=WTEXT, anchor="mt")
    draw.line([(100, 192), (SQ-100, 192)], fill=GOLD, width=1)

    # 4×2 grid of pages
    show = [1, 3, 9, 10, 73, 97, 113, 121]
    labels = ["Cover", "Welcome", "Day Morning", "Day Evening",
              "Shadow Work", "Moon Calendar", "Bonus Pages", "Closing"]
    pw, ph = 420, int(420 * 11/8.5)
    cols, rows = 4, 2
    gap = 22
    total_w = cols * pw + (cols-1) * gap
    gx0 = (SQ - total_w) // 2
    gy0 = 218

    for i, (pn, lbl) in enumerate(zip(show, labels)):
        col = i % cols
        row = i // cols
        x = gx0 + col * (pw + gap)
        y = gy0 + row * (ph + gap + 50)
        paste_page(img, P(pn), x, y, pw, ph, border_color=GOLD, shadow=True)
        draw.text((x + pw//2, y + ph + 8), lbl,
                  font=F(AR, 26), fill=LGOLD, anchor="mt")

    # Stats bar
    sy = gy0 + 2*(ph+50+gap) + 10
    draw.line([(100, sy), (SQ-100, sy)], fill=GOLD, width=1)
    stats = [
        ("28", "DAYS"), ("56", "DAILY PAGES"), ("8", "SHADOW WORK"),
        ("16", "SYNC LOG PAGES"), ("16", "MOON CALENDAR"), ("8", "BONUS PAGES"),
    ]
    sw = (SQ - 160) // len(stats)
    for i, (num, lbl) in enumerate(stats):
        sx = 80 + i * sw + sw // 2
        draw.text((sx, sy + 20), num, font=F(IT, 64), fill=LGOLD, anchor="mt")
        draw.text((sx, sy + 94), lbl, font=F(AR, 22), fill=WTEXT, anchor="mt")

    save(img, "04-121-pages-overview.jpg")


# ══════════════════════════════════════════════════════════════════════════════
# IMAGE 05 — 369 Method explanation page
# ══════════════════════════════════════════════════════════════════════════════
def make_method_page():
    pw, ph = 1500, int(1500 * 11/8.5)
    img = canvas(SQ, CREAM)
    draw = ImageDraw.Draw(img)
    x = (SQ - pw) // 2
    y = (SQ - ph) // 2
    paste_page(img, P(4), x, y, pw, ph, border_color=GOLD, shadow=True)
    # Header bar
    draw.rectangle([0, 0, SQ, 80], fill=INK)
    draw.text((SQ//2, 10), "THE 369 METHOD — NIKOLA TESLA'S SACRED CODE",
              font=F(AR, 40), fill=LGOLD, anchor="mt")
    save(img, "05-method-page.jpg")


# ══════════════════════════════════════════════════════════════════════════════
# IMAGE 06 — Shadow Work (2 pages side by side)
# ══════════════════════════════════════════════════════════════════════════════
def make_shadow_work():
    img = canvas(SQ, CREAM)
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, SQ, 150], fill=INK)
    draw.text((SQ//2, 18), "SHADOW WORK",
              font=F(IT, 80), fill=LGOLD, anchor="mt")
    draw.text((SQ//2, 106), "8 deep transformation prompts to clear what's blocking you",
              font=F(CI, 34), fill=WTEXT, anchor="mt")

    pw, ph = 880, int(880 * 11/8.5)
    gap = 40
    y = 175
    x1 = (SQ // 2) - pw - gap // 2
    x2 = (SQ // 2) + gap // 2

    paste_page(img, P(73), x1, y, pw, ph, border_color=DGOLD, shadow=True)
    paste_page(img, P(90), x2, y, pw, ph, border_color=DGOLD, shadow=True)

    save(img, "06-shadow-work.jpg")


# ══════════════════════════════════════════════════════════════════════════════
# IMAGE 07 — Moon Calendar (dark full-bleed)
# ══════════════════════════════════════════════════════════════════════════════
def make_moon_calendar():
    pw, ph = 1500, int(1500 * 11/8.5)
    img = canvas(SQ, DARKBG)
    draw = ImageDraw.Draw(img)
    x = (SQ - pw) // 2
    y = (SQ - ph) // 2
    paste_page(img, P(97), x, y, pw, ph, border_color=LGOLD, shadow=True)
    # Footer strip
    draw.rectangle([0, SQ-90, SQ, SQ], fill=DARKBG)
    draw.line([(100, SQ-88), (SQ-100, SQ-88)], fill=GOLD, width=1)
    draw.text((SQ//2, SQ-72),
              "MOON CALENDAR — 4 LUNAR CYCLES · INTENTIONS · RELEASE · INTEGRATION",
              font=F(AR, 30), fill=LGOLD, anchor="mt")
    save(img, "07-moon-calendar.jpg")


# ══════════════════════════════════════════════════════════════════════════════
# IMAGE 08 — Moon Phase Guide (dark page 8)
# ══════════════════════════════════════════════════════════════════════════════
def make_moon_phase_guide():
    pw, ph = 1500, int(1500 * 11/8.5)
    img = canvas(SQ, DARKBG)
    draw = ImageDraw.Draw(img)
    x = (SQ - pw) // 2
    y = (SQ - ph) // 2
    paste_page(img, P(8), x, y, pw, ph, border_color=LGOLD, shadow=True)
    draw.rectangle([0, SQ-90, SQ, SQ], fill=DARKBG)
    draw.line([(100, SQ-88), (SQ-100, SQ-88)], fill=GOLD, width=1)
    draw.text((SQ//2, SQ-72),
              "MOON PHASE GUIDE — ALIGN YOUR PRACTICE WITH THE LUNAR CYCLE",
              font=F(AR, 30), fill=LGOLD, anchor="mt")
    save(img, "08-moon-phase-guide.jpg")


# ══════════════════════════════════════════════════════════════════════════════
# IMAGE 09 — Synchronicity Log
# ══════════════════════════════════════════════════════════════════════════════
def make_sync_log():
    img = canvas(SQ, CREAM)
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, SQ, 150], fill=INK)
    draw.text((SQ//2, 18), "SYNCHRONICITY LOG",
              font=F(IT, 80), fill=LGOLD, anchor="mt")
    draw.text((SQ//2, 106), "16 pages to record signs, alignments & evidence from the universe",
              font=F(CI, 34), fill=WTEXT, anchor="mt")

    pw, ph = 880, int(880 * 11/8.5)
    gap = 40
    y = 175
    x1 = (SQ//2) - pw - gap//2
    x2 = (SQ//2) + gap//2

    paste_page(img, P(81), x1, y, pw, ph, border_color=DGOLD, shadow=True)
    paste_page(img, P(110), x2, y, pw, ph, border_color=DGOLD, shadow=True)

    save(img, "09-synchronicity-log.jpg")


# ══════════════════════════════════════════════════════════════════════════════
# IMAGE 10 — Weekly Review
# ══════════════════════════════════════════════════════════════════════════════
def make_weekly_review():
    pw, ph = 1500, int(1500 * 11/8.5)
    img = canvas(SQ, CREAM)
    draw = ImageDraw.Draw(img)
    x = (SQ - pw) // 2
    y = (SQ - ph) // 2
    paste_page(img, P(65), x, y, pw, ph, border_color=GOLD, shadow=True)
    draw.rectangle([0, 0, SQ, 80], fill=INK)
    draw.text((SQ//2, 10),
              "WEEKLY REVIEWS — 4 PAGES TO TRACK YOUR EVIDENCE & SHIFTS",
              font=F(AR, 38), fill=LGOLD, anchor="mt")
    save(img, "10-weekly-review.jpg")


# ══════════════════════════════════════════════════════════════════════════════
# IMAGE 11 — Bonus Pages spread
# ══════════════════════════════════════════════════════════════════════════════
def make_bonus_pages():
    img = canvas(SQ, CREAM)
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, SQ, 150], fill=INK)
    draw.text((SQ//2, 18), "BONUS PAGES",
              font=F(IT, 80), fill=LGOLD, anchor="mt")
    draw.text((SQ//2, 106),
              "Dream Journal · Letters to the Universe · Overflow · Visualization & more",
              font=F(CI, 30), fill=WTEXT, anchor="mt")

    pw, ph = 880, int(880 * 11/8.5)
    gap = 40
    y = 175
    x1 = (SQ//2) - pw - gap//2
    x2 = (SQ//2) + gap//2

    paste_page(img, P(113), x1, y, pw, ph, border_color=DGOLD, shadow=True)
    paste_page(img, P(50),  x2, y, pw, ph, border_color=DGOLD, shadow=True)

    save(img, "11-bonus-pages.jpg")


# ══════════════════════════════════════════════════════════════════════════════
# IMAGE 12 — Closing page (dark, full bleed)
# ══════════════════════════════════════════════════════════════════════════════
def make_closing():
    pw, ph = 1500, int(1500 * 11/8.5)
    img = canvas(SQ, DARKBG)
    draw = ImageDraw.Draw(img)
    x = (SQ - pw) // 2
    y = (SQ - ph) // 2
    paste_page(img, P(121), x, y, pw, ph, border_color=LGOLD, shadow=True)
    draw.rectangle([0, SQ-90, SQ, SQ], fill=DARKBG)
    draw.line([(100, SQ-88), (SQ-100, SQ-88)], fill=GOLD, width=1)
    draw.text((SQ//2, SQ-72),
              "THE PORTAL IS OPEN  ·  PAGE 121",
              font=F(AR, 34), fill=LGOLD, anchor="mt")
    save(img, "12-closing-page.jpg")


# ══════════════════════════════════════════════════════════════════════════════
# IMAGE 13 — iPad / GoodNotes mockup
# ══════════════════════════════════════════════════════════════════════════════
def make_ipad_mockup():
    img = canvas(SQ, DARKBG)
    draw = ImageDraw.Draw(img)

    # Subtle bg circles
    for r in range(200, 900, 60):
        c = tuple(max(0, int(DARKBG[i] + 12)) for i in range(3))
        draw.ellipse([SQ//2-r, SQ//2-r, SQ//2+r, SQ//2+r], outline=c, width=1)

    draw.text((SQ//2, 60), "TABLET NAVIGATION EDITION",
              font=F(AR, 46), fill=LGOLD, anchor="mt")
    draw.text((SQ//2, 120), "Full clickable outline · Jump to any section · Any PDF app on any device",
              font=F(CI, 34), fill=WTEXT, anchor="mt")

    # iPad frame (silver)
    ipad_w, ipad_h = 980, 1320
    ipad_x = (SQ - ipad_w) // 2
    ipad_y = 190

    # Outer bezel
    draw.rounded_rectangle([ipad_x, ipad_y, ipad_x+ipad_w, ipad_y+ipad_h],
                           radius=54, fill=(52, 48, 44), outline=(90, 82, 70), width=3)
    # Screen area
    sx, sy = ipad_x + 26, ipad_y + 26
    sw, sh = ipad_w - 52, ipad_h - 52
    draw.rounded_rectangle([sx, sy, sx+sw, sy+sh], radius=12, fill=WHITE)

    # Page inside screen — evening page
    page_margin = 10
    paste_page(img, P(20), sx + page_margin, sy + page_margin,
               sw - 2*page_margin, sh - 2*page_margin, shadow=False)

    # Home bar
    bar_y = ipad_y + ipad_h - 24
    draw.rounded_rectangle([ipad_x + ipad_w//2 - 60, bar_y,
                            ipad_x + ipad_w//2 + 60, bar_y + 8],
                           radius=4, fill=(90, 82, 70))

    # Small overlay callout
    draw.rounded_rectangle([ipad_x + ipad_w + 30, ipad_y + 200,
                            ipad_x + ipad_w + 480, ipad_y + 480],
                           radius=16, fill=BGRAY, outline=GOLD, width=2)
    draw.text((ipad_x + ipad_w + 256, ipad_y + 220), "OUTLINE",
              font=F(AR, 34), fill=LGOLD, anchor="mt")
    draw.text((ipad_x + ipad_w + 256, ipad_y + 268), "NAVIGATION",
              font=F(AR, 34), fill=LGOLD, anchor="mt")
    for line, dy in [("Cover", 318), ("Daily Practice", 356), ("Week 1", 394),
                     ("Shadow Work", 432)]:
        draw.text((ipad_x + ipad_w + 256, ipad_y + dy), f"› {line}",
                  font=F(CR, 26), fill=WTEXT, anchor="mt")

    draw.line([(100, SQ-90), (SQ-100, SQ-90)], fill=GOLD, width=1)
    draw.text((SQ//2, SQ-70),
              "GOODNOTES · NOTABILITY · SAMSUNG NOTES · ANY PDF APP WITH STYLUS",
              font=F(AR, 28), fill=GOLD, anchor="mt")

    save(img, "13-ipad-tablet-nav-mockup.jpg")


# ══════════════════════════════════════════════════════════════════════════════
# IMAGE 14 — Digital fillable demo (laptop-style)
# ══════════════════════════════════════════════════════════════════════════════
def make_laptop_mockup():
    img = canvas(SQ, DARKBG)
    draw = ImageDraw.Draw(img)

    draw.text((SQ//2, 50), "TYPE DIRECTLY INTO EVERY FIELD",
              font=F(AR, 50), fill=LGOLD, anchor="mt")
    draw.text((SQ//2, 114), "Works in Adobe Reader · Chrome · Safari · iPhone · Android — no app needed",
              font=F(CI, 30), fill=WTEXT, anchor="mt")

    # Laptop body
    lw, lh = 1500, 960
    lx = (SQ - lw) // 2
    ly = 180

    # Lid
    draw.rounded_rectangle([lx, ly, lx+lw, ly+lh], radius=18,
                           fill=(36, 32, 28), outline=(70, 62, 54), width=3)
    # Screen bezel (inner)
    bx, by = lx + 30, ly + 30
    bw, bh = lw - 60, lh - 60
    draw.rounded_rectangle([bx, by, bx+bw, by+bh], radius=10, fill=(20, 16, 13))

    # Page on screen
    paste_page(img, P(9), bx + 8, by + 8, bw - 16, bh - 16, shadow=False)

    # Keyboard base
    kx, ky = lx - 40, ly + lh
    kw, kh = lw + 80, 80
    draw.rounded_rectangle([kx, ky, kx+kw, ky+kh], radius=10,
                           fill=(42, 38, 34), outline=(70, 62, 54), width=2)
    # Trackpad
    tp_w = 280
    draw.rounded_rectangle([kx + kw//2 - tp_w//2, ky+12,
                            kx + kw//2 + tp_w//2, ky+kh-12],
                           radius=6, fill=(52, 48, 44), outline=(80, 72, 62), width=1)

    # Callout bubbles
    cbs = [
        (lx - 420, ly + 140, "1,553", "Typeable Fields"),
        (lx - 420, ly + 320, "ZERO", "Software Needed"),
        (lx - 420, ly + 500, "ALL", "Devices Supported"),
    ]
    for cx2, cy2, n, lbl in cbs:
        draw.rounded_rectangle([cx2, cy2, cx2+360, cy2+130],
                               radius=12, fill=BGRAY, outline=GOLD, width=2)
        draw.text((cx2+180, cy2+10), n, font=F(IT, 56), fill=LGOLD, anchor="mt")
        draw.text((cx2+180, cy2+76), lbl, font=F(AR, 28), fill=WTEXT, anchor="mt")

    draw.line([(100, SQ-90), (SQ-100, SQ-90)], fill=GOLD, width=1)
    draw.text((SQ//2, SQ-70),
              "DIGITAL FILLABLE PDF — INSTANT DOWNLOAD · TYPE & SAVE · PRINT ANYTIME",
              font=F(AR, 28), fill=GOLD, anchor="mt")

    save(img, "14-digital-fillable-demo.jpg")


# ══════════════════════════════════════════════════════════════════════════════
# IMAGE 15 — Features at a glance (infographic)
# ══════════════════════════════════════════════════════════════════════════════
def make_features():
    img = canvas(SQ, DARKBG)
    draw = ImageDraw.Draw(img)

    draw.line([(100, 72), (SQ-100, 72)], fill=GOLD, width=2)
    draw.text((SQ//2, 96), "EVERYTHING INSIDE THE PORTAL",
              font=F(IT, 82), fill=WTEXT, anchor="mt")
    draw.line([(100, 204), (SQ-100, 204)], fill=GOLD, width=1)

    features = [
        ("◆  28 DAYS of morning, midday & evening writing",         "3 + 6 + 9 repetitions = 504 total per portal"),
        ("◆  DAILY ENERGY BARS",                                    "Shade your vibration level 1-10 morning & evening"),
        ("◆  GRATITUDE SEEDS",                                      "Capture daily moments of alignment and thanks"),
        ("◆  SYNCHRONICITY LOG",                                    "16 pages — record signs & evidence from the universe"),
        ("◆  4 WEEKLY REVIEWS",                                     "Track belief shifts, evidence & energy patterns"),
        ("◆  MONTHLY REVIEW",                                       "4-page deep reflection on your 28-day portal"),
        ("◆  8 SHADOW WORK PAGES",                                  "Release blocks, ancestral patterns & limiting beliefs"),
        ("◆  MOON CALENDAR",                                        "4 lunar cycles — new, waxing, full & waning moon pages"),
        ("◆  8 BONUS PAGES",                                        "Overflow, dream journal, visualization & more"),
        ("◆  SACRED GEOMETRY",                                      "Flower of Life woven throughout for high-vibe energy"),
        ("◆  FLOWER OF LIFE COVER",                                 "Luxe dark design with gold accents — premium feel"),
        ("◆  INSTANT DIGITAL DOWNLOAD",                             "4 files: printable, fillable, tablet nav & A4 edition"),
    ]

    y = 230
    col_w = (SQ - 200) // 2
    for i, (title, desc) in enumerate(features):
        col = i % 2
        row = i // 2
        x = 100 + col * col_w
        ry = y + row * 148

        if row % 2 == 0 and col == 0:
            draw.rectangle([98, ry - 8, SQ - 98, ry + 132], fill=BGRAY)

        draw.text((x + 10, ry), title, font=F(AR, 30), fill=LGOLD)
        draw.text((x + 10, ry + 46), desc, font=F(CI, 28), fill=WTEXT)
        draw.line([(x + 10, ry + 90), (x + col_w - 30, ry + 90)],
                  fill=DGOLD, width=1)

    draw.line([(100, SQ-90), (SQ-100, SQ-90)], fill=GOLD, width=2)
    draw.text((SQ//2, SQ-70),
              "THE PORTAL  ·  369 MANIFESTATION JOURNAL  ·  121 PAGES",
              font=F(AR, 34), fill=LGOLD, anchor="mt")

    save(img, "15-features-at-a-glance.jpg")


# ══════════════════════════════════════════════════════════════════════════════
# IMAGE 16 — Welcome + Method pages (dark pair)
# ══════════════════════════════════════════════════════════════════════════════
def make_welcome_pair():
    img = canvas(SQ, DARKBG)
    draw = ImageDraw.Draw(img)

    draw.text((SQ//2, 40), "STEP THROUGH THE PORTAL",
              font=F(IT, 80), fill=WTEXT, anchor="mt")
    draw.line([(100, 148), (SQ-100, 148)], fill=GOLD, width=1)

    pw, ph = 880, int(880 * 11/8.5)
    gap = 40
    y = 176
    x1 = (SQ//2) - pw - gap//2
    x2 = (SQ//2) + gap//2

    paste_page(img, P(3), x1, y, pw, ph, border_color=LGOLD, shadow=True)
    paste_page(img, P(4), x2, y, pw, ph, border_color=DGOLD, shadow=True)

    ty = y + ph + 24
    draw.text((x1 + pw//2, ty), "WELCOME", font=F(AR, 34), fill=LGOLD, anchor="mt")
    draw.text((x2 + pw//2, ty), "THE 369 METHOD", font=F(AR, 34), fill=LGOLD, anchor="mt")

    save(img, "16-welcome-method.jpg")


# ══════════════════════════════════════════════════════════════════════════════
# IMAGE 17 — Typing demo: fillable PDF with text visible in fields
# ══════════════════════════════════════════════════════════════════════════════
def make_typing_demo():
    img = canvas(SQ, DARKBG)
    draw = ImageDraw.Draw(img)

    # Header
    draw.line([(80, 68), (SQ-80, 68)], fill=GOLD, width=2)
    draw.text((SQ//2, 92), "TYPE YOUR INTENTIONS DIRECTLY IN THE PDF",
              font=F(AR, 44), fill=LGOLD, anchor="mt")
    draw.text((SQ//2, 152), "No printing. No pen. Just open in your browser or any free PDF app.",
              font=F(CI, 32), fill=WTEXT, anchor="mt")
    draw.line([(80, 204), (SQ-80, 204)], fill=GOLD, width=1)

    # Page preview: morning page (page 9)
    pw, ph = 1020, int(1020 * 11/8.5)
    px = (SQ - pw) // 2 + 200
    py = 224
    paste_page(img, P(9), px, py, pw, ph, border_color=GOLD, shadow=True)

    # Simulate typed text overlaid on the page's affirmation fields
    # Fields are approximately at top of page after header (~28% down the page height)
    field_y_ratios = [0.28, 0.35, 0.42]  # rough relative positions on page
    typed_lines = [
        "I am worthy of abundance and love.",
        "I am worthy of abundance and love.",
        "I am worthy of abundance and love.",
    ]
    for ratio, text in zip(field_y_ratios, typed_lines):
        fy = py + int(ph * ratio)
        fx = px + 36
        fw = pw - 72
        # Subtle highlight to simulate an active text field
        draw.rectangle([fx, fy, fx + fw, fy + 26], fill=(40, 34, 30))
        draw.text((fx + 8, fy + 4), text, font=F(CR, 22), fill=LGOLD)

    # Left callout column
    callouts = [
        ("CLICK", "any field to type"),
        ("SAVE", "your progress instantly"),
        ("PRINT", "anytime you want"),
        ("WORKS", "in free Adobe Reader"),
    ]
    cx0 = 60
    cy0 = py + 80
    for i, (bold, sub) in enumerate(callouts):
        cy = cy0 + i * 200
        draw.rounded_rectangle([cx0, cy, cx0+310, cy+160], radius=14,
                               fill=BGRAY, outline=GOLD, width=2)
        draw.text((cx0+155, cy+18), bold, font=F(AR, 46), fill=LGOLD, anchor="mt")
        draw.text((cx0+155, cy+80), sub, font=F(CI, 28), fill=WTEXT, anchor="mt")

    # Bottom footer
    draw.line([(80, SQ-90), (SQ-80, SQ-90)], fill=GOLD, width=1)
    draw.text((SQ//2, SQ-68),
              "1,553 FILLABLE FIELDS  ·  ZERO SOFTWARE REQUIRED  ·  ALL DEVICES SUPPORTED",
              font=F(AR, 28), fill=GOLD, anchor="mt")

    save(img, "17-typing-demo-fillable.jpg")


# ══════════════════════════════════════════════════════════════════════════════
# RUN ALL
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print(f"Saving to {MOCK_DIR}\n")

    make_thumbnail()
    make_bundle_overview()
    make_cover_full()
    make_daily_spread()
    make_pages_overview()
    make_method_page()
    make_shadow_work()
    make_moon_calendar()
    make_moon_phase_guide()
    make_sync_log()
    make_weekly_review()
    make_bonus_pages()
    make_closing()
    make_ipad_mockup()
    make_laptop_mockup()
    make_features()
    make_welcome_pair()
    make_typing_demo()

    files = sorted(os.listdir(MOCK_DIR))
    print(f"\n{len(files)} mockup images created in outputs/etsy-mockups/")
