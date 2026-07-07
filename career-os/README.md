# Career OS — The Career Atelier

A premium, **fully offline** career toolkit. Open `index.html` in any modern
browser and it just works — no install, no build step, no framework, no server,
no account, no internet required.

Career OS gives you 40+ career tools (including eight role-specific résumés), a
résumé builder, and a job tracker, all wrapped in an editorial "atelier" design
with five occupation editions.

---

## What's inside

- **Dashboard** — a Career Readiness ring that grows as you use the tools,
  plus live application/interview/offer counts pulled straight from your Job
  Tracker.
- **Résumé Builder** — a multi-section form with a live one-page preview and
  export to **PDF (print), plain text, and Word (.doc)**. Autosaves. Save
  **multiple named résumé profiles** (e.g. one tailored per target role) and
  switch between them freely. One-click **Load example** drops in a polished,
  occupation-aware sample résumé to edit from, and a live **Résumé Score**
  checklist tells you what's still missing — both fully offline, no AI call.
- **Job Tracker** — a drag-and-drop Kanban board (Wishlist → Applied →
  Interview → Offer → Rejected) with search, filter, autosave, and
  **CSV export** for a real backup you can open in Excel or Sheets.
- **40+ AI prompt tools** across **Build · Résumés · Apply · Interview · Track**.
  Each turns a few inputs into an expert-grade prompt you copy into Claude or
  ChatGPT — you never have to write the prompt yourself. Includes eight
  role-specific résumés (Career Change, Executive, Federal, Healthcare, IT/Tech,
  Teacher, Student/New-Grad, Military Transition).
- **Bonuses** — 500 power verbs, an achievement library, résumé/ATS/interview/
  LinkedIn checklists, networking + professional email templates, salary
  research & negotiation scripts, and a career planning workbook.
- **Help Center** and real, persisted **Settings**.

### How the prompt tools work

Career OS runs offline, so it can't call an AI for you. Instead, each tool
**composes a world-class prompt** from your inputs and hands it to you with one
click:

1. Fill in a few fields and press **Compose prompt**.
2. Press **Copy prompt**, then **Open Claude** or **Open ChatGPT**.
3. Paste, and the AI returns your finished résumé bullets, cover letter,
   interview answers, and so on.

The prompt is hidden by default — press **View prompt** if you're curious.

---

## Five occupation editions

One jewel accent changes per edition while the parchment-and-gold identity stays
constant. Switch any time via the top-right edition switcher or **Settings**:

| Edition | Accent |
| --- | --- |
| General | Oxblood |
| Nursing / Healthcare | Peacock |
| Software / Tech | Indigo |
| Teaching / Education | Cognac |
| Executive | Graphite |

Switching re-skins the whole app and tailors every tool's examples and
keywording to that field.

---

## Your data & privacy

Everything stays **on your device**, in the browser's local storage. Nothing you
type is ever uploaded. If you switch browsers or devices, your entries won't
follow you — so **export your résumé** and keep a copy of anything important.

- **Settings → Autosave** toggles whether entries persist between visits (turn
  it off on a shared computer).
- **Settings → Clear all saved data** wipes everything from this device.

---

## File structure

```
career-os/
├─ index.html            the whole app shell
├─ css/style.css         "The Career Atelier" design system
├─ js/
│  ├─ occupations.js     OCCUPATIONS config — the 5 editions
│  ├─ modules.js         MODULES config — the 33 prompt tools
│  ├─ resume.js          Résumé Builder (custom view)
│  ├─ tracker.js         Job Tracker (custom view)
│  ├─ extras.js          Settings / Help / Bonuses
│  └─ app.js             engine: store, router, renderers, occupation reskin
├─ fonts/                Fraunces · Jost · Space Mono (bundled .woff2, offline)
└─ assets/icons/
```

---

## Customizing (no coding required for the basics)

Career OS is **config-driven** — the whole value is that adding a tool or a
whole occupation edition is configuration, not code.

### Add a new tool

Open `js/modules.js`, copy any entry, and edit the values:

```js
{
  id:"my-tool", group:"Build", name:"My Tool", tag:"Draft",
  icon:'<path d="M4 6h16M4 12h16M4 18h10"/>',
  intro:"One line describing the tool.",
  fields:[
    {key:"role", label:"Your role", type:"input", ph:o=>o.roleEx},
    {key:"detail", label:"Details", type:"textarea", ph:_=>"placeholder text"},
  ],
  buildPrompt:(v,o)=>
`You are a [named expert].
Do X for a ${v.role||o.roleEx}.
Details: ${v.detail||'[fallback]'}
Rules: ...`
},
```

That's it — the renderer draws the form and wires up the buttons. No view code
changes. `group` can be `Build`, `Apply`, `Interview`, or `Track`.

### Ship a new occupation edition

Open `js/occupations.js`, copy an entry, and change the accent, seal letter,
tagline, greeting, and example variables. To make it the default, set the
fallback in `js/app.js` (`store.occ` returns `'general'` by default).

Also add a matching entry to `RESUME_EXAMPLES` in `js/resume.js` — without
one, the Résumé Builder's "Load example" falls back to the General edition's
sample for the new occupation instead of one tailored to it.

To sell a niche edition (e.g. *Career OS — Nursing Edition*), duplicate the
whole folder, set the default edition, tweak the example variables, and list it
separately. Same engine, new skin.

---

## Browser support

Any current version of Chrome, Edge, Safari, or Firefox. For the smoothest
clipboard behavior, serve the folder over a simple local web server or open it
in a normal browser tab; opening directly via `file://` works too, with an
automatic copy fallback.

---

## License

See `LICENSE.txt` for personal and commercial terms.

© The Career Atelier. All rights reserved.
