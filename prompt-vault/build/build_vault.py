#!/usr/bin/env python3
"""Generate vault.html — the 48-page Claude Prompt Vault (2026 relaunch edition).

Usage:  python3 build_vault.py [--companion-url URL]

Page map (48 pages, US Letter):
  1 cover · 2 why · 3 toc · 4 how-to
  5 BEGINNER tier divider · S1 6-8 · S2 9-11
  12 INTERMEDIATE tier divider · S3 13-15 · S4 16-18 · S5 19-21 · S6 22-24
  25 ADVANCED tier divider · S7 26-28 · S8 29-31 · S9 32-34 · S10 35-37 · S11 38-40 · S12 41-43
  44-45 hidden features & power keywords · 46 cheat sheet · 47 claude hacks · 48 closing
Each section = 1 neon mini-map page + 2 light prompt pages (5 + 4 prompts).
"""
import argparse
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vault_data import (TIERS, SECTIONS, PROMPTS, WHY_ITEMS, HOW_STEPS, HOW_PRO_TIP,
                        HIDDEN_FEATURES, CHEAT_SHEET, CLAUDE_HACKS, section_prompts)

COMPANION_PLACEHOLDER = "[ADD YOUR GOOGLE DOC LINK]"

TIER_SECTIONS = {
    "beginner": [s for s in SECTIONS if s["tier"] == "beginner"],
    "intermediate": [s for s in SECTIONS if s["tier"] == "intermediate"],
    "advanced": [s for s in SECTIONS if s["tier"] == "advanced"],
}
TIER_TAGLINE = {
    "beginner": "Start here. Everyday wins, zero learning curve.",
    "intermediate": "Level up. Content, audience, and business prompts.",
    "advanced": "Full power. Strategy, research, and pro workflows.",
}
SECTION_START_PAGE = {1: 6, 2: 9, 3: 13, 4: 16, 5: 19, 6: 22,
                      7: 26, 8: 29, 9: 32, 10: 35, 11: 38, 12: 41}


def esc(s):
    return html.escape(s, quote=False)


