#!/usr/bin/env python3
"""Generate the 10 Etsy listing images as HTML (2700x2025) -> screenshot via render_images.mjs.

Image briefs are from the Optimization Kit, Section 5. Order matters:
01 hero · 02 before/after (priority) · 03 what's inside · 04 page spread · 05 click-to-copy
06 hidden tease · 07 who it's for · 08 how it works · 09 cheat sheet phone · 10 value stack
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
W, H = 2700, 2025
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images_html")
os.makedirs(OUT, exist_ok=True)

BASE_CSS = f"""
@font-face {{ font-family:'Fraunces'; font-weight:500 700;
  src:url('../../assets/fonts/fraunces-roman.woff2') format('woff2'); }}
@font-face {{ font-family:'Jost'; font-weight:400 600;
  src:url('../../assets/fonts/jost.woff2') format('woff2'); }}
@font-face {{ font-family:'Space Mono'; font-weight:400;
  src:url('../../assets/fonts/spacemono-400.woff2') format('woff2'); }}
@font-face {{ font-family:'Space Mono'; font-weight:700;
  src:url('../../assets/fonts/spacemono-700.woff2') format('woff2'); }}
*{{ margin:0; padding:0; box-sizing:border-box; }}
body{{ width:{W}px; height:{H}px; overflow:hidden; background:#0b0b11; color:#fff;
  font-family:'Jost',sans-serif; position:relative; }}
