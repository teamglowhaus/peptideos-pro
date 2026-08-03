# -*- coding: utf-8 -*-
"""Compose the 15 Etsy listing images (2000x1600 JPG) from real PDF renders.
Rerun after any PDF rebuild so previews stay accurate."""
import os, sys, math
import fitz
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FONTS = os.path.join(ROOT, "02_Main_Workbook_Source", "assets", "fonts")

W, H = 2000, 1600
INDIGO = (35, 41, 70)
NIGHT = (25, 29, 51)
IVORY = (250, 246, 238)
CREAM = (253, 251, 244)
GOLD = (168, 137, 79)
GOLD_SOFT = (201, 177, 131)
TERRA = (194, 119, 91)
PLUM_PALE = (237, 231, 238)
WASH = (246, 239, 224)
INK = (51, 48, 60)

def F(name, size):
    files = {"serif": "CormorantGaramond-500.ttf", "serifsb": "CormorantGaramond-600.ttf",
             "serifit": "CormorantGaramond-Italic-500.ttf", "marc": "Marcellus-400.ttf",
             "lato": "Lato-400.ttf", "latob": "Lato-700.ttf"}
    return ImageFont.truetype(os.path.join(FONTS, files[name]), size)

PDFS = {
 "letter": os.path.join(ROOT, "03_Main_Workbook_PDFs", "Lions_Gate_Activation_US_Letter.pdf"),
 "digital": os.path.join(ROOT, "04_Digital_Editions", "Lions_Gate_Activation_Digital_US_Letter.pdf"),
 "pocket": os.path.join(ROOT, "06_Planner_Insert_PDFs", "Lions_Gate_Planner_Pocket_3.5x6.pdf"),
 "compact": os.path.join(ROOT, "06_Planner_Insert_PDFs", "Lions_Gate_Planner_Compact_4.25x6.75.pdf"),
 "classic": os.path.join(ROOT, "06_Planner_Insert_PDFs", "Lions_Gate_Planner_Classic_5.5x8.5.pdf"),
 "monarch": os.path.join(ROOT, "06_Planner_Insert_PDFs", "Lions_Gate_Planner_Monarch_8.5x11.pdf"),
 "cards": os.path.join(ROOT, "08_Bonus_Files", "Lions_Gate_Affirmation_Cards_US_Letter.pdf"),
 "tabs": os.path.join(ROOT, "08_Bonus_Files", "Lions_Gate_Planner_Tabs_US_Letter.pdf"),
 "quick": os.path.join(ROOT, "08_Bonus_Files", "Lions_Gate_Quick_Start.pdf"),
 "readme": os.path.join(ROOT, "09_Customer_Guides", "Lions_Gate_Read_Me_First.pdf"),
}
_docs = {}
def doc(key):
    if key not in _docs:
        _docs[key] = fitz.open(PDFS[key])
    return _docs[key]

def find_page(key, needle, start=None):
    d = doc(key)
    if start is None:
        # skip cover, front matter and the table of contents (which contains
        # every page title) in the big books
        start = 14 if key in ("letter", "digital") else 0
    for i in range(start, len(d)):
        if needle in d[i].get_text():
            return i
    return 0

def render(key, pno, height, border=True):
    d = doc(key)
    zoom = height / d[pno].rect.height
    pix = d[pno].get_pixmap(matrix=fitz.Matrix(zoom * 2, zoom * 2))
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    im = im.resize((int(pix.width / 2), int(pix.height / 2)), Image.LANCZOS)
    if border:
        b = Image.new("RGB", (im.width + 2, im.height + 2), (210, 202, 186))
        b.paste(im, (1, 1))
        im = b
    return im

