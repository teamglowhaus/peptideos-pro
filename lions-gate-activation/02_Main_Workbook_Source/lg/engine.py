"""Flowing page-layout engine for all editions of THE LION'S GATE 8/8 ACTIVATION.

Content is authored once as block lists; the engine reflows it for any PageSpec
(US Letter, A4, digital, Pocket, Compact, Classic, Monarch), draws the visual
chrome for each template family, paginates with automatic continuation pages,
and produces a clickable table of contents plus PDF outline bookmarks.
"""
import math
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.colors import Color
from . import theme as T
from . import motifs as M


# ================================================================ text utils
def _segments(text):
    """Parse minimal inline markup: **bold**, *italic*. Returns [(style, str)]."""
    out, buf, i, style = [], "", 0, "r"
    while i < len(text):
        if text.startswith("**", i):
            if buf: out.append((style, buf)); buf = ""
            style = "r" if style == "b" else "b"; i += 2
        elif text[i] == "*":
            if buf: out.append((style, buf)); buf = ""
            style = "r" if style == "i" else "i"; i += 1
        else:
            buf += text[i]; i += 1
    if buf: out.append((style, buf))
    return out


def _wrap(text, fonts, size, width):
    """Wrap marked-up text into lines. Each line is a list of words; each word
    is a list of (font, fragment) so styles can change mid-word (e.g. *word*,)."""
    words = []       # list of word = [(font, frag), ...]
    open_word = False
    for style, seg in _segments(text):
        font = fonts[style]
        parts = seg.split(" ")
        for pi, part in enumerate(parts):
            if pi > 0:
                open_word = False
            if part == "":
                continue
            if open_word and words:
                words[-1].append((font, part))
            else:
                words.append([(font, part)])
                open_word = True
        if seg.endswith(" "):
            open_word = False

    def wwidth(word):
        return sum(pdfmetrics.stringWidth(f2, f1, size) for f1, f2 in word)

    lines, cur, cur_w = [], [], 0.0
    space_w = pdfmetrics.stringWidth(" ", fonts["r"], size)
    for word in words:
        ww = wwidth(word)
        add = ww if not cur else ww + space_w
        if cur and cur_w + add > width:
            lines.append(cur); cur, cur_w = [word], ww
        else:
            cur.append(word); cur_w += add
    if cur: lines.append(cur)
    return lines


def _line_width(ln, size, space_w):
    return sum(pdfmetrics.stringWidth(fr, f, size) for wd in ln for f, fr in wd) + space_w * (len(ln) - 1)


def _draw_lines(c, lines, x, y_top, size, lead, color, fonts, align="left", width=None):
    y = y_top - size * 0.85
    space_w = pdfmetrics.stringWidth(" ", fonts["r"], size)
    for ln in lines:
        total = _line_width(ln, size, space_w)
        if align == "center" and width:
            cx = x + (width - total) / 2.0
        elif align == "right" and width:
            cx = x + width - total
        else:
            cx = x
        for wd in ln:
            for f, fr in wd:
                c.setFont(f, size); c.setFillColor(color)
                c.drawString(cx, y, fr)
                cx += pdfmetrics.stringWidth(fr, f, size)
            cx += space_w
        y -= lead
    return y_top - len(lines) * lead


def _lines_to_markup(lines, fonts):
    """Rebuild markup text from wrapped lines (for paragraph continuation)."""
    out_words = []
    for ln in lines:
        for wd in ln:
            frags = []
            for f, fr in wd:
                if f == fonts.get("i"):
                    frags.append("*" + fr + "*")
                elif f == fonts.get("b"):
                    frags.append("**" + fr + "**")
                else:
                    frags.append(fr)
            out_words.append("".join(frags))
    return " ".join(out_words)


def _kicker_text(c, x, y, text, size, color, letterspace=1.6, align="left", cx=None):
    c.setFont(T.DISPLAY, size); c.setFillColor(color)
    t = text.upper()
    tw = pdfmetrics.stringWidth(t, T.DISPLAY, size) + letterspace * (len(t) - 1)
    if align == "center" and cx is not None:
        x = cx - tw / 2.0
    c.saveState()
    tx = c.beginText(x, y)
    tx.setFont(T.DISPLAY, size)
    tx.setCharSpace(letterspace)
    tx.textOut(t)
    c.drawText(tx)
    c.restoreState()
    return tw