.mono{{ font-family:'Space Mono',monospace; }}
.serif{{ font-family:'Fraunces',serif; font-weight:700; }}
.neonbar{{ position:absolute; top:0; left:0; right:0; height:26px; display:flex; z-index:5; }}
.neonbar div{{ flex:1; }}
.nb1{{ background:#00e5ff; }} .nb2{{ background:#ff2d95; }} .nb3{{ background:#c6ff00; }}
.brand{{ position:absolute; bottom:44px; left:0; right:0; text-align:center;
  font-family:'Space Mono',monospace; font-size:26px; letter-spacing:.24em; color:#6d6d7c;
  text-transform:uppercase; z-index:5; }}
.glow{{ position:absolute; border-radius:50%; filter:blur(220px); opacity:.32; z-index:0; }}
.chip{{ font-family:'Space Mono',monospace; letter-spacing:.16em; border:3px solid;
  border-radius:10px; padding:14px 34px; text-transform:uppercase; }}
"""


def page(name, body, extra_css=""):
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{BASE_CSS}{extra_css}</style></head>
<body>{body}</body></html>"""
    with open(os.path.join(OUT, name), "w") as f:
        f.write(html)


def neon():
    return '<div class="neonbar"><div class="nb1"></div><div class="nb2"></div><div class="nb3"></div></div>'


# ---------- 01 HERO ----------
page("img01_hero.html", f"""
{neon()}
<div class="glow" style="width:1200px;height:1200px;background:#00e5ff;top:-400px;left:-300px"></div>
<div class="glow" style="width:1100px;height:1100px;background:#ff2d95;bottom:-450px;right:-250px"></div>
<div class="hero-wrap">
  <div class="hero-left">
    <div class="mono kicker">The Complete AI Prompt Collection</div>
    <div class="serif htitle"><span style="color:#fff">CLAUDE</span><br>
      <span style="color:#ff2d95">PROMPT</span><br><span style="color:#c6ff00">VAULT</span></div>
    <div class="hline">108 Prompts. Copy. Paste. Done.</div>
    <div class="hchips">
      <span class="chip" style="color:#00e5ff;border-color:#00e5ff">Beginner</span>
      <span class="chip" style="color:#ff2d95;border-color:#ff2d95">Intermediate</span>
      <span class="chip" style="color:#c6ff00;border-color:#c6ff00">Advanced</span>
    </div>
    <div class="hsub mono">Instant Download &nbsp;·&nbsp; Works with free Claude</div>
  </div>
  <div class="tablet">
    <div class="tablet-screen"><img src="../pagepng/p01.png"></div>
  </div>
</div>
<div class="brand">GlowHaus Digital · glowhaus.co</div>
""", f"""
.hero-wrap{{ position:relative; z-index:2; display:flex; align-items:center; height:100%;
  padding:100px 130px 140px; gap:60px; }}
.hero-left{{ flex:1.15; }}
.kicker{{ color:#00e5ff; font-size:34px; letter-spacing:.3em; text-transform:uppercase; }}
.htitle{{ font-size:218px; line-height:.98; margin-top:44px; letter-spacing:.005em; }}
.hline{{ margin-top:56px; font-size:74px; font-weight:600; color:#fff; }}
.hchips{{ display:flex; gap:30px; margin-top:52px; }}
.hchips .chip{{ font-size:30px; }}
.hsub{{ margin-top:52px; font-size:32px; color:#9a9aa8; letter-spacing:.12em; }}
.tablet{{ flex:.95; display:flex; justify-content:center; }}
.tablet-screen{{ width:940px; border-radius:36px; border:22px solid #1d1d27; outline:3px solid #33333f;
  overflow:hidden; transform:rotate(4deg); box-shadow:0 80px 160px rgba(0,0,0,.75),
  0 0 120px rgba(0,229,255,.18); }}
.tablet-screen img{{ width:100%; display:block; }}
""")

# ---------- 02 BEFORE / AFTER ----------
page("img02_before_after.html", f"""
{neon()}
<div class="ba-head">
  <div class="serif" style="font-size:84px">Same question. <span style="color:#c6ff00">Wildly different answer.</span></div>
  <div style="font-size:38px;color:#9a9aa8;margin-top:18px">The prompt is the difference.</div>
</div>
<div class="ba-cols">
  <div class="ba-col">
    <div class="ba-label mono" style="background:#2a2a34;color:#9a9aa8">&#10007; &nbsp;WHAT MOST PEOPLE TYPE</div>
    <div class="bubble user mono">write me a headline for my candle shop</div>
    <div class="bubble ai">
      <div class="ai-tag mono">Claude</div>
      <p style="color:#8b8b98">"Beautiful Handmade Candles for Every Occasion"</p>
      <div class="ba-verdict" style="color:#6d6d7c">Generic. Forgettable. Sounds like every
      other shop on the internet.<br><br><span class="mono" style="font-size:30px;letter-spacing:.14em">
      1 WEAK OPTION &nbsp;·&nbsp; STILL STARING AT THE PAGE</span></div>
    </div>
  </div>
  <div class="ba-col win">
    <div class="ba-label mono" style="background:#c6ff00;color:#0b0b11">&#10003; &nbsp;VAULT PROMPT #047</div>
    <div class="bubble user mono" style="border-color:#c6ff00">Write 10 headline options for a sales page selling
    [hand-poured soy candles]. Mix: transformation, curiosity, specificity, social proof, and pain-point
    opener. Target audience: [stressed-out young professionals].</div>
    <div class="bubble ai" style="border-color:#3a3a1a">
      <div class="ai-tag mono" style="color:#c6ff00">Claude</div>
      <p>"The 60-Hour Candle That Makes Your Apartment Smell Like a Day Off"</p>
      <p style="margin-top:18px">"4,000+ Burned. Zero Regrets. Meet the Candle With a Waitlist."</p>
      <p style="margin-top:18px">"Your Shoulders Drop the Second You Light It."</p>
      <p style="margin-top:22px;color:#c6ff00;font-size:30px" class="mono">+ 7 more angles in seconds</p>
    </div>
  </div>
</div>
<div class="brand">Claude Prompt Vault · 108 tested prompts · GlowHaus Digital</div>
""", """
.ba-head{ text-align:center; padding-top:120px; position:relative; z-index:2; }
.ba-cols{ display:flex; gap:64px; padding:90px 120px 0; position:relative; z-index:2;
  height:1560px; align-items:stretch; }
.ba-col{ flex:1; background:#12121a; border:2px solid #26262f; border-radius:28px; padding:60px;
  display:flex; flex-direction:column; }
.ba-col.win{ border-color:#c6ff00; box-shadow:0 0 140px rgba(198,255,0,.14); }
.ba-label{ display:inline-block; font-size:34px; font-weight:700; letter-spacing:.14em;
  padding:18px 36px; border-radius:10px; align-self:flex-start; }
.bubble{ border:2px solid #2c2c38; border-radius:20px; padding:42px 48px; margin-top:44px;
  font-size:39px; line-height:1.5; }
.bubble.user{ background:#1a1a24; color:#e8e8f0; }
.bubble.ai{ background:#0e0e15; flex:1; }
.bubble.ai p{ font-size:40px; line-height:1.45; color:#f0f0f6; }
.ai-tag{ font-size:28px; color:#9a9aa8; letter-spacing:.2em; margin-bottom:24px; text-transform:uppercase; }
.ba-verdict{ margin-top:auto; padding-top:40px; font-size:34px; }
""")

# ---------- 03 WHAT'S INSIDE ----------
cats = [
    ("01", "Daily Life & Everyday Tasks", "#00e5ff"), ("02", "Writing & Personal Messages", "#00e5ff"),
    ("03", "Content Creation", "#ff2d95"), ("04", "Social Media Strategy", "#ff2d95"),
    ("05", "Business & Email", "#ff2d95"), ("06", "Sales & Copywriting", "#ff2d95"),
    ("07", "Strategy & Planning", "#c6ff00"), ("08", "Research & Analysis", "#c6ff00"),
    ("09", "Digital Marketing", "#c6ff00"), ("10", "Skincare & Beauty Business", "#c6ff00"),
    ("11", "UGC & Brand Outreach", "#c6ff00"), ("12", "Meta-Prompts", "#c6ff00"),
]
cat_html = "".join(
    f'<div class="cat"><span class="mono cnum" style="color:{c}">{n}</span><span>{t}</span></div>'
    for n, t, c in cats)
page("img03_whats_inside.html", f"""
{neon()}
<div class="wi-head">
  <div class="serif" style="font-size:88px">What's inside the vault</div>
  <div class="mono wi-stats">108 PROMPTS &nbsp;·&nbsp; 12 CATEGORIES &nbsp;·&nbsp; 48 PAGES &nbsp;·&nbsp; BONUS COPY DOC</div>
</div>
<div class="wi-grid">{cat_html}</div>
<div class="wi-extras">
  <span>+ 11 Hidden Power Keywords</span><span>+ Quick-Reference Cheat Sheet</span><span>+ 8 Claude Hacks</span>
</div>
<div class="brand">Every prompt numbered 001–108 · tagged with exactly when to use it</div>
""", """
.wi-head{ text-align:center; padding-top:130px; }
.wi-stats{ margin-top:34px; font-size:42px; color:#00e5ff; letter-spacing:.14em; }
.wi-grid{ display:grid; grid-template-columns:repeat(3,1fr); gap:56px; padding:160px 140px 0; }
.cat{ display:flex; align-items:center; gap:32px; background:#12121a; border:2px solid #26262f;
  border-radius:22px; padding:80px 48px; font-size:43px; font-weight:500; }
.cnum{ font-size:40px; font-weight:700; }
.wi-extras{ display:flex; justify-content:center; gap:80px; margin-top:170px; font-size:42px;
  color:#c9c9d6; }
""")

# ---------- 04 REAL PAGE SPREAD ----------
page("img04_page_spread.html", f"""
{neon()}
<div class="glow" style="width:1100px;height:1100px;background:#ff2d95;top:-350px;right:-300px"></div>
<div class="ps-head">
  <div class="serif" style="font-size:84px">Actual pages. <span style="color:#00e5ff">Actual density.</span></div>
  <div style="font-size:38px;color:#9a9aa8;margin-top:16px">No filler pages — every spread works for you.</div>
</div>
<div class="ps-fan">
  <img src="../pagepng/p06.png" style="transform:rotate(-7deg) translateY(40px)">
  <img src="../pagepng/p07.png" style="transform:translateY(-10px); z-index:3; box-shadow:0 60px 140px rgba(0,0,0,.8)">
  <img src="../pagepng/p30.png" style="transform:rotate(7deg) translateY(40px)">
</div>
<div class="brand">Section mini-maps · numbered prompts · USE-THIS-WHEN tags on all 108</div>
""", """
.ps-head{ text-align:center; padding-top:100px; position:relative; z-index:2; }
.ps-fan{ display:flex; justify-content:center; align-items:flex-start; gap:-40px;
  margin-top:90px; position:relative; z-index:2; }
.ps-fan img{ width:860px; border-radius:14px; border:2px solid #2c2c38;
  box-shadow:0 50px 110px rgba(0,0,0,.7); }
.ps-fan img:nth-child(1){ margin-right:-120px; }
.ps-fan img:nth-child(3){ margin-left:-120px; }
""")

# ---------- 05 CLICK-TO-COPY ----------
page("img05_click_to_copy.html", f"""
{neon()}
<div class="glow" style="width:1100px;height:1100px;background:#00e5ff;bottom:-400px;left:-300px"></div>
<div class="cc-head">
  <div class="mono" style="font-size:34px;color:#00e5ff;letter-spacing:.26em">&#127873; BONUS — INCLUDED FREE</div>
  <div class="serif" style="font-size:84px;margin-top:24px">Click-to-copy companion doc</div>
  <div style="font-size:38px;color:#9a9aa8;margin-top:16px">Every prompt in a clean doc. No PDF copy-paste weirdness.</div>
</div>
<div class="doc">
  <div class="doc-toolbar"><span class="dot" style="background:#ff5f57"></span>
    <span class="dot" style="background:#febc2e"></span><span class="dot" style="background:#28c840"></span>
    <span class="doc-title">Claude Prompt Vault — Companion Doc</span></div>
  <div class="doc-body">
    <div class="doc-h">SECTION 6: SALES &amp; COPYWRITING</div>
    <div class="doc-p"><b>046 — Product Description</b></div>
    <div class="doc-p sel">Write a compelling product description for [product name]. Features: [list].
      Target buyer: [describe]. Lead with the transformation and benefit, not just the specs. Close with a CTA.
      <div class="copytip mono">Copy &nbsp;&#8984;C</div>
      <div class="cursor"></div>
    </div>
    <div class="doc-p"><b>047 — Sales Page Headlines</b></div>
    <div class="doc-p">Write 10 headline options for a sales page selling [product or service]. Mix:
      transformation, curiosity, specificity, social proof, and pain-point opener. Target audience: [describe].</div>
    <div class="doc-p"><b>048 — Launch Announcement</b></div>
    <div class="doc-p">Write a product launch announcement for [product] going live on [date]. Include:
      what it is, who it is for, what makes it different, what is included, price, and a strong CTA.</div>
  </div>
</div>
<div class="brand">Select · copy · paste into Claude — works on phone and desktop</div>
""", """
.cc-head{ text-align:center; padding-top:110px; position:relative; z-index:2; }
.doc{ width:2050px; margin:80px auto 0; background:#fff; border-radius:24px; overflow:hidden;
  box-shadow:0 60px 140px rgba(0,0,0,.75), 0 0 120px rgba(0,229,255,.15); position:relative; z-index:2; }
.doc-toolbar{ display:flex; align-items:center; gap:16px; background:#ececf1; padding:30px 42px; }
.dot{ width:28px; height:28px; border-radius:50%; }
.doc-title{ margin-left:26px; color:#5c5c68; font-size:32px; font-weight:500; }
.doc-body{ padding:70px 100px 90px; color:#1c1c26; }
.doc-h{ font-family:'Space Mono',monospace; font-weight:700; font-size:38px; letter-spacing:.08em;
  border-bottom:3px solid #ececf1; padding-bottom:26px; }
.doc-p{ font-size:40px; line-height:1.55; margin-top:40px; position:relative; }
.doc-p b{ font-size:42px; }
.sel{ background:#b8d8ff; border-radius:6px; padding:18px 22px; }
.copytip{ position:absolute; right:60px; top:-64px; background:#1c1c26; color:#fff; font-size:30px;
  padding:16px 34px; border-radius:12px; box-shadow:0 16px 40px rgba(0,0,0,.35); }
.cursor{ position:absolute; right:200px; bottom:-20px; width:0; height:0;
  border-left:26px solid #1c1c26; border-bottom:42px solid transparent;
  border-right:10px solid transparent; transform:rotate(-12deg); }
""")

# ---------- 06 HIDDEN FEATURES TEASE ----------
page("img06_hidden_tease.html", f"""
{neon()}
<div class="ht-head">
  <div class="serif" style="font-size:84px">11 phrases most Claude users <span style="color:#ff2d95">never discover</span></div>
  <div style="font-size:38px;color:#9a9aa8;margin-top:16px">The Hidden Features section alone is worth the price.</div>
</div>
<div class="ht-stage">
  <img src="../pagepng/p44.png" class="ht-page">
  <div class="ht-reveal" style="top:340px;border-left-color:#00e5ff">
    <div class="mono ht-k" style="color:#00e5ff">&#8220;Act As [Role]&#8221;</div>
    <div class="ht-b">The single most powerful prompt modifier. Instantly changes the quality and depth of every answer.</div>
  </div>
  <div class="ht-reveal" style="top:700px;border-left-color:#ff2d95">
    <div class="mono ht-k" style="color:#ff2d95">&#8220;Don't Hold Back — Be Blunt&#8221;</div>
    <div class="ht-b">Gets you the unfiltered feedback that actually helps you grow. The most underused phrase in the guide.</div>
  </div>
  <div class="ht-lock mono">+ 9 MORE INSIDE</div>
</div>
<div class="brand">Hidden Features &amp; Power Keywords · pages 44–45</div>
""", """
.ht-head{ text-align:center; padding-top:96px; position:relative; z-index:2; }
.ht-stage{ position:relative; width:1200px; margin:70px auto 0; }
.ht-page{ width:1200px; border-radius:16px; filter:blur(14px) brightness(.85); opacity:.9; }
.ht-reveal{ position:absolute; left:-190px; right:-190px; background:#12121a;
  border:2px solid #2c2c38; border-left:14px solid; border-radius:20px; padding:36px 48px;
  box-shadow:0 40px 100px rgba(0,0,0,.7); }
.ht-k{ font-weight:700; font-size:40px; }
.ht-b{ margin-top:14px; font-size:33px; color:#c9c9d6; line-height:1.45; }
.ht-lock{ position:absolute; bottom:70px; left:50%; transform:translateX(-50%);
  background:#c6ff00; color:#0b0b11; font-weight:700; font-size:34px; letter-spacing:.16em;
  padding:22px 48px; border-radius:14px; }
""")

# ---------- 07 WHO IT'S FOR ----------
aud = [
    ("Content Creators", "tired of the blank page", "#00e5ff"),
    ("Etsy &amp; Digital Sellers", "writing their own listings", "#ff2d95"),
    ("UGC Creators", "pitching brands that pay", "#c6ff00"),
    ("Side-Hustlers", "building after hours", "#00e5ff"),
    ("Small Business Owners", "doing their own marketing", "#ff2d95"),
    ("Complete Beginners", "who want a head start", "#c6ff00"),
]
aud_html = "".join(
    f'<div class="aud" style="border-color:{c}"><div class="aud-t" style="color:{c}">{t}</div>'
    f'<div class="aud-s">{s}</div></div>' for t, s, c in aud)
page("img07_who_for.html", f"""
{neon()}
<div class="wf-head">
  <div class="serif" style="font-size:92px">Made for people who <span style="color:#00e5ff">do the work themselves</span></div>
</div>
<div class="wf-grid">{aud_html}</div>
<div class="wf-note">If AI has felt "meh" so far — it's not you, it's your prompts.</div>
<div class="brand">Claude Prompt Vault · Beginner to Advanced · GlowHaus Digital</div>
""", """
.wf-head{ text-align:center; padding:160px 200px 0; }
.wf-grid{ display:grid; grid-template-columns:repeat(3,1fr); gap:56px; padding:170px 150px 0; }
.aud{ border:3px solid; border-radius:26px; background:#12121a; padding:130px 48px; text-align:center; }
.aud-t{ font-size:52px; font-weight:600; }
.aud-s{ margin-top:24px; font-size:37px; color:#9a9aa8; }
.wf-note{ text-align:center; margin-top:170px; font-size:46px; color:#c9c9d6; }
""")

# ---------- 08 HOW IT WORKS ----------
page("img08_how_it_works.html", f"""
{neon()}
<div class="hw-head"><div class="serif" style="font-size:92px">From blank page to done <span style="color:#c6ff00">in 30 seconds</span></div></div>
<div class="hw-steps">
  <div class="hw-step"><div class="hw-n serif" style="color:#00e5ff">1</div>
    <div class="hw-t">FIND</div><div class="hw-b">Jump to your section. Every prompt is numbered and tagged with when to use it.</div></div>
  <div class="hw-arrow mono">&#8594;</div>
  <div class="hw-step"><div class="hw-n serif" style="color:#ff2d95">2</div>
    <div class="hw-t">COPY</div><div class="hw-b">Grab it from the PDF or the click-to-copy bonus doc. No retyping.</div></div>
  <div class="hw-arrow mono">&#8594;</div>
  <div class="hw-step"><div class="hw-n serif" style="color:#c6ff00">3</div>
    <div class="hw-t">PASTE</div><div class="hw-b">Swap the [BRACKETS] with your details. Professional output in seconds.</div></div>
</div>
<div class="hw-foot mono">WORKS WITH THE FREE CLAUDE.AI PLAN — AND CHATGPT TOO</div>
<div class="brand">GlowHaus Digital · Instant Digital Download</div>
""", """
.hw-head{ text-align:center; padding:200px 180px 0; }
.hw-steps{ display:flex; align-items:stretch; justify-content:center; gap:50px; padding:240px 130px 0; }
.hw-step{ width:700px; background:#12121a; border:2px solid #26262f; border-radius:28px;
  padding:150px 64px; text-align:center; }
.hw-n{ font-size:200px; }
.hw-t{ font-family:'Space Mono',monospace; font-size:56px; font-weight:700; letter-spacing:.3em;
  margin-top:36px; }
.hw-b{ margin-top:46px; font-size:41px; color:#c9c9d6; line-height:1.5; }
.hw-arrow{ align-self:center; font-size:100px; color:#4c4c58; }
.hw-foot{ text-align:center; margin-top:230px; font-size:40px; color:#c6ff00; letter-spacing:.18em; }
""")

# ---------- 09 CHEAT SHEET PHONE ----------
page("img09_cheat_sheet.html", f"""
{neon()}
<div class="glow" style="width:1100px;height:1100px;background:#c6ff00;top:-400px;right:-300px;opacity:.18"></div>
<div class="cs-wrap">
  <div class="cs-left">
    <div class="mono" style="font-size:34px;color:#c6ff00;letter-spacing:.26em">QUICK-REFERENCE CHEAT SHEET</div>
    <div class="serif" style="font-size:96px;margin-top:30px;line-height:1.05">Keep it open<br>while you work</div>
    <div style="font-size:40px;color:#c9c9d6;margin-top:44px;line-height:1.5;max-width:900px">
      One page. 8 categories. 24 power phrases.<br>The fastest way to upgrade any prompt you write —
      on your phone, tablet, or second screen.</div>
    <div class="cs-tags mono">ROLE · TONE · FORMAT · DEPTH<br>ITERATE · CRITIQUE · OUTPUT · POWER</div>
  </div>
  <div class="phone"><div class="phone-notch"></div><div class="phone-screen"><img src="../pagepng/p46.png"></div></div>
</div>
<div class="brand">Page 46 of the vault · print it, pin it, screenshot it</div>
""", """
.cs-wrap{ display:flex; align-items:center; height:100%; padding:100px 150px 140px; gap:80px;
  position:relative; z-index:2; }
.cs-left{ flex:1.3; }
.cs-tags{ margin-top:56px; font-size:36px; color:#8b8b98; line-height:1.8; letter-spacing:.1em; }
.phone{ position:relative; width:850px; border-radius:64px; border:24px solid #1d1d27;
  outline:3px solid #33333f; overflow:hidden; transform:rotate(-4deg);
  box-shadow:0 80px 160px rgba(0,0,0,.75), 0 0 120px rgba(198,255,0,.12); }
.phone-notch{ position:absolute; top:18px; left:50%; transform:translateX(-50%); width:220px;
  height:34px; background:#1d1d27; border-radius:20px; z-index:3; }
.phone-screen img{ width:100%; display:block; }
""")

# ---------- 10 VALUE STACK ----------
page("img10_value_stack.html", f"""
{neon()}
<div class="vs-head"><div class="serif" style="font-size:92px">Everything you get</div></div>
<div class="vs-list">
  <div class="vs-row"><span>48-page designed PDF — 108 numbered prompts</span><span class="mono vsv">$29 value</span></div>
  <div class="vs-row"><span>USE-THIS-WHEN tag on every single prompt</span><span class="mono vsv">included</span></div>
  <div class="vs-row"><span>Click-to-copy companion doc (the killer bonus)</span><span class="mono vsv">$15 value</span></div>
  <div class="vs-row"><span>11 Hidden Power Keywords + 8 Claude Hacks</span><span class="mono vsv">$12 value</span></div>
  <div class="vs-row"><span>Quick-Reference Cheat Sheet</span><span class="mono vsv">$9 value</span></div>
</div>
<div class="vs-anchor">
  <div class="mono" style="font-size:36px;letter-spacing:.2em;color:#0b0b11">108 PROMPTS + CHEAT SHEET + BONUS DOC</div>
  <div class="serif" style="font-size:76px;color:#0b0b11;margin-top:10px">Less than 12&#162; per prompt</div>
</div>
<div class="vs-foot mono">INSTANT DOWNLOAD &nbsp;·&nbsp; WORKS WITH FREE CLAUDE &nbsp;·&nbsp; MESSAGE ME WITH ANY ISSUE — I'LL MAKE IT RIGHT</div>
<div class="brand">GlowHaus Digital · glowhaus.co</div>
""", """
.vs-head{ text-align:center; padding-top:140px; }
.vs-list{ width:2100px; margin:100px auto 0; }
.vs-row{ display:flex; justify-content:space-between; align-items:center; background:#12121a;
  border:2px solid #26262f; border-radius:22px; padding:54px 70px; font-size:46px; margin-top:34px; }
.vs-row span:first-child{ font-weight:500; }
.vsv{ color:#00e5ff; font-size:38px; }
.vs-anchor{ width:2100px; margin:80px auto 0; background:#c6ff00; border-radius:24px;
  text-align:center; padding:64px; }
.vs-foot{ text-align:center; margin-top:110px; font-size:33px; color:#9a9aa8; letter-spacing:.14em; }
""")

print(f"wrote 10 image HTML files to {OUT}")