def css():
    return """
@font-face { font-family:'Fraunces'; font-style:normal; font-weight:500 700;
  src:url('../assets/fonts/fraunces-roman.woff2') format('woff2'); }
@font-face { font-family:'Jost'; font-style:normal; font-weight:400 600;
  src:url('../assets/fonts/jost.woff2') format('woff2'); }
@font-face { font-family:'Space Mono'; font-style:normal; font-weight:400;
  src:url('../assets/fonts/spacemono-400.woff2') format('woff2'); }
@font-face { font-family:'Space Mono'; font-style:normal; font-weight:700;
  src:url('../assets/fonts/spacemono-700.woff2') format('woff2'); }

:root{
  --ink:#0b0b11; --ink2:#14141d; --paper:#ffffff; --paper2:#f4f5f8;
  --cyan:#00e5ff; --magenta:#ff2d95; --lime:#c6ff00;
  --cyan-d:#007c8f; --magenta-d:#c40d69; --lime-d:#6f9400;
  --grey:#8b8b98; --line:#e3e4ea;
}
*{ margin:0; padding:0; box-sizing:border-box; }
html,body{ background:#222; }
.page{ width:8.5in; height:11in; overflow:hidden; position:relative;
  page-break-after:always; break-after:page; background:var(--paper);
  font-family:'Jost',sans-serif; color:var(--ink); }
.dark{ background:var(--ink); color:#fff; }

/* shared chrome */
.mono{ font-family:'Space Mono',monospace; }
.eyebrow{ font-family:'Space Mono',monospace; font-size:7.5pt; letter-spacing:.22em;
  text-transform:uppercase; }
.pgfoot{ position:absolute; left:.7in; right:.7in; bottom:.42in; display:flex;
  justify-content:space-between; align-items:center; font-family:'Space Mono',monospace;
  font-size:7pt; letter-spacing:.18em; text-transform:uppercase; color:var(--grey); }
.dark .pgfoot{ color:#5a5a68; }
.neonbar{ position:absolute; top:0; left:0; right:0; height:.09in; display:flex; }
.neonbar div{ flex:1; }
.nb-c{ background:var(--cyan);} .nb-m{ background:var(--magenta);} .nb-l{ background:var(--lime);}

/* ============ COVER ============ */
.cover{ display:flex; flex-direction:column; align-items:center; text-align:center;
  padding:1.1in .8in .9in; }
.cover .eyebrow{ color:#9a9aa8; }
.cover-collection{ margin-top:.72in; color:var(--cyan); font-family:'Space Mono',monospace;
  font-size:9pt; letter-spacing:.3em; text-transform:uppercase; }
.cover h1{ font-family:'Fraunces',serif; font-weight:700; font-size:64pt; line-height:1.02;
  margin-top:.22in; letter-spacing:.01em; }
.cover h1 .w1{ color:#fff; } .cover h1 .w2{ color:var(--magenta); } .cover h1 .w3{ color:var(--lime); }
.cover-sub{ margin-top:.34in; padding-top:.22in; border-top:1px solid #2c2c38; width:5.6in;
  font-size:13.5pt; font-weight:500; color:#fff; }
.cover-sub2{ margin-top:.08in; font-size:10pt; color:#9a9aa8; }
.cover-chips{ display:flex; gap:.18in; margin-top:.3in; }
.chip{ font-family:'Space Mono',monospace; font-size:7.5pt; letter-spacing:.18em;
  padding:.07in .22in; border-radius:3px; border:1.5px solid; text-transform:uppercase; }
.chip-c{ color:var(--cyan); border-color:var(--cyan); }
.chip-m{ color:var(--magenta); border-color:var(--magenta); }
.chip-l{ color:var(--lime); border-color:var(--lime); }
.cover-count{ margin-top:.42in; display:flex; align-items:baseline; gap:.14in; }
.cover-count .big{ font-family:'Fraunces',serif; font-weight:700; font-size:40pt; color:var(--cyan); }
.cover-count .lbl{ font-size:11pt; color:#cfcfda; text-align:left; line-height:1.25; }
.cover-bullets{ margin-top:.34in; display:flex; flex-direction:column; gap:.11in;
  font-size:10.5pt; color:#e8e8f0; }
.cover-bullets span::before{ content:'◆  '; font-size:7pt; vertical-align:.06em; }
.cb-c::before{ color:var(--cyan);} .cb-m::before{ color:var(--magenta);} .cb-l::before{ color:var(--lime);}

/* ============ WHY ============ */
.matter{ padding:.85in .8in 1in; }
.matter-head .eyebrow{ color:var(--grey); }
.dark .matter-head .eyebrow{ color:#7c7c8c; }
.matter h2{ font-family:'Fraunces',serif; font-weight:700; font-size:27pt; line-height:1.08;
  margin-top:.14in; }
.matter-lede{ margin-top:.16in; font-size:11pt; color:#c9c9d6; max-width:6in; line-height:1.5; }
.matter.flexpage{ display:flex; flex-direction:column; }
.why-grid{ display:grid; grid-template-columns:1fr 1fr; grid-auto-rows:1fr; gap:.28in;
  margin-top:.42in; flex:1; margin-bottom:.35in; }
.why-card{ border:1px solid #26262f; border-radius:6px; padding:.3in .3in; background:#111119;
  display:flex; flex-direction:column; justify-content:center; }
.why-card h3{ font-size:14.5pt; font-weight:600; }
.why-card p{ margin-top:.1in; font-size:10.8pt; color:#b9b9c6; line-height:1.5; }
.why-card:nth-child(3n+1) h3{ color:var(--cyan); }
.why-card:nth-child(3n+2) h3{ color:var(--magenta); }
.why-card:nth-child(3n) h3{ color:var(--lime); }

/* ============ TOC ============ */
.toc-tier{ margin-top:.24in; }
.toc-tier-label{ display:flex; align-items:center; gap:.14in; font-family:'Space Mono',monospace;
  font-size:8.5pt; letter-spacing:.24em; }
.toc-tier-label::after{ content:''; flex:1; height:1px; background:#26262f; }
.toc-row{ display:flex; align-items:baseline; gap:.14in; padding:.082in 0; font-size:11.5pt; }
.toc-num{ font-family:'Space Mono',monospace; font-size:9.5pt; color:#6d6d7c; width:.36in; }
.toc-title{ font-weight:500; color:#f0f0f6; }
.toc-dots{ flex:1; border-bottom:1px dotted #33333f; transform:translateY(-3px); }
.toc-page{ font-family:'Space Mono',monospace; font-size:10pt; color:#9a9aa8; }

/* ============ HOW ============ */
.how-steps{ margin-top:.4in; display:flex; flex-direction:column; gap:.26in; }
.how-step{ display:flex; gap:.26in; border:1px solid #26262f; background:#111119;
  border-radius:6px; padding:.26in .3in; }
.how-num{ font-family:'Fraunces',serif; font-weight:700; font-size:26pt; width:.55in; }
.how-step:nth-child(1) .how-num{ color:var(--cyan); }
.how-step:nth-child(2) .how-num{ color:var(--magenta); }
.how-step:nth-child(3) .how-num{ color:var(--lime); }
.how-step h3{ font-family:'Space Mono',monospace; font-size:10.5pt; letter-spacing:.16em; }
.how-step p{ margin-top:.08in; font-size:10pt; color:#c2c2cf; line-height:1.5; }
.protip{ margin-top:.34in; border-left:3px solid var(--lime); background:#15151d;
  padding:.2in .26in; border-radius:0 6px 6px 0; }
.protip .eyebrow{ color:var(--lime); }
.protip p{ margin-top:.07in; font-size:10pt; color:#d6d6e0; line-height:1.5; }
.bonusnote{ margin-top:.34in; border:1.5px dashed var(--cyan); border-radius:6px;
  padding:.18in .26in; }
.bonusnote .eyebrow{ color:var(--cyan); }
.bonusnote p{ margin-top:.06in; font-size:10pt; color:#e8e8f0; line-height:1.5; }
.bonusnote .mono{ font-size:9.5pt; color:var(--cyan); }

/* ============ TIER DIVIDER ============ */
.tierpage{ display:flex; flex-direction:column; justify-content:center; align-items:center;
  text-align:center; padding:1in; }
.tier-kicker{ font-family:'Space Mono',monospace; font-size:10pt; letter-spacing:.3em;
  color:#7c7c8c; text-transform:uppercase; }
.tier-name{ font-family:'Fraunces',serif; font-weight:700; font-size:56pt; margin-top:.22in; }
.tier-tag{ margin-top:.18in; font-size:14pt; color:#c9c9d6; }
.tier-secs{ margin-top:.55in; width:6.2in; display:flex; flex-direction:column; gap:.19in; }
.tier-sec{ display:flex; align-items:baseline; gap:.2in; border:1px solid #26262f;
  border-radius:6px; padding:.2in .28in; background:#111119; text-align:left; }
.tier-sec .n{ font-family:'Space Mono',monospace; font-size:10.5pt; }
.tier-sec .t{ font-size:13.5pt; font-weight:500; color:#f0f0f6; }
.tier-sec .c{ margin-left:auto; font-family:'Space Mono',monospace; font-size:9.5pt; color:#6d6d7c; }

/* ============ MINI-MAP ============ */
.minimap{ padding:.75in .8in .95in; display:flex; flex-direction:column; }
.mm-tierchip{ display:inline-block; align-self:flex-start; }
.mm-secnum{ position:absolute; top:.58in; right:.8in; font-family:'Fraunces',serif;
  font-weight:700; font-size:46pt; color:#22222c; }
.minimap h2{ font-family:'Fraunces',serif; font-weight:700; font-size:33pt; margin-top:.16in;
  max-width:6in; line-height:1.05; }
.mm-best{ margin-top:.15in; font-size:11.5pt; color:#c9c9d6; }
.mm-best b{ font-family:'Space Mono',monospace; font-size:8.5pt; letter-spacing:.2em;
  font-weight:700; text-transform:uppercase; }
.mm-list{ margin-top:.3in; border-top:1px solid #26262f; flex:1; display:flex;
  flex-direction:column; }
.mm-row{ display:flex; align-items:center; gap:.22in; flex:1;
  border-bottom:1px solid #1c1c26; }
.mm-row .n{ font-family:'Space Mono',monospace; font-size:10.5pt; width:.46in; flex:none; }
.mm-row .t{ font-size:13.5pt; font-weight:500; color:#f0f0f6; }
.mm-row .use{ margin-left:auto; max-width:3.2in; text-align:right; font-size:9.3pt;
  color:#8b8b98; line-height:1.35; }
.mm-note{ margin-top:.24in; border:1.5px dashed var(--cyan); border-radius:6px;
  padding:.15in .22in; font-size:10pt; color:#e8e8f0; }
.mm-note .mono{ color:var(--cyan); font-size:9.5pt; }

/* ============ PROMPT PAGES (light) ============ */
/* Page is a flex column; .pcol distributes boxes so the page fills edge-to-edge.
   Type scales per page density via an inline font-size on .pcol (em-based inside). */
.prompts{ padding:.62in .68in .95in; background:var(--paper); display:flex;
  flex-direction:column; }
.pp-head{ display:flex; align-items:center; justify-content:space-between; flex:none;
  background:var(--ink); border-radius:6px; padding:.145in .26in; }
.pp-head .sec{ font-family:'Space Mono',monospace; font-size:8.5pt; letter-spacing:.16em;
  text-transform:uppercase; }
.pp-head .brand{ font-family:'Space Mono',monospace; font-size:7pt; letter-spacing:.18em;
  color:#8b8b98; text-transform:uppercase; }
.pcol{ flex:1; display:flex; flex-direction:column; justify-content:space-between;
  margin-top:.15in; gap:.12in; }
.pbox{ border:1px solid var(--line); border-left-width:4px; border-radius:5px;
  background:var(--paper2); padding:1.15em 1.85em 1.25em; }
.pbox-use{ font-size:.97em; color:#4c4c58; line-height:1.4; }
.pbox-use b{ font-family:'Space Mono',monospace; font-size:.86em; letter-spacing:.14em;
  font-weight:700; }
.pbox-titlerow{ display:flex; align-items:center; gap:.16in; margin-top:.6em; }
.pbox-num{ font-family:'Space Mono',monospace; font-weight:700; font-size:1.15em;
  background:var(--ink); border-radius:3px; padding:.2em .65em; }
.pbox-title{ font-size:1.54em; font-weight:600; letter-spacing:.01em; }
.pbox-copy{ margin-left:auto; font-family:'Space Mono',monospace; font-size:.82em;
  letter-spacing:.1em; color:#9a9aa4; }
.pbox-body{ margin-top:.65em; font-family:'Space Mono',monospace; font-size:1em;
  line-height:1.55; color:#1c1c26; }

/* ============ HIDDEN FEATURES / HACKS (light) ============ */
.featwrap{ flex:1; display:flex; flex-direction:column; justify-content:space-between;
  margin-top:.22in; gap:.14in; }
.featcard{ border:1px solid var(--line); border-radius:5px; display:flex; flex-direction:column;
  justify-content:center; padding:.2in .28in; background:var(--paper2);
  border-left:4px solid var(--ink); }
.featcard h3{ font-family:'Space Mono',monospace; font-weight:700; font-size:12.5pt; }
.featcard p{ margin-top:.09in; font-size:11pt; color:#3a3a46; line-height:1.55; }
.light-head .eyebrow{ color:#8b8b98; }
.light-head h2{ font-family:'Fraunces',serif; font-weight:700; font-size:24pt; margin-top:.1in; }
.light-head .lede{ margin-top:.08in; font-size:10.5pt; color:#5c5c68; }

/* ============ CHEAT SHEET ============ */
.cheat-grid{ display:grid; grid-template-columns:1fr 1fr; grid-auto-rows:1fr; gap:.17in;
  margin-top:.28in; flex:1; }
.cheat-card{ border:1px solid var(--line); border-radius:5px; background:var(--paper2);
  padding:.14in .22in; display:flex; flex-direction:column; justify-content:center; }
.cheat-card h3{ font-family:'Space Mono',monospace; font-weight:700; font-size:10.2pt;
  letter-spacing:.2em; padding-bottom:.07in; border-bottom:1px solid var(--line); }
.cheat-card li{ list-style:none; font-family:'Space Mono',monospace; font-size:8.8pt;
  color:#2a2a36; line-height:1.42; margin-top:.08in; }
.cheat-stack{ margin-top:.26in; border-left:4px solid var(--magenta); background:var(--paper2);
  border:1px solid var(--line); border-left:4px solid var(--magenta); border-radius:5px;
  padding:.16in .24in; font-size:10pt; color:#3a3a46; line-height:1.5; }
.cheat-stack b{ font-family:'Space Mono',monospace; font-size:8.5pt; letter-spacing:.16em;
  color:var(--magenta-d); }

/* ============ CLOSING ============ */
.closing{ display:flex; flex-direction:column; justify-content:center; align-items:center;
  text-align:center; padding:1in; }
.closing h2{ font-family:'Fraunces',serif; font-weight:700; font-size:38pt; line-height:1.1; }
.closing h2 span{ color:var(--lime); }
.closing .sub{ margin-top:.22in; font-size:12.5pt; color:#c9c9d6; }
.closing .steps{ margin-top:.3in; font-family:'Space Mono',monospace; font-size:10pt;
  letter-spacing:.12em; color:var(--cyan); }
.closing .review{ margin-top:.62in; border:1px solid #26262f; background:#111119;
  border-radius:6px; padding:.24in .38in; max-width:5.2in; }
.closing .review h3{ font-size:13pt; font-weight:600; color:var(--magenta); }
.closing .review p{ margin-top:.08in; font-size:10pt; color:#c2c2cf; line-height:1.5; }
"""


