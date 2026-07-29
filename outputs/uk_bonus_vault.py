# -*- coding: utf-8 -*-
"""
Скарбниця бонусів — Портал 369 (Ukrainian Bonus Vault)
10 pages, built independently for US Letter and A4.
Design mirrors the English Bonus Vault: gold-on-ink luxury, Lora/Arsenal/Jura.
"""
import os, math, random
from reportlab.pdfgen import canvas as rlc
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

HERE = os.path.dirname(os.path.abspath(__file__))
FD   = "/mnt/skills/examples/canvas-design/canvas-fonts"

INK    = HexColor("#1a1410")
GOLD   = HexColor("#c9a84c")
DGOLD  = HexColor("#a08034")
CREAM  = HexColor("#faf6f0")
DARKBG = HexColor("#120e0b")
WTEXT  = HexColor("#ede5cc")
LGOLD  = HexColor("#e0c060")
BFILL  = HexColor("#ece7de")

W = H = M = IW = None   # set per size


def fonts():
    for n, f in [("Lora", "Lora-Regular.ttf"), ("LoraI", "Lora-Italic.ttf"),
                 ("LoraB", "Lora-Bold.ttf"), ("Ars", "ArsenalSC-Regular.ttf"),
                 ("Jura", "Jura-Light.ttf")]:
        pdfmetrics.registerFont(TTFont(n, os.path.join(FD, f)))
    pdfmetrics.registerFont(TTFont("Sym", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))


def corner_marks(c, color=GOLD):
    arm, pad = 14, 26
    c.saveState(); c.setStrokeColor(color); c.setLineWidth(0.8)
    for (x, y, sx, sy) in [(pad, H-pad, 1, -1), (W-pad, H-pad, -1, -1),
                           (pad, pad, 1, 1), (W-pad, pad, -1, 1)]:
        c.line(x, y, x+sx*arm, y); c.line(x, y, x, y+sy*arm)
    c.restoreState()


def cream_bg(c):
    c.saveState(); c.setFillColor(CREAM); c.rect(0, 0, W, H, stroke=0, fill=1); c.restoreState()


def dark_bg(c):
    c.saveState(); c.setFillColor(DARKBG); c.rect(0, 0, W, H, stroke=0, fill=1); c.restoreState()


def starfield(c, n=110, seed=9):
    rnd = random.Random(seed)
    c.saveState()
    for _ in range(n):
        x, y = rnd.uniform(0, W), rnd.uniform(0, H)
        r = rnd.choice([0.5, 0.7, 0.9, 1.3])
        a = rnd.uniform(0.15, 0.6)
        c.setFillColor(LGOLD); c.setFillAlpha(a)
        c.circle(x, y, r, stroke=0, fill=1)
    c.restoreState()


def seed_of_life(c, cx, cy, r, color=LGOLD, alpha=0.85, lw=1.1):
    c.saveState(); c.setStrokeColor(color); c.setStrokeAlpha(alpha)
    c.setFillAlpha(0); c.setLineWidth(lw)
    pts = [(0, 0)] + [(r*math.cos(math.pi/3*i), r*math.sin(math.pi/3*i)) for i in range(6)]
    for ox, oy in pts:
        c.circle(cx+ox, cy+oy, r, stroke=1, fill=0)
    c.setLineWidth(0.8)
    for rr in (2*r*1.02, 2*r*1.14, 2*r*1.30):
        c.setStrokeAlpha(alpha*0.5)
        c.circle(cx, cy, rr, stroke=1, fill=0)
    c.restoreState()


def glow(c, cx, cy, rmax, color=LGOLD, steps=24, amax=0.05):
    c.saveState(); c.setFillColor(color)
    for i in range(steps, 0, -1):
        c.setFillAlpha(amax*(1-i/steps))
        c.circle(cx, cy, rmax*i/steps, stroke=0, fill=1)
    c.restoreState()


def rule(c, y, color=GOLD, x0=None, x1=None, w=0.75):
    c.saveState(); c.setStrokeColor(color); c.setLineWidth(w)
    c.line(x0 or M, y, x1 or W-M, y); c.restoreState()


