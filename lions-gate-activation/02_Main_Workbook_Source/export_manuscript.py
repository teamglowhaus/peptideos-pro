# -*- coding: utf-8 -*-
"""Export the complete written content of The Lion's Gate 8/8 Activation as a
single design-tool-ready Markdown manuscript (no layout, just structured text),
so the copy can be re-designed in Canva, another AI platform, InDesign, etc."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "05_Planner_Insert_Source"))

import build_main
import planner_content
from affirmations import AFFIRMATIONS, CARD_SETS, WALLPAPERS

DAY_WORDS = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight"]

def block_md(blk):
    kind = blk[0]
    if kind in ("p", "cp"):
        return [blk[1], ""]
    if kind == "pi":
        return ["*%s*" % blk[1], ""]
    if kind == "note":
        return ["> Note: %s" % blk[1], ""]
    if kind == "h2":
        return ["### %s" % blk[1], ""]
    if kind == "h3":
        return ["#### %s" % blk[1], ""]
    if kind == "ck":
        return ["*%s*" % blk[1], ""]
    if kind == "quote":
        return ["> %s" % blk[1], ""]
    if kind == "aff":
        return ["> ✦ Affirmation: “%s”" % blk[1], ""]
    if kind == "callout":
        return ["> **%s** — %s" % (blk[1], blk[2]), ""]
    if kind == "prompt":
        return ["**Prompt:** %s  *(%d writing lines)*" % (blk[1], blk[2]), ""]
    if kind == "lines":
        return ["*(%d ruled writing lines)*" % blk[1], ""]
    if kind == "linesfill":
        return ["*(rest of page: ruled writing lines)*", ""]
    if kind == "dotsfill":
        return ["*(rest of page: dot grid)*", ""]
    if kind == "box":
        label = blk[2] if len(blk) > 2 and blk[2] else "open writing box"
        return ["*(writing box: %s)*" % label, ""]
    if kind == "check":
        return ["- [ ] %s" % it for it in blk[1]] + [""]
    if kind == "bullets":
        return ["- %s" % it for it in blk[1]] + [""]
    if kind == "cardaff":
        return ["- ✦ %s" % it for it in blk[1]] + [""]
    if kind == "steps":
        return ["%d. **%s** — %s" % (i + 1, t, d) for i, (t, d) in enumerate(blk[1])] + [""]
    if kind == "fields":
        return ["- %s: ______________________" % it for it in blk[1]] + [""]
    if kind == "twocol":
        return ["*(two writing columns, %d lines each: “%s” | “%s”)*" % (blk[3], blk[1], blk[2]), ""]
    if kind == "table":
        headers, rows = blk[1], blk[2]
        out = ["| " + " | ".join(str(h) for h in headers) + " |",
               "|" + "---|" * len(headers)]
        for r in rows:
            out.append("| " + " | ".join(str(c) if str(c).strip() else " " for c in r) + " |")
        return out + [""]
    if kind == "kv":
        return ["- **%s** — %s" % (k, v) for k, v in blk[1]] + [""]
    if kind == "scale":
        return ["**Scale 1–10:** %s" % blk[1], ""]
    if kind == "wheel":
        return ["*(satisfaction wheel with 8 slices: %s)*" % ", ".join(blk[1]), ""]
    if kind == "grid":
        return ["*(tracker grid — rows: %s; columns: %s)*" % (", ".join(blk[1]), ", ".join(str(c) for c in blk[2])), ""]
    if kind == "sig":
        return ["*(signature line: %s)*" % blk[1], ""]
    if kind == "daymark":
        return ["## Day %s — %s" % (DAY_WORDS[blk[1] - 1] if isinstance(blk[1], int) else blk[1], blk[2]),
                "*%s*" % blk[3], ""]
    if kind in ("spacer", "rule", "ornament"):
        return []
    return []

def pages_md(pages, out):
    for pg in pages:
        kind = pg.get("kind", "page")
        if kind == "cover":
            out += ["# %s" % pg.get("title", "The Lion's Gate 8/8 Activation")]
            if pg.get("subtitle"):
                out += ["*%s*" % pg["subtitle"]]
            if pg.get("tagline"):
                out += ["*%s*" % pg["tagline"]]
            out += [""]
            continue
        if kind == "back":
            out += ["---", "", "> %s" % pg.get("quote", ""), ""]
            continue
        if kind == "divider":
            out += ["---", "", "# Part %s — %s" % (pg.get("num", ""), pg["title"])]
            if pg.get("subtitle"):
                out += ["*%s*" % pg["subtitle"]]
            out += [""]
            continue
        if kind == "toc":
            out += ["*(Table of contents generated automatically)*", ""]
            continue
        title = pg.get("title", "")
        if title:
            out += ["## %s" % title]
            if pg.get("subtitle"):
                out += ["*%s*" % pg["subtitle"]]
            out += [""]
        for blk in pg.get("blocks", []):
            out += block_md(blk)
    return out

def main():
    out = [
        "# THE LION'S GATE 8/8 ACTIVATION — COMPLETE MANUSCRIPT",
        "",
        "All written content of the product, in reading order, free of layout.",
        "Formatting notes in *(italic parentheses)* describe the writing space each",
        "exercise provides. © 2026 GlowHausDigital. All rights reserved.",
        "",
        "═" * 60, "", "# BOOK ONE — THE MAIN WORKBOOK", "",
    ]
    out = pages_md(build_main.assemble(), out)

    out += ["", "═" * 60, "", "# BOOK TWO — THE PLANNER EDITION (condensed)", ""]
    out = pages_md(planner_content.PAGES, out)

    import importlib
    sys.path.insert(0, os.path.join(ROOT, "08_Bonus_Files"))
    bonuses = importlib.import_module("build_bonuses")
    out += ["", "═" * 60, "", "# BOOK THREE — THE QUICK-START GUIDE", ""]
    out = pages_md(bonuses.QS_PAGES, out)

    guides = importlib.import_module("build_guides") if False else None
    sys.path.insert(0, os.path.join(ROOT, "09_Customer_Guides"))
    g = importlib.import_module("build_guides")
    for pages, _, title in g.GUIDES:
        out += ["", "═" * 60, "", "# CUSTOMER GUIDE — %s" % title.upper(), ""]
        out = pages_md(pages, out)

    out += ["", "═" * 60, "", "# THE 88 AFFIRMATIONS", ""]
    for fam, lines in AFFIRMATIONS.items():
        out += ["## %s" % fam, ""]
        out += ["%d. %s" % (i + 1, ln) for i, ln in enumerate(lines)]
        out += [""]

    out += ["═" * 60, "", "# THE 32 AFFIRMATION CARD TEXTS", ""]
    for cat, lines in CARD_SETS.items():
        out += ["## %s (8 cards)" % cat, ""]
        out += ["- %s" % ln for ln in lines]
        out += [""]

    out += ["═" * 60, "", "# THE 12 PHONE WALLPAPER LINES", ""]
    out += ["%d. %s" % (i + 1, ln) for i, ln in enumerate(WALLPAPERS)]
    out += [""]

    path = os.path.join(ROOT, "Lions_Gate_Complete_Manuscript.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    words = sum(len(l.split()) for l in out)
    print("wrote %s (%d lines, ~%d words)" % (path, len(out), words))

if __name__ == "__main__":
    main()