def shadow_paste(base, im, x, y, angle=0):
    if angle:
        im = im.rotate(angle, expand=True, fillcolor=None, resample=Image.BICUBIC)
    sh = Image.new("RGBA", (im.width + 40, im.height + 40), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    sd.rectangle([20, 24, 20 + im.width, 24 + im.height], fill=(20, 18, 30, 90))
    sh = sh.filter(ImageFilter.GaussianBlur(12))
    base.paste(sh, (x - 20, y - 20), sh)
    base.paste(im, (x, y))

def kicker(d, cx, y, text, size, color, ls=6, anchor="m"):
    f = F("marc", size)
    t = text.upper()
    widths = [d.textlength(ch, font=f) for ch in t]
    total = sum(widths) + ls * (len(t) - 1)
    x = cx - total / 2 if anchor == "m" else cx
    for ch, w_ in zip(t, widths):
        d.text((x, y), ch, font=f, fill=color)
        x += w_ + ls

def center(d, cx, y, text, font, color, maxw=None):
    lines = [text]
    if maxw:
        lines = wrap(d, text, font, maxw)
    for ln in lines:
        w_ = d.textlength(ln, font=font)
        d.text((cx - w_ / 2, y), ln, font=font, fill=color)
        y += int(font.size * 1.18)
    return y

def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) > maxw and cur:
            lines.append(cur); cur = w_
        else:
            cur = t
    if cur: lines.append(cur)
    return lines

def stars_bg(d, seed, color, n, x0, y0, x1, y1):
    s = seed
    def r():
        nonlocal s
        s = (s * 9301 + 49297) % 233280
        return s / 233280.0
    for i in range(n):
        x = x0 + r() * (x1 - x0); y = y0 + r() * (y1 - y0); sz = r()
        if i % 9 == 0:
            L = 8 + sz * 8
            d.line([(x - L, y), (x + L, y)], fill=color, width=2)
            d.line([(x, y - L), (x, y + L)], fill=color, width=2)
        else:
            rad = 1 + sz * 2.2
            d.ellipse([x - rad, y - rad, x + rad, y + rad], fill=color)

def base(bg=IVORY):
    img = Image.new("RGB", (W, H), bg)
    return img, ImageDraw.Draw(img)

