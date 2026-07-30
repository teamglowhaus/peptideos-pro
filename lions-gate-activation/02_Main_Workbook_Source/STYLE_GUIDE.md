# Lion's Gate 8/8 Activation — Content & Style Guide

This guide governs every page of every edition. Content modules are Python files
exporting a `PAGES` list consumed by the layout engine in `lg/engine.py`.

## Voice

Write as a thoughtful, spiritually open woman who respects both intuition and
reality. Warm, human, intelligent, reassuring, emotionally perceptive, grounded,
encouraging, substantial, nonjudgmental. Second person ("you"), occasional
first-person framing in letters. American English.

**Ethical framing (non-negotiable):**
- The Lion's Gate is presented as a modern spiritual/astrological tradition and
  reflective practice — never as a scientifically proven energetic event.
- Use framings like: "In modern spiritual practice…", "Many practitioners
  associate…", "You may choose to view this date as…", "This symbolic period can
  serve as…", "Use this date as an invitation to…"
- Never promise outcomes (money, love, pregnancy, healing, business results).
- Never state crystals cure conditions, tarot predicts fixed futures, or that
  the reader attracted her hardships.
- Manifestation is framed as: clarity + self-concept + repetition + real action.
- Rituals support reflection; they do not replace medical, psychological, legal
  or financial care.
- Never use manifestation to target/control a specific person.

**Banned phrases** (and close variants): "embark on a transformative journey",
"unlock your limitless potential", "step into your highest self", "harness
cosmic energies", "quantum leap", "raise your vibration" (without explanation),
"the universe will deliver", "your dream life is inevitable", "simply believe",
"everything happens for a reason", "you are a magnet for millions", "in today's
fast-paced world", "dive into", "elevate your", "unleash".

**Structural rules:**
- Do not open exercises with "Take a moment" (vary openers heavily).
- Avoid em dashes; prefer commas, colons or separate sentences.
- Avoid repeating sentence skeletons across pages ("This exercise will help
  you…" everywhere). Every prompt in the book must be unique.
- No toxic positivity; acknowledge difficulty, allow ambivalence.
- No filler pages. Every page earns its place.

## Page schema

```python
PAGES = [
  {
    "family": "education",     # education|exercise|ritual|meditation|day|action|integration|reference|front|planner
    "section": "Desire Clarity",   # running-head kicker (title case, short)
    "title": "The Feeling Beneath the Goal",
    "subtitle": "optional serif-italic dek under the title",
    "toc": True,               # include in Contents (mark key pages only)
    "wash": True,              # optional tinted background for the family
    "blocks": [...],
  },
]
```

## Blocks (with approx. vertical cost at US Letter; usable page height ≈ 600pt,
title area ≈ 60–90pt)

| Block | Cost | Use |
|---|---|---|
| `("p", text)` | ~15.5pt/line (~90 chars/line) | body paragraph; `*italic*`, `**bold**` inline |
| `("pi", text)` | same | italic aside |
| `("note", text)` | ~12pt/line | small gray caption/safety note |
| `("h2", text)` | ~27pt | sub-heading with short gold rule |
| `("h3", text)` | ~20pt | run-in heading |
| `("quote", text)` | ~18pt/line + 16 | serif-italic pull quote with botanical |
| `("aff", text)` | ~60pt | centered display affirmation (adds quotes itself) |
| `("callout", title, text)` | text + ~40pt | gold wash rounded box |
| `("prompt", q, n)` | ~35pt + n×26 | framed journaling prompt with n ruled lines |
| `("lines", n)` | n×26 | bare ruled lines |
| `("linesfill",)` | rest of page | fill remainder with ruled lines |
| `("dotsfill",)` | rest of page | dot grid |
| `("box", h, "label")` | h | open writing box |
| `("check", [items])` | ~16pt/item | checkbox list |
| `("bullets", [items])` | ~16pt/item | gold-dot bullets |
| `("steps", [(t, d), …])` | ~38pt/step | numbered gold-circle steps |
| `("fields", [labels])` | 26pt each | label + fill-in line |
| `("twocol", "L", "R", n)` | ~20 + n×26 | two labeled line columns |
| `("table", hdrs, rows, widths?)` | ~20pt/row | banded table (widths = fractions) |
| `("kv", [(term, def)])` | ~35pt/pair | serif term + definition |
| `("scale", label)` | ~45pt | 1–10 circle scale |
| `("wheel", [8 labels])` | ~330pt | satisfaction wheel |
| `("grid", rows, cols)` | ~22pt/row | tracker grid (≤10 cols) |
| `("sig", label)` | ~35pt | signature line |
| `("rule",)` | 16pt | thin rule with star |
| `("spacer", h)` | h | vertical space |
| `("cardaff", [strings])` | ~22pt each | affirmation list with stars |
| `("daymark", n, "Name", "dateline")` | ~95pt | Day-page solar header (day pages only) |

The engine reflows overflow onto continuation pages automatically, but author
pages to fit: main workbook pages should be complete thoughts. Writing space is
generous: most exercise pages should give at least 8–14 ruled lines total.

## Design families (chrome is automatic)

education (warm gold wash option), exercise (cream), ritual (rose accents +
sun-ray corner), meditation (plum wash + constellation), day (solar daymark),
action (geometric corner), integration (crescent), reference (compact).

## Typography (automatic)

Cormorant Garamond headings, Lato body, Marcellus kickers. Never set body copy
in italic serif. Fine print ≥ 8.5pt.
