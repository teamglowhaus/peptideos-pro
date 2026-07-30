# -*- coding: utf-8 -*-
"""Condensed planner-insert edition of The Lion's Gate 8/8 Activation.
Not a shrunk workbook: short prompts, one primary exercise per page, sections
matched to the nine printable tabs (Begin, Prepare, Release, Clarify, Embody,
Activate, Act, Integrate, Notes)."""

def divider(num, title, subtitle, motif, seed):
    return {"kind": "divider", "num": num, "title": title, "subtitle": subtitle,
            "motif": motif, "seed": seed, "toc_label": "%s — %s" % (num, title)}

DAYS = [
    (1, "Awareness", "See what is actually here, kindly.",
     "Three true sentences about my life this week:",
     "Ten minutes bringing one cluttered corner to order.",
     "I can look at my life honestly and kindly at once.",
     "What today's looking showed me:"),
    (2, "Release", "Set down what no longer fits.",
     "The heaviest thing I carry that I never chose:",
     "Cancel or hand back one expired obligation.",
     "What I set down was never the price of being loved.",
     "What resisted release today:"),
    (3, "Worthiness", "Receive without proving.",
     "What I would ask for if asking cost nothing:",
     "Accept one compliment with only a thank-you.",
     "I can be given to without owing a performance.",
     "What receiving plainly felt like:"),
    (4, "Courage", "Let yourself be seen.",
     "Where I shrink to keep others comfortable:",
     "Be five percent more visible, once, today.",
     "Courage can be quiet, and mine counts.",
     "What my five percent set in motion:"),
    (5, "Clarity", "Choose one intention.",
     "If this year improved one thing, I choose:",
     "Tell one trusted person my focus, in one sentence.",
     "Choosing one thing is how anything gets built.",
     "How the choice feels tonight:"),
    (6, "Embodiment", "Practice being her.",
     "On an ordinary Tuesday, she differs from me by:",
     "Live one full hour today at her standard.",
     "Small behaviors are bricks in my next identity.",
     "The moment that felt most natural as her:"),
    (7, "Aligned Action", "Give the intention a calendar.",
     "By September 8, these would exist or be booked:",
     "Schedule the 24-hour action, then do it early.",
     "I honor my desire with my calendar.",
     "Seeing dates attached, I feel:"),
    (8, "Activation", "Cross the gate on purpose.",
     "The intention I carry through, final wording:",
     "Complete my chosen ritual, unhurried.",
     "I walked through on my own two feet.",
     "What the ritual actually felt like:"),
]

def day_pages():
    out = []
    for n, name, tag, prompt, action, aff, evening in DAYS:
        out.append({
            "family": "day", "section": "Activate", "title": "",
            "toc": n in (1, 8), "toc_label": "Day %d — %s" % (n, name),
            "blocks": [
                ("daymark", n, name, tag),
                ("prompt", prompt, 4),
                ("h3", "Today's action"),
                ("p", action),
                ("check", ["Grounding breath", "Prompt answered", "Action done"]),
                ("aff", aff),
                ("prompt", evening, 3),
            ],
        })
    return out