def diamond_rule(c, y):
    mid = W/2
    c.saveState(); c.setStrokeColor(GOLD); c.setLineWidth(0.75)
    c.line(M, y, mid-10, y); c.line(mid+10, y, W-M, y)
    c.setFillColor(GOLD); c.setFont("Sym", 9)
    c.drawCentredString(mid, y-3.5, "◆")
    c.restoreState()


def footer(c, text="ПОРТАЛ 369  ·  СКАРБНИЦЯ БОНУСІВ", dark=False):
    c.saveState()
    c.setStrokeColor(LGOLD if dark else GOLD); c.setLineWidth(0.6)
    c.line(M+30, 40, W-M-30, 40)
    c.setFillColor(LGOLD if dark else DGOLD); c.setFont("Ars", 8)
    c.drawCentredString(W/2, 26, text)
    c.restoreState()


def wrap(c, text, font, size, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur+" "+w_).strip()
        if c.stringWidth(t, font, size) <= maxw or not cur: cur = t
        else: lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines


def para(c, text, x, y, maxw, font="Lora", size=10.5, lh=15, color=INK):
    c.setFillColor(color); c.setFont(font, size)
    for ln in wrap(c, text, font, size, maxw):
        c.drawString(x, y, ln); y -= lh
    return y


def bonus_header(c, tag, title, subtitle):
    corner_marks(c)
    y = H - M - 14
    c.setFillColor(DGOLD); c.setFont("Ars", 11)
    c.drawCentredString(W/2, y, tag)
    y -= 12; rule(c, y); y -= 40
    c.setFillColor(INK); c.setFont("Lora", 30)
    c.drawCentredString(W/2, y, title)
    y -= 20
    c.setFillColor(INK); c.setFont("LoraI", 12)
    c.drawCentredString(W/2, y, subtitle)
    y -= 14; diamond_rule(c, y); y -= 28
    return y


# ═══ Page 1 — Cover ═══════════════════════════════════════════════════════════
def p_cover(c):
    dark_bg(c); starfield(c)
    cy = H*0.55
    glow(c, W/2, cy, W*0.30)
    seed_of_life(c, W/2, cy, W*0.105)
    glow(c, W/2, cy, W*0.045, amax=0.5)

    y = H - M - 50
    c.setFillColor(LGOLD); c.setFont("Ars", 13)
    c.drawCentredString(W/2, y, "ТИ ЩОЙНО ВІДКРИЛА")
    y -= 44
    c.setFillColor(WTEXT); c.setFont("Lora", 44)
    c.drawCentredString(W/2, y, "СКАРБНИЦЮ БОНУСІВ")
    y -= 14; rule(c, y, LGOLD, M+70, W-M-70, 0.9); y -= 26
    c.setFillColor(LGOLD); c.setFont("LoraI", 14)
    c.drawCentredString(W/2, y, "П'ять дарунків, щоб підсилити твою практику 369")

    items = ["ШВИДКИЙ СТАРТ 369", "НАБІР ДЛЯ ДОШКИ ВІЗУАЛІЗАЦІЇ",
             "30 КАРТОК АФІРМАЦІЙ", "ЧЕКИ МАНІФЕСТАЦІЇ",
             "ШПАЛЕРИ ДЛЯ ТЕЛЕФОНА Й ПЛАНШЕТА"]
    y = cy - W*0.16
    c.setFont("Ars", 12)
    for it in items:
        c.setFillColor(LGOLD)
        c.drawCentredString(W/2, y, it)
        y -= 26

    y -= 22
    c.setFillColor(WTEXT); c.setFont("LoraI", 11)
    c.drawCentredString(W/2, y, "Дякую, що обрала «Портал». Твоя підтримка означає все.")
    y -= 18
    c.drawCentredString(W/2, y, "Слідкуй за повідомленнями на Etsy — там на тебе чекає знижка на наступне замовлення.")

    c.setFillColor(LGOLD); c.setFont("Ars", 8)
    c.drawCentredString(W/2, 40, "GLOWHAUS DIGITAL · 2026")


