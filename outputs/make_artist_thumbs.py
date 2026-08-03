#!/usr/bin/env python3
"""
20 artist-style Etsy thumbnails for the 369 Portal Manifestation Journal.
Output: outputs/etsy-artist-thumbs/artist-01.jpg .. artist-20.jpg  (2000x2000)
"""

import os, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE     = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/mnt/skills/examples/canvas-design/canvas-fonts"
OUT_DIR  = os.path.join(HERE, "etsy-artist-thumbs")
os.makedirs(OUT_DIR, exist_ok=True)

DARKBG = (18, 14, 11)
NAVY   = (14, 16, 28)
CREAM  = (250, 246, 240)
GOLD   = (201, 168, 76)
LGOLD  = (224, 192, 96)
DGOLD  = (160, 128, 52)
INK    = (26, 20, 16)
WTEXT  = (237, 229, 204)
BGRAY  = (38, 32, 28)

SQ = 2000

_font_cache = {}
def F(name, size):
    key = (name, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    return _font_cache[key]

IT = "Italiana-Regular.ttf"
AR = "ArsenalSC-Regular.ttf"
CR = "CrimsonPro-Regular.ttf"
CI = "CrimsonPro-Italic.ttf"

_page_cache = {}
def P(n):
    if n not in _page_cache:
        _page_cache[n] = Image.open(
            os.path.join(HERE, f"preview-page{n:03d}-{n:03d}.png")).convert("RGB")
    return _page_cache[n]

def canvas(bg=DARKBG):
    return Image.new("RGB", (SQ, SQ), bg)

def ctext(d, text, y, font, fill, anchor="mt", x=SQ//2):
    d.text((x, y), text, font=font, fill=fill, anchor=anchor)

def paste_page(img, page, x, y, w, h, border=GOLD, shadow=True, rotate=0):
    pr = page.resize((w, h), Image.LANCZOS)
    if border:
        b = Image.new("RGB", (w + 6, h + 6), border)
        b.paste(pr, (3, 3))
        pr = b
    if rotate:
        pr = pr.convert("RGBA").rotate(rotate, expand=True,
                                       resample=Image.BICUBIC)
    if shadow:
        sh = Image.new("RGBA", (pr.width + 60, pr.height + 60), (0, 0, 0, 0))
        sd = ImageDraw.Draw(sh)
        if rotate:
            mask = pr.split()[3].point(lambda a: 140 if a > 0 else 0)
            sh.paste((0, 0, 0, 140), (30, 30), mask)
        else:
            sd.rectangle([30, 30, 30 + pr.width, 30 + pr.height], fill=(0, 0, 0, 140))
        sh = sh.filter(ImageFilter.GaussianBlur(16))
        img.paste(sh.convert("RGB"), (x - 30 + 8, y - 30 + 12), sh.split()[3])
    if pr.mode == "RGBA":
        img.paste(pr.convert("RGB"), (x, y), pr.split()[3])
    else:
        img.paste(pr, (x, y))

def starfield(d, n=220, seed=7, region=(0, 0, SQ, SQ)):
    rnd = random.Random(seed)
    x0, y0, x1, y1 = region
    for _ in range(n):
        x, y = rnd.randint(x0, x1), rnd.randint(y0, y1)
        r = rnd.choice([1, 1, 1, 2, 2, 3])
        bright = rnd.randint(60, 200)
        col = (bright, int(bright * 0.92), int(bright * 0.72))
        d.ellipse([x - r, y - r, x + r, y + r], fill=col)
        if r == 3 and rnd.random() < 0.5:
            d.line([(x - 9, y), (x + 9, y)], fill=col, width=1)
            d.line([(x, y - 9), (x, y + 9)], fill=col, width=1)

def flower_of_life(d, cx, cy, r, rings=2, color=GOLD, width=2):
    pts = [(0.0, 0.0)]
    for ring in range(1, rings + 1):
        for i in range(6 * ring):
            ang = math.pi / 3 * (i / ring)
            for a in range(6):
                base = math.pi / 3 * a
                px = ring * r * math.cos(base) + 0
        # hexagonal close packing
    pts = set([(0, 0)])
    for q in range(-rings, rings + 1):
        for s in range(-rings, rings + 1):
            if abs(q + s) <= rings:
                x = r * (q + s / 2) * 2 * 0.866
                y = r * s * 1.5
                pts.add((round(x, 1), round(y, 1)))
    for (px, py) in pts:
        d.ellipse([cx + px - r, cy + py - r, cx + px + r, cy + py + r],
                  outline=color, width=width)

def moon_glyph(d, cx, cy, r, phase, color=LGOLD):
    """phase 0=new .. 4=full .. 8=new; simple artistic moons."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=3)
    if phase == 4:
        d.ellipse([cx - r + 6, cy - r + 6, cx + r - 6, cy + r - 6], fill=color)
    elif phase != 0:
        frac = abs(phase - 4) / 4          # 0 full .. 1 new
        off = int(r * 2 * frac * (1 if phase < 4 else -1))
        full = Image.new("L", (2 * r, 2 * r), 0)
        fd = ImageDraw.Draw(full)
        fd.ellipse([6, 6, 2 * r - 6, 2 * r - 6], fill=255)
        fd.ellipse([6 + off, 6, 2 * r - 6 + off, 2 * r - 6], fill=0)
        sw = Image.new("RGB", (2 * r, 2 * r), color)
        base = d._image if hasattr(d, "_image") else None

def moon_disc(img, cx, cy, r, frac, color=LGOLD):
    """Paste a moon disc; frac 0..1 illumination, side alternates."""
    m = Image.new("RGBA", (2 * r + 8, 2 * r + 8), (0, 0, 0, 0))
    md = ImageDraw.Draw(m)
    md.ellipse([4, 4, 2 * r + 4, 2 * r + 4], outline=color + (255,), width=3)
    if frac > 0.02:
        md.ellipse([8, 8, 2 * r, 2 * r], fill=color + (int(90 + 165 * frac),))
        if frac < 0.98:
            off = int((1 - frac) * 1.6 * r)
            md.ellipse([8 - off, 8, 2 * r - off, 2 * r], fill=(0, 0, 0, 255))
            md.ellipse([8 - off, 8, 2 * r - off, 2 * r],
                       fill=DARKBG + (255,))
    img.paste(m, (cx - r - 4, cy - r - 4), m)

def deco_corners(d, m=70, s=150, color=GOLD, w=3):
    for (x, y, dx, dy) in [(m, m, 1, 1), (SQ - m, m, -1, 1),
                           (m, SQ - m, 1, -1), (SQ - m, SQ - m, -1, -1)]:
        d.line([(x, y), (x + s * dx, y)], fill=color, width=w)
        d.line([(x, y), (x, y + s * dy)], fill=color, width=w)
        d.line([(x + 14 * dx, y + 14 * dy), (x + (s - 40) * dx, y + 14 * dy)],
               fill=DGOLD, width=1)
        d.line([(x + 14 * dx, y + 14 * dy), (x + 14 * dx, y + (s - 40) * dy)],
               fill=DGOLD, width=1)

def radial_glow(img, cx, cy, r_max, color=GOLD, strength=26):
    glow = Image.new("L", (SQ, SQ), 0)
    gd = ImageDraw.Draw(glow)
    steps = 26
    for i in range(steps, 0, -1):
        rr = int(r_max * i / steps)
        val = int(strength * (1 - i / steps))
        gd.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=val)
    glow = glow.filter(ImageFilter.GaussianBlur(60))
    overlay = Image.new("RGB", (SQ, SQ), color)
    img.paste(overlay, (0, 0), glow)

def vertical_gradient(top, bottom):
    img = Image.new("RGB", (SQ, SQ))
    for y in range(SQ):
        t = y / SQ
        img.paste(tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)),
                  (0, y, SQ, y + 1))
    return img

def save(img, idx):
    name = f"artist-{idx:02d}.jpg"
    img.save(os.path.join(OUT_DIR, name), "JPEG", quality=93)
    print(f"  {name}")

BRAND_FOOT = "THE PORTAL  ·  369 MANIFESTATION JOURNAL  ·  GLOWHAUSDIGITAL"

def footer(d, color=DGOLD, y=SQ - 90):
    ctext(d, BRAND_FOOT, y, F(AR, 30), color)


# 01 — Celestial starfield hero
def t01():
    img = vertical_gradient(NAVY, DARKBG)
    d = ImageDraw.Draw(img)
    starfield(d, 260, seed=11)
    radial_glow(img, SQ // 2, 880, 700)
    d = ImageDraw.Draw(img)
    flower_of_life(d, SQ // 2, 880, 90, rings=2, color=DGOLD, width=2)
    ctext(d, "A  S A C R E D  P R A C T I C E", 170, F(AR, 40), LGOLD)
    ctext(d, "THE PORTAL", 230, F(IT, 230), WTEXT)
    ctext(d, "3 · 6 · 9  Manifestation Journal", 500, F(IT, 78), LGOLD)
    ctext(d, "Write your reality into existence.", 1360, F(CI, 60), WTEXT)
    ctext(d, "28 DAYS  ·  123 PAGES  ·  6 FILE FORMATS", 1490, F(AR, 42), GOLD)
    deco_corners(d)
    footer(d)
    save(img, 1)

# 02 — Golden arch portal doorway with cover
def t02():
    img = canvas()
    d = ImageDraw.Draw(img)
    starfield(d, 150, seed=22)
    cx, top, w = SQ // 2, 330, 900
    bot = 1700
    # arch glow
    radial_glow(img, cx, 900, 760, strength=20)
    d = ImageDraw.Draw(img)
    for i, off in enumerate((0, 26, 52)):
        r = w // 2 - off
        d.arc([cx - r, top + off, cx + r, top + w - off + 60],
              180, 360, fill=(GOLD, DGOLD, LGOLD)[i], width=4 - i)
        d.line([(cx - r, top + w // 2 + 30), (cx - r, bot)],
               fill=(GOLD, DGOLD, LGOLD)[i], width=4 - i)
        d.line([(cx + r, top + w // 2 + 30), (cx + r, bot)],
               fill=(GOLD, DGOLD, LGOLD)[i], width=4 - i)
    pw = 560; ph = int(pw * 11 / 8.5)
    paste_page(img, P(1), cx - pw // 2, 760, pw, ph)
    ctext(d, "STEP THROUGH", 150, F(AR, 44), LGOLD)
    ctext(d, "The Portal", 196, F(IT, 150), WTEXT)
    ctext(d, "369 Manifestation Journal  ·  28-Day Sacred Practice", 1790,
          F(CI, 52), GOLD)
    footer(d, y=SQ - 80)
    save(img, 2)

# 03 — Moon phase arc
def t03():
    img = vertical_gradient(DARKBG, NAVY)
    d = ImageDraw.Draw(img)
    starfield(d, 200, seed=33)
    cx, cy, R = SQ // 2, 1500, 1050
    fracs = [0.0, 0.25, 0.5, 0.75, 1.0, 0.75, 0.5, 0.25, 0.0]
    for i, fr in enumerate(fracs):
        ang = math.pi * (1 - i / (len(fracs) - 1))
        x = int(cx + R * math.cos(ang))
        y = int(cy - R * math.sin(ang))
        moon_disc(img, x, y, 56, fr)
    d = ImageDraw.Draw(img)
    ctext(d, "WORK  WITH  THE  MOON", 700, F(AR, 46), LGOLD)
    ctext(d, "THE PORTAL", 770, F(IT, 200), WTEXT)
    ctext(d, "3 · 6 · 9 Manifestation Journal", 1010, F(IT, 72), LGOLD)
    ctext(d, "8-Phase Moon Guide  ·  4 Lunar Cycles of Journaling", 1160,
          F(CI, 50), WTEXT)
    ctext(d, "NEW MOON INTENTIONS  ·  FULL MOON RELEASE", 1280, F(AR, 38), GOLD)
    footer(d)
    save(img, 3)

# 04 — Giant 369 typographic poster
def t04():
    img = canvas()
    d = ImageDraw.Draw(img)
    for r in range(200, 1400, 90):
        d.ellipse([SQ//2 - r, 1050 - r, SQ//2 + r, 1050 + r],
                  outline=(30, 25, 19), width=2)
    ctext(d, "3 6 9", 300, F(IT, 560), LGOLD)
    ctext(d, "“If you only knew the magnificence of the 3, 6 and 9,",
          1050, F(CI, 58), WTEXT)
    ctext(d, "you would have a key to the universe.”", 1130, F(CI, 58), WTEXT)
    ctext(d, "—  N I K O L A  T E S L A", 1260, F(AR, 40), GOLD)
    d.line([(500, 1400), (1500, 1400)], fill=GOLD, width=2)
    ctext(d, "THE PORTAL", 1450, F(IT, 120), WTEXT)
    ctext(d, "Manifestation Journal · 28 Days · 504 Repetitions", 1600,
          F(CI, 50), LGOLD)
    deco_corners(d)
    footer(d)
    save(img, 4)

# 05 — Sacred geometry mandala
def t05():
    img = canvas()
    d = ImageDraw.Draw(img)
    cx, cy = SQ // 2, SQ // 2
    flower_of_life(d, cx, cy, 260, rings=2, color=(52, 42, 28), width=2)
    for r in (820, 860, 900):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(60, 48, 30), width=2)
    pw = 660; ph = int(pw * 11 / 8.5)
    paste_page(img, P(1), cx - pw // 2, cy - ph // 2 + 60, pw, ph)
    ctext(d, "SACRED GEOMETRY  ·  SACRED PRACTICE", 130, F(AR, 42), LGOLD)
    ctext(d, "The 369 Portal", 190, F(IT, 130), WTEXT)
    ctext(d, "A manifestation journal designed like a ritual object", 1830,
          F(CI, 52), GOLD)
    save(img, 5)

# 06 — Fanned pages collage
def t06():
    img = canvas()
    d = ImageDraw.Draw(img)
    starfield(d, 120, seed=66)
    pw = 520; ph = int(pw * 11 / 8.5)
    paste_page(img, P(10), 200, 620, pw, ph, rotate=8)
    paste_page(img, P(11), 720, 660, pw, ph, rotate=-3)
    paste_page(img, P(74), 1240, 620, pw, ph, rotate=-9)
    d = ImageDraw.Draw(img)
    ctext(d, "INSIDE THE PORTAL", 150, F(AR, 46), LGOLD)
    ctext(d, "123 Pages of Guided Practice", 210, F(IT, 110), WTEXT)
    ctext(d, "Morning · Midday · Evening scripting  +  shadow work,", 1560,
          F(CI, 54), WTEXT)
    ctext(d, "moon cycles, synchronicity logs & weekly evidence reviews", 1640,
          F(CI, 54), WTEXT)
    footer(d)
    save(img, 6)

# 07 — Sun / moon split
def t07():
    img = canvas()
    left = vertical_gradient((242, 233, 214), CREAM).crop((0, 0, SQ // 2, SQ))
    img.paste(left, (0, 0))
    d = ImageDraw.Draw(img)
    starfield(d, 120, seed=77, region=(SQ // 2, 0, SQ, SQ))
    # sun
    scx, scy = SQ // 4, 560
    d.ellipse([scx - 130, scy - 130, scx + 130, scy + 130], outline=DGOLD, width=5)
    for i in range(24):
        a = math.tau * i / 24
        x1, y1 = scx + 160 * math.cos(a), scy + 160 * math.sin(a)
        x2, y2 = scx + (210 if i % 2 == 0 else 185) * math.cos(a), scy + (210 if i % 2 == 0 else 185) * math.sin(a)
        d.line([(x1, y1), (x2, y2)], fill=DGOLD, width=4)
    moon_disc(img, 3 * SQ // 4, 560, 140, 0.85)
    d = ImageDraw.Draw(img)
    d.text((SQ // 4, 830), "MORNING", font=F(AR, 52), fill=INK, anchor="mt")
    d.text((SQ // 4, 900), "Write it 3×", font=F(IT, 84), fill=DGOLD, anchor="mt")
    d.text((3 * SQ // 4, 830), "EVENING", font=F(AR, 52), fill=LGOLD, anchor="mt")
    d.text((3 * SQ // 4, 900), "Write it 9×", font=F(IT, 84), fill=WTEXT, anchor="mt")
    d.text((SQ // 4, 1060), "+ 6× at midday", font=F(CI, 54), fill=INK, anchor="mt")
    d.text((3 * SQ // 4, 1060), "= 504 signals", font=F(CI, 54), fill=WTEXT, anchor="mt")
    d.line([(SQ // 2, 0), (SQ // 2, SQ)], fill=GOLD, width=4)
    d.rectangle([220, 1300, SQ - 220, 1660], fill=DARKBG, outline=GOLD, width=3)
    ctext(d, "THE PORTAL", 1340, F(IT, 130), WTEXT)
    ctext(d, "369 Manifestation Journal", 1500, F(IT, 66), LGOLD)
    footer(d)
    save(img, 7)

# 08 — Constellation 3-6-9
def t08():
    img = vertical_gradient(NAVY, DARKBG)
    d = ImageDraw.Draw(img)
    starfield(d, 300, seed=88)
    rnd = random.Random(3)
    nodes = [(400, 500), (700, 380), (1050, 470), (1380, 360), (1650, 520),
             (1500, 830), (1150, 760), (800, 860), (500, 780)]
    for i in range(len(nodes) - 1):
        d.line([nodes[i], nodes[i + 1]], fill=DGOLD, width=2)
    for i, (x, y) in enumerate(nodes):
        r = 10 if i % 3 else 16
        d.ellipse([x - r, y - r, x + r, y + r], fill=LGOLD)
        d.ellipse([x - r - 8, y - r - 8, x + r + 8, y + r + 8], outline=DGOLD, width=1)
    for i, lbl in [(0, "3"), (4, "6"), (8, "9")]:
        x, y = nodes[i]
        d.text((x, y - 90), lbl, font=F(IT, 110), fill=WTEXT, anchor="mm")
    ctext(d, "YOUR DESIRE, WRITTEN IN THE STARS", 1080, F(AR, 44), LGOLD)
    ctext(d, "THE PORTAL", 1140, F(IT, 190), WTEXT)
    ctext(d, "369 Manifestation Journal", 1370, F(IT, 76), LGOLD)
    ctext(d, "Instant Download  ·  Print + Fillable + iPad", 1500, F(CI, 52), GOLD)
    footer(d)
    save(img, 8)

# 09 — Art-deco frame
def t09():
    img = canvas()
    d = ImageDraw.Draw(img)
    for i, m in enumerate((90, 120, 140)):
        d.rectangle([m, m, SQ - m, SQ - m], outline=(GOLD, DGOLD, LGOLD)[i],
                    width=(4, 1, 2)[i])
    # deco fans in corners
    for (cx, cy, a0) in [(140, 140, 0), (SQ - 140, 140, 90),
                         (SQ - 140, SQ - 140, 180), (140, SQ - 140, 270)]:
        for k in range(5):
            r = 60 + k * 28
            d.arc([cx - r, cy - r, cx + r, cy + r], a0, a0 + 90, fill=DGOLD, width=2)
    ctext(d, "· EST. IN THE QUANTUM FIELD ·", 260, F(AR, 40), LGOLD)
    ctext(d, "THE", 360, F(IT, 110), WTEXT)
    ctext(d, "PORTAL", 480, F(IT, 260), LGOLD)
    d.line([(560, 800), (1440, 800)], fill=GOLD, width=3)
    ctext(d, "3 · 6 · 9", 840, F(IT, 150), WTEXT)
    ctext(d, "MANIFESTATION JOURNAL", 1040, F(AR, 62), GOLD)
    ctext(d, "Twenty-Eight Days · One Moon Cycle · Infinite Possibility",
          1160, F(CI, 54), WTEXT)
    flower_of_life(d, SQ // 2, 1480, 60, rings=1, color=DGOLD, width=2)
    ctext(d, "WRITE  ·  BELIEVE  ·  RECEIVE", 1700, F(AR, 48), LGOLD)
    save(img, 9)

# 10 — Handwriting ritual
def t10():
    img = canvas(CREAM)
    d = ImageDraw.Draw(img)
    line_y = 480
    for i in range(9):
        d.line([(240, line_y + i * 110), (SQ - 240, line_y + i * 110)],
               fill=(208, 198, 182), width=2)
    msg = "I am living in my dream home surrounded by abundance."
    for i in range(9):
        d.text((260, line_y + i * 110 - 66), msg,
               font=F(CI, 52), fill=(90 + i * 6, 78 + i * 5, 60 + i * 4))
    d.rectangle([0, 0, SQ, 360], fill=DARKBG)
    ctext(d, "THE RITUAL IS SIMPLE", 60, F(AR, 44), LGOLD)
    ctext(d, "Write it until you believe it.", 120, F(IT, 110), WTEXT)
    ctext(d, "3× morning   ·   6× midday   ·   9× evening", 280, F(CI, 48), GOLD)
    d.rectangle([0, SQ - 260, SQ, SQ], fill=DARKBG)
    ctext(d, "THE PORTAL  ·  369 MANIFESTATION JOURNAL", SQ - 200, F(AR, 46), LGOLD)
    ctext(d, "Guided pages for all 28 days — never face a blank page", SQ - 130,
          F(CI, 44), WTEXT)
    save(img, 10)

# 11 — Gold panels format showcase
def t11():
    img = canvas()
    d = ImageDraw.Draw(img)
    ctext(d, "SIX FORMATS · ONE PORTAL", 110, F(AR, 46), LGOLD)
    ctext(d, "Every Way You Journal", 170, F(IT, 110), WTEXT)
    formats = [("US LETTER", "8.5 × 11 in"), ("A4", "International"),
               ("FC CLASSIC", "5.5 × 8.5 in"), ("FC COMPACT", "4.25 × 6.75 in"),
               ("FILLABLE PDF", "Type anywhere"), ("TABLET NAV", "GoodNotes ready")]
    bw, bh = 780, 360
    for i, (t1, t2) in enumerate(formats):
        x = 180 + (i % 2) * (bw + 80)
        y = 420 + (i // 2) * (bh + 60)
        d.rounded_rectangle([x, y, x + bw, y + bh], radius=24,
                            outline=GOLD, width=3, fill=BGRAY)
        d.text((x + bw // 2, y + 70), t1, font=F(AR, 64), fill=LGOLD, anchor="mm")
        d.text((x + bw // 2, y + 170), t2, font=F(IT, 66), fill=WTEXT, anchor="mm")
        d.text((x + bw // 2, y + 270), "✦", font=F(CR, 44), fill=DGOLD, anchor="mm")
    ctext(d, "One purchase · every device · print or digital", 1760, F(CI, 56), GOLD)
    footer(d)
    save(img, 11)

# 12 — Crescent night sky
def t12():
    img = vertical_gradient((10, 12, 24), (24, 18, 12))
    d = ImageDraw.Draw(img)
    starfield(d, 320, seed=12)
    moon_disc(img, 1500, 420, 220, 0.3)
    d = ImageDraw.Draw(img)
    ctext(d, "BEGIN ON THE NEW MOON", 900, F(AR, 48), LGOLD, x=760)
    d.text((760, 970), "The Portal", font=F(IT, 220), fill=WTEXT, anchor="mt")
    d.text((760, 1230), "369 Manifestation Journal", font=F(IT, 80), fill=LGOLD,
           anchor="mt")
    d.text((760, 1370), "One moon cycle. One desire.", font=F(CI, 58), fill=WTEXT,
           anchor="mt")
    d.text((760, 1450), "Everything changes.", font=F(CI, 58), fill=GOLD, anchor="mt")
    footer(d)
    save(img, 12)

# 13 — Page spiral
def t13():
    img = canvas()
    d = ImageDraw.Draw(img)
    cx, cy = SQ // 2, SQ // 2 + 80
    pages = [10, 11, 66, 74, 82, 98, 114, 122]
    pw = 300; ph = int(pw * 11 / 8.5)
    for i, pg in enumerate(pages):
        a = math.tau * i / len(pages) - math.pi / 2
        x = int(cx + 560 * math.cos(a)) - pw // 2
        y = int(cy + 560 * math.sin(a)) - ph // 2
        paste_page(img, P(pg), x, y, pw, ph,
                   rotate=int(-math.degrees(a) - 90) % 360 - 180 if False else 0)
    d = ImageDraw.Draw(img)
    flower_of_life(d, cx, cy, 40, rings=1, color=DGOLD, width=2)
    d.ellipse([cx - 190, cy - 190, cx + 190, cy + 190], outline=GOLD, width=3)
    d.text((cx, cy - 60), "123", font=F(IT, 120), fill=LGOLD, anchor="mm")
    d.text((cx, cy + 50), "PAGES", font=F(AR, 44), fill=WTEXT, anchor="mm")
    ctext(d, "A COMPLETE MANIFESTATION SYSTEM", 90, F(AR, 46), LGOLD)
    ctext(d, "Every page has a purpose.", 150, F(IT, 100), WTEXT)
    footer(d)
    save(img, 13)

# 14 — Tesla quote minimal
def t14():
    img = canvas(CREAM)
    d = ImageDraw.Draw(img)
    d.rectangle([80, 80, SQ - 80, SQ - 80], outline=DGOLD, width=3)
    d.rectangle([104, 104, SQ - 104, SQ - 104], outline=GOLD, width=1)
    ctext(d, "❝", 220, F(CR, 220), GOLD)
    ctext(d, "If you only knew the", 540, F(IT, 110), INK)
    ctext(d, "magnificence of the", 670, F(IT, 110), INK)
    ctext(d, "3, 6 and 9,", 800, F(IT, 150), DGOLD)
    ctext(d, "you would have a key", 990, F(IT, 110), INK)
    ctext(d, "to the universe.", 1120, F(IT, 110), INK)
    ctext(d, "— NIKOLA TESLA", 1330, F(AR, 46), DGOLD)
    d.line([(700, 1460), (1300, 1460)], fill=GOLD, width=2)
    ctext(d, "This journal is that key.", 1510, F(CI, 64), INK)
    ctext(d, "THE PORTAL · 369 MANIFESTATION JOURNAL", 1680, F(AR, 44), DGOLD)
    save(img, 14)

# 15 — Checklist "what you get"
def t15():
    img = canvas()
    d = ImageDraw.Draw(img)
    ctext(d, "EVERYTHING YOU RECEIVE", 110, F(AR, 46), LGOLD)
    ctext(d, "The Complete Bundle", 170, F(IT, 110), WTEXT)
    items = ["28 days of guided 3·6·9 scripting pages",
             "8-phase Moon Guide + 4 lunar cycle calendars",
             "8 shadow work deep-dive pages",
             "16 synchronicity log pages",
             "Weekly + monthly evidence reviews",
             "Dream journal, letters to the universe & bonus pages",
             "Fillable PDF — type on phone, tablet or computer",
             "Tablet edition with full bookmark navigation",
             "4 print sizes: Letter, A4, FC Classic & Compact"]
    y = 420
    for it in items:
        d.ellipse([200, y + 6, 248, y + 54], outline=GOLD, width=3)
        d.line([(212, y + 30), (224, y + 44)], fill=LGOLD, width=4)
        d.line([(224, y + 44), (240, y + 16)], fill=LGOLD, width=4)
        d.text((300, y + 30), it, font=F(CR, 54), fill=WTEXT, anchor="lm")
        y += 130
    ctext(d, "INSTANT DOWNLOAD  ·  BEGIN TONIGHT", 1740, F(AR, 48), GOLD)
    footer(d)
    save(img, 15)

# 16 — Day 1 → Day 28 journey
def t16():
    img = canvas()
    d = ImageDraw.Draw(img)
    starfield(d, 100, seed=16)
    pw = 620; ph = int(pw * 11 / 8.5)
    paste_page(img, P(10), 150, 460, pw, ph, rotate=4)
    paste_page(img, P(122), SQ - 150 - pw, 460, pw, ph, rotate=-4)
    d = ImageDraw.Draw(img)
    # arrow
    ax0, ax1, ay = 830, 1170, 850
    d.line([(ax0, ay), (ax1, ay)], fill=GOLD, width=6)
    d.polygon([(ax1, ay), (ax1 - 36, ay - 22), (ax1 - 36, ay + 22)], fill=GOLD)
    d.text((490, 400), "DAY 1", font=F(AR, 60), fill=LGOLD, anchor="mm")
    d.text((SQ - 490, 400), "DAY 28", font=F(AR, 60), fill=LGOLD, anchor="mm")
    d.text((SQ // 2, 950), "one moon cycle", font=F(CI, 52), fill=WTEXT, anchor="mm")
    ctext(d, "FROM INTENTION TO EVIDENCE", 120, F(AR, 46), LGOLD)
    ctext(d, "Your 28-Day Transformation", 180, F(IT, 104), WTEXT)
    ctext(d, "THE PORTAL · 369 MANIFESTATION JOURNAL", 1700, F(AR, 48), GOLD)
    ctext(d, "504 repetitions · daily energy tracking · weekly proof it's working",
          1780, F(CI, 50), WTEXT)
    save(img, 16)

# 17 — Concentric portal rings
def t17():
    img = canvas()
    d = ImageDraw.Draw(img)
    cx, cy = SQ // 2, SQ // 2
    for i, r in enumerate(range(120, 960, 60)):
        col = LGOLD if i % 4 == 0 else (DGOLD if i % 2 else (48, 40, 26))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col,
                  width=3 if i % 4 == 0 else 1)
    radial_glow(img, cx, cy, 300, strength=34)
    d = ImageDraw.Draw(img)
    d.text((cx, cy - 110), "ENTER", font=F(AR, 54), fill=LGOLD, anchor="mm")
    d.text((cx, cy), "THE PORTAL", font=F(IT, 130), fill=WTEXT, anchor="mm")
    d.text((cx, cy + 120), "3 · 6 · 9", font=F(IT, 80), fill=LGOLD, anchor="mm")
    ctext(d, "MANIFESTATION JOURNAL — INSTANT DIGITAL DOWNLOAD", 1840,
          F(AR, 42), GOLD)
    ctext(d, "A 28-day writing ritual built on Tesla's sacred code", 1910,
          F(CI, 44), WTEXT)
    save(img, 17)

# 18 — Moon glyph pattern wall
def t18():
    img = canvas()
    d = ImageDraw.Draw(img)
    rnd = random.Random(18)
    fracs = [0, 0.25, 0.5, 0.75, 1.0, 0.75, 0.5, 0.25]
    for row in range(8):
        for col in range(8):
            x = 160 + col * 245
            y = 160 + row * 245
            moon_disc(img, x, y, 52, fracs[(row + col) % 8],
                      color=(DGOLD if (row + col) % 2 else (70, 58, 38)))
    d = ImageDraw.Draw(img)
    box = Image.new("RGB", (1560, 560), DARKBG)
    img.paste(box, (220, 700))
    d.rectangle([220, 700, 1780, 1260], outline=GOLD, width=4)
    d.rectangle([244, 724, 1756, 1236], outline=DGOLD, width=1)
    ctext(d, "THE PORTAL", 780, F(IT, 190), WTEXT)
    ctext(d, "369 MANIFESTATION JOURNAL", 1010, F(AR, 56), LGOLD)
    ctext(d, "Aligned with every phase of the moon", 1100, F(CI, 52), GOLD)
    save(img, 18)

# 19 — 28 days badge / stats
def t19():
    img = vertical_gradient(DARKBG, (30, 24, 16))
    d = ImageDraw.Draw(img)
    starfield(d, 140, seed=19)
    cx = SQ // 2
    d.ellipse([cx - 420, 260, cx + 420, 1100], outline=GOLD, width=5)
    d.ellipse([cx - 390, 290, cx + 390, 1070], outline=DGOLD, width=2)
    d.text((cx, 500), "28", font=F(IT, 360), fill=LGOLD, anchor="mm")
    d.text((cx, 760), "D A Y S", font=F(AR, 80), fill=WTEXT, anchor="mm")
    d.text((cx, 880), "to open your portal", font=F(CI, 60), fill=GOLD, anchor="mm")
    stats = [("504", "REPETITIONS"), ("123", "PAGES"), ("6", "FORMATS")]
    for i, (n, lbl) in enumerate(stats):
        x = 380 + i * 620
        d.text((x, 1350), n, font=F(IT, 150), fill=WTEXT, anchor="mm")
        d.text((x, 1470), lbl, font=F(AR, 42), fill=LGOLD, anchor="mm")
        if i < 2:
            d.line([(x + 310, 1290), (x + 310, 1500)], fill=DGOLD, width=2)
    ctext(d, "THE PORTAL  ·  369 MANIFESTATION JOURNAL", 1700, F(AR, 50), GOLD)
    ctext(d, "The universe rewards those who show up daily.", 1790, F(CI, 52), WTEXT)
    save(img, 19)

# 20 — The Portal is Open (emotional closer)
def t20():
    img = vertical_gradient(NAVY, DARKBG)
    d = ImageDraw.Draw(img)
    starfield(d, 260, seed=20)
    radial_glow(img, SQ // 2, 1050, 800, strength=22)
    d = ImageDraw.Draw(img)
    flower_of_life(d, SQ // 2, 1050, 130, rings=2, color=DGOLD, width=2)
    for r in (520, 560):
        d.ellipse([SQ//2 - r, 1050 - r, SQ//2 + r, 1050 + r],
                  outline=(70, 58, 36), width=2)
    ctext(d, "AT THE END OF 28 DAYS", 210, F(AR, 44), LGOLD)
    ctext(d, "The Portal is Open.", 280, F(IT, 160), WTEXT)
    ctext(d, "You did not just write in a journal.", 1650, F(CI, 60), WTEXT)
    ctext(d, "You sent a signal the universe could not ignore.", 1740, F(CI, 60),
          LGOLD)
    footer(d, y=SQ - 70)
    save(img, 20)


if __name__ == "__main__":
    for fn in (t01, t02, t03, t04, t05, t06, t07, t08, t09, t10,
               t11, t12, t13, t14, t15, t16, t17, t18, t19, t20):
        fn()
    print("\n20 artist thumbnails created in outputs/etsy-artist-thumbs/")