def foot(page_no, dark=False):
    return (f'<div class="pgfoot"><span>The Claude Prompt Vault · 2026 Edition</span>'
            f'<span>{page_no:02d}</span></div>')


def neonbar():
    return '<div class="neonbar"><div class="nb-c"></div><div class="nb-m"></div><div class="nb-l"></div></div>'


def cover_page():
    return f'''<div class="page dark cover">{neonbar()}
  <div class="eyebrow">GlowHaus Digital &nbsp;·&nbsp; 2026 Edition &nbsp;·&nbsp; Digital Download</div>
  <div class="cover-collection">The Complete AI Prompt Collection</div>
  <h1><span class="w1">CLAUDE</span><br><span class="w2">PROMPT</span><br><span class="w3">VAULT</span></h1>
  <div class="cover-sub">108 Copy-Paste Prompts &nbsp;·&nbsp; Beginner to Advanced</div>
  <div class="cover-sub2">Business · Content · Marketing · Life · Hidden Features</div>
  <div class="cover-chips">
    <span class="chip chip-c">Beginner</span>
    <span class="chip chip-m">Intermediate</span>
    <span class="chip chip-l">Advanced</span>
  </div>
  <div class="cover-count"><span class="big">108</span>
    <span class="lbl">numbered prompts<br>across 12 categories</span></div>
  <div class="cover-bullets">
    <span class="cb-c">Every prompt tagged with exactly when to use it</span>
    <span class="cb-m">Hidden features most users never find</span>
    <span class="cb-l">Copy. Paste. Get results in 30 seconds.</span>
  </div>
  <div class="pgfoot"><span>claude.ai · Instant Digital Download</span><span>glowhaus.co</span></div>
</div>'''


