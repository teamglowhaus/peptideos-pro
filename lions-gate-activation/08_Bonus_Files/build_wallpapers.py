# -*- coding: utf-8 -*-
"""Build the 12 phone wallpapers (light + dark variants) and zip them."""
import os, sys, math, zipfile, textwrap
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "02_Main_Workbook_Source"))
from PIL import Image, ImageDraw, ImageFont
from affirmations import WALLPAPERS

W, H = 1170, 2532          # standard modern phone canvas; scales cleanly
FONTS = os.path.join(ROOT, "02_Main_Workbook_Source", "assets", "fonts")

INDIGO = (30, 33, 58)
INDIGO_DEEP = (22, 24, 44)
IVORY = (250, 246, 238)
CREAM = (253, 251, 244)
GOLD = (196, 168, 110)
GOLD_SOFT = (216, 196, 150)
INK = (43, 40, 60)

def rand_seq(seed):
    s = seed
    while True:
        s = (s * 9301 + 49297) % 233280
        yield s / 233280.0

def stars(d, seed, color, n=70, y0=0, y1=H):
    r = rand_seq(seed)
    for i in range(n):
        x = next(r) * W
        y = y0 + next(r) * (y1 - y0)
        size = next(r)
        if i % 11 == 0:
            s = 7 + size * 7
            d.line([(x - s, y), (x + s, y)], fill=color, width=2)
            d.line([(x, y - s), (x, y + s)], fill=color, width=2)
            d.line([(x - s * 0.45, y - s * 0.45), (x + s * 0.45, y + s * 0.45)], fill=color, width=1)
            d.line([(x - s * 0.45, y + s * 0.45), (x + s * 0.45, y - s * 0.45)], fill=color, width=1)
        else:
            rad = 1 + size * 2.4
            d.ellipse([x - rad, y - rad, x + rad, y + rad], fill=color)

def arch(d, cx, cy, w, h, color, width=3, layers=3, gap=26):
    """Round-top arch: dome at the top (cy), legs running down to cy + h."""
    for i in range(layers):
        ww = width if i == 0 else max(1, width - 1)
        aw = w - 2 * i * gap
        y_top = cy + i * gap
        bottom = cy + h
        r = aw / 2
        x0 = cx - r
        d.arc([x0, y_top, x0 + aw, y_top + 2 * r], 180, 360, fill=color, width=ww)
        d.line([(x0, y_top + r), (x0, bottom)], fill=color, width=ww)
        d.line([(x0 + aw, y_top + r), (x0 + aw, bottom)], fill=color, width=ww)

def eight_star(d, cx, cy, R, color, width=2):
    pts = []
    for i in range(16):
        ang = math.pi / 8 * i - math.pi / 2
        rad = R if i % 2 == 0 else R * 0.36
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(pts, outline=color, width=width)

def wrap_text(text, font, maxw, d):
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) > maxw and cur:
            lines.append(cur); cur = w_
        else:
            cur = t
    if cur: lines.append(cur)
    return lines

