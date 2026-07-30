# -*- coding: utf-8 -*-
"""Build bonus files: Quick-Start guide, affirmation cards (Letter + A4),
planner tabs (Letter + A4)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "02_Main_Workbook_Source"))
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.pdfbase import pdfmetrics
from lg import theme as T, engine, motifs as M
from affirmations import CARD_SETS

IN = 72.0
MM = 72.0 / 25.4
T.register_fonts()

# ================================================================ QUICK START
QS_PAGES = [
{"kind": "cover", "title": "The Lion's Gate Quick Start",
 "subtitle": "Fifteen honest minutes for anyone beginning close to August 8",
 "tagline": "Part of The Lion's Gate 8/8 Activation"},
{
 "family": "front", "section": "Quick Start", "title": "If the Portal Is Nearly Here", "toc": False,
 "blocks": [
    ("p", "You found this close to the date, and that is completely fine; this guide exists exactly for you. In modern spiritual practice, August 8 is treated as a doorway for intention-setting: Leo season's courage, the star Sirius returning to the dawn sky, the abundance-flavored number eight standing twice. Symbolic rather than scientific, and no less useful for it. A date can gather your attention wonderfully, and attention is where everything in this guide runs."),
    ("h2", "What to print (or not)"),
    ("bullets", [
      "Nothing, if you are on a tablet or phone: every exercise works on any paper or app.",
      "If you like paper, print only this guide; the full workbook can wait for the weekend.",
      "Have scrap paper ready for the release exercise; it gets destroyed on purpose.",
    ]),
    ("h2", "What not to worry about"),
    ("bullets", [
      "Supplies: none required. Candles, crystals and cards are decoration, not admission.",
      "Belief: curiosity is enough. The structure stands on reflection and action.",
      "Being late: the gate is a symbol. Even done on August 12, this works. Doors like this are made, not found.",
    ]),
    ("note", "Gentle reminder: this guide supports reflection and planning; it is not medical, mental-health, financial or legal advice, and outcomes are never guaranteed."),
 ],
},
{
 "family": "exercise", "section": "Quick Start", "title": "Fifteen Minutes of Preparation", "toc": False,
 "blocks": [
    ("check", ["One clear surface, one glass of water, phone silenced", "Ten minutes to tidy the corner of the room you can see", "Two honest scale marks below"]),
    ("scale", "My energy as I arrive at this season"),
    ("scale", "How clearly I can name what I want"),
    ("prompt", "The real reason I am doing this, in one sentence:", 2),
 ],
},
{
 "family": "exercise", "section": "Quick Start", "title": "Release, Then Choose", "toc": False,
 "blocks": [
    ("h2", "The release (five minutes)"),
    ("p", "On scrap paper, not here, write one pattern, story or weight you are finished carrying. One is enough. Tear the paper slowly into small pieces and set them aside to discard outside your door tonight. Notice your shoulders when it is done."),
    ("prompt", "What I released, named once here for the record:", 2),
    ("h2", "The intention (five minutes)"),
    ("p", "Write one present-tense sentence describing what you are choosing to build. Test it against four marks before you keep it."),
    ("prompt", "My intention:", 2),
    ("check", ["Specific", "Mine, not borrowed", "Carries a feeling I can name", "Has an action attached"]),
 ],
},
{
 "family": "exercise", "section": "Quick Start", "title": "A Two-Minute Visualization", "toc": False,
 "blocks": [
    ("p", "Close your eyes and step inside one ordinary scene from the life your intention builds: a morning, a desk, a kitchen. Notice the light, your posture, the way you answer the first message of the day. Stay two unhurried minutes. This is rehearsal, not escape; you are showing your nervous system the standard."),
    ("prompt", "What I saw, in enough detail to find it again:", 4),
 ],
},
{
 "family": "ritual", "section": "Quick Start", "title": "The 15-Minute Gate Ritual", "toc": False,
 "blocks": [
    ("steps", [
      ("Ground", "Five slow breaths, exhale longer than the inhale, feet on the floor."),
      ("Open", "Say quietly: I am giving myself fifteen honest minutes. That is enough."),
      ("Release", "If anything remains beyond the earlier release, write and tear it now."),
      ("Intend", "Read your intention aloud once, unflinching."),
      ("See", "Two minutes back inside your visualized scene."),
      ("Script", "Three calm sentences describing that life as if reporting it."),
      ("Affirm", "One line in your own words; believable beats impressive."),
      ("Commit", "One action, one date, within 72 hours. Calendar it now."),
      ("Close", "Drink the water. Say: done is beautiful."),
    ]),
    ("note", "Candle optional; never leave a flame unattended. A lamp dimmed low carries the same symbolism."),
 ],
},
{
 "family": "action", "section": "Quick Start", "title": "The Aligned-Action Page", "toc": False,
 "blocks": [
    ("fields", ["Within 24 hours I will", "Within 72 hours I will", "Within 8 days I will", "Within 30 days I will"]),
    ("prompt", "If my most likely obstacle appears, then I will:", 2),
    ("prompt", "Who I am telling about this plan:", 1),
    ("aff", "I honor my desire with action."),
 ],
},
{
 "family": "integration", "section": "Quick Start", "title": "Tomorrow Morning", "toc": False,
 "blocks": [
    ("p", "Rituals fade; follow-through compounds. Before noon tomorrow, do the 24-hour action, then answer these two lines. That is the entire assignment."),
    ("prompt", "How last night sits with me this morning:", 3),
    ("prompt", "The action is done or scheduled for:", 1),
    ("h2", "When you want more"),
    ("p", "The complete workbook in your download holds the full eight-day arc, the deeper rituals, the guided meditation, shadow work, scripting, the aligned-action system and thirty days of integration. It will meet you whenever this season allows."),
 ],
},
{
 "family": "front", "section": "Quick Start", "title": "License & Thanks", "toc": False,
 "blocks": [
    ("p", "Your purchase includes a single-user personal-use license: print and use these files for yourself as often as you like. Please do not share, resell or redistribute them, or use them with clients or groups without a separate license. The full license lives in the main workbook."),
    ("p", "Thank you for spending part of your Lion's Gate season with this guide. If it supports you, an honest review helps another reader decide whether it may support her too; and if any file misbehaves, message GlowHausDigital on Etsy so I can make it right."),
    ("ornament",),
    ("cp", "*May the next honest step be kind to you.*", 2),
 ],
},
{"kind": "back", "quote": "Fifteen sincere minutes can outweigh a year of waiting for the perfect evening.", "brand": "GlowHausDigital"},
]

def build_quick_start():
    book = engine.Book(T.spec("letter"), title="The Lion's Gate Quick Start",
                       subtitle="Fifteen honest minutes for anyone beginning close to August 8")
    book.extend(QS_PAGES)
    n = book.build(os.path.join(HERE, "Lions_Gate_Quick_Start.pdf"))
    print("quick start:", n, "pages")

# ================================================================ CARDS
CARD_W, CARD_H = 3.5 * IN, 2.5 * IN

def card_front(c, x, y, cat, text, idx):
    c.setFillColor(T.CREAM)
    c.setStrokeColor(T.GOLD)
    c.setLineWidth(1.0)
    c.roundRect(x + 5, y + 5, CARD_W - 10, CARD_H - 10, 8, stroke=1, fill=1)
    c.setLineWidth(0.5)
    c.roundRect(x + 9, y + 9, CARD_W - 18, CARD_H - 18, 6, stroke=1, fill=0)
    M.eight_point_star(c, x + CARD_W / 2, y + CARD_H - 26, 6.5, color=T.GOLD, weight=0.5)
    engine._kicker_text(c, 0, y + CARD_H - 44, cat, 7, T.AMBER, align="center", cx=x + CARD_W / 2)
    fonts = {"r": T.SERIF_MED, "i": T.SERIF_IT_M, "b": T.SERIF_SB}
    size = 13.5
    lines = engine._wrap(text, fonts, size, CARD_W - 46)
    while len(lines) > 4 and size > 10.5:
        size -= 0.5
        lines = engine._wrap(text, fonts, size, CARD_W - 46)
    total_h = len(lines) * size * 1.22
    ty = y + (CARD_H - 52) / 2 + total_h / 2 + 8
    engine._draw_lines(c, lines, x + 23, ty, size, size * 1.22, T.INDIGO, fonts, align="center", width=CARD_W - 46)
    M.dot(c, x + CARD_W / 2 - 14, y + 18, 1.1, T.GOLD)
    M.sparkle(c, x + CARD_W / 2, y + 18, 3.2, color=T.GOLD)
    M.dot(c, x + CARD_W / 2 + 14, y + 18, 1.1, T.GOLD)
    c.setFont(T.BODY, 4.6); c.setFillColor(T.LINE_WARM)
    c.drawCentredString(x + CARD_W / 2, y + 8.5, "© 2026 GlowHausDigital · personal use")

def card_back(c, x, y):
    c.setFillColor(T.INDIGO)
    c.roundRect(x + 5, y + 5, CARD_W - 10, CARD_H - 10, 8, stroke=0, fill=1)
    M.starfield(c, x + 16, y + 16, CARD_W - 32, CARD_H - 32, seed=5, n=14)
    M.portal_arch(c, x + CARD_W / 2 - 20, y + CARD_H / 2 - 26, 40, 44, color=T.GOLD_ON_DARK, weight=0.7, layers=2)
    M.eight_point_star(c, x + CARD_W / 2, y + CARD_H / 2 - 2, 7, color=T.GOLD_ON_DARK, weight=0.5)

def card_back_light(c, x, y):
    c.setFillColor(T.IVORY)
    c.setStrokeColor(T.GOLD_SOFT)
    c.setLineWidth(0.8)
    c.roundRect(x + 5, y + 5, CARD_W - 10, CARD_H - 10, 8, stroke=1, fill=1)
    M.sacred_geometry(c, x + CARD_W / 2, y + CARD_H / 2, 22, color=T.GOLD_PALE, weight=0.5)
    M.eight_point_star(c, x + CARD_W / 2, y + CARD_H / 2, 6, color=T.GOLD_SOFT, weight=0.5)

def cut_marks(c, page_w, page_h, left, bottom, cols, rows):
    c.setStrokeColor(T.INK_SOFT)
    c.setLineWidth(0.4)
    for i in range(cols + 1):
        x = left + i * CARD_W
        c.line(x, bottom - 16, x, bottom - 5)
        c.line(x, bottom + rows * CARD_H + 5, x, bottom + rows * CARD_H + 16)
    for j in range(rows + 1):
        y = bottom + j * CARD_H
        c.line(left - 16, y, left - 5, y)
        c.line(left + cols * CARD_W + 5, y, left + cols * CARD_W + 16, y)

def build_cards(page_key, out_name):
    if page_key == "letter":
        pw, ph = 8.5 * IN, 11 * IN
    else:
        pw, ph = 210 * MM, 297 * MM
    cols, rows = 2, 4
    left = (pw - cols * CARD_W) / 2.0
    bottom = (ph - rows * CARD_H) / 2.0
    path = os.path.join(HERE, out_name)
    c = rl_canvas.Canvas(path, pagesize=(pw, ph))
    c.setTitle("Lion's Gate Affirmation Cards")
    c.setAuthor("GlowHausDigital")
    for cat, texts in CARD_SETS.items():
        # front sheet
        for i, t in enumerate(texts):
            col, row = i % cols, rows - 1 - i // cols
            card_front(c, left + col * CARD_W, bottom + row * CARD_H, cat, t, i)
        cut_marks(c, pw, ph, left, bottom, cols, rows)
        c.setFont(T.BODY, 7); c.setFillColor(T.INK_SOFT)
        c.drawCentredString(pw / 2, bottom / 2.5, "%s · print at 100%% · duplex with the pattern page (flip on long edge), or print fronts only" % cat)
        c.showPage()
        # back sheet (same grid; horizontally symmetric so long-edge duplex aligns)
        for i in range(len(texts)):
            col, row = i % cols, rows - 1 - i // cols
            card_back(c, left + col * CARD_W, bottom + row * CARD_H)
        cut_marks(c, pw, ph, left, bottom, cols, rows)
        c.setFont(T.BODY, 7); c.setFillColor(T.INK_SOFT)
        c.drawCentredString(pw / 2, bottom / 2.5, "Card backs · indigo set · skip this page for the ink-light option")
        c.showPage()
    # ink-light back page
    for i in range(8):
        col, row = i % cols, rows - 1 - i // cols
        card_back_light(c, left + col * CARD_W, bottom + row * CARD_H)
    cut_marks(c, pw, ph, left, bottom, cols, rows)
    c.setFont(T.BODY, 7); c.setFillColor(T.INK_SOFT)
    c.drawCentredString(pw / 2, bottom / 2.5, "Optional ink-light card backs · use instead of the indigo backs on any sheet")
    c.showPage()
    # instructions page via engine-style manual drawing
    s = T.spec("letter" if page_key == "letter" else "a4")
    b = engine.Book(s, title="Affirmation Cards")
    b.pages = [{
        "family": "reference", "section": "Affirmation Cards", "title": "Printing & Cutting Your 32 Cards",
        "blocks": [
            ("p", "Thirty-two affirmations in four families: Abundance, Self-Concept, Courage & Action, Receiving & Trust. Eight cards per sheet, finished size 3.5 x 2.5 inches."),
            ("steps", [
                ("Print", "Use cardstock if you have it, at 100 percent scale (actual size). For patterned backs, print duplex and flip on the long edge; for an ink-light deck, print the front sheets only, or pair them with the final light-back page."),
                ("Test", "Print one sheet first and check the fronts and backs align before committing the full set."),
                ("Cut", "Slice along the small edge marks with a ruler and craft knife, or sharp scissors. The inner gold frame keeps every card readable even if your cut wanders a little."),
                ("Use", "One card on the mirror, one in the wallet, one on the desk. Rotate on Sundays; retire any card whose sentence stops feeling true."),
            ]),
            ("note", "License summary: for your personal use only; please do not sell, share or gift printed sets, and do not post scans or photos of full card texts as shareable content. Full license in the main workbook. © 2026 GlowHausDigital."),
        ],
    }]
    # render instruction page onto the same canvas
    b._measuring = False
    b.page_no = 0
    b._begin_page(c)
    b._draw_flow_page(c, b.pages[0], final=False)
    c.save()
    print("cards:", out_name)

# ================================================================ TABS
TABS = ["Begin", "Prepare", "Release", "Clarify", "Embody", "Activate", "Act", "Integrate", "Notes"]
TAB_W, TAB_H = 1.7 * IN, 0.55 * IN

def draw_tab(c, x, y, label, side, colored, idx):
    """A fold-over tab: two faces joined at a dashed fold line. side: R or L."""
    total_w = TAB_W * 2
    if colored:
        fills = [T.INDIGO, T.PLUM, T.AMBER, T.TERRACOTTA, T.ROSE, T.GOLD, T.INDIGO, T.PLUM, T.AMBER]
        fill = fills[idx % len(fills)]
        c.setFillColor(fill)
        c.setStrokeColor(T.GOLD)
        c.setLineWidth(0.7)
        c.roundRect(x, y, total_w, TAB_H, 6, stroke=1, fill=1)
        txt_color = T.INDIGO if fill in (T.ROSE, T.GOLD) else T.STARLIGHT
    else:
        c.setFillColor(T.CREAM)
        c.setStrokeColor(T.INK_SOFT)
        c.setLineWidth(0.7)
        c.roundRect(x, y, total_w, TAB_H, 6, stroke=1, fill=1)
        txt_color = T.INDIGO
    # fold line
    c.setStrokeColor(T.GOLD_SOFT if colored else T.INK_SOFT)
    c.setLineWidth(0.5)
    c.setDash(3, 3)
    c.line(x + TAB_W, y + 2, x + TAB_W, y + TAB_H - 2)
    c.setDash()
    for fx in (x + TAB_W / 2, x + TAB_W * 1.5):
        engine._kicker_text(c, 0, y + TAB_H / 2 - 3.4, label, 8.6, txt_color, align="center", cx=fx)
        M.dot(c, fx - pdfmetrics.stringWidth(label.upper(), T.DISPLAY, 8.6) / 2 - 11, y + TAB_H / 2, 1.0,
              T.GOLD_ON_DARK if colored else T.GOLD)
        M.dot(c, fx + pdfmetrics.stringWidth(label.upper(), T.DISPLAY, 8.6) / 2 + 11, y + TAB_H / 2, 1.0,
              T.GOLD_ON_DARK if colored else T.GOLD)

def build_tabs(page_key, out_name):
    if page_key == "letter":
        pw, ph = 8.5 * IN, 11 * IN
    else:
        pw, ph = 210 * MM, 297 * MM
    path = os.path.join(HERE, out_name)
    c = rl_canvas.Canvas(path, pagesize=(pw, ph))
    c.setTitle("Lion's Gate Planner Tabs")
    c.setAuthor("GlowHausDigital")
    for colored in (True, False):
        for side in ("right", "left"):
            c.setFillColor(T.IVORY)
            c.rect(0, 0, pw, ph, stroke=0, fill=1)
            engine._kicker_text(c, 0, ph - 46, "Lion's Gate planner tabs · %s-side set · %s" %
                                (side, "color" if colored else "printer-friendly"), 9, T.GOLD, align="center", cx=pw / 2)
            top = ph - 90
            for i, label in enumerate(TABS):
                y = top - i * (TAB_H + 26) - TAB_H
                x = (pw - TAB_W * 2) / 2
                draw_tab(c, x, y, label, side, colored, i)
                # cut guides
                c.setStrokeColor(T.INK_SOFT); c.setLineWidth(0.35)
                c.line(x - 20, y - 7, x + TAB_W * 2 + 20, y - 7)
                M.sparkle(c, x + TAB_W * 2 + 30, y + TAB_H / 2, 2.6, color=T.GOLD_SOFT)
            c.setFont(T.BODY, 8); c.setFillColor(T.INK_SOFT)
            c.drawCentredString(pw / 2, 40, "Cut on the solid lines · fold on the dashed center line over the page edge · %s tabs face %s" %
                                ("these", side))
            c.showPage()
    # instructions
    s = T.spec("letter" if page_key == "letter" else "a4")
    b = engine.Book(s, title="Planner Tabs")
    b.pages = [{
        "family": "reference", "section": "Planner Tabs", "title": "Using Your Section Tabs",
        "blocks": [
            ("p", "Nine tabs matching the planner edition's sections: Begin, Prepare, Release, Clarify, Embody, Activate, Act, Integrate, Notes. Right-side and left-side sets are included, in full color and a printer-friendly outline version."),
            ("steps", [
                ("Print", "Cardstock recommended, 100 percent scale. Choose the color or printer-friendly pages, right- or left-side sets to taste."),
                ("Cut", "Cut each tab out along the solid lines; the small horizontal guide under each tab marks a clean straight edge."),
                ("Fold", "Fold on the dashed center line so the label shows on both faces, and slip the fold over the outer edge of the section's first page."),
                ("Attach", "Double-sided tape or a glue stick inside the fold holds them; repositionable tape lets you rearrange later."),
                ("Laminate (optional)", "For a deck that lasts years, laminate the printed sheet before cutting, then cut and fold; score the fold line lightly first."),
            ]),
            ("note", "Tabs extend past the page edge by design; trim the depth to suit your binder. Punch positions vary between binders, so tabs deliberately avoid the ring edge. Personal use only. © 2026 GlowHausDigital."),
        ],
    }]
    b._measuring = False
    b.page_no = 0
    b._begin_page(c)
    b._draw_flow_page(c, b.pages[0], final=False)
    c.save()
    print("tabs:", out_name)

if __name__ == "__main__":
    build_quick_start()
    build_cards("letter", "Lions_Gate_Affirmation_Cards_US_Letter.pdf")
    build_cards("a4", "Lions_Gate_Affirmation_Cards_A4.pdf")
    build_tabs("letter", "Lions_Gate_Planner_Tabs_US_Letter.pdf")
    build_tabs("a4", "Lions_Gate_Planner_Tabs_A4.pdf")