def why_page():
    cards = "".join(f'<div class="why-card"><h3>{esc(t)}</h3><p>{esc(b)}</p></div>'
                    for t, b in WHY_ITEMS)
    return f'''<div class="page dark matter flexpage">{neonbar()}
  <div class="matter-head"><div class="eyebrow">Why You Need This · GlowHaus Digital · 2026</div>
  <h2>Stop leaving time &amp; money<br>on the table.</h2>
  <p class="matter-lede">Most people use Claude like a basic search engine and get basic results.
  This vault gives you the exact prompts that unlock professional-level AI output, every single time.</p></div>
  <div class="why-grid">{cards}</div>
  {foot(2)}
</div>'''


def toc_page():
    def row(num, title, page):
        return (f'<div class="toc-row"><span class="toc-num">{num:02d}</span>'
                f'<span class="toc-title">{esc(title)}</span><span class="toc-dots"></span>'
                f'<span class="toc-page">{page:02d}</span></div>')
    out, idx = [], 1
    out.append(row(idx, "Why You Need This Guide", 2)); idx += 1
    out.append(row(idx, "How to Use This Guide", 4)); idx += 1
    for tier_key in ("beginner", "intermediate", "advanced"):
        t = TIERS[tier_key]
        out.append(f'<div class="toc-tier"><div class="toc-tier-label" style="color:{t["color"]}">'
                   f'{t["label"]} · PROMPTS {TIER_SECTIONS[tier_key][0]["num"]*9-8:03d}–'
                   f'{TIER_SECTIONS[tier_key][-1]["num"]*9:03d}</div></div>')
        for s in TIER_SECTIONS[tier_key]:
            out.append(row(idx, s["title"], SECTION_START_PAGE[s["num"]])); idx += 1
    out.append('<div class="toc-tier"><div class="toc-tier-label" style="color:#8b8b98">EXTRAS</div></div>')
    for title, page in (("Hidden Features & Power Keywords", 44),
                        ("Quick Reference Cheat Sheet", 46),
                        ("Bonus: Claude Hacks", 47)):
        out.append(row(idx, title, page)); idx += 1
    return f'''<div class="page dark matter">{neonbar()}
  <div class="matter-head"><div class="eyebrow">Table of Contents · GlowHaus Digital · 2026</div>
  <h2>What's Inside Your Vault</h2></div>
  {''.join(out)}
  {foot(3)}
</div>'''


