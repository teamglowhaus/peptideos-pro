"""Hand-drawn vector motifs: celestial, solar and leonine line art.

Everything here is original geometry drawn with reportlab primitives so the
artwork is resolution-independent, ink-light and consistent across editions.
"""
import math
from reportlab.lib.colors import Color
from . import theme as T


def _poly(c, pts, stroke=None, fill=None, width=0.6, closed=True):
    p = c.beginPath()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    if closed:
        p.close()
    if stroke: c.setStrokeColor(stroke)
    if fill: c.setFillColor(fill)
    c.setLineWidth(width)
    c.drawPath(p, stroke=1 if stroke else 0, fill=1 if fill else 0)


def eight_point_star(c, x, y, r, color=T.GOLD, fill=False, weight=0.6):
    """Elegant 8-spike star: long thin spikes alternating with short ones."""
    pts = []
    for i in range(16):
        ang = math.pi / 8 * i + math.pi / 2
        rad = r if i % 2 == 0 else r * 0.36
        pts.append((x + rad * math.cos(ang), y + rad * math.sin(ang)))
    _poly(c, pts, stroke=None if fill else color, fill=color if fill else None, width=weight)


def sparkle(c, x, y, r, color=T.GOLD, weight=0.5):
    """Tiny four-point sparkle."""
    pts = []
    for i in range(8):
        ang = math.pi / 4 * i + math.pi / 2
        rad = r if i % 2 == 0 else r * 0.28
        pts.append((x + rad * math.cos(ang), y + rad * math.sin(ang)))
    _poly(c, pts, fill=color, width=weight)


def dot(c, x, y, r, color=T.GOLD):
    c.setFillColor(color)
    c.circle(x, y, r, stroke=0, fill=1)


def sun_rays(c, x, y, r_in, r_out, color=T.GOLD, n=24, weight=0.55, arc=(0, 360)):
    """Radial thin rays alternating long/short, optionally over a partial arc."""
    c.setStrokeColor(color)
    c.setLineWidth(weight)
    a0, a1 = math.radians(arc[0]), math.radians(arc[1])
    for i in range(n + 1):
        ang = a0 + (a1 - a0) * i / n
        ro = r_out if i % 2 == 0 else r_in + (r_out - r_in) * 0.45
        c.line(x + r_in * math.cos(ang), y + r_in * math.sin(ang),
               x + ro * math.cos(ang), y + ro * math.sin(ang))


def portal_arch(c, x, y, w, h, color=T.GOLD, weight=0.8, layers=3, gap=None):
    """Nested round-top arches — the 'gate'. (x,y) is bottom-left of outer arch."""
    gap = gap or max(3.0, w * 0.045)
    c.setStrokeColor(color)
    for i in range(layers):
        c.setLineWidth(weight if i == 0 else weight * 0.6)
        ax, aw = x + i * gap, w - 2 * i * gap
        ah = h - i * gap
        r = aw / 2.0
        p = c.beginPath()
        p.moveTo(ax, y)
        p.lineTo(ax, y + ah - r)
        p.arcTo(ax, y + ah - 2 * r, ax + aw, y + ah, startAng=180, extent=-180)
        p.lineTo(ax + aw, y)
        c.drawPath(p, stroke=1, fill=0)


def constellation(c, x, y, w, h, color=T.GOLD, seed=7, n=7, weight=0.4):
    """Small constellation: deterministic pseudo-random dots joined by hairlines."""
    pts = []
    s = seed
    for i in range(n):
        s = (s * 9301 + 49297) % 233280
        fx = s / 233280.0
        s = (s * 9301 + 49297) % 233280
        fy = s / 233280.0
        pts.append((x + fx * w, y + fy * h))
    c.setStrokeColor(color)
    c.setLineWidth(weight)
    for a, b in zip(pts, pts[1:]):
        c.line(a[0], a[1], b[0], b[1])
    for i, (px, py) in enumerate(pts):
        if i % 3 == 0:
            sparkle(c, px, py, 3.2, color=color)
        else:
            dot(c, px, py, 1.1, color=color)


def infinity(c, x, y, w, color=T.GOLD, weight=0.9):
    """Lemniscate centered at (x, y) with total width w."""
    a = w / 2.0
    b = a * 0.42
    c.setStrokeColor(color)
    c.setLineWidth(weight)
    p = c.beginPath()
    p.moveTo(x, y)
    p.curveTo(x + a * 0.55, y + b, x + a, y + b, x + a, y)
    p.curveTo(x + a, y - b, x + a * 0.55, y - b, x, y)
    p.curveTo(x - a * 0.55, y + b, x - a, y + b, x - a, y)
    p.curveTo(x - a, y - b, x - a * 0.55, y - b, x, y)
    c.drawPath(p, stroke=1, fill=0)


def botanical(c, x, y, h, color=T.GOLD, weight=0.55, flip=False):
    """Delicate laurel-like sprig rising from (x, y)."""
    d = -1 if flip else 1
    c.setStrokeColor(color)
    c.setLineWidth(weight)
    p = c.beginPath()
    p.moveTo(x, y)
    p.curveTo(x + d * h * 0.12, y + h * 0.35, x + d * h * 0.05, y + h * 0.7, x + d * h * 0.18, y + h)
    c.drawPath(p, stroke=1, fill=0)
    for i in range(4):
        t = 0.25 + i * 0.2
        sx = x + d * h * (0.12 * math.sin(t * 2.4))
        sy = y + h * t
        for side in (-1, 1):
            leaf = c.beginPath()
            leaf.moveTo(sx, sy)
            leaf.curveTo(sx + side * h * 0.09, sy + h * 0.03,
                         sx + side * h * 0.11, sy + h * 0.09,
                         sx + side * h * 0.02, sy + h * 0.11)
            c.drawPath(leaf, stroke=1, fill=0)