PAGES = [
# ---------------------------------------------------------------- BEGIN
{"kind": "cover", "title": "The Lion's Gate 8/8 Activation",
 "subtitle": "Planner Edition · Printable ring-bound inserts",
 "tagline": "Eight days · One aligned plan"},
{
 "family": "planner", "section": "Begin", "title": "About This Edition", "toc": True,
 "blocks": [
    ("p", "The Lion's Gate 8/8 Activation, planner edition. Copyright © 2026 GlowHausDigital. All rights reserved. Licensed for a single user's personal use: print for yourself, punch it, annotate it, repeat it yearly. Please do not resell, redistribute, share files or copies, or use it with clients or groups without a separate license (message GlowHausDigital on Etsy)."),
    ("p", "Thank you, truly, for bringing this into your planner. You chose to give your becoming a place among your appointments, which is exactly where it thrives. Move at your own pace, skip what does not fit, and if a file misbehaves, message me on Etsy so I can help."),
    ("note", "For reflection, education and planning only; not a substitute for medical, mental-health, financial or legal care. Outcomes are not guaranteed. Candle steps are optional; never leave a flame unattended."),
    ("note", "Franklin Planner and FranklinCovey are trademarks of their respective owners. This independent product is not affiliated with, sponsored by, approved by or endorsed by them; brand names appear only to identify compatible page dimensions. Measure your pages before printing."),
    ("fields", ["This planner belongs to", "My eight days run from", "to"]),
 ],
},
{
 "family": "planner", "section": "Begin", "title": "The Lion's Gate, Briefly", "toc": True,
 "blocks": [
    ("p", "In modern spiritual practice, August 8 is treated as a doorway: Leo season's courage, the dawn return of the star Sirius, and the abundance-flavored number eight, twice. It is symbolism rather than science, and symbolism is enough; a date agreed upon is a powerful place to gather your attention."),
    ("p", "Eight themed days, a gate-day ritual, and real follow-through. A pen and honesty are the only requirements; every tool stays optional."),
    ("kv", [
      ("The arc", "Awareness, Release, Worthiness, Courage, Clarity, Embodiment, Aligned Action, Activation."),
      ("The rule", "Small and done beats grand and abandoned."),
      ("The promise", "None. The structure is real, the effort is yours, and that pairing is the point."),
    ]),
 ],
},
{
 "family": "planner", "section": "Begin", "title": "Quick Start & Supplies", "toc": False,
 "blocks": [
    ("h3", "Starting late? Do only this"),
    ("check", ["One release, written and torn", "One intention, said without flinching", "One action inside 72 hours, scheduled", "One affirmation kept where I will see it"]),
    ("h3", "Supplies (all optional beyond a pen)"),
    ("check", ["Pen I like", "Scrap paper for releasing", "Water", "Candle or battery candle", "One meaningful object", "Deck of cards, if I use one"]),
    ("h3", "Prepare the week"),
    ("check", ["Ten-minute space reset", "Phone-quiet window chosen for day 8", "Ritual length picked: 15 or 45 minutes", "These pages punched and in their home"]),
 ],
},

# ---------------------------------------------------------------- PREPARE
divider("I", "Prepare", "Make room before you ask for more", "botanical", 31),
{
 "family": "planner", "section": "Prepare", "title": "Open Loops", "toc": True,
 "blocks": [
    ("p", "List what sits unfinished and taxing you quietly: conversations, tasks, decisions. Then mark each one: C to close it this week, S to schedule it, R to release it entirely."),
    ("lines", 9),
    ("prompt", "The loop whose closing would free the most of me:", 2),
 ],
},
{
 "family": "planner", "section": "Prepare", "title": "Energy In, Energy Out", "toc": False,
 "blocks": [
    ("twocol", "Fills me", "Drains me", 5),
    ("prompt", "One boundary I will practice this season, in one sentence:", 2),
    ("prompt", "How money feels this month, in three honest words:", 1),
 ],
},

# ---------------------------------------------------------------- RELEASE
divider("II", "Release", "Set it down with respect", "moon", 32),
{
 "family": "planner", "section": "Release", "title": "Ready to Stop Carrying", "toc": True,
 "blocks": [
    ("prompt", "I am done carrying:", 3),
    ("prompt", "It tried to protect me from:", 2),
    ("prompt", "In its place, I choose:", 2),
    ("note", "Mark the ending: write the old weight on scrap paper, tear it slowly, discard it outside. No fire needed."),
 ],
},
{
 "family": "planner", "section": "Release", "title": "The Belief Underneath", "toc": False,
 "blocks": [
    ("prompt", "A sentence I say about myself that keeps me small:", 2),
    ("prompt", "Whose voice it originally was:", 2),
    ("prompt", "A kinder line I can actually believe:", 2),
    ("aff", "I can question an old story without betraying who first believed it."),
 ],
},

# ---------------------------------------------------------------- CLARIFY
divider("III", "Clarify", "From scattered wishes to one clean intention", "star", 33),
{
 "family": "planner", "section": "Clarify", "title": "The Uncensored Wish List", "toc": True,
 "blocks": [
    ("p", "Everything you want, unedited, unsorted, unjudged. Keep the pen moving."),
    ("linesfill",),
 ],
},
{
 "family": "planner", "section": "Clarify", "title": "Underneath the Want", "toc": False,
 "blocks": [
    ("prompt", "The desire I keep circling:", 2),
    ("prompt", "The feeling it would give me:", 2),
    ("prompt", "The need underneath that feeling:", 2),
    ("prompt", "One way to feed that need this month, no permission required:", 2),
 ],
},
{
 "family": "planner", "section": "Clarify", "title": "Eight Areas, One Line Each", "toc": False,
 "blocks": [
    ("fields", ["Wealth", "Career", "Love", "Confidence", "Home", "Creativity", "Wellness", "Spirit"]),
    ("prompt", "The area pulling hardest this season:", 2),
 ],
},
{
 "family": "planner", "section": "Clarify", "title": "Top Eight, Then One", "toc": True,
 "blocks": [
    ("fields", ["1", "2", "3", "4", "5", "6", "7", "8"]),
    ("prompt", "My primary 8/8 intention, one present-tense sentence:", 3),
    ("check", ["Specific", "Mine, not borrowed", "Has a feeling I can name", "Has an action attached"]),
 ],
},

# ---------------------------------------------------------------- EMBODY
divider("IV", "Embody", "Practice being the woman who has it", "constellation", 34),
{
 "family": "planner", "section": "Embody", "title": "Now and Next", "toc": True,
 "blocks": [
    ("twocol", "My current self", "My future self", 7),
    ("prompt", "What she has stopped explaining or tolerating:", 2),
 ],
},
{
 "family": "planner", "section": "Embody", "title": "Her Profile", "toc": False,
 "blocks": [
    ("fields", ["Her first hour of the day", "Her money habit", "Her standard in love", "Her workspace", "Her answer to overwhelm"]),
    ("prompt", "Her decision filter, three questions she asks before a yes:", 3),
 ],
},
{
 "family": "planner", "section": "Embody", "title": "Evidence & Menu", "toc": False,
 "blocks": [
    ("h3", "Proof I am already becoming her"),
    ("lines", 4),
    ("h3", "Daily embodiment menu (pick one, any day)"),
    ("check", ["Her posture for one meeting", "Her patience with one email", "Her bedtime once", "Her no, said kindly", "Her thank-you, said plainly"]),
    ("aff", "Every small behavior I repeat is a vote for her."),
 ],
},

# ---------------------------------------------------------------- ACTIVATE
divider("V", "Activate", "Eight themed days and the gate itself", "lion", 35),
{
 "family": "planner", "section": "Activate", "title": "The Eight Days at a Glance", "toc": True,
 "blocks": [
    ("grid", ["Done"], ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8"]),
    ("kv", [
      ("Daily shape", "One grounding breath, one prompt, one action, one affirmation, one evening line."),
      ("Time needed", "Fifteen to thirty minutes. Missed days merge kindly into the next."),
    ]),
 ],
},
] + day_pages() + [
{
 "family": "ritual", "section": "Activate", "title": "The 15-Minute Gate Ritual", "toc": True,
 "blocks": [
    ("steps", [
      ("Ground", "Five slow breaths, longer exhales."),
      ("Release", "One finished pattern, written, torn, set aside for outside."),
      ("Intend", "The intention aloud, once, unflinching."),
      ("See", "Two minutes inside one ordinary scene of it, specific and warm."),
      ("Script", "Three calm present-tense sentences."),
      ("Commit", "One action, one date, calendared now."),
      ("Close", "Water, and: done is beautiful."),
    ]),
 ],
},
{
 "family": "ritual", "section": "Activate", "title": "The 45-Minute Gate Ritual", "toc": False,
 "blocks": [
    ("steps", [
      ("Prepare (5)", "Tidy surface, silence phone, water, optional candle safely placed."),
      ("Ground (5)", "Four counts in, six out, ten rounds."),
      ("Release (8)", "Finish in writing: I am done carrying... I forgive myself for... I leave here... Tear it slowly."),
      ("Intend (5)", "Test the sentence: specific, mine, feelable, actionable."),
      ("Visualize (7)", "One full scene: morning light, your hands, one thing handled her way."),
      ("Script (8)", "Half a page, present tense, believable beats spectacular."),
      ("Activate (4)", "Intention onto a small card; eight slow breaths between palms."),
      ("Commit (3)", "Actions at 24 hours, 72 hours, 8 days. First one calendared."),
    ]),
    ("note", "After: snuff the candle with thanks, eat something grounding, no comparison scrolling tonight."),
 ],
},
{
 "family": "ritual", "section": "Activate", "title": "Gate Day, In Ink", "toc": False,
 "blocks": [
    ("prompt", "Through this Lion's Gate I commit to becoming, doing and allowing:", 4),
    ("sig", "Signed, on my gate day"),
    ("prompt", "One image or phrase from tonight I want to keep:", 2),
 ],
},
{
 "family": "planner", "section": "Activate", "title": "The 88-Word Script", "toc": False,
 "blocks": [
    ("p", "Describe the life your intention builds in exactly 88 words, present tense, every word chosen. Count them; the constraint is the ceremony."),
    ("linesfill",),
 ],
},

# ---------------------------------------------------------------- ACT
divider("VI", "Act", "Where intention meets calendar", "sun", 36),
{
 "family": "action", "section": "Act", "title": "Intention to Action Map", "toc": True,
 "blocks": [
    ("fields", ["My intention", "Real in 30 days looks like", "Milestone one", "Milestone two"]),
    ("prompt", "Milestone one, broken into pieces small enough for a Tuesday:", 4),
 ],
},
{
 "family": "action", "section": "Act", "title": "First Eight Moves", "toc": False,
 "blocks": [
    ("fields", ["1", "2", "3", "4", "5", "6", "7", "8"]),
    ("note", "Each move gets a date in your weekly pages before this planner closes today."),
 ],
},
{
 "family": "action", "section": "Act", "title": "Four Horizons", "toc": False,
 "blocks": [
    ("fields", ["Within 24 hours", "Within 72 hours", "Within 8 days", "Within 30 days"]),
    ("prompt", "If my likely obstacle shows up, then I will:", 3),
    ("prompt", "Who knows about this plan, and when we check in:", 2),
 ],
},
{
 "family": "action", "section": "Act", "title": "Thirty Days, Tracked", "toc": False,
 "blocks": [
    ("grid", ["Week 1", "Week 2", "Week 3", "Week 4"], ["M", "T", "W", "T", "F", "S", "S"]),
    ("fields", ["The habit this grid is watching"]),
 ],
},

# ---------------------------------------------------------------- INTEGRATE
divider("VII", "Integrate", "The thirty days after the gate", "infinity", 37),
{
 "family": "integration", "section": "Integrate", "title": "The Morning After", "toc": True,
 "blocks": [
    ("prompt", "How the ritual felt, recorded before the day begins:", 3),
    ("prompt", "What stayed with me overnight:", 2),
    ("check", ["24-hour action done or scheduled"]),
 ],
},
{
 "family": "integration", "section": "Integrate", "title": "Check-Ins: Day 3 & Day 8", "toc": False,
 "blocks": [
    ("h3", "Day three"),
    ("prompt", "What is settling, and where resistance is showing up:", 3),
    ("h3", "Day eight"),
    ("prompt", "First evidence of movement, and what needs adjusting:", 3),
 ],
},
{
 "family": "integration", "section": "Integrate", "title": "The Thirty-Day Review", "toc": False,
 "blocks": [
    ("twocol", "Changed in me", "Changed around me", 5),
    ("prompt", "What happened, what did not, what surprised me:", 3),
    ("prompt", "The practice I am keeping past this season:", 2),
 ],
},
{
 "family": "integration", "section": "Integrate", "title": "Opportunity Log", "toc": False,
 "blocks": [
    ("p", "Openings, invitations, coincidences, offers. Noticing more usually means your attention has changed; answer each one with a response."),
    ("table", ["Date", "What I noticed", "How I responded"],
      [["1.", "", ""], ["2.", "", ""], ["3.", "", ""], ["4.", "", ""], ["5.", "", ""], ["6.", "", ""]],
      [0.16, 0.46, 0.38]),
 ],
},
{
 "family": "planner", "section": "Integrate", "title": "Pocket Affirmations", "toc": False,
 "blocks": [
    ("cardaff", [
      "I trust the next honest step.",
      "I am available for aligned opportunities.",
      "I can receive without abandoning myself.",
      "My actions are beginning to match my intentions.",
      "Courage can be quiet and consistent.",
      "I make room for a life that fits me.",
      "I keep small promises to myself, and they are adding up.",
      "I honor my desire with action.",
    ]),
    ("prompt", "My own line, in my own words:", 2),
 ],
},
{
 "family": "planner", "section": "Integrate", "title": "A Three-Card Check-In", "toc": False,
 "blocks": [
    ("p", "Any deck, cards as mirrors rather than verdicts: pull three for Release, Receive, Act. Note first impressions before consulting a booklet, and end with one real-world step."),
    ("fields", ["Release", "Receive", "Act"]),
    ("prompt", "The action this pull suggests:", 2),
 ],
},
{
 "family": "planner", "section": "Integrate", "title": "Stones, If You Like Them", "toc": False,
 "blocks": [
    ("kv", [
      ("Citrine", "Traditionally associated with warmth and plenty; keep it near your workspace as a nudge toward optimism."),
      ("Carnelian", "Associated with courage and vitality; hold it before the brave call."),
      ("Rose quartz", "Associated with gentleness toward oneself; bedside duty."),
      ("Clear quartz", "The all-purpose stand-in for any intention."),
    ]),
    ("note", "Symbolic companions only; no stone treats or cures anything. A pebble from a meaningful walk serves the same purpose beautifully."),
 ],
},

# ---------------------------------------------------------------- NOTES
divider("VIII", "Notes", "Room to think", "geometry", 38),
{"family": "planner", "section": "Notes", "title": "Notes", "toc": False, "blocks": [("linesfill",)]},
{"family": "planner", "section": "Notes", "title": "Notes", "toc": False, "blocks": [("linesfill",)]},
{"family": "planner", "section": "Notes", "title": "Ideas & Sparks", "toc": False, "blocks": [("dotsfill",)]},
{"family": "planner", "section": "Notes", "title": "Ideas & Sparks", "toc": False, "blocks": [("dotsfill",)]},
{"kind": "back", "quote": "Small and done, again and again, becomes a life.", "brand": "GlowHausDigital"},
]