def how_page(companion_url):
    steps = "".join(
        f'<div class="how-step"><div class="how-num">{i+1:02d}</div>'
        f'<div><h3>{esc(t)}</h3><p>{esc(b)}</p></div></div>'
        for i, (t, b) in enumerate(HOW_STEPS))
    return f'''<div class="page dark matter">{neonbar()}
  <div class="matter-head"><div class="eyebrow">How to Use This Guide · GlowHaus Digital · 2026</div>
  <h2>3 Steps. That's All.</h2></div>
  <div class="how-steps">{steps}</div>
  <div class="protip"><div class="eyebrow">Pro Tip</div><p>{esc(HOW_PRO_TIP)}</p></div>
  <div class="bonusnote"><div class="eyebrow">Your Bonus Is Waiting</div>
    <p>Companion copy-paste doc — every prompt in this vault in one clean, click-to-copy
    Google Doc. No PDF copy-paste weirdness.<br>
    <span class="mono">&#128279; {esc(companion_url)}</span> — bookmark this page.</p></div>
  {foot(4)}
</div>'''


def tier_page(tier_key, page_no):
    t = TIERS[tier_key]
    secs = "".join(
        f'<div class="tier-sec"><span class="n" style="color:{t["color"]}">S{s["num"]:02d}</span>'
        f'<span class="t">{esc(s["title"])}</span>'
        f'<span class="c">{(s["num"]-1)*9+1:03d}–{s["num"]*9:03d}</span></div>'
        for s in TIER_SECTIONS[tier_key])
    return f'''<div class="page dark tierpage">{neonbar()}
  <div class="tier-kicker">Skill Tier {["beginner","intermediate","advanced"].index(tier_key)+1} of 3</div>
  <div class="tier-name" style="color:{t["color"]}">{t["label"]}</div>
  <div class="tier-tag">{esc(TIER_TAGLINE[tier_key])}</div>
  <div class="tier-secs">{secs}</div>
  {foot(page_no)}
</div>'''