def lion_medallion(c, x, y, r, color=T.GOLD, weight=0.7):
    """Sun-lion medallion: inner circle wrapped in a mane of alternating flame
    rays — reads as both sun and lion without cartoon features."""
    c.setStrokeColor(color)
    c.setLineWidth(weight)
    c.circle(x, y, r * 0.52, stroke=1, fill=0)
    c.setLineWidth(weight * 0.6)
    c.circle(x, y, r * 0.46, stroke=1, fill=0)
    n = 16
    for i in range(n):
        ang = 2 * math.pi * i / n
        r0 = r * 0.56
        r1 = r if i % 2 == 0 else r * 0.8
        # curved flame ray (mane lock)
        x0, y0 = x + r0 * math.cos(ang), y + r0 * math.sin(ang)
        x1, y1 = x + r1 * math.cos(ang + 0.09), y + r1 * math.sin(ang + 0.09)
        mx = x + (r0 + (r1 - r0) * 0.5) * math.cos(ang - 0.12)
        my = y + (r0 + (r1 - r0) * 0.5) * math.sin(ang - 0.12)
        p = c.beginPath()
        p.moveTo(x0, y0)
        p.curveTo(mx, my, mx, my, x1, y1)
        c.drawPath(p, stroke=1, fill=0)
    eight_point_star(c, x, y, r * 0.24, color=color, fill=True, weight=0.4)


def corner_ornament(c, x, y, size, color=T.GOLD, quadrant="tl", weight=0.6):
    """Fine double-rule corner with a small star. quadrant: tl/tr/bl/br."""
    sx = 1 if quadrant in ("tl", "bl") else -1
    sy = -1 if quadrant in ("tl", "tr") else 1
    c.setStrokeColor(color)
    c.setLineWidth(weight)
    c.line(x, y, x + sx * size, y)
    c.line(x, y, x, y + sy * size)
    g = size * 0.14
    c.setLineWidth(weight * 0.55)
    c.line(x + sx * g, y + sy * g, x + sx * (size * 0.62), y + sy * g)
    c.line(x + sx * g, y + sy * g, x + sx * g, y + sy * (size * 0.62))
    eight_point_star(c, x + sx * g, y + sy * g, size * 0.13, color=color, weight=0.45)


def rule_with_star(c, x0, x1, y, color=T.GOLD, weight=0.7, r=4.2):
    """Thin horizontal rule with a centered eight-point star."""
    mid = (x0 + x1) / 2.0
    c.setStrokeColor(color)
    c.setLineWidth(weight)
    c.line(x0, y, mid - r * 2.2, y)
    c.line(mid + r * 2.2, y, x1, y)
    eight_point_star(c, mid, y, r, color=color, weight=0.5)


def crescent(c, x, y, r, color=T.GOLD, weight=0.6):
    """Fine-line crescent moon."""
    c.setStrokeColor(color)
    c.setLineWidth(weight)
    p = c.beginPath()
    p.arc(x - r, y - r, x + r, y + r, startAng=300, extent=180)
    c.drawPath(p, stroke=1, fill=0)
    p = c.beginPath()
    p.arc(x - r * 0.55, y - r * 0.92, x + r * 1.18, y + r * 0.88, startAng=300, extent=160)
    c.drawPath(p, stroke=1, fill=0)


def starfield(c, x, y, w, h, color=None, seed=11, n=42):
    """Scatter of faint stars for dark pages."""
    color = color or Color(0.85, 0.78, 0.62, alpha=0.9)
    s = seed
    for i in range(n):
        s = (s * 9301 + 49297) % 233280; fx = s / 233280.0
        s = (s * 9301 + 49297) % 233280; fy = s / 233280.0
        s = (s * 9301 + 49297) % 233280; fr = s / 233280.0
        px, py = x + fx * w, y + fy * h
        if i % 9 == 0:
            eight_point_star(c, px, py, 4.5 + fr * 3, color=color, weight=0.4)
        elif i % 5 == 0:
            sparkle(c, px, py, 2.4 + fr * 1.6, color=color)
        else:
            dot(c, px, py, 0.55 + fr * 0.65, color=color)


def sacred_geometry(c, x, y, r, color=T.GOLD, weight=0.4):
    """Overlapping-circle rosette (seed-of-life style), very faint."""
    c.setStrokeColor(color)
    c.setLineWidth(weight)
    c.circle(x, y, r, stroke=1, fill=0)
    for i in range(6):
        ang = math.pi / 3 * i
        c.circle(x + r * math.cos(ang), y + r * math.sin(ang), r, stroke=1, fill=0)


def gate_886(c, x, y, h, color=T.GOLD, weight=0.8):
    """Pair of tall '8'-evoking stacked circles beside an arch — abstract 8/8 mark."""
    r = h * 0.18
    for cx in (x - h * 0.28, x + h * 0.28):
        c.setStrokeColor(color)
        c.setLineWidth(weight)
        c.circle(cx, y + h * 0.3, r, stroke=1, fill=0)
        c.circle(cx, y + h * 0.66, r * 0.82, stroke=1, fill=0)
    portal_arch(c, x - h * 0.16, y + h * 0.12, h * 0.32, h * 0.72, color=color, weight=weight * 0.7, layers=2)
