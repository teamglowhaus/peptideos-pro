"""Visual system for THE LION'S GATE 8/8 ACTIVATION — palette, typography, page specs."""
import os
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "fonts")

# ---------------------------------------------------------------- palette
INDIGO      = HexColor("#232946")   # deep midnight indigo (covers, dividers)
INDIGO_DEEP = HexColor("#191D33")   # deepest night (cover vignettes)
INK         = HexColor("#33303C")   # body text
INK_SOFT    = HexColor("#575263")   # secondary text
IVORY       = HexColor("#FAF6EE")   # primary page background
CREAM       = HexColor("#FDFBF4")   # luminous cream (boxes)
GOLD        = HexColor("#A8894F")   # muted antique gold (rules, ornaments)
GOLD_SOFT   = HexColor("#C9B183")   # lighter gold
GOLD_PALE   = HexColor("#E6D9BC")   # faint gold (backgrounds of chips)
AMBER       = HexColor("#B97F42")   # burnished amber
TERRACOTTA  = HexColor("#C2775B")   # soft terracotta
ROSE        = HexColor("#C4958D")   # dusty rose
ROSE_PALE   = HexColor("#F2E6E0")   # rose wash
PLUM        = HexColor("#6C5677")   # subtle plum
PLUM_PALE   = HexColor("#EDE7EE")   # plum wash
LINE_WARM   = HexColor("#C8BBA6")   # writing lines
LINE_FAINT  = HexColor("#DDD3C2")   # faint rules / dot grid
WASH_GOLD   = HexColor("#F6EFE0")   # golden wash panels
STARLIGHT   = HexColor("#EFE7D3")   # light text on indigo
GOLD_ON_DARK= HexColor("#D9C08E")

# tint used per template family for washes
FAMILY_WASH = {
    "education": WASH_GOLD, "exercise": CREAM, "ritual": ROSE_PALE,
    "meditation": PLUM_PALE, "day": WASH_GOLD, "action": CREAM,
    "integration": PLUM_PALE, "reference": CREAM, "planner": CREAM,
    "front": CREAM, "bonus": WASH_GOLD,
}

# ---------------------------------------------------------------- fonts
SERIF      = "Cormorant"        # headings
SERIF_MED  = "Cormorant-Med"
SERIF_SB   = "Cormorant-Semi"
SERIF_BOLD = "Cormorant-Bold"
SERIF_IT   = "Cormorant-Italic"
SERIF_IT_M = "Cormorant-Italic-Med"
DISPLAY    = "Marcellus"        # kickers / small caps display
BODY       = "Lato"
BODY_LIGHT = "Lato-Light"
BODY_BOLD  = "Lato-Bold"
BODY_IT    = "Lato-Italic"

_registered = False

def register_fonts():
    global _registered
    if _registered:
        return
    faces = [
        (SERIF, "CormorantGaramond-400.ttf"), (SERIF_MED, "CormorantGaramond-500.ttf"),
        (SERIF_SB, "CormorantGaramond-600.ttf"), (SERIF_BOLD, "CormorantGaramond-700.ttf"),
        (SERIF_IT, "CormorantGaramond-Italic-400.ttf"), (SERIF_IT_M, "CormorantGaramond-Italic-500.ttf"),
        (DISPLAY, "Marcellus-400.ttf"),
        (BODY, "Lato-400.ttf"), (BODY_LIGHT, "Lato-300.ttf"),
        (BODY_BOLD, "Lato-700.ttf"), (BODY_IT, "Lato-Italic-400.ttf"),
    ]
    for name, fn in faces:
        pdfmetrics.registerFont(TTFont(name, os.path.join(FONT_DIR, fn)))
    _registered = True

# ---------------------------------------------------------------- page specs
IN = 72.0
MM = 72.0 / 25.4