# ═══ Page 2 — Quick-start ═════════════════════════════════════════════════════
def p_quickstart(c):
    cream_bg(c)
    y = bonus_header(c, "БОНУС 1", "Швидкий старт 369",
                     "Усе, що потрібно, щоб почати вже сьогодні, — на одній сторінці.")
    steps = [
        ("ОБЕРИ ОДНЕ БАЖАННЯ",
         "Одне конкретне бажання. Не п'ять — одне. Метод 369 працює через сфокусоване "
         "повторення: один чіткий сигнал завжди сильніший за розсіяний."),
        ("СФОРМУЛЮЙ СВОЄ ТВЕРДЖЕННЯ",
         "Формула: «Я така вдячна й щаслива тепер, коли [бажання], бо [почуття].» "
         "Теперішній час. Емоційно наповнено. Конкретно."),
        ("РАНОК — НАПИШИ 3 РАЗИ",
         "Протягом години після пробудження, ще до телефона. Відчувай кожне слово, "
         "коли пишеш. Це садить зерно на весь день."),
        ("ОПІВДНІ — НАПИШИ 6 РАЗІВ",
         "Близько обіду. Стиш шум, зроби три глибокі вдихи, повернися до бажання. "
         "Це підсилює ранковий сигнал саме тоді, коли енергія спадає."),
        ("ВЕЧІР — НАПИШИ 9 РАЗІВ",
         "Протягом години перед сном. Підсвідомість опрацьовує те, що отримала "
         "останнім. Пиши з повною віддачею — а потім повністю відпусти."),
        ("ВІДСТЕЖУЙ ЗНАКИ",
         "Ангельські числа, несподівані дзвінки, суголосні миті. Занотовуй кожен у "
         "щоденнику. Докази накопичуються — а віра йде за доказами."),
    ]
    for i, (t, d) in enumerate(steps, 1):
        c.saveState()
        c.setStrokeColor(GOLD); c.setLineWidth(1.2); c.setFillAlpha(0)
        c.circle(M+13, y-2, 12, stroke=1, fill=0); c.restoreState()
        c.setFillColor(INK); c.setFont("LoraI", 13)
        c.drawCentredString(M+13, y-6, str(i))
        c.setFillColor(INK); c.setFont("Ars", 12)
        c.drawString(M+36, y-4, t)
        y -= 22
        y = para(c, d, M+36, y, IW-46) - 8
        if i < 6: rule(c, y+4, GOLD); y -= 14
    y -= 6
    c.saveState()
    c.setStrokeColor(GOLD); c.setLineWidth(1); c.setFillColor(HexColor("#f4eddd"))
    bh = 52
    c.rect(M, y-bh, IW, bh, stroke=1, fill=1); c.restoreState()
    c.setFillColor(INK); c.setFont("LoraI", 11.5)
    c.drawCentredString(W/2, y-20, "Одне бажання. Три сесії. Двадцять вісім днів. Це весь метод.")
    c.drawCentredString(W/2, y-38, "Щоденник тримає структуру — тобі лишається просто приходити.")
    footer(c)


