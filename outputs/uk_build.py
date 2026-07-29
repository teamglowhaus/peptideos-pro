# -*- coding: utf-8 -*-
"""
Build the Ukrainian edition in two independently-optimised print sizes.

Every coordinate in the builder is derived from W/H/M/IW at draw time, so
patching those module globals before a build makes each page genuinely
reflow for that paper size (line lengths, centring, vertical rhythm) — not
a scaled copy.
"""
import os
from reportlab.pdfgen import canvas as rlc
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch

import interior_uk_gen as b

HERE = os.path.dirname(os.path.abspath(__file__))


def _run(c):
    pn = 1
    b.build_cover(c);              c.showPage(); pn += 1
    b.build_title_page(c, pn);     c.showPage(); pn += 1
    b.build_license_page(c, pn);   c.showPage(); pn += 1
    b.build_welcome(c, pn);        c.showPage(); pn += 1
    b.build_method(c, pn);         c.showPage(); pn += 1
    b.build_how_to_use(c, pn);     c.showPage(); pn += 1
    b.build_portal_intention(c, pn); c.showPage(); pn += 1
    b.build_commitments(c, pn);    c.showPage(); pn += 1
    b.build_moon_overview(c, pn);  c.showPage(); pn += 1
    for day in range(1, 29):
        b.build_morning_page(c, day, pn); c.showPage(); pn += 1
        b.build_evening_page(c, day, pn); c.showPage(); pn += 1
    for week in range(1, 5):
        b.build_weekly_review(c, week, pn); c.showPage(); pn += 1
    for i in range(4):
        b.build_monthly_review(c, i, pn); c.showPage(); pn += 1
    for i in range(8):
        b.build_shadow_work(c, i, pn); c.showPage(); pn += 1
    for _ in range(16):
        b.build_sync_log(c, pn); c.showPage(); pn += 1
    for month_idx in range(4):
        for page_in_month in range(4):
            b.build_moon_calendar(c, month_idx, page_in_month, pn)
            c.showPage(); pn += 1
    for i in range(8):
        b.build_bonus_page(c, i, pn); c.showPage(); pn += 1
    b.build_closing(c, pn);   c.showPage(); pn += 1
    b.build_thank_you(c, pn); c.showPage()
    return pn


def build(pagesize, out_path, label):
    # Independently optimise geometry for this paper size
    b.W, b.H = pagesize
    b.M  = 0.75 * inch
    b.IW = b.W - 2 * b.M
    b.PRINT_SAFE = True          # cream backgrounds so handwriting shows in print
    b.setup_fonts()
    c = rlc.Canvas(out_path, pagesize=pagesize)
    pn = _run(c)
    c.save()
    print(f"Saved  {out_path}  ({pn} pages, {os.path.getsize(out_path)//1024} KB)  [{label}]")


if __name__ == "__main__":
    build(letter, os.path.join(HERE, "Портал 369 — Щоденник маніфестації — US Letter.pdf"), "US LETTER")
    build(A4,     os.path.join(HERE, "Портал 369 — Щоденник маніфестації — A4.pdf"),        "A4")