class PageSpec:
    """Everything size-dependent: dimensions, margins, type scale, decor density."""
    def __init__(self, key, w, h, *, m_top, m_bottom, m_outer, m_bind,
                 body, lead, prompt, h1, h2, kicker, fine, line_gap,
                 mirrored=False, decor="full", digital=False, columns_ok=True):
        self.key = key
        self.w, self.h = w, h
        self.m_top, self.m_bottom = m_top, m_bottom
        self.m_outer, self.m_bind = m_outer, m_bind
        self.body, self.lead = body, lead
        self.prompt = prompt
        self.h1, self.h2, self.kicker, self.fine = h1, h2, kicker, fine
        self.line_gap = line_gap          # spacing of ruled writing lines
        self.mirrored = mirrored          # planner duplex margins
        self.decor = decor                # "full" | "light" | "minimal"
        self.digital = digital
        self.columns_ok = columns_ok

    def margins(self, page_index):
        """(left, right) margins. Odd pages (1st, 3rd...) bind on the left."""
        if not self.mirrored:
            return self.m_bind, self.m_outer
        if page_index % 2 == 0:            # recto: binding left
            return self.m_bind, self.m_outer
        return self.m_outer, self.m_bind   # verso: binding right

    @property
    def text_w(self):
        return self.w - self.m_bind - self.m_outer


def spec(key):
    if key == "letter":
        return PageSpec("letter", 8.5*IN, 11*IN, m_top=0.92*IN, m_bottom=0.78*IN,
                        m_outer=0.8*IN, m_bind=0.8*IN, body=11, lead=15.5, prompt=11.5,
                        h1=26, h2=15.5, kicker=9.5, fine=8.5, line_gap=26)
    if key == "a4":
        return PageSpec("a4", 210*MM, 297*MM, m_top=24*MM, m_bottom=20*MM,
                        m_outer=19*MM, m_bind=19*MM, body=11, lead=15.5, prompt=11.5,
                        h1=25, h2=15, kicker=9.5, fine=8.5, line_gap=25)
    if key == "letter_digital":
        s = spec("letter"); s.key = "letter_digital"; s.digital = True; s.line_gap = 30
        return s
    if key == "a4_digital":
        s = spec("a4"); s.key = "a4_digital"; s.digital = True; s.line_gap = 29
        return s
    if key == "pocket":
        return PageSpec("pocket", 3.5*IN, 6*IN, m_top=0.42*IN, m_bottom=0.38*IN,
                        m_outer=0.28*IN, m_bind=0.72*IN, body=10, lead=13.4, prompt=10.5,
                        h1=15.5, h2=12, kicker=7.5, fine=7, line_gap=21,
                        mirrored=True, decor="minimal", columns_ok=False)
    if key == "compact":
        return PageSpec("compact", 4.25*IN, 6.75*IN, m_top=0.5*IN, m_bottom=0.42*IN,
                        m_outer=0.32*IN, m_bind=0.8*IN, body=10.2, lead=13.9, prompt=11,
                        h1=17.5, h2=12.5, kicker=8, fine=7.5, line_gap=22,
                        mirrored=True, decor="light", columns_ok=False)
    if key == "classic":
        return PageSpec("classic", 5.5*IN, 8.5*IN, m_top=0.62*IN, m_bottom=0.5*IN,
                        m_outer=0.42*IN, m_bind=0.92*IN, body=10.8, lead=14.8, prompt=11.5,
                        h1=20, h2=13.5, kicker=8.5, fine=8, line_gap=24,
                        mirrored=True, decor="light")
    if key == "monarch":
        return PageSpec("monarch", 8.5*IN, 11*IN, m_top=0.85*IN, m_bottom=0.7*IN,
                        m_outer=0.6*IN, m_bind=1.15*IN, body=11, lead=15.5, prompt=11.5,
                        h1=24, h2=15, kicker=9.5, fine=8.5, line_gap=26,
                        mirrored=True, decor="full")
    raise KeyError(key)