# ================================================================ the book
class Book:
    def __init__(self, spec, title="", subtitle="", brand="GlowHausDigital"):
        self.s = spec
        self.title, self.subtitle, self.brand = title, subtitle, brand
        self.pages = []          # page dicts
        self.toc_entries = []    # (level, label, page_no) filled during layout
        self._measuring = False

    def add(self, page):
        self.pages.append(page)

    def extend(self, pages):
        self.pages.extend(pages)

    # ---------------------------------------------------------- build
    def build(self, path):
        T.register_fonts()
        # pass 1: measure pagination (records toc page numbers, total pages)
        self._measuring = True
        c = rl_canvas.Canvas(path, pagesize=(self.s.w, self.s.h))
        self.toc_entries = []
        self._render(c, final=False)
        # pass 2: real render with TOC page numbers known
        self._measuring = False
        c = rl_canvas.Canvas(path, pagesize=(self.s.w, self.s.h))
        c.setTitle(self.title)
        c.setAuthor(self.brand)
        c.setSubject(self.subtitle)
        self.total = self._render(c, final=True)
        c.save()
        return self.total

    def _render(self, c, final):
        self.page_no = 0
        toc_snapshot = list(self.toc_entries)
        if not final:
            self.toc_entries = []
        outline_stack = []
        for pg in self.pages:
            kind = pg.get("kind", "page")
            if kind == "cover":
                self._begin_page(c)
                self._draw_cover(c, pg)
                self._finish(c)
            elif kind == "back":
                self._begin_page(c)
                self._draw_back(c, pg)
                self._finish(c)
            elif kind == "divider":
                self._begin_page(c)
                self._record_toc(pg, 0)
                if final:
                    self._bookmark(c, pg["title"], 0)
                self._draw_divider(c, pg)
                self._finish(c)
            elif kind == "toc":
                self._draw_toc(c, pg, toc_snapshot, final)
            else:
                self._draw_flow_page(c, pg, final)
        return self.page_no

    # ---------------------------------------------------------- page plumbing
    def _begin_page(self, c):
        self.page_no += 1

    def _finish(self, c):
        c.showPage()

    def _bookmark(self, c, label, level):
        key = "p%d_%s" % (self.page_no, abs(hash(label)) % 99999)
        c.bookmarkPage(key)
        try:
            c.addOutlineEntry(label, key, level=level, closed=(level == 0))
        except Exception:
            pass
        return key

    def _record_toc(self, pg, level):
        if pg.get("toc") is False:
            return
        label = pg.get("toc_label", pg.get("title", ""))
        if label:
            self.toc_entries.append((level, label, self.page_no))

    # ---------------------------------------------------------- chrome
    def _chrome(self, c, pg, cont=False):
        """Background + header/footer + decor for a flow page. Returns content box."""
        s = self.s
        fam = pg.get("family", "exercise")
        left, right = s.margins(self.page_no - 1)
        # background
        c.setFillColor(T.IVORY)
        c.rect(0, 0, s.w, s.h, stroke=0, fill=1)
        wash = pg.get("wash")
        if wash:
            c.setFillColor(T.FAMILY_WASH.get(fam, T.CREAM))
            c.rect(0, 0, s.w, s.h, stroke=0, fill=1)
        x0, x1 = left, s.w - right
        y_top = s.h - s.m_top
        # header: kicker + rule
        kick = pg.get("section", "")
        if kick and s.decor != "minimal":
            _kicker_text(c, x0, s.h - s.m_top * 0.52, kick, s.kicker, T.GOLD)
            M.sparkle(c, x1 - 4, s.h - s.m_top * 0.52 + s.kicker * 0.35, 3.4, color=T.GOLD_SOFT)
        elif kick:
            _kicker_text(c, x0, s.h - s.m_top * 0.5, kick, s.kicker, T.GOLD)
        c.setStrokeColor(T.GOLD_SOFT); c.setLineWidth(0.6)
        c.line(x0, s.h - s.m_top * 0.36, x1, s.h - s.m_top * 0.36)
        # family decor accents (rotated to avoid repetition)
        self._family_decor(c, fam, pg, x0, x1)
        # footer
        self._footer(c, left, right)
        return x0, x1, y_top, s.m_bottom + s.fine + 10

    def _footer(self, c, left, right):
        s = self.s
        y = s.m_bottom * 0.45
        c.setFont(T.BODY, s.fine); c.setFillColor(T.INK_SOFT)
        num = str(self.page_no)
        if s.mirrored:
            # planner: number at outer edge
            if (self.page_no - 1) % 2 == 0:
                c.drawRightString(s.w - right, y, num)
                M.dot(c, s.w - right - pdfmetrics.stringWidth(num, T.BODY, s.fine) - 7, y + s.fine * 0.3, 1.0, T.GOLD)
            else:
                c.drawString(left, y, num)
                M.dot(c, left + pdfmetrics.stringWidth(num, T.BODY, s.fine) + 7, y + s.fine * 0.3, 1.0, T.GOLD)
        else:
            cx = s.w / 2.0
            c.drawCentredString(cx, y, num)
            M.dot(c, cx - pdfmetrics.stringWidth(num, T.BODY, s.fine) / 2 - 9, y + s.fine * 0.32, 1.0, T.GOLD)
            M.dot(c, cx + pdfmetrics.stringWidth(num, T.BODY, s.fine) / 2 + 9, y + s.fine * 0.32, 1.0, T.GOLD)
        if s.digital and hasattr(self, "_toc_pageno"):
            c.setFont(T.DISPLAY, s.fine)
            c.setFillColor(T.GOLD)
            label = "CONTENTS"
            tw = pdfmetrics.stringWidth(label, T.DISPLAY, s.fine)
            lx = s.w - right - tw
            c.drawString(lx, y, label)
            c.linkAbsolute("", "TOC", (lx - 2, y - 3, lx + tw + 2, y + s.fine + 2), thickness=0)

    def _family_decor(self, c, fam, pg, x0, x1):
        s = self.s
        if s.decor == "minimal":
            return
        seed = pg.get("decor_seed", self.page_no)
        v = seed % 4
        gold = Color(0.66, 0.54, 0.31, alpha=0.55)
        y_low = s.m_bottom * 0.9
        if fam in ("education", "front"):
            if v == 0: M.corner_ornament(c, x1, y_low, 26, quadrant="br", color=gold)
            elif v == 1: M.constellation(c, x1 - 64, y_low - 8, 58, 30, color=gold, seed=seed * 3 + 1, n=6)
            elif v == 2: M.botanical(c, x1 - 10, y_low - 6, 34, color=gold)
            else: M.crescent(c, x1 - 12, y_low + 6, 7, color=gold)
        elif fam in ("exercise", "planner"):
            if v == 0: M.sparkle(c, x1 - 6, y_low + 2, 3.2, color=gold)
            elif v == 1: M.eight_point_star(c, x1 - 8, y_low + 4, 6, color=gold, weight=0.5)
            elif v == 2: M.infinity(c, x1 - 22, y_low + 4, 26, color=gold, weight=0.6)
            else: M.dot(c, x1 - 6, y_low + 3, 1.4, gold)
        elif fam == "ritual":
            M.sun_rays(c, x0 - s.m_bind * 0.4, s.h, 10, 26, color=gold, n=10, arc=(-80, 10))
            if v % 2: M.botanical(c, x1 - 8, y_low - 6, 30, color=gold, flip=True)
        elif fam == "meditation":
            M.constellation(c, x1 - 70, y_low - 6, 62, 34, color=gold, seed=seed * 5 + 3, n=7)
        elif fam == "day":
            pass  # day pages draw their own solar header
        elif fam == "action":
            M.corner_ornament(c, x1, y_low, 20, quadrant="br", color=gold, weight=0.5)
        elif fam == "integration":
            M.crescent(c, x1 - 10, y_low + 6, 6.5, color=gold)
            if v % 2: M.dot(c, x1 - 24, y_low + 10, 1.0, gold)
        elif fam == "reference":
            M.eight_point_star(c, x1 - 7, y_low + 4, 5, color=gold, weight=0.45)

    # ---------------------------------------------------------- flow rendering
    def _draw_flow_page(self, c, pg, final, ):
        s = self.s
        blocks = list(pg.get("blocks", []))
        first = True
        while True:
            self._begin_page(c)
            x0, x1, y, y_min = self._chrome(c, pg, cont=not first)
            if first:
                self._record_toc(pg, pg.get("toc_level", 1))
                if final and pg.get("title"):
                    self._bookmark(c, pg["title"], pg.get("toc_level", 1))
                if final and pg.get("anchor"):
                    c.bookmarkPage(pg["anchor"])
            y = self._page_head(c, pg, x0, x1, y, cont=not first)
            width = x1 - x0
            # flow blocks
            while blocks:
                blk = blocks[0]
                used, rest = self._draw_block(c, blk, x0, y, width, y_min, pg)
                if used is None:      # doesn't fit at all here
                    if y >= s.h - s.m_top - 4 and rest is None:
                        # taller than a full page: force-draw to avoid infinite loop
                        blocks.pop(0)
                        continue
                    break
                y -= used
                blocks.pop(0)
                if rest is not None:
                    blocks.insert(0, rest)
                    break
            self._finish(c)
            if not blocks:
                break
            first = False

    def _page_head(self, c, pg, x0, x1, y, cont=False):
        s = self.s
        title = pg.get("title", "")
        if not title:
            return y
        fonts = {"r": T.SERIF_MED, "i": T.SERIF_IT_M, "b": T.SERIF_SB}
        size = s.h1 * (0.82 if cont else 1.0)
        lines = _wrap(title, fonts, size, x1 - x0)
        _draw_lines(c, lines, x0, y, size, size * 1.06, T.INDIGO, fonts)
        y -= len(lines) * size * 1.06 + 2
        if cont:
            c.setFont(T.SERIF_IT, s.body + 1); c.setFillColor(T.GOLD)
            c.drawString(x0, y - s.body, "continued")
            y -= s.body + 6
        sub = pg.get("subtitle")
        if sub and not cont:
            sf = {"r": T.SERIF_IT, "i": T.SERIF, "b": T.SERIF_IT_M}
            sl = _wrap(sub, sf, s.h2 * 0.92, x1 - x0)
            _draw_lines(c, sl, x0, y - 2, s.h2 * 0.92, s.h2 * 1.05, T.INK_SOFT, sf)
            y -= len(sl) * s.h2 * 1.05 + 4
        # short gold underline
        c.setStrokeColor(T.GOLD); c.setLineWidth(1.0)
        c.line(x0, y - 2, x0 + min(52, (x1 - x0) * 0.2), y - 2)
        return y - s.lead * 0.9

    # ---------------------------------------------------------- blocks
    def _draw_block(self, c, blk, x, y, w, y_min, pg):
        """Draw block top-aligned at y. Return (height_used, rest_block|None).
        Return (None, None) if it can't start on this page."""
        s = self.s
        kind = blk[0]
        avail = y - y_min
        BF = {"r": T.BODY, "i": T.BODY_IT, "b": T.BODY_BOLD}
        SF = {"r": T.SERIF_MED, "i": T.SERIF_IT_M, "b": T.SERIF_SB}

        if kind == "spacer":
            return (min(blk[1], avail), None)

        if kind == "cp":       # centered serif paragraph (front-matter display text)
            fonts = {"r": T.SERIF_MED, "i": T.SERIF_IT_M, "b": T.SERIF_SB}
            size = s.body + (blk[2] if len(blk) > 2 else 3)
            lines = _wrap(blk[1], fonts, size, w * 0.86)
            need = len(lines) * size * 1.3 + 6
            if need > avail: return (None, None)
            _draw_lines(c, lines, x + w * 0.07, y, size, size * 1.3, T.INK, fonts, align="center", width=w * 0.86)
            return (need, None)

        if kind == "ck":       # centered letterspaced kicker line
            if avail < 22: return (None, None)
            _kicker_text(c, 0, y - s.kicker * 1.4, blk[1], s.kicker, T.GOLD, align="center", cx=x + w / 2.0)
            return (s.kicker * 2.4, None)

        if kind == "ornament":  # centered motif row
            if avail < 30: return (None, None)
            M.rule_with_star(c, x + w * 0.33, x + w * 0.67, y - 12, r=3.6)
            return (30, None)

        if kind == "rule":
            if avail < 14: return (None, None)
            M.rule_with_star(c, x + w * 0.2, x + w * 0.8, y - 7, r=3.4)
            return (16, None)

        if kind in ("p", "pi", "note"):
            size = s.body if kind != "note" else s.fine + 0.5
            fonts = BF if kind == "p" else {"r": T.BODY_IT, "i": T.BODY, "b": T.BODY_BOLD} if kind == "pi" else BF
            color = T.INK if kind == "p" else T.INK_SOFT
            lead = s.lead if kind != "note" else size * 1.35
            lines = _wrap(blk[1], fonts, size, w)
            n_fit = int(avail // lead)
            if n_fit < 2 and len(lines) > 1:
                return (None, None)
            if len(lines) <= n_fit:
                _draw_lines(c, lines, x, y, size, lead, color, fonts)
                return (len(lines) * lead + lead * 0.45, None)
            # split paragraph
            head, tail = lines[:n_fit], lines[n_fit:]
            _draw_lines(c, head, x, y, size, lead, color, fonts)
            return (n_fit * lead, (kind, _lines_to_markup(tail, fonts)))

        if kind == "h2":
            size = s.h2
            lines = _wrap(blk[1], SF, size, w)
            need = len(lines) * size * 1.12 + 9
            if need + s.lead * 2 > avail:  # keep with following content
                return (None, None)
            _draw_lines(c, lines, x, y - 4, size, size * 1.12, T.PLUM if pg.get("family") == "meditation" else T.INDIGO, SF)
            c.setStrokeColor(T.GOLD_SOFT); c.setLineWidth(0.7)
            c.line(x, y - need + 2, x + 30, y - need + 2)
            return (need + 4, None)

        if kind == "h3":
            size = s.body + 1
            if avail < size * 3: return (None, None)
            c.setFont(T.BODY_BOLD, size); c.setFillColor(T.INDIGO)
            c.drawString(x, y - size, blk[1])
            return (size * 1.7, None)

        if kind == "quote":
            fonts = {"r": T.SERIF_IT_M, "i": T.SERIF_MED, "b": T.SERIF_SB}
            size = s.body + 3.5
            lines = _wrap(blk[1], fonts, size, w * 0.86)
            need = len(lines) * size * 1.22 + 16
            if need > avail: return (None, None)
            M.botanical(c, x + 3, y - need + 8, need - 18, color=T.GOLD_SOFT, weight=0.5)
            _draw_lines(c, lines, x + w * 0.07, y - 8, size, size * 1.22, T.PLUM, fonts)
            return (need, None)

        if kind == "aff":
            fonts = {"r": T.SERIF_MED, "i": T.SERIF_IT_M, "b": T.SERIF_SB}
            size = s.body + 4
            lines = _wrap("“" + blk[1] + "”", fonts, size, w * 0.84)
            need = len(lines) * size * 1.2 + 30
            if need > avail: return (None, None)
            M.rule_with_star(c, x + w * 0.3, x + w * 0.7, y - 6, r=3.2)
            _draw_lines(c, lines, x + w * 0.08, y - 16, size, size * 1.2, T.INDIGO, fonts, align="center", width=w * 0.84)
            return (need, None)

        if kind == "callout":
            title, text = blk[1], blk[2]
            fonts = BF
            size = s.body - 0.3
            lines = _wrap(text, fonts, size, w - 26)
            th = (s.body + 2) * 1.3 if title else 0
            need = len(lines) * size * 1.38 + th + 22
            if need > avail: return (None, None)
            c.setFillColor(T.WASH_GOLD if pg.get("family") != "ritual" else T.CREAM)
            c.setStrokeColor(T.GOLD_SOFT); c.setLineWidth(0.7)
            c.roundRect(x, y - need + 6, w, need - 8, 6, stroke=1, fill=1)
            cy = y - 8
            if title:
                c.setFont(T.BODY_BOLD, s.body); c.setFillColor(T.AMBER)
                c.drawString(x + 13, cy - s.body, title)
                cy -= th
            _draw_lines(c, lines, x + 13, cy - 3, size, size * 1.38, T.INK, fonts)
            return (need + 4, None)

        if kind == "lines":
            n = blk[1]
            gap = s.line_gap
            n_fit = max(0, int((avail - 6) // gap))
            if n_fit == 0: return (None, None)
            draw_n = min(n, n_fit)
            c.setStrokeColor(T.LINE_WARM); c.setLineWidth(0.5)
            yy = y - gap
            for i in range(draw_n):
                c.line(x, yy, x + w, yy); yy -= gap
            rest = ("lines", n - draw_n) if n > draw_n else None
            return (draw_n * gap + 4, rest)

        if kind == "linesfill":
            gap = s.line_gap
            n_fit = max(0, int((avail - 6) // gap))
            c.setStrokeColor(T.LINE_WARM); c.setLineWidth(0.5)
            yy = y - gap
            for i in range(n_fit):
                c.line(x, yy, x + w, yy); yy -= gap
            return (avail, None)

        if kind == "dotsfill":
            gap = max(13, s.line_gap * 0.55)
            c.setFillColor(T.LINE_FAINT)
            yy = y - gap
            while yy > y_min:
                xx = x
                while xx <= x + w:
                    c.circle(xx, yy, 0.7, stroke=0, fill=1)
                    xx += gap
                yy -= gap
            return (avail, None)

        if kind == "prompt":
            text, n = blk[1], blk[2]
            fonts = {"r": T.BODY, "i": T.BODY_IT, "b": T.BODY_BOLD}
            size = s.prompt
            lines = _wrap(text, fonts, size, w - 20)
            head = len(lines) * size * 1.32 + 14
            gap = s.line_gap
            need_min = head + gap + 12
            if need_min > avail: return (None, None)
            n_fit = int((avail - head - 12) // gap)
            draw_n = min(n, max(1, n_fit))
            box_h = head + draw_n * gap + 8
            # frame
            c.setStrokeColor(T.GOLD_SOFT); c.setLineWidth(0.8)
            c.setFillColor(T.CREAM)
            c.roundRect(x, y - box_h, w, box_h, 5, stroke=1, fill=1)
            M.sparkle(c, x + 10, y - 11, 3.0, color=T.GOLD)
            _draw_lines(c, lines, x + 20, y - 8, size, size * 1.32, T.INDIGO, fonts)
            c.setStrokeColor(T.LINE_WARM); c.setLineWidth(0.5)
            yy = y - head - gap * 0.85
            for i in range(draw_n):
                c.line(x + 14, yy, x + w - 14, yy); yy -= gap
            rest = ("lines", n - draw_n) if n - draw_n > 0 else None
            return (box_h + 8, rest)

        if kind == "box":
            h_req, label = blk[1], (blk[2] if len(blk) > 2 else None)
            need = min(h_req, avail)
            if need < 40: return (None, None)
            c.setStrokeColor(T.GOLD_SOFT); c.setLineWidth(0.8)
            c.setFillColor(T.CREAM)
            c.roundRect(x, y - need + 4, w, need - 8, 5, stroke=1, fill=1)
            if label:
                c.setFont(T.BODY_IT, s.fine + 1); c.setFillColor(T.INK_SOFT)
                c.drawString(x + 10, y - s.fine - 8, label)
            return (need, None)

        if kind in ("check", "bullets"):
            items = blk[1]
            fonts = BF
            size = s.body
            lead = size * 1.42
            done, used = 0, 0
            for it in items:
                lines = _wrap(it, fonts, size, w - 22)
                need = len(lines) * lead + 4
                if used + need > avail:
                    break
                yy = y - used
                if kind == "check":
                    c.setStrokeColor(T.GOLD); c.setLineWidth(0.8)
                    c.roundRect(x + 1, yy - size - 1.5, size * 0.82, size * 0.82, 2, stroke=1, fill=0)
                else:
                    M.dot(c, x + 4, yy - size * 0.62, 1.5, T.GOLD)
                _draw_lines(c, lines, x + 22, yy, size, lead, T.INK, fonts)
                used += need
                done += 1
            if done == 0: return (None, None)
            rest = (kind, items[done:]) if done < len(items) else None
            return (used + 4, rest)

        if kind == "steps":
            items = blk[1]
            size = s.body
            done, used = 0, 0
            for idx, (st, sd) in enumerate(items):
                tl = _wrap(sd, BF, size, w - 34)
                need = size * 1.5 + len(tl) * size * 1.35 + 8
                if used + need > avail:
                    break
                yy = y - used
                # numbered gold circle
                r = size * 0.72
                c.setStrokeColor(T.GOLD); c.setLineWidth(0.9)
                c.circle(x + r, yy - r - 1, r, stroke=1, fill=0)
                c.setFont(T.SERIF_SB, size + 1); c.setFillColor(T.AMBER)
                c.drawCentredString(x + r, yy - r - 1 - (size + 1) * 0.34, str(blk[2] + idx if len(blk) > 2 else idx + 1))
                c.setFont(T.BODY_BOLD, size); c.setFillColor(T.INDIGO)
                c.drawString(x + 34, yy - size, st)
                _draw_lines(c, tl, x + 34, yy - size * 1.5, size, size * 1.35, T.INK, BF)
                used += need
                done += 1
            if done == 0: return (None, None)
            rest = ("steps", items[done:], (blk[2] if len(blk) > 2 else 1) + done) if done < len(items) else None
            return (used + 2, rest)

        if kind == "fields":
            items = blk[1]
            size = s.body
            row_h = s.line_gap
            done, used = 0, 0
            for label in items:
                if used + row_h > avail: break
                yy = y - used - size
                c.setFont(T.BODY, size); c.setFillColor(T.INK)
                lw = pdfmetrics.stringWidth(label, T.BODY, size)
                c.drawString(x, yy, label)
                c.setStrokeColor(T.LINE_WARM); c.setLineWidth(0.5)
                c.line(x + lw + 8, yy - 2, x + w, yy - 2)
                used += row_h; done += 1
            if done == 0: return (None, None)
            rest = ("fields", items[done:]) if done < len(items) else None
            return (used + 4, rest)

        if kind == "twocol":
            lt, rt, n = blk[1], blk[2], blk[3]
            gap = s.line_gap
            head = s.body * 1.6
            need = head + min(n, 3) * gap + 10
            if need > avail: return (None, None)
            n_fit = int((avail - head - 10) // gap)
            draw_n = min(n, n_fit)
            colw = (w - 18) / 2.0
            for ci, ttl in enumerate((lt, rt)):
                cx = x + ci * (colw + 18)
                c.setFont(T.BODY_BOLD, s.body); c.setFillColor(T.INDIGO)
                c.drawString(cx, y - s.body, ttl)
                c.setStrokeColor(T.GOLD_SOFT); c.setLineWidth(0.8)
                c.line(cx, y - head + 3, cx + colw, y - head + 3)
                c.setStrokeColor(T.LINE_WARM); c.setLineWidth(0.5)
                yy = y - head - gap * 0.8
                for i in range(draw_n):
                    c.line(cx, yy, cx + colw, yy); yy -= gap
            c.setStrokeColor(T.GOLD_SOFT); c.setLineWidth(0.5)
            c.line(x + colw + 9, y - 2, x + colw + 9, y - head - draw_n * gap)
            rest = ("twocol", lt + " (cont.)", rt + " (cont.)", n - draw_n) if n - draw_n > 0 else None
            return (head + draw_n * gap + 8, rest)

        if kind == "table":
            headers, rows = blk[1], blk[2]
            widths = blk[3] if len(blk) > 3 else None
            size = s.body - 0.5
            if widths is None:
                widths = [1.0 / len(headers)] * len(headers)
            colx = [x]
            for fw in widths:
                colx.append(colx[-1] + fw * w)
            # wrap all cells
            def cell_lines(txt, ci, bold=False):
                f = {"r": T.BODY_BOLD if bold else T.BODY, "i": T.BODY_IT, "b": T.BODY_BOLD}
                return _wrap(str(txt), f, size, colx[ci + 1] - colx[ci] - 10), f
            hh = max(len(cell_lines(h, i, True)[0]) for i, h in enumerate(headers)) * size * 1.3 + 8
            done, used = 0, hh
            if hh + size * 2.4 > avail: return (None, None)
            # header band
            c.setFillColor(T.INDIGO)
            c.rect(x, y - hh, w, hh, stroke=0, fill=1)
            for i, h in enumerate(headers):
                ls, f = cell_lines(h, i, True)
                _draw_lines(c, ls, colx[i] + 5, y - 4, size, size * 1.3, T.STARLIGHT, f)
            for ri, row in enumerate(rows):
                cls = [cell_lines(cell, ci) for ci, cell in enumerate(row)]
                rh = max(len(l[0]) for l in cls) * size * 1.3 + 7
                if used + rh > avail:
                    break
                yy = y - used
                if ri % 2 == 1:
                    c.setFillColor(T.WASH_GOLD)
                    c.rect(x, yy - rh, w, rh, stroke=0, fill=1)
                for ci, (ls, f) in enumerate(cls):
                    _draw_lines(c, ls, colx[ci] + 5, yy - 3.5, size, size * 1.3, T.INK, f)
                used += rh
                done += 1
            c.setStrokeColor(T.GOLD_SOFT); c.setLineWidth(0.7)
            c.rect(x, y - used, w, used, stroke=1, fill=0)
            rest = ("table", headers, rows[done:], widths) if done < len(rows) else None
            return (used + 8, rest)

        if kind == "kv":
            pairs = blk[1]
            size = s.body
            done, used = 0, 0
            for k, v in pairs:
                vl = _wrap(v, BF, size, w - 16)
                need = size * 1.45 + len(vl) * size * 1.32 + 6
                if used + need > avail: break
                yy = y - used
                c.setFont(T.SERIF_SB, size + 2); c.setFillColor(T.AMBER)
                c.drawString(x, yy - size, k)
                _draw_lines(c, vl, x + 16, yy - size * 1.5, size, size * 1.32, T.INK, BF)
                used += need; done += 1
            if done == 0: return (None, None)
            rest = ("kv", pairs[done:]) if done < len(pairs) else None
            return (used + 4, rest)

        if kind == "scale":
            label = blk[1]
            size = s.body
            need = size * 1.4 + 26
            if need > avail: return (None, None)
            c.setFont(T.BODY, size); c.setFillColor(T.INK)
            c.drawString(x, y - size, label)
            r = min(9.0, w / 26.0)
            span = w - 2 * r
            for i in range(10):
                cx = x + r + span * i / 9.0
                cy = y - size * 1.5 - r - 4
                c.setStrokeColor(T.GOLD); c.setLineWidth(0.8)
                c.circle(cx, cy, r, stroke=1, fill=0)
                c.setFont(T.BODY, s.fine); c.setFillColor(T.INK_SOFT)
                c.drawCentredString(cx, cy - s.fine * 0.35, str(i + 1))
            return (need + r, None)

        if kind == "wheel":
            labels = blk[1]
            R = min(w * 0.33, avail * 0.36)
            if R < 46: return (None, None)
            cx, cy = x + w / 2.0, y - R - s.body * 2.6
            n = len(labels)
            for ring in range(1, 6):
                c.setStrokeColor(T.LINE_WARM if ring < 5 else T.GOLD)
                c.setLineWidth(0.5 if ring < 5 else 0.9)
                c.circle(cx, cy, R * ring / 5.0, stroke=1, fill=0)
            for i in range(n):
                ang = 2 * math.pi * i / n + math.pi / 2
                c.setStrokeColor(T.GOLD_SOFT); c.setLineWidth(0.6)
                c.line(cx, cy, cx + R * math.cos(ang), cy + R * math.sin(ang))
            c.setFont(T.BODY, s.fine + 0.5); c.setFillColor(T.INDIGO)
            for i, lab in enumerate(labels):
                ang = 2 * math.pi * (i + 0.5) / n + math.pi / 2
                lx = cx + (R + 10) * math.cos(ang)
                ly = cy + (R + 10) * math.sin(ang)
                if math.cos(ang) > 0.3:
                    c.drawString(lx, ly - s.fine * 0.3, lab)
                elif math.cos(ang) < -0.3:
                    c.drawRightString(lx, ly - s.fine * 0.3, lab)
                else:
                    c.drawCentredString(lx, ly - s.fine * 0.3, lab)
            need = 2 * R + s.body * 5.4
            return (min(avail, need), None)

        if kind == "grid":
            rlabels, clabels = blk[1], blk[2]
            size = s.fine + 1
            label_w = max(pdfmetrics.stringWidth(rl, T.BODY, size) for rl in rlabels) + 10
            cell = min(24.0, (w - label_w) / max(1, len(clabels)))
            head = size * 1.8
            row_h = max(cell * 0.8, size * 1.9)
            done, used = 0, head
            if head + row_h > avail: return (None, None)
            c.setFont(T.BODY_BOLD, size); c.setFillColor(T.INDIGO)
            for ci, cl in enumerate(clabels):
                c.drawCentredString(x + label_w + cell * (ci + 0.5), y - size, str(cl))
            for ri, rl in enumerate(rlabels):
                if used + row_h > avail: break
                yy = y - used
                c.setFont(T.BODY, size); c.setFillColor(T.INK)
                c.drawString(x, yy - row_h * 0.62, rl)
                for ci in range(len(clabels)):
                    c.setStrokeColor(T.LINE_WARM); c.setLineWidth(0.5)
                    c.rect(x + label_w + cell * ci, yy - row_h, cell, row_h, stroke=1, fill=0)
                used += row_h; done += 1
            rest = ("grid", rlabels[done:], clabels) if done < len(rlabels) else None
            return (used + 6, rest)

        if kind == "sig":
            label = blk[1]
            need = s.body * 3
            if need > avail: return (None, None)
            c.setStrokeColor(T.GOLD); c.setLineWidth(0.7)
            c.line(x + w * 0.1, y - s.body * 1.6, x + w * 0.62, y - s.body * 1.6)
            c.setFont(T.BODY_IT, s.fine + 1); c.setFillColor(T.INK_SOFT)
            c.drawString(x + w * 0.1, y - s.body * 1.6 - s.fine - 3, label)
            return (need, None)

        if kind == "daymark":
            # solar day header: number in rayed circle + day name
            n, name, date_line = blk[1], blk[2], blk[3]
            R = s.h1 * 1.15
            need = R * 2 + 14
            if need > avail: return (None, None)
            cx = x + R + 2
            cy = y - R - 4
            M.sun_rays(c, cx, cy, R * 0.78, R, color=T.GOLD, n=28, weight=0.6)
            c.setStrokeColor(T.GOLD); c.setLineWidth(1.0)
            c.circle(cx, cy, R * 0.7, stroke=1, fill=0)
            c.setFont(T.SERIF_SB, s.h1 * 1.25); c.setFillColor(T.INDIGO)
            c.drawCentredString(cx, cy - s.h1 * 0.44, str(n))
            tx = x + R * 2 + 16
            _kicker_text(c, tx, cy + s.h2 * 0.6, "Day " + ["One","Two","Three","Four","Five","Six","Seven","Eight"][n-1], s.kicker + 1, T.AMBER)
            c.setFont(T.SERIF_SB, s.h1); c.setFillColor(T.INDIGO)
            c.drawString(tx, cy - s.h1 * 0.5, name)
            c.setFont(T.BODY_IT, s.fine + 1); c.setFillColor(T.INK_SOFT)
            c.drawString(tx, cy - s.h1 * 0.5 - s.fine * 1.6, date_line)
            return (need, None)

        if kind == "cardaff":
            # affirmation list with stars (for affirmation pages)
            items = blk[1]
            size = s.body + 0.5
            fonts = {"r": T.SERIF_MED, "i": T.SERIF_IT_M, "b": T.SERIF_SB}
            done, used = 0, 0
            for it in items:
                ls = _wrap(it, fonts, size + 1.5, w - 20)
                need = len(ls) * (size + 1.5) * 1.24 + 7
                if used + need > avail: break
                yy = y - used
                M.eight_point_star(c, x + 4, yy - size * 0.7, 3.6, color=T.GOLD, weight=0.5)
                _draw_lines(c, ls, x + 18, yy, size + 1.5, (size + 1.5) * 1.24, T.INK, fonts)
                used += need; done += 1
            if done == 0: return (None, None)
            rest = ("cardaff", items[done:]) if done < len(items) else None
            return (used + 4, rest)

        raise ValueError("unknown block %r" % (kind,))

    # ---------------------------------------------------------- special pages
    def _draw_cover(self, c, pg):
        s = self.s
        c.setFillColor(T.INDIGO_DEEP)
        c.rect(0, 0, s.w, s.h, stroke=0, fill=1)
        c.setFillColor(T.INDIGO)
        c.rect(0, s.h * 0.12, s.w, s.h * 0.83, stroke=0, fill=1)
        M.starfield(c, s.w * 0.06, s.h * 0.5, s.w * 0.88, s.h * 0.44, seed=pg.get("seed", 5), n=46)
        M.starfield(c, s.w * 0.06, s.h * 0.08, s.w * 0.88, s.h * 0.22, seed=3, n=16)
        cx = s.w / 2.0
        # arch frame with medallion — the visual centerpiece, above the title
        aw = s.w * 0.5
        ah = s.h * 0.36
        M.portal_arch(c, cx - aw / 2, s.h * 0.42, aw, ah, color=T.GOLD_ON_DARK, weight=1.1, layers=3)
        M.lion_medallion(c, cx, s.h * 0.60, min(aw, ah) * 0.30, color=T.GOLD_ON_DARK, weight=0.8)
        # brand
        _kicker_text(c, 0, s.h * 0.93, pg.get("brand", self.brand), s.kicker + 1, T.GOLD_ON_DARK, align="center", cx=cx)
        # title
        title = pg.get("title", self.title)
        fonts = {"r": T.SERIF_MED, "i": T.SERIF_IT_M, "b": T.SERIF_SB}
        size = s.h1 * 1.45
        lines = _wrap(title, fonts, size, s.w * 0.84)
        ty = s.h * 0.36
        _draw_lines(c, lines, cx - s.w * 0.42, ty, size, size * 1.08, T.STARLIGHT, fonts, align="center", width=s.w * 0.84)
        ty -= len(lines) * size * 1.08 + s.h2 * 1.0
        sub = pg.get("subtitle", self.subtitle)
        if sub:
            sf = {"r": T.SERIF_IT, "i": T.SERIF, "b": T.SERIF_IT_M}
            ssize = s.h2 * 0.95
            sl = _wrap(sub, sf, ssize, s.w * 0.7)
            _draw_lines(c, sl, cx - s.w * 0.35, ty, ssize, ssize * 1.25, T.GOLD_ON_DARK, sf, align="center", width=s.w * 0.7)
            ty -= len(sl) * ssize * 1.25
        tag = pg.get("tagline")
        if tag and ty > s.h * 0.19:
            _kicker_text(c, 0, s.h * 0.135, tag, s.kicker, T.GOLD_SOFT, align="center", cx=cx)
        M.rule_with_star(c, cx - s.w * 0.16, cx + s.w * 0.16, s.h * 0.105, color=T.GOLD_ON_DARK, r=3.6)

    def _draw_back(self, c, pg):
        s = self.s
        c.setFillColor(T.INDIGO_DEEP)
        c.rect(0, 0, s.w, s.h, stroke=0, fill=1)
        M.starfield(c, s.w * 0.1, s.h * 0.15, s.w * 0.8, s.h * 0.7, seed=9, n=40)
        cx = s.w / 2.0
        M.eight_point_star(c, cx, s.h * 0.58, 22, color=T.GOLD_ON_DARK, weight=0.8)
        fonts = {"r": T.SERIF_IT_M, "i": T.SERIF_MED, "b": T.SERIF_SB}
        size = s.h2 * 1.1
        lines = _wrap(pg.get("quote", ""), fonts, size, s.w * 0.6)
        ty = s.h * 0.5
        _draw_lines(c, lines, cx - s.w * 0.3, ty, size, size * 1.3, T.STARLIGHT, fonts, align="center", width=s.w * 0.6)
        _kicker_text(c, 0, s.h * 0.12, pg.get("brand", self.brand), s.kicker, T.GOLD_ON_DARK, align="center", cx=cx)

    def _draw_divider(self, c, pg):
        s = self.s
        c.setFillColor(T.INDIGO)
        c.rect(0, 0, s.w, s.h, stroke=0, fill=1)
        seed = pg.get("seed", self.page_no)
        M.starfield(c, s.w * 0.08, s.h * 0.6, s.w * 0.84, s.h * 0.32, seed=seed, n=30)
        cx = s.w / 2.0
        num = pg.get("num", "")
        if num:
            _kicker_text(c, 0, s.h * 0.78, "Part " + num, s.kicker + 1, T.GOLD_SOFT, align="center", cx=cx)
        # motif varies per divider
        motif = pg.get("motif", "star")
        my = s.h * 0.62
        gold = T.GOLD_ON_DARK
        if motif == "arch":
            M.portal_arch(c, cx - 40, my - 30, 80, 92, color=gold, weight=1.0)
        elif motif == "lion":
            M.lion_medallion(c, cx, my + 10, 44, color=gold)
        elif motif == "sun":
            M.sun_rays(c, cx, my + 10, 22, 44, color=gold, n=32, weight=0.7)
            c.setStrokeColor(gold); c.setLineWidth(1.0); c.circle(cx, my + 10, 18, stroke=1, fill=0)
        elif motif == "moon":
            M.crescent(c, cx, my + 10, 26, color=gold, weight=0.9)
        elif motif == "infinity":
            M.infinity(c, cx, my + 10, 90, color=gold, weight=1.1)
        elif motif == "constellation":
            M.constellation(c, cx - 55, my - 15, 110, 60, color=gold, seed=seed * 7 + 2, n=8)
        elif motif == "geometry":
            M.sacred_geometry(c, cx, my + 8, 30, color=gold, weight=0.5)
        elif motif == "botanical":
            M.botanical(c, cx - 20, my - 25, 75, color=gold, weight=0.7)
            M.botanical(c, cx + 20, my - 25, 75, color=gold, weight=0.7, flip=True)
        else:
            M.eight_point_star(c, cx, my + 10, 34, color=gold, weight=0.9)
        fonts = {"r": T.SERIF_MED, "i": T.SERIF_IT_M, "b": T.SERIF_SB}
        size = s.h1 * 1.18
        lines = _wrap(pg["title"], fonts, size, s.w * 0.76)
        ty = s.h * 0.47
        _draw_lines(c, lines, cx - s.w * 0.38, ty, size, size * 1.1, T.STARLIGHT, fonts, align="center", width=s.w * 0.76)
        ty -= len(lines) * size * 1.1 + 8
        sub = pg.get("subtitle")
        if sub:
            sf = {"r": T.SERIF_IT, "i": T.SERIF, "b": T.SERIF_IT_M}
            sl = _wrap(sub, sf, s.h2, s.w * 0.62)
            _draw_lines(c, sl, cx - s.w * 0.31, ty, s.h2, s.h2 * 1.25, T.GOLD_ON_DARK, sf, align="center", width=s.w * 0.62)
            ty -= len(sl) * s.h2 * 1.25
        M.rule_with_star(c, cx - s.w * 0.14, cx + s.w * 0.14, ty - 10, color=T.GOLD_SOFT, r=3.2)

    def _draw_toc(self, c, pg, entries, final):
        s = self.s
        per_page = max(10, int((s.h - s.m_top - s.m_bottom - s.h1 * 2.4) // (s.body * 1.75)))
        chunks = [entries[i:i + per_page]] if False else [entries[i:i + per_page] for i in range(0, max(len(entries), 1), per_page)]
        for chunk_i, chunk in enumerate(chunks):
            self._begin_page(c)
            if chunk_i == 0:
                self._toc_pageno = self.page_no
            x0, x1, y, y_min = self._chrome(c, {"family": "front", "section": pg.get("section", "Contents")})
            if chunk_i == 0:
                if final:
                    c.bookmarkPage("TOC")
                    self._bookmark(c, "Contents", 0)
                fonts = {"r": T.SERIF_MED, "i": T.SERIF_IT_M, "b": T.SERIF_SB}
                _draw_lines(c, _wrap("Contents", fonts, s.h1, x1 - x0), x0, y, s.h1, s.h1 * 1.1, T.INDIGO, fonts)
                c.setStrokeColor(T.GOLD); c.setLineWidth(1.0)
                c.line(x0, y - s.h1 * 1.3, x0 + 52, y - s.h1 * 1.3)
                y -= s.h1 * 1.3 + s.lead
            for level, label, pno in chunk:
                size = s.body + (2.2 if level == 0 else 0)
                font = T.SERIF_SB if level == 0 else T.BODY
                color = T.INDIGO if level == 0 else T.INK
                indent = 0 if level == 0 else 14
                if level == 0:
                    y -= size * 0.55
                c.setFont(font, size); c.setFillColor(color)
                c.drawString(x0 + indent, y - size, label)
                c.setFont(T.BODY, s.body - 0.5); c.setFillColor(T.INK_SOFT)
                c.drawRightString(x1, y - size, str(pno))
                lw = pdfmetrics.stringWidth(label, font, size)
                nw = pdfmetrics.stringWidth(str(pno), T.BODY, s.body - 0.5)
                c.setStrokeColor(T.LINE_FAINT); c.setLineWidth(0.5)
                c.setDash(1, 3)
                c.line(x0 + indent + lw + 6, y - size, x1 - nw - 6, y - size)
                c.setDash()
                if final and self.s.digital:
                    c.linkAbsolute("", "pg%d" % pno, (x0, y - size - 2, x1, y + 2), thickness=0)
                y -= size * 1.75
            self._finish(c)

    def page_anchor_pass(self):
        """Ensure every page gets an anchor 'pgN' for TOC links (digital)."""
        pass


def make_anchor_hook(book):
    """Digital editions: drop a named destination on every page so TOC links work."""
    orig_begin = book._begin_page
    def begin(c):
        orig_begin(c)
        try:
            c.bookmarkPage("pg%d" % book.page_no)
        except Exception:
            pass
    book._begin_page = begin
