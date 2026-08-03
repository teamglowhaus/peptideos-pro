# -*- coding: utf-8 -*-
"""Front matter: title, copyright, license, thank-you, disclaimer, welcome,
how-to-use, format guidance, ownership, beginning check-in.
The cover and the table of contents are inserted by the build script."""

PAGES = [

# ---------------------------------------------------------------- title page
{
 "family": "front", "section": "", "title": "", "toc": False,
 "blocks": [
    ("spacer", 90),
    ("ck", "GlowHausDigital presents"),
    ("spacer", 14),
    ("cp", "The Lion's Gate 8/8 Activation", 17),
    ("spacer", 6),
    ("cp", "*An Eight-Day Manifestation, Self-Concept and Aligned-Action Experience*", 3),
    ("spacer", 20),
    ("ornament",),
    ("spacer", 20),
    ("cp", "Release what limits you. Clarify what you truly desire. Embody your next identity, and create an aligned plan for the life you are ready to build.", 1),
    ("spacer", 170),
    ("ck", "A guided workbook for the season of August 8"),
 ],
},

# ---------------------------------------------------------------- copyright
{
 "family": "front", "section": "About This Edition", "title": "Copyright", "toc": False,
 "blocks": [
    ("p", "The Lion's Gate 8/8 Activation. Copyright © 2026 GlowHausDigital. All rights reserved."),
    ("p", "No portion of this publication may be reproduced, distributed, resold, transmitted, stored in a shared retrieval system or used commercially without prior written permission, except for the personal use permitted by the license included in this edition."),
    ("p", "This workbook was written, designed and produced with care for individual readers. Sharing files, links or printed copies outside your household deprives independent creators of the income that makes work like this possible. Thank you for honoring that."),
    ("spacer", 8),
    ("kv", [
      ("Published by", "GlowHausDigital"),
      ("Website", "[INSERT WEBSITE OR ETSY SHOP URL]"),
      ("Contact", "[INSERT CONTACT EMAIL]"),
      ("Edition", "First edition, 2026. Typeset in Cormorant Garamond, Marcellus and Lato (all licensed under the SIL Open Font License)."),
    ]),
    ("spacer", 8),
    ("note", "Trademark notice: Franklin Planner and FranklinCovey are trademarks of their respective owners. This independently created digital product is not affiliated with, sponsored by, approved by or endorsed by Franklin Planner or FranklinCovey. Brand names are used only to help customers identify compatible page dimensions. Please measure your existing planner pages and binder before printing."),
    ("note", "This is a digital product. No physical item will be shipped."),
 ],
},

# ---------------------------------------------------------------- license
{
 "family": "front", "section": "Your License", "title": "Personal-Use License", "toc": True,
 "subtitle": "Plain words about what your purchase includes",
 "blocks": [
    ("p", "This workbook now belongs to your personal practice. Your purchase includes a single-user, personal-use license, which is simpler than it sounds: this copy is for you."),
    ("h2", "You are welcome to"),
    ("check", [
      "Download the files and keep them for your own use",
      "Print any pages, in any quantity, for yourself, as many times as you like",
      "Use the files on your personal tablet or digital note-taking device",
      "Place printed pages inside your own planner or binder",
      "Make reasonable backup copies for your own records",
      "Complete the workbook privately, or alongside members of your immediate household",
    ]),
    ("h2", "Please do not"),
    ("bullets", [
      "Resell, redistribute or share the files, the download link, or printed copies with friends, clients, students or group members",
      "Upload the files to a shared drive, membership site, social-media group or any public website",
      "Use the product, in whole or in part, inside a paid course, coaching package, workshop, retreat, membership or client service",
      "Extract and resell individual pages, or copy the artwork, prompts, layouts, affirmations or written content into another product",
      "Claim the work as your own, use it for print-on-demand, create derivative products for resale, or use it as a commercial-use template",
      "Use the files or their text for training artificial-intelligence systems or datasets",
      "Remove copyright notices and redistribute the content",
      "Buy one copy to serve an entire organization, classroom, coaching group or client base",
    ]),
 ],
},

{
 "family": "front", "section": "Your License", "title": "Practitioners, Groups & Gifts", "toc": False,
 "blocks": [
    ("h2", "If you work with clients or groups"),
    ("p", "Coaches, therapists, teachers, workshop facilitators, retreat organizers, spiritual practitioners, group leaders, membership owners, businesses and organizations are so welcome here, and a separate license is required before using this material with the people you serve. Message GlowHausDigital through Etsy and we will find the right arrangement."),
    ("h2", "Want to share it with someone?"),
    ("p", "The kindest way is also the simplest: gift her a copy of her own. She receives clean files, the current edition and her own fresh season, and your purchase keeps supporting the work. Etsy makes digital gifting easy at checkout."),
    ("spacer", 14),
    ("quote", "Your purchase supports the time, care, writing and design that went into creating this experience. Thank you for respecting the license and directing others to purchase their own copy."),
    ("spacer", 10),
    ("ornament",),
 ],
},

# ---------------------------------------------------------------- thank you
{
 "family": "front", "section": "A Note of Thanks", "title": "Thank You", "toc": False, "wash": True,
 "blocks": [
    ("p", "Thank you for allowing this workbook to become part of your Lion's Gate experience. You did not purchase a promise that one date will change everything. You chose to create space to listen to yourself, clarify what matters and take your next steps with intention. That choice says something good about where you are headed."),
    ("p", "Please use this book in whatever way actually supports you. Move slowly if slow is what you need. Skip any exercise that does not resonate, and return to it later or never. Write in the margins, ignore the suggested schedule, start on August 3 or in October. Nothing here needs to be completed perfectly to count."),
    ("p", "If this experience supports you, your honest review can help another buyer understand whether it may support her too. And if anything is wrong with your files, message me through Etsy before anything else; I would genuinely like to fix it for you."),
    ("spacer", 10),
    ("cp", "*I hope these eight days give you something that lasts far longer than a season.*", 2),
    ("spacer", 14),
    ("ck", "With warmth"),
    ("cp", "[INSERT YOUR FIRST NAME] · GlowHausDigital", 1),
    ("note", "Find me: GlowHausDigital on Etsy · [INSERT SOCIAL HANDLE, OPTIONAL]"),
 ],
},

# ---------------------------------------------------------------- disclaimer
{
 "family": "front", "section": "Please Read", "title": "A Clear and Caring Disclaimer", "toc": False,
 "blocks": [
    ("p", "This workbook is offered for personal reflection, education, spiritual exploration, journaling, entertainment, planning and self-development. It is one woman's carefully designed invitation to think, feel and act on purpose. It is not, and cannot be, a substitute for professional care."),
    ("callout", "This product does not replace", "Medical care, mental-health care, therapy, financial advice, legal advice, crisis support, or professional diagnosis and treatment of any kind. If you are struggling, please reach out to a qualified professional or a local crisis line. Doing so is not a failure of faith or of manifestation. It is self-respect in action."),
    ("h2", "Working safely"),
    ("bullets", [
      "Candles and smoke: never leave a flame unattended, keep it away from fabric and hair, and skip open flame entirely if your space or health makes it unwise. Battery candles carry the symbolism just as well.",
      "Essential oils and baths: patch-test oils, dilute properly, and check safety guidance if you are pregnant or have sensitivities.",
      "Crystals: decorative and symbolic only. They do not treat, cure or prevent any condition.",
      "Feelings: some prompts reach into old stories. If an exercise stirs more than you want to hold today, stop, breathe, and come back another time, or bring the topic to someone qualified to support you.",
    ]),
    ("p", "Outcomes are not guaranteed, and no honest product can promise you a specific result: not money, not love, not healing, not success. What this workbook offers is structure, clarity and encouragement for the effort only you can make. In my experience, that is worth far more than a promise."),
 ],
},

# ---------------------------------------------------------------- welcome letter
{
 "family": "front", "section": "Welcome", "title": "A Letter Before You Begin", "toc": True,
 "blocks": [
    ("p", "Dear reader,"),
    ("p", "Every August, a quiet excitement moves through spiritual communities as the calendar approaches the eighth day of the eighth month. Some call it the Lion's Gate Portal. Some simply call it 8/8. However you found your way here, I want to tell you what this book believes, so you can decide how you want to walk through it."),
    ("p", "This book believes that dates are doorways when we decide they are. It believes that desire is information, that self-concept is the quiet engine underneath most outcomes, and that spiritual intention becomes far more powerful when it is paired with self-awareness, embodiment and practical action. You will find symbolism here, and star-lore, and ritual, because those things help intentions feel real enough to act on. You will not find promises that the sky will do your work for you."),
    ("p", "Over eight days, you will move through a complete arc: noticing what is, releasing what no longer fits, exploring worthiness and courage, choosing clear intentions, practicing the identity that matches them, and building a plan you can actually live. On August 8, or whichever day you choose as your gate, you will gather it all into one unhurried ritual. Then, and this is the part most products skip, you will keep going, with check-ins that carry you thirty days past the portal."),
    ("p", "You do not need to believe anything in particular. You need only be willing to tell yourself the truth, gently, and to take one honest step at a time."),
    ("p", "I am so glad you are here."),
    ("sig", "GlowHausDigital"),
 ],
},

# ---------------------------------------------------------------- how to use
{
 "family": "front", "section": "Welcome", "title": "How to Use This Experience", "toc": True,
 "blocks": [
    ("p", "There is no single correct way through these pages, but it helps to know how the book is built. The parts are sequenced the way change usually happens: understanding, clearing, honest excavation, clarity, identity, practice, action, integration."),
    ("steps", [
      ("Orient", "Read Part I and II lightly, like a conversation. Fill in the definitions pages so the vocabulary is yours, not mine."),
      ("Prepare", "In the days before your eight-day arc begins, work through Preparation and Clearing at an easy pace."),
      ("Travel the eight days", "One day, one theme, roughly twenty to forty minutes. Ideally August 1 through 8, but any eight consecutive days work."),
      ("Cross the gate", "On day eight, choose one of the complete rituals: fifteen minutes, forty-five minutes, or the full immersive version."),
      ("Integrate", "Use the check-ins on the morning after, at three days, eight days and thirty days. This is where intention becomes pattern."),
    ]),
    ("h2", "If you are short on time"),
    ("p", "Life does not always leave room for a full arc, and late arrivals are still arrivals. The Choose Your Path page ahead offers a fifteen-minute path and a forty-five-minute path that touch every essential beat. The separate Quick-Start Guide included with your purchase does the same, and the Quick Reference part at the back compresses the whole system onto a handful of pages."),
    ("callout", "One kind rule", "Nothing in this book is homework. If a page does not speak to your life, turn past it without apology. An experience half-completed with sincerity is worth more than one finished out of obligation."),
 ],
},

# ---------------------------------------------------------------- format guidance
{
 "family": "front", "section": "Welcome", "title": "Choose the Format That Fits Your Ritual", "toc": True,
 "blocks": [
    ("p", "Your purchase includes several editions of this experience, because a practice you can actually reach for is worth more than a beautiful file you never open."),
    ("table",
      ["Edition", "Best for", "Notes"],
      [
        ["Full workbook, US Letter", "Printing at home in North America", "8.5 × 11 in, printer-friendly light pages"],
        ["Full workbook, A4", "Printing outside North America", "210 × 297 mm, reflowed, not shrunk"],
        ["Digital edition (Letter and A4)", "Tablets and annotation apps", "Clickable contents, roomier writing lines"],
        ["Planner inserts, 4 sizes", "Ring-bound planner users", "Pocket, Compact, Classic and Monarch sizes"],
        ["Quick-Start Guide", "Beginning close to August 8", "The essentials in a single short read"],
        ["Affirmation cards + extras", "Keeping the season visible", "32 cards, planner tabs, phone wallpapers"],
      ],
      [0.30, 0.33, 0.37]),
    ("h2", "Three honest suggestions"),
    ("bullets", [
      "If you love handwriting but hate printing whole books, print only the Eight-Day Activation and the ritual pages, and keep the rest on a screen.",
      "If you use a ring planner, the Classic size edition is the most complete planner companion; the insert guide explains printing and punching.",
      "If you are reading this on August 7, breathe. Open the Quick-Start Guide tonight and let the rest of the book find you after the portal.",
    ]),
    ("note", "Printing details, tablet instructions and planner sizing all have their own guides in your download, so nothing here depends on guesswork."),
 ],
},

# ---------------------------------------------------------------- ownership
{
 "family": "front", "section": "", "title": "", "toc": False, "wash": True,
 "blocks": [
    ("spacer", 60),
    ("ck", "This copy belongs to"),
    ("spacer", 4),
    ("lines", 1),
    ("spacer", 26),
    ("ck", "Her season begins"),
    ("spacer", 4),
    ("lines", 1),
    ("spacer", 30),
    ("ornament",),
    ("spacer", 24),
    ("cp", "*Eight days set aside, on purpose, for the woman she is becoming.*", 2),
 ],
},

# ---------------------------------------------------------------- beginning check-in
{
 "family": "front", "section": "Beginning", "title": "Where I Am Standing Today", "toc": True,
 "subtitle": "A beginning intention and an honest emotional check-in",
 "blocks": [
    ("p", "Before the teaching, before the rituals, mark the starting point. Future you will love having this page to look back on."),
    ("fields", ["Today's date", "Days until August 8 (or until my chosen gate day)"]),
    ("prompt", "Right now, in one unfiltered sentence, my life feels like:", 2),
    ("scale", "My energy level as this season opens"),
    ("scale", "How connected I feel to what I actually want"),
    ("prompt", "I am giving myself these eight days because:", 3),
    ("prompt", "If only one thing were different by early September, I would want it to be:", 3),
    ("note", "There are no wrong answers on this page. It is a snapshot, not a judgment."),
 ],
},
]