def footer(d, text="GlowHausDigital · digital download · nothing ships"):
    kicker(d, W // 2, H - 56, text, 22, GOLD, ls=3)

def gold_rule(d, cx, y, half=120):
    d.line([(cx - half, y), (cx - 24, y)], fill=GOLD, width=3)
    d.line([(cx + 24, y), (cx + half, y)], fill=GOLD, width=3)
    star8(d, cx, y, 14, GOLD)

def star8(d, cx, cy, R, color, width=3):
    pts = []
    for i in range(16):
        ang = math.pi / 8 * i - math.pi / 2
        rad = R if i % 2 == 0 else R * 0.36
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(pts, outline=color, width=width)

def save(img, n, name):
    img.save(os.path.join(HERE, "%02d_%s.jpg" % (n, name)), "JPEG", quality=90)
    print("image %02d %s" % (n, name))

# ---------------------------------------------------------------- images
def img01():
    img, d = base(NIGHT)
    stars_bg(d, 7, GOLD_SOFT, 90, 0, 0, W, H * 0.9)
    cover = render("letter", 0, 1250)
    shadow_paste(img, cover, W - cover.width - 150, 175)
    kicker(d, 560, 130, "GlowHausDigital", 30, GOLD_SOFT, anchor="m")
    f = F("serif", 118)
    y = center(d, 560, 340, "More Than a", f, IVORY)
    y = center(d, 560, y + 222 - 222, "Manifestation", f, IVORY)
    y = center(d, 560, y, "Journal", f, IVORY)
    gold_rule(d, 560, y + 60)
    fs = F("serifit", 52)
    center(d, 560, y + 110, "An eight-day Lion's Gate 8/8 experience:", fs, GOLD_SOFT)
    center(d, 560, y + 175, "release, clarify, embody, act.", fs, GOLD_SOFT)
    kicker(d, 560, y + 300, "Digital download · print + tablet + planner", 26, IVORY, ls=3)
    save(img, 1, "hero")

def img02():
    img, d = base(IVORY)
    f = F("serif", 96)
    center(d, W // 2, 90, "Everything in Your Download", f, INDIGO)
    fl = F("lato", 42)
    center(d, W // 2, 215, "178-page workbook · 4 planner sizes · rituals, cards, tabs, wallpapers, guides", fl, INK)
    shots = [
        ("letter", 0), ("letter", find_page("letter", "three truest sentences")),
        ("letter", find_page("letter", "The Golden Hour")), ("classic", 0),
        ("cards", 0), ("tabs", 0), ("quick", 0), ("readme", 0),
    ]
    x, y = 90, 330
    for i, (k, p) in enumerate(shots):
        im = render(k, p, 480)
        if im.width > 400:
            im = im.resize((int(im.width * 400 / im.width), int(im.height * 400 / im.width)), Image.LANCZOS)
        shadow_paste(img, im, x, y + (30 if i % 2 else 0))
        x += im.width + 45
        if x > W - 380 and i < len(shots) - 1:
            x, y = 90, y + 560
    footer(d)
    save(img, 2, "included")

def img03():
    img, d = base(IVORY)
    d.rectangle([0, 0, 820, H], fill=INDIGO)
    stars_bg(d, 11, GOLD_SOFT, 40, 0, 0, 820, H)
    # medallion
    cx, cy = 410, 480
    d.ellipse([cx - 130, cy - 130, cx + 130, cy + 130], outline=GOLD_SOFT, width=4)
    star8(d, cx, cy, 60, GOLD_SOFT, width=4)
    for i in range(16):
        ang = 2 * math.pi * i / 16
        r0, r1 = 150, 195 if i % 2 == 0 else 172
        d.line([(cx + r0 * math.cos(ang), cy + r0 * math.sin(ang)),
                (cx + r1 * math.cos(ang), cy + r1 * math.sin(ang))], fill=GOLD_SOFT, width=3)
    f = F("serif", 76)
    center(d, 410, 760, "Spiritual Intention.", f, IVORY)
    center(d, 410, 860, "Grounded Action.", f, IVORY)
    checks = ["No filler pages", "No guaranteed-outcome hype", "Every intention ends in a real plan",
              "Honest about what the date is"]
    fy = 300
    fb = F("serif", 56)
    for cktext in checks:
        d.ellipse([900, fy + 8, 948, fy + 56], outline=GOLD, width=4)
        d.line([(912, fy + 32), (922, fy + 44)], fill=GOLD, width=5)
        d.line([(922, fy + 44), (938, fy + 18)], fill=GOLD, width=5)
        d.text((980, fy), cktext, font=fb, fill=INK)
        fy += 150
    im = render("letter", find_page("letter", "Intention-to-Outcome"), 560)
    shadow_paste(img, im, 1350, 940)
    fl = F("lato", 36)
    d.text((900, 1000), "Aligned-action planning,\nobstacle forecasts and\n30 days of integration\nare built into the book.", font=fl, fill=INK)
    footer(d)
    save(img, 3, "different")

def img04():
    img, d = base(IVORY)
    f = F("serif", 100)
    center(d, W // 2, 90, "An Eight-Day Activation", f, INDIGO)
    themes = ["Awareness", "Release", "Worthiness", "Courage", "Clarity", "Embodiment", "Action", "Activation"]
    y = 300
    xw = (W - 240) / 8.0
    fl = F("latob", 34)
    fs = F("serifsb", 56)
    d.line([(120 + xw / 2, y), (W - 120 - xw / 2, y)], fill=GOLD_SOFT, width=3)
    for i, t in enumerate(themes):
        cx = 120 + xw * i + xw / 2
        d.ellipse([cx - 44, y - 44, cx + 44, y + 44], fill=IVORY, outline=GOLD, width=4)
        w_ = d.textlength(str(i + 1), font=fs)
        d.text((cx - w_ / 2, y - 38), str(i + 1), font=fs, fill=INDIGO)
        w_ = d.textlength(t, font=fl)
        d.text((cx - w_ / 2, y + 70), t, font=fl, fill=INK)
    p1 = find_page("letter", "three truest sentences")
    p2 = find_page("letter", "Day 4 · Going Deeper")
    im1 = render("letter", p1, 900)
    im2 = render("letter", p2, 900)
    shadow_paste(img, im1, 340, 480, angle=2)
    shadow_paste(img, im2, 1000, 520, angle=-2)
    footer(d)
    save(img, 4, "eight_days")

def img05():
    img, d = base(INDIGO)
    stars_bg(d, 5, GOLD_SOFT, 60, 0, 0, W, 400)
    f = F("serif", 100)
    center(d, W // 2, 80, "Three Complete 8/8 Rituals", f, IVORY)
    fl = F("lato", 40)
    center(d, W // 2, 215, "15, 45 and 90 minutes · plus candle-free, crystal-free, secular, partner and circle versions", fl, GOLD_SOFT, maxw=1600)
    pages = [find_page("letter", "Prepare (1 min)"), find_page("letter", "Prepare (5 min)"), find_page("letter", "Threshold (10 min)")]
    x = 130
    for p in pages:
        im = render("letter", p, 1050)
        shadow_paste(img, im, x, 400)
        x += im.width + 60
    footer(d)
    save(img, 5, "rituals")

def img06():
    img, d = base(IVORY)
    f = F("serif", 100)
    center(d, W // 2, 90, "Become Her On Purpose", f, INDIGO)
    fl = F("lato", 42)
    center(d, W // 2, 220, "Self-concept work, future-self letters, the identity bridge, a daily embodiment menu", fl, INK, maxw=1500)
    p1 = find_page("letter", "The Future Self, Page One")
    p2 = find_page("letter", "The Identity Bridge")
    im1 = render("letter", p1, 1050)
    im2 = render("letter", p2, 1050)
    shadow_paste(img, im1, 300, 380, angle=1.5)
    shadow_paste(img, im2, 1080, 400, angle=-1.5)
    footer(d)
    save(img, 6, "self_concept")

def img07():
    img, d = base(WASH)
    f = F("serif", 100)
    center(d, W // 2, 90, "Money Work With Clear Eyes", f, INDIGO)
    fl = F("lato", 42)
    center(d, W // 2, 220, "Money story, receiving, honest next moves, a 30-day prosperity action map", fl, INK, maxw=1500)
    d.line([(W // 2 - 200, 300), (W // 2 + 200, 300)], fill=TERRA, width=4)
    p1 = find_page("letter", "Your Money Story")
    p2 = find_page("letter", "Thirty Days of Prosperity")
    im1 = render("letter", p1, 1050)
    im2 = render("letter", p2, 1050)
    shadow_paste(img, im1, 300, 380, angle=-1.5)
    shadow_paste(img, im2, 1080, 400, angle=1.5)
    fs = F("serifit", 40)
    center(d, W // 2, 1500, "No income promises, ever. Structure and honesty instead.", fs, INK)
    save(img, 7, "abundance")

def img08():
    img, d = base(IVORY)
    d.rectangle([0, 0, 700, H], fill=PLUM_PALE)
    # crescent
    d.ellipse([230, 240, 470, 480], outline=GOLD, width=5)
    d.ellipse([290, 230, 500, 440], fill=PLUM_PALE)
    f = F("serif", 84)
    center(d, 350, 560, "Release What", f, INDIGO)
    center(d, 350, 665, "Limits You", f, INDIGO)
    fl = F("lato", 38)
    center(d, 350, 800, "Trigger maps, inherited beliefs,", fl, INK)
    center(d, 350, 855, "believable reframes, and a", fl, INK)
    center(d, 350, 910, "full release ceremony.", fl, INK)
    p1 = find_page("letter", "The Trigger-to-Belief Map")
    p2 = find_page("letter", "Building the Believable Bridge")
    im1 = render("letter", p1, 1080)
    im2 = render("letter", p2, 1080)
    shadow_paste(img, im1, 780, 260, angle=1.5)
    shadow_paste(img, im2, 1420, 300, angle=-1.5)
    footer(d)
    save(img, 8, "shadow_release")

def img09():
    img, d = base(IVORY)
    f = F("serif", 100)
    center(d, W // 2, 90, "Scripting That Feels True", f, INDIGO)
    fl = F("lato", 42)
    center(d, W // 2, 220, "The 88-word script, worked examples, and 88 affirmations that do not lie to you", fl, INK, maxw=1560)
    p1 = find_page("letter", "The 88-Word Script")
    p2 = find_page("letter", "Eighty-Eight Affirmations")
    im1 = render("letter", p1, 1000)
    im2 = render("letter", p2, 1000)
    shadow_paste(img, im1, 240, 400, angle=1.5)
    shadow_paste(img, im2, 990, 420, angle=-1)
    # quote card
    card = Image.new("RGB", (420, 560), INDIGO)
    cd = ImageDraw.Draw(card)
    stars_bg(cd, 9, GOLD_SOFT, 16, 0, 0, 420, 560)
    star8(cd, 210, 110, 30, GOLD_SOFT)
    fq = F("serifit", 44)
    qy = 200
    for ln in wrap(cd, "Courage can be quiet and consistent.", fq, 330):
        w_ = cd.textlength(ln, font=fq)
        cd.text(((420 - w_) / 2, qy), ln, font=fq, fill=IVORY)
        qy += 56
    shadow_paste(img, card, 1560, 620)
    footer(d)
    save(img, 9, "scripting")

def img10():
    img, d = base(IVORY)
    f = F("serif", 96)
    center(d, W // 2, 80, "Release. Embody. Act. Integrate.", f, INDIGO)
    verbs = ["Release", "Embody", "Act", "Integrate"]
    fl = F("latob", 36)
    x = 330
    for i, v in enumerate(verbs):
        d.ellipse([x - 40, 230, x + 40, 310], outline=GOLD, width=4)
        fw = F("serifsb", 52)
        w_ = d.textlength(str(i + 1), font=fw)
        d.text((x - w_ / 2, 240), str(i + 1), font=fw, fill=INDIGO)
        w_ = d.textlength(v, font=fl)
        d.text((x - w_ / 2, 330), v, font=fl, fill=INK)
        x += 450
    p1 = find_page("letter", "Four Horizons")
    p2 = find_page("letter", "Keeping the Momentum")
    im1 = render("letter", p1, 1000)
    im2 = render("letter", p2, 1000)
    shadow_paste(img, im1, 320, 450, angle=-1.5)
    shadow_paste(img, im2, 1060, 470, angle=1.5)
    footer(d)
    save(img, 10, "action")

def img11():
    img, d = base(INDIGO)
    stars_bg(d, 13, GOLD_SOFT, 55, 0, 0, W, 380)
    f = F("serif", 96)
    center(d, W // 2, 80, "Optional Tools, Honest Framing", f, IVORY)
    fl = F("lato", 40)
    center(d, W // 2, 210, "Tarot spreads, crystal reference, symbols — and no-supplies versions of everything", fl, GOLD_SOFT, maxw=1600)
    p1 = find_page("letter", "The Lion's Gate Eight-Card Spread")
    p2 = find_page("letter", "A Working Crystal Shelf")
    im1 = render("letter", p1, 1050)
    im2 = render("letter", p2, 1050)
    shadow_paste(img, im1, 380, 380, angle=1)
    shadow_paste(img, im2, 1120, 400, angle=-1)
    fs = F("serifit", 42)
    center(d, W // 2, 1505, "Everything works with just a pen.", fs, GOLD_SOFT)
    save(img, 11, "tools")

def img12():
    img, d = base(IVORY)
    f = F("serif", 92)
    center(d, W // 2, 80, "Designed for Print, Tablet and Planner", f, INDIGO)
    fl = F("lato", 40)
    center(d, W // 2, 205, "US Letter + A4 print editions · digital annotation editions with clickable contents", fl, INK, maxw=1600)
    im1 = render("letter", find_page("letter", "How to Use This Experience", start=5), 1000)
    shadow_paste(img, im1, 240, 380, angle=-1)
    # tablet frame with digital page
    tab = render("digital", find_page("digital", "Where I Am Standing"), 900)
    frame = Image.new("RGB", (tab.width + 70, tab.height + 70), (28, 28, 34))
    frame.paste(tab, (35, 35))
    fr = ImageDraw.Draw(frame)
    fr.rounded_rectangle([6, 6, frame.width - 6, frame.height - 6], radius=28, outline=(70, 70, 80), width=4)
    shadow_paste(img, frame, 1080, 400)
    kicker(d, W // 2, 1500, "Digital download · nothing ships · annotation edition (no form fields)", 26, GOLD, ls=3)
    save(img, 12, "formats")

def img13():
    img, d = base(IVORY)
    f = F("serif", 92)
    center(d, W // 2, 70, "Four Planner Insert Sizes Included", f, INDIGO)
    fl = F("lato", 40)
    center(d, W // 2, 195, "Pocket 3.5×6 · Compact 4.25×6.75 · Classic 5.5×8.5 · Monarch 8.5×11 · print-and-trim files included", fl, INK, maxw=1700)
    # actual relative sizes: scale 105 px/inch
    scale = 76
    entries = [("pocket", 3.5, 6, "Pocket"), ("compact", 4.25, 6.75, "Compact"),
               ("classic", 5.5, 8.5, "Classic"), ("monarch", 8.5, 11, "Monarch")]
    x = 85
    fb = F("latob", 34)
    for key, wi, hi, label in entries:
        im = render(key, 0, int(hi * scale))
        y = 320 + int((11 - hi) * scale)
        shadow_paste(img, im, x, y)
        w_ = d.textlength(label, font=fb)
        d.text((x + im.width / 2 - w_ / 2, y + im.height + 18), label, font=fb, fill=INK)
        x += im.width + 60
    fn = F("lato", 26)
    note = ("Not affiliated with, sponsored by or endorsed by Franklin Planner or FranklinCovey; brand names identify "
            "compatible page dimensions only. Measure your existing pages before printing.")
    center(d, W // 2, 1520, note, fn, (110, 104, 120), maxw=1700)
    save(img, 13, "planner_sizes")

def img14():
    img, d = base(NIGHT)
    stars_bg(d, 17, GOLD_SOFT, 70, 0, 0, W, H)
    f = F("serif", 96)
    center(d, W // 2, 80, "Beautiful Enough to Keep", f, IVORY)
    fl = F("lato", 40)
    center(d, W // 2, 210, "32 affirmation cards · 9 planner tabs · 12 phone wallpapers in dark and light", fl, GOLD_SOFT, maxw=1600)
    im1 = render("cards", 0, 850)
    shadow_paste(img, im1, 170, 380, angle=1.5)
    im2 = render("tabs", 0, 850)
    shadow_paste(img, im2, 880, 400, angle=-1.5)
    for i, wp in enumerate(["LionsGate_Wallpaper_01_Dark.png", "LionsGate_Wallpaper_07_Light.png"]):
        p = os.path.join(ROOT, "08_Bonus_Files", "wallpapers", wp)
        wim = Image.open(p).resize((260, 563), Image.LANCZOS)
        fr = Image.new("RGB", (wim.width + 16, wim.height + 16), (28, 28, 34))
        fr.paste(wim, (8, 8))
        shadow_paste(img, fr, 1520 + i * 180, 420 + i * 120)
    footer(d)
    save(img, 14, "bonuses")

def img15():
    img, d = base(IVORY)
    kicker(d, W // 2, 110, "Before you buy · the honest fine print", 30, GOLD)
    f = F("serif", 100)
    center(d, W // 2, 170, "Personal-Use Digital Download", f, INDIGO)
    gold_rule(d, W // 2, 330)
    items = [
        "Instant download after purchase. No physical item will be shipped.",
        "Personal-use license for one person. Client, group and classroom licensing available by message.",
        "Reflective, educational and spiritual content. No outcomes are guaranteed, and honesty about that is part of the design.",
        "Works without crystals, cards, candles or any purchases. Every ritual has a no-supplies version.",
        "Franklin Planner and FranklinCovey are trademarks of their respective owners. This independent product is not affiliated with, sponsored by, approved by or endorsed by them; brand names identify compatible page dimensions only. Measure your planner pages before printing.",
        "Questions or file trouble? Message the shop through Etsy. A real person answers.",
    ]
    fl = F("lato", 42)
    y = 420
    for it in items:
        star8(d, 180, y + 26, 14, GOLD)
        lines = wrap(d, it, fl, 1520)
        for ln in lines:
            d.text((240, y), ln, font=fl, fill=INK)
            y += 56
        y += 52
    footer(d, "GlowHausDigital · The Lion's Gate 8/8 Activation")
    save(img, 15, "license_info")

if __name__ == "__main__":
    only = [int(a) for a in sys.argv[1:]] or range(1, 16)
    fns = {1: img01, 2: img02, 3: img03, 4: img04, 5: img05, 6: img06, 7: img07,
           8: img08, 9: img09, 10: img10, 11: img11, 12: img12, 13: img13, 14: img14, 15: img15}
    for i in only:
        fns[i]()