def minimap_page(section, page_no, companion_url):
    t = TIERS[section["tier"]]
    prompts = section_prompts(section["num"])
    rows = "".join(
        f'<div class="mm-row"><span class="n" style="color:{t["color"]}">{n:03d}</span>'
        f'<span class="t">{esc(title)}</span><span class="use">{esc(use)}</span></div>'
        for n, title, use, _ in prompts)
    note = ""
    if section["num"] == 1:
        note = (f'<div class="mm-note"><b>&#128279; Companion copy-paste doc:</b> '
                f'<span class="mono">{esc(companion_url)}</span> — bookmark this page. '
                f'Every prompt in this vault, formatted to copy cleanly on desktop and mobile.</div>')
    return f'''<div class="page dark minimap">{neonbar()}
  <div class="mm-secnum">{section["num"]:02d}</div>
  <span class="chip chip-x mm-tierchip" style="color:{t["color"]};border-color:{t["color"]}">{t["label"]}</span>
  <h2>{esc(section["title"])}</h2>
  <div class="mm-best"><b style="color:{t["color"]}">Best for:</b> {esc(section["best_for"])}</div>
  {note}
  <div class="mm-list">{rows}</div>
  {foot(page_no)}
</div>'''


def prompt_scale(prompts):
    """Per-page body font size (pt): sparser pages get bigger type so the page fills.

    Calibrated so the densest 5-box page sits at 9.1pt (known to fit) and sparse
    pages scale up, capped to stay inside the box distribution slack.
    """
    chars = sum(len(u) + len(b) + len(t) // 2 for _, t, u, b in prompts)
    c0 = 1240 if len(prompts) >= 5 else 1330
    pt = 9.1 * (c0 / max(chars, 1)) ** 0.5
    return max(9.1, min(11.6, pt))


def prompt_page(section, prompts, page_no):
    t = TIERS[section["tier"]]
    boxes = "".join(
        f'''<div class="pbox" style="border-left-color:{t["color"]}">
      <div class="pbox-use"><b style="color:{t["dark"]}">USE THIS WHEN:</b> {esc(use)}</div>
      <div class="pbox-titlerow"><span class="pbox-num" style="color:{t["color"]}">#{n:03d}</span>
        <span class="pbox-title">{esc(title)}</span><span class="pbox-copy">copy &amp; paste &#8595;</span></div>
      <div class="pbox-body">{esc(body)}</div>
    </div>''' for n, title, use, body in prompts)
    return f'''<div class="page prompts">
  <div class="pp-head"><span class="sec" style="color:{t["color"]}">{t["label"]} — {esc(section["title"])}</span>
    <span class="brand">GlowHaus Digital · 2026</span></div>
  <div class="pcol" style="font-size:{prompt_scale(prompts):.2f}pt">{boxes}</div>
  {foot(page_no)}
</div>'''


def hidden_pages():
    def card(title, body, color):
        return (f'<div class="featcard" style="border-left-color:{color}">'
                f'<h3>{esc(title)}</h3><p>{esc(body)}</p></div>')
    colors = ["#00e5ff", "#ff2d95", "#c6ff00"]
    first = "".join(card(t, b, colors[i % 3]) for i, (t, b) in enumerate(HIDDEN_FEATURES[:5]))
    second = "".join(card(t, b, colors[i % 3]) for i, (t, b) in enumerate(HIDDEN_FEATURES[5:]))
    p1 = f'''<div class="page prompts">
  <div class="light-head"><div class="eyebrow">Hidden Features · GlowHaus Digital · 2026</div>
  <h2>Hidden Features &amp; Power Keywords</h2>
  <p class="lede">11 phrases that change what Claude gives you — most users never discover these.</p></div>
  <div class="featwrap">{first}</div>
  {foot(44)}
</div>'''
    p2 = f'''<div class="page prompts">
  <div class="light-head"><div class="eyebrow">Hidden Features · Continued</div>
  <h2>Power Keywords, Continued</h2></div>
  <div class="featwrap">{second}</div>
  {foot(45)}
</div>'''
    return p1 + p2


def cheat_page():
    cards = "".join(
        f'<div class="cheat-card"><h3 style="color:{["#007c8f","#c40d69","#6f9400"][i % 3]}">{esc(cat)}</h3>'
        + "".join(f'<li>{esc(line)}</li>' for line in lines) + '</div>'
        for i, (cat, lines) in enumerate(CHEAT_SHEET))
    return f'''<div class="page prompts">
  <div class="light-head"><div class="eyebrow">Quick Reference · GlowHaus Digital · 2026</div>
  <h2>Quick Reference Cheat Sheet</h2>
  <p class="lede">Keep this page open every time you use Claude.</p></div>
  <div class="cheat-grid">{cards}</div>
  <div class="cheat-stack" style="flex:none;margin-bottom:.05in"><b>STACK THEM &nbsp;&#8594;</b>&nbsp;
  Combine one line from each column in a single prompt — role + tone + format + depth — and you'll
  get professional output on the first try, not the fifth.</div>
  {foot(46)}
</div>'''


def hacks_page():
    colors = ["#00e5ff", "#ff2d95", "#c6ff00"]
    cards = "".join(
        f'<div class="featcard" style="border-left-color:{colors[i % 3]};padding:.12in .26in">'
        f'<h3 style="font-size:10.5pt">{esc(t)}</h3><p style="font-size:9.6pt;margin-top:.05in;line-height:1.45">{esc(b)}</p></div>'
        for i, (t, b) in enumerate(CLAUDE_HACKS))
    return f'''<div class="page prompts">
  <div class="light-head"><div class="eyebrow">Bonus · GlowHaus Digital · 2026</div>
  <h2>Claude Hacks Most People Miss</h2>
  <p class="lede">8 things power users do that others don't.</p></div>
  <div class="featwrap" style="gap:.1in">{cards}</div>
  {foot(47)}
</div>'''


def closing_page():
    return f'''<div class="page dark closing">{neonbar()}
  <h2>You now have the vault.<br><span>Use it like a weapon.</span></h2>
  <p class="sub">Every prompt is a shortcut others don't have.</p>
  <p class="steps">COPY &nbsp;·&nbsp; PASTE &nbsp;·&nbsp; CUSTOMIZE &nbsp;·&nbsp; REPEAT</p>
  <div class="review"><h3>Loved this? Leave a review on Etsy.</h3>
  <p>Your review helps other creators find this vault. Thank you for your support.</p></div>
  <div class="pgfoot"><span>The Claude Prompt Vault · GlowHaus Digital</span><span>2026 Edition · Digital Download</span></div>
</div>'''


def build(companion_url):
    pages = [cover_page(), why_page(), toc_page(), how_page(companion_url)]
    page_no = 5
    for tier_key in ("beginner", "intermediate", "advanced"):
        pages.append(tier_page(tier_key, page_no)); page_no += 1
        for s in TIER_SECTIONS[tier_key]:
            prompts = section_prompts(s["num"])
            pages.append(minimap_page(s, page_no, companion_url)); page_no += 1
            pages.append(prompt_page(s, prompts[:5], page_no)); page_no += 1
            pages.append(prompt_page(s, prompts[5:], page_no)); page_no += 1
    pages.append(hidden_pages())   # pages 44-45
    pages.append(cheat_page())     # 46
    pages.append(hacks_page())     # 47
    pages.append(closing_page())   # 48
    return f'''<!DOCTYPE html><html><head><meta charset="utf-8">
<title>Claude Prompt Vault — 2026 Edition</title>
<style>@page {{ size: letter; margin: 0; }}{css()}</style></head>
<body>{''.join(pages)}</body></html>'''


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--companion-url", default=COMPANION_PLACEHOLDER)
    ap.add_argument("-o", "--out", default=os.path.join(os.path.dirname(__file__), "vault.html"))
    args = ap.parse_args()
    html_out = build(args.companion_url)
    with open(args.out, "w") as f:
        f.write(html_out)
    print(f"wrote {args.out} ({len(html_out)//1024} KB)")