def make(idx, text, dark, out):
    img = Image.new("RGB", (W, H), INDIGO if dark else IVORY)
    d = ImageDraw.Draw(img)
    if dark:
        # vertical gradient
        for y in range(H):
            t = y / H
            c = tuple(int(a + (b - a) * t) for a, b in zip(INDIGO, INDIGO_DEEP))
            d.line([(0, y), (W, y)], fill=c)
        stars(d, seed=idx * 7 + 3, color=GOLD_SOFT, n=64, y0=int(H * 0.06), y1=int(H * 0.46))
        stars(d, seed=idx * 13 + 5, color=(120, 116, 96), n=30, y0=int(H * 0.72), y1=int(H * 0.97))
        fg, accent = IVORY, GOLD_SOFT
    else:
        for y in range(H):
            t = y / H
            c = tuple(int(a + (b - a) * t) for a, b in zip(CREAM, (244, 236, 220)))
            d.line([(0, y), (W, y)], fill=c)
        stars(d, seed=idx * 7 + 3, color=(214, 200, 168), n=40, y0=int(H * 0.06), y1=int(H * 0.4))
        fg, accent = INK, GOLD
    # motif: arch + star, upper-middle (below clock zone)
    arch_top = int(H * 0.30)
    arch(d, W / 2, arch_top, 360, 330, accent, width=3)
    eight_star(d, W / 2, arch_top + 205, 46, accent, width=3)
    # text block centered ~0.55-0.68 height (safe zone between clock and dock)
    serif = ImageFont.truetype(os.path.join(FONTS, "CormorantGaramond-500.ttf"), 92)
    lines = wrap_text(text, serif, int(W * 0.74), d)
    if len(lines) > 4:
        serif = ImageFont.truetype(os.path.join(FONTS, "CormorantGaramond-500.ttf"), 78)
        lines = wrap_text(text, serif, int(W * 0.76), d)
    lh = int(serif.size * 1.22)
    total = len(lines) * lh
    y = int(H * 0.60) - total // 2
    for ln in lines:
        w_ = d.textlength(ln, font=serif)
        d.text(((W - w_) / 2, y), ln, font=serif, fill=fg)
        y += lh
    # small mark
    marc = ImageFont.truetype(os.path.join(FONTS, "Marcellus-400.ttf"), 34)
    mark = "8 · 8"
    w_ = d.textlength(mark, font=marc)
    d.text(((W - w_) / 2, int(H * 0.755)), mark, font=marc, fill=accent)
    d.line([(W / 2 - 90, H * 0.80), (W / 2 - 24, H * 0.80)], fill=accent, width=2)
    d.line([(W / 2 + 24, H * 0.80), (W / 2 + 90, H * 0.80)], fill=accent, width=2)
    eight_star(d, W / 2, int(H * 0.80), 12, accent, width=2)
    img.save(out, "PNG")

README = """THE LION'S GATE 8/8 ACTIVATION — PHONE WALLPAPERS
(c) 2026 GlowHausDigital. All rights reserved.

WHAT'S HERE
12 affirmation wallpapers, each in a Dark (midnight indigo) and a Light
(warm ivory) version. Sized 1170 x 2532 px, which displays beautifully on
virtually all current phones; your phone will scale it automatically.

HOW TO INSTALL
iPhone: save the image to Photos, then Settings > Wallpaper > Add New
Wallpaper > Photos, choose the image, position it, and set as Lock Screen,
Home Screen, or both.
Android: save the image, open it in Photos/Gallery, tap the menu (three
dots) > Use as > Wallpaper, then choose Lock screen or Home screen.
Tip: the text sits in the middle band on purpose, clear of the clock and
the app dock on most phones. If your launcher crops differently, use your
phone's reposition/zoom controls when setting it.

LICENSE (SHORT VERSION)
For your personal use on your own devices only. Please do not share the
files or the ZIP, repost the designs, use them commercially, or include
them in any product or service. The full Personal-Use License is inside
the main workbook.

THANK YOU
Thank you for letting these small reminders live where your attention
lives. If they support your season, an honest review on Etsy helps
another reader find them. — GlowHausDigital
"""

if __name__ == "__main__":
    outdir = os.path.join(HERE, "wallpapers")
    os.makedirs(outdir, exist_ok=True)
    files = []
    for i, text in enumerate(WALLPAPERS, 1):
        for dark in (True, False):
            name = "LionsGate_Wallpaper_%02d_%s.png" % (i, "Dark" if dark else "Light")
            make(i, text, dark, os.path.join(outdir, name))
            files.append(name)
    with open(os.path.join(outdir, "READ_ME_Wallpapers.txt"), "w") as f:
        f.write(README)
    zpath = os.path.join(HERE, "Lions_Gate_Phone_Wallpapers.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(os.path.join(outdir, "READ_ME_Wallpapers.txt"), "READ_ME_Wallpapers.txt")
        for name in files:
            z.write(os.path.join(outdir, name), name)
    print("wallpapers zip:", zpath, len(files), "images")