# ═══ Page 3 — Vision board ════════════════════════════════════════════════════
def p_visionboard(c):
    cream_bg(c)
    y = bonus_header(c, "БОНУС 2", "Набір для дошки візуалізації",
                     "Твої бажання заслуговують бути на видноті щодня. Створи дошку, яка тримає їх живими.")
    secs = [
        ("ЗБЕРИ", "Роздрукуй слова для вирізання з наступної сторінки. Додай зображення "
                  "з журналів, фотографії або роздруківки — ті, від яких у грудях стає ширше."),
        ("РОЗМІСТИ", "Використай сітку з 9 зон, постер або коркову дошку. Постав формулювання "
                     "свого бажання 369 у самий центр — усе інше обертається навколо нього."),
        ("АКТИВУЙ", "Дивися на дошку під час кожної сесії письма 369. Образ + написане "
                    "повторення + почуття — це сигнал повного спектра."),
        ("ОНОВЛЮЙ", "На кожен молодик прибирай те, що більше не відгукується, і додавай нове. "
                    "Жива дошка маніфестує. Застигла — лише прикрашає."),
    ]
    for t, d in secs:
        c.setFillColor(DGOLD); c.setFont("Ars", 12)
        c.drawString(M, y, t); y -= 20
        y = para(c, d, M, y, IW) - 6
        rule(c, y+2, GOLD); y -= 20
    c.setFillColor(INK); c.setFont("Ars", 11)
    c.drawString(M, y, "9 ЗОН ПОВНОЦІННОГО ЖИТТЯ:")
    y -= 16
    zones = ["ЛЮБОВ", "ДОБРОБУТ", "ЗДОРОВ'Я",
             "ДІМ", "ПРИЗНАЧЕННЯ", "СВОБОДА",
             "РАДІСТЬ", "ДУХ", "НАЙВИЩА Я"]
    bw = (IW - 40) / 3; bh = 40
    for i, z in enumerate(zones):
        x = M + (i % 3) * (bw + 20)
        yy = y - (i // 3) * (bh + 12)
        c.saveState()
        c.setFillColor(BFILL); c.setStrokeColor(GOLD); c.setLineWidth(1)
        c.rect(x, yy-bh, bw, bh, stroke=1, fill=1); c.restoreState()
        c.setFillColor(INK); c.setFont("Ars", 11)
        c.drawCentredString(x+bw/2, yy-bh/2-4, z)
    footer(c)


# ═══ Page 4 — Word cut-outs ═══════════════════════════════════════════════════
def p_cutouts(c):
    cream_bg(c); corner_marks(c)
    y = H - M - 14
    c.setFillColor(DGOLD); c.setFont("Ars", 11)
    c.drawCentredString(W/2, y, "НАБІР ДЛЯ ДОШКИ ВІЗУАЛІЗАЦІЇ · СЛОВА ДЛЯ ВИРІЗАННЯ · ДРУКУЙ І РІЖ")
    y -= 12; rule(c, y); y -= 30
    words = ["ДОСТАТОК", "Я ГІДНА", "СВОБОДА", "ЛЮБОВ",
             "ГРОШІ ТЕЧУТЬ", "ДИВА", "ВДЯЧНІСТЬ", "СИЛА",
             "РАДІСТЬ", "Я ОБИРАЮ СЕБЕ", "ГАРМОНІЯ", "УСПІХ",
             "НАТХНЕННЯ", "ДОВІРА", "ЛЕГКІСТЬ", "ЩЕДРІСТЬ",
             "Я СЯЮ", "ЕНЕРГІЯ", "СПОКІЙ", "ТУТ І ЗАРАЗ",
             "МОЄ ВЖЕ МОЄ", "ЗДОРОВ'Я", "БЕЗМЕЖНІСТЬ", "Я ВДЯЧНА"]
    cols = 2
    bw = (IW - 24) / cols
    bh = (y - 70) / 12 - 8
    for i, w_ in enumerate(words):
        x = M + (i % cols) * (bw + 24)
        yy = y - (i // cols) * (bh + 8)
        c.saveState()
        c.setStrokeColor(DGOLD); c.setLineWidth(0.8); c.setDash(4, 3)
        c.rect(x, yy-bh, bw, bh, stroke=1, fill=0); c.restoreState()
        size = 17 if len(w_) <= 12 else 14
        c.setFillColor(INK); c.setFont("Lora", size)
        c.drawCentredString(x+bw/2, yy-bh/2-5, w_)
    footer(c, "ДРУКУЙ НА ЩІЛЬНОМУ ПАПЕРІ  ·  РІЖ УЗДОВЖ ПУНКТИРНИХ ЛІНІЙ")


# ═══ Pages 5-7 — Affirmation cards ════════════════════════════════════════════
CARDS = [
 "Я така вдячна й щаслива тепер, коли достаток тече до мене з легкістю.",
 "Усе, чого я бажаю, вже в дорозі до мене.",
 "Я — магніт для див, грошей і суголосних можливостей.",
 "Всесвіт щомиті діє на мою користь.",
 "Я відпускаю весь опір і дозволяю своїм бажанням здійснитися.",
 "Моя частота зростає щодня.",
 "Я гідна всього, що закликаю у своє життя.",
 "Те, що призначене мені, не омине мене.",
 "Я повністю довіряю божественному таймінгу.",
 "Мої думки творять мою реальність, і я обираю їх свідомо.",
 "Мені безпечно отримувати більше, ніж я будь-коли мала.",
 "Гроші люблять мене й повертаються до мене знову і знову.",
 "Я дозволяю добру знаходити мене без зусиль.",
 "Кожен мій подих наближає моє бажання.",
 "Я живу у стані вдячності, і Всесвіт це чує.",
 "Моє серце відкрите для чудес.",
 "Я вже є тією версією себе, яка має все це.",
 "Знаки та синхронічності ведуть мене щодня.",
 "Я обираю віру замість сумніву.",
 "Моя енергія притягує саме те, що мені потрібно.",
 "Мої мрії не завеликі. Моя віра розширюється, щоб умістити їх.",
 "Я з любов'ю відпускаю минуле і створюю нове.",
 "Достаток — мій природний стан.",
 "Я щодня притягую щасливі випадковості.",
 "Усе складається для мене найкращим чином.",
 "Я довіряю собі та своєму шляху.",
 "Моя вібрація сьогодні вища, ніж учора.",
 "Я приймаю любов, підтримку і достаток з відкритим серцем.",
 "Я створюю своє життя словом, почуттям і дією.",
 "Портал відчинено — і я входжу в нього.",
]

def p_cards(c, part):
    cream_bg(c); corner_marks(c)
    lo, hi = part*10+1, part*10+10
    y = H - M - 14
    c.setFillColor(DGOLD); c.setFont("Ars", 11)
    c.drawCentredString(W/2, y, f"БОНУС 3 · КАРТКИ АФІРМАЦІЙ · {lo}–{hi}")
    y -= 12; rule(c, y); y -= 24
    cards = CARDS[part*10:part*10+10]
    cols, rows = 2, 5
    gap = 14
    bw = (IW - gap) / cols
    bh = (y - 64 - (rows-1)*gap) / rows
    for i, txt in enumerate(cards):
        x = M + (i % cols) * (bw + gap)
        yy = y - (i // cols) * (bh + gap)
        c.saveState()
        c.setStrokeColor(DGOLD); c.setLineWidth(0.8); c.setDash(4, 3)
        c.rect(x, yy-bh, bw, bh, stroke=1, fill=0)
        c.setDash()
        c.setStrokeColor(GOLD); c.setLineWidth(0.9)
        c.roundRect(x+5, yy-bh+5, bw-10, bh-10, 7, stroke=1, fill=0)
        c.restoreState()
        c.setFillColor(DGOLD); c.setFont("Ars", 9)
        c.drawCentredString(x+bw/2, yy-20, "3 · 6 · 9")
        lines = wrap(c, "«"+txt+"»", "LoraI", 10.5, bw-36)
        ty = yy - bh/2 + (len(lines)-1)*7
        c.setFillColor(INK); c.setFont("LoraI", 10.5)
        for ln in lines:
            c.drawCentredString(x+bw/2, ty, ln); ty -= 14
        c.setFillColor(DGOLD); c.setFont("Ars", 7.5)
        c.drawCentredString(x+bw/2, yy-bh+14, f"{part*10+i+1} З 30")
    footer(c, "ДРУКУЙ НА ЩІЛЬНОМУ ПАПЕРІ  ·  РІЖ УЗДОВЖ ПУНКТИРНИХ ЛІНІЙ")


# ═══ Pages 8-9 — Manifestation checks ═════════════════════════════════════════
def _check(c, x, y_top, w_, h_):
    c.saveState()
    c.setStrokeColor(GOLD); c.setLineWidth(1.4)
    c.roundRect(x, y_top-h_, w_, h_, 10, stroke=1, fill=0)
    c.setLineWidth(0.6)
    c.roundRect(x+5, y_top-h_+5, w_-10, h_-10, 7, stroke=1, fill=0)
    for (ox, oy) in [(14, -14), (w_-14, -14), (14, -h_+14), (w_-14, -h_+14)]:
        c.circle(x+ox, y_top+oy, 4, stroke=1, fill=0)
    c.restoreState()
    pad = 26
    yy = y_top - 32
    c.setFillColor(INK); c.setFont("Lora", 17)
    c.drawString(x+pad, yy, "БАНК ВСЕСВІТНЬОГО ДОСТАТКУ")
    c.setFont("Ars", 9); c.setFillColor(DGOLD)
    dtx = x + w_ - pad - 110
    c.drawString(dtx, yy+2, "ДАТА")
    c.saveState(); c.setStrokeColor(INK); c.setLineWidth(0.7)
    c.line(dtx+34, yy, x+w_-pad, yy); c.restoreState()
    yy -= 15
    c.setFillColor(DGOLD); c.setFont("Ars", 8.5)
    c.drawString(x+pad, yy, "ФІЛІЯ 3 · 6 · 9   ·   БЕЗМЕЖНІ КОШТИ ДОСТУПНІ")
    yy -= 34
    c.setFillColor(INK); c.setFont("Ars", 9.5)
    c.drawString(x+pad, yy+9, "ОТРИМУВАЧ")
    c.saveState(); c.setStrokeColor(INK); c.setLineWidth(0.7)
    c.line(x+pad+78, yy+6, x+w_-pad-140, yy+6); c.restoreState()
    c.saveState()
    c.setStrokeColor(GOLD); c.setLineWidth(1.1)
    c.rect(x+w_-pad-120, yy-6, 120, 30, stroke=1, fill=0)
    c.restoreState()
    c.setFillColor(DGOLD); c.setFont("Sym", 13)
    c.drawString(x+w_-pad-112, yy+2, "₴")
    yy -= 32
    c.saveState(); c.setStrokeColor(INK); c.setLineWidth(0.7)
    c.line(x+pad, yy, x+w_-pad-80, yy); c.restoreState()
    c.setFillColor(INK); c.setFont("Ars", 9.5)
    c.drawString(x+w_-pad-70, yy+2, "СЛОВАМИ")
    yy -= 44
    c.setFont("Ars", 9.5)
    c.drawString(x+pad, yy+2, "ПРИЗНАЧЕННЯ")
    c.saveState(); c.setStrokeColor(INK); c.setLineWidth(0.7)
    c.line(x+pad+92, yy, x+pad+230, yy)
    c.restoreState()
    c.drawString(x+w_-pad-210, yy+2, "ПІДПИС")
    c.saveState(); c.setStrokeColor(INK); c.setLineWidth(0.7)
    c.line(x+w_-pad-152, yy, x+w_-pad, yy); c.restoreState()
    c.setFillColor(DGOLD); c.setFont("LoraI", 9)
    c.drawCentredString(x+w_/2, y_top-h_+16,
        "«Всесвіт — моє джерело. Достаток — моє право від народження.»")


def p_checks(c, second=False):
    cream_bg(c); corner_marks(c)
    y = H - M - 14
    c.setFillColor(DGOLD); c.setFont("Ars", 11)
    c.drawCentredString(W/2, y, "БОНУС 4 · ЧЕКИ МАНІФЕСТАЦІЇ 369 · ДРУКУЙ І ЗАПОВНЮЙ")
    y -= 12; rule(c, y); y -= 34
    if not second:
        c.setFillColor(INK); c.setFont("Lora", 26)
        c.drawCentredString(W/2, y, "Банк Всесвітнього Достатку")
        y -= 20
        c.setFillColor(INK); c.setFont("LoraI", 11.5)
        c.drawCentredString(W/2, y, "Випиши собі чек від Всесвіту. Постав дату. Підпиши. Тримай на видноті щодня.")
        y -= 12; diamond_rule(c, y)
    else:
        c.setFillColor(INK); c.setFont("LoraI", 12)
        c.drawCentredString(W/2, y, "Випиши по одному на кожен місячний цикл — або подаруй тому, кого любиш.")
        y -= 10; diamond_rule(c, y)
    y -= 30
    ch = (y - 70) / 2 - 18
    ch = min(ch, 250)
    _check(c, M, y, IW, ch)
    _check(c, M, y - ch - 30, IW, ch)
    footer(c, "ПИШИ  ·  ВІР  ·  ОТРИМУЙ")


# ═══ Page 10 — Wallpapers ═════════════════════════════════════════════════════
def p_wallpapers(c):
    dark_bg(c); starfield(c, seed=12)
    cy = H*0.63
    glow(c, W/2, cy, W*0.22)
    seed_of_life(c, W/2, cy, W*0.075)
    glow(c, W/2, cy, W*0.035, amax=0.5)

    y = H - M - 30
    c.setFillColor(LGOLD); c.setFont("Ars", 12)
    c.drawCentredString(W/2, y, "БОНУС 5 · ШПАЛЕРИ ДЛЯ ТЕЛЕФОНА Й ПЛАНШЕТА")
    y -= 46
    c.setFillColor(WTEXT); c.setFont("Lora", 34)
    c.drawCentredString(W/2, y, "Неси частоту із собою")
    y -= 34
    c.setFillColor(LGOLD); c.setFont("LoraI", 12)
    c.drawCentredString(W/2, y, "Кремові й зоряні шпалери, створені, щоб твоє бажання")
    y -= 18
    c.drawCentredString(W/2, y, "було перед очима щоразу, як ти дивишся на телефон.")

    by = cy - W*0.24
    bw, bh = IW*0.72, 74
    bx = W/2 - bw/2
    c.saveState()
    c.setStrokeColor(LGOLD); c.setLineWidth(1.2)
    c.roundRect(bx, by-bh, bw, bh, 12, stroke=1, fill=0)
    c.restoreState()
    c.setFillColor(LGOLD); c.setFont("Ars", 11)
    c.drawCentredString(W/2, by-24, "ЗАВАНТАЖ СВОЇ ШПАЛЕРИ ТУТ:")
    c.setFillColor(WTEXT); c.setFont("Jura", 10.5)
    c.drawCentredString(W/2, by-42, "drive.google.com/drive/folders/")
    c.drawCentredString(W/2, by-58, "1Vw1oyMQY7N_k3g4qp2oE2gLQK371fJ0x")

    y = by - bh - 40
    c.setFillColor(WTEXT); c.setFont("LoraI", 10.5)
    c.drawCentredString(W/2, y, "Напиши мені на Etsy, якщо виникнуть труднощі з доступом до бонусів.")
    y -= 16
    c.drawCentredString(W/2, y, "Відповідаю протягом 24 годин і завжди рада допомогти.")

    y -= 56
    c.setFillColor(LGOLD); c.setFont("Lora", 24)
    c.drawCentredString(W/2, y, "3   ·   6   ·   9")
    y -= 24
    c.setFont("Ars", 11)
    c.drawCentredString(W/2, y, "ПИШИ  ·  ВІР  ·  ОТРИМУЙ")

    c.setFillColor(LGOLD); c.setFont("Ars", 8)
    c.drawCentredString(W/2, 40, "© 2026 GLOWHAUS DIGITAL · ЛИШЕ ДЛЯ ОСОБИСТОГО ВИКОРИСТАННЯ")


def build(pagesize, out, label):
    global W, H, M, IW
    W, H = pagesize
    M = 0.75 * inch
    IW = W - 2*M
    c = rlc.Canvas(out, pagesize=pagesize)
    p_cover(c);        c.showPage()
    p_quickstart(c);   c.showPage()
    p_visionboard(c);  c.showPage()
    p_cutouts(c);      c.showPage()
    for part in range(3):
        p_cards(c, part); c.showPage()
    p_checks(c, False); c.showPage()
    p_checks(c, True);  c.showPage()
    p_wallpapers(c);    c.showPage()
    c.save()
    print(f"Saved  {out}  (10 pages, {os.path.getsize(out)//1024} KB)  [{label}]")


if __name__ == "__main__":
    fonts()
    build(letter, os.path.join(HERE, "Скарбниця бонусів — Портал 369 — US Letter.pdf"), "US LETTER")
    build(A4,     os.path.join(HERE, "Скарбниця бонусів — Портал 369 — A4.pdf"), "A4")
