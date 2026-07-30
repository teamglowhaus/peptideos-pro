# Post-Portal Integration (content module)
# Family: integration / Kicker: Integration

PAGES = [

    # 1 — Education: After the Portal Closes
    {
        "family": "integration",
        "section": "Integration",
        "title": "After the Portal Closes",
        "subtitle": "The date was a doorway. The walking is ordinary days.",
        "toc": True,
        "wash": True,
        "blocks": [
            ("p", "On August 9 the candles are put away, the feeds move on, and your life is still your life. This is the moment most Lion's Gate products pretend does not exist, and it is the moment that decides whether the last eight days become a memory or a turning."),
            ("h2", "Nothing failed"),
            ("p", "If your circumstances look identical the morning after, nothing went wrong. A doorway changes your direction, not your scenery. In modern spiritual practice the portal is the beginning of a season, not the delivery date, and the work you did still counts even while it is invisible."),
            ("h2", "Integration is repetition plus noticing"),
            ("p", "Integration has two humble ingredients. Repetition: the handful of practices you keep doing on days that feel like nothing. Noticing: catching the small evidence of change, in your choices and in your openings, before your old story explains it away. The pages ahead schedule both for you."),
            ("callout", "How to use this section",
             "Set gentle reminders now: the morning after, day three, day eight, and day thirty. Five honest minutes at each checkpoint will do more than an hour of scrolling for signs."),
            ("quote", "A portal is only ever as real as the week after it."),
        ],
    },

    # 2 — Morning-after reflection (August 9)
    {
        "family": "integration",
        "section": "Integration",
        "title": "The Morning After",
        "subtitle": "August 9, before the day gets loud",
        "toc": True,
        "blocks": [
            ("p", "Write this while the ritual is still close, ideally with your first drink of the morning. You are not measuring results yet; you are catching impressions before they fade."),
            ("prompt", "How the ritual actually felt while it was happening, in unedited words:", 3),
            ("prompt", "What stayed with me overnight, an image, a phrase, a feeling, a stubborn thought:", 3),
            ("h3", "First proof"),
            ("check", [
                "My 24-hour action is already done",
                "My 24-hour action is scheduled, with a day and a time",
            ]),
            ("prompt", "The action, and when it happened or will happen:", 2),
            ("lines", 3),
        ],
    },

    # 3 — Three-day + eight-day check-ins
    {
        "family": "integration",
        "section": "Integration",
        "title": "Two Check-Ins: Day Three and Day Eight",
        "subtitle": "First the settling, then the evidence",
        "blocks": [
            ("h2", "Day three: the settling"),
            ("p", "By now the glow has faded into regular life, which is exactly on schedule. Resistance often makes its first appearance here."),
            ("prompt", "Where resistance is showing up, and what it might be trying to protect me from:", 3),
            ("fields", [
                "My energy since the ritual, described honestly",
                "A feeling from the eight days that is starting to settle in",
            ]),
            ("h2", "Day eight: the evidence"),
            ("p", "One week of walking. Look for small proof, in your behavior first, in your circumstances second."),
            ("prompt", "The first small evidence I can point to, inner or outer, however modest:", 3),
            ("fields", [
                "Is the daily practice holding? What is really happening",
                "One adjustment my plan has earned this week",
            ]),
        ],
    },

    # 4 — 30-day check-in
    {
        "family": "integration",
        "section": "Integration",
        "title": "The Thirty-Day Check-In",
        "subtitle": "Results without judgment",
        "toc": True,
        "blocks": [
            ("p", "A month is long enough for honest data and short enough to change course. Read your intention map again before you write, then report like a kind scientist: curious, precise, unimpressed by drama."),
            ("twocol", "Internal changes I notice in myself", "Practical changes I can point to", 4),
            ("prompt", "What happened, what did not happen, and what genuinely surprised me:", 4),
            ("prompt", "The revisions my plan has earned, deadlines, sizes, or the plan itself:", 3),
            ("note", "Revising a plan is evidence you are steering, not proof you have failed. Only abandoned plans stay perfect."),
        ],
    },

    # 5 — Synchronicity and opportunity log
    {
        "family": "integration",
        "section": "Integration",
        "title": "Synchronicity and Opportunity Log",
        "subtitle": "A record of openings, kept with both feet on the ground",
        "blocks": [
            ("p", "Over the coming weeks, log the coincidences, introductions, ideas and invitations that seem to line up with your intention. Keep the record; skip the mythology."),
            ("callout", "A grounded way to read this log",
             "When you start noticing more opportunities, the most likely explanation is that your attention has changed, and that is genuinely powerful. You do not need a supernatural explanation for it to matter. What matters is the last column: openings reward the woman who responds with action."),
            ("table",
             ["Date", "What I noticed", "How I responded"],
             [["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""],
              ["", "", ""], ["", "", ""], ["", "", ""]],
             [0.14, 0.48, 0.38]),
            ("prompt", "A pattern I am beginning to see in what I keep noticing:", 2),
        ],
    },

    # 6 — What I Am Continuing
    {
        "family": "integration",
        "section": "Integration",
        "title": "What I Am Continuing",
        "subtitle": "Some practices earned a permanent place. Some are complete.",
        "blocks": [
            ("p", "You were never meant to keep all of it. Choose the few practices that fit an ordinary week, and release the rest without a backward glance."),
            ("h3", "Earning a permanent place"),
            ("check", [
                "Morning grounding, in some form",
                "A journaling practice, even a short one",
                "My affirmation or self-concept work",
                "The evening reflection",
                "The evidence and opportunity log",
                "A weekly look at my plan",
                "Something of my own invention:",
            ]),
            ("prompt", "Why these particular practices deserve space in my regular week:", 3),
            ("h3", "Retired without guilt"),
            ("p", "A practice can be finished the way a good book is finished: complete, not abandoned."),
            ("prompt", "What I am setting down now, with thanks and zero apology:", 3),
        ],
    },

    # 7 — Letter to next year's self + next-year review
    {
        "family": "integration",
        "section": "Integration",
        "title": "A Letter Across the Year",
        "subtitle": "Written now, opened before the next Lion's Gate season",
        "blocks": [
            ("p", "Tell the woman who opens this next August what this season was really like: what you hoped, what you feared, what you want her to remember about who you were when you wrote it. Seal it if you like, or fold this page's corner."),
            ("box", 230, "Dear me, one year from now"),
            ("fields", [
                "Written on (date)",
                "To be opened on or before (date)",
            ]),
            ("rule",),
            ("h2", "Next August: the review"),
            ("note", "Leave this section blank. Complete it next year, after you have read the letter and before you set new intentions."),
            ("twocol", "Where I was when I wrote this", "What unfolded, expected and not", 3),
            ("fields", [
                "What I want for the year ahead",
                "Review completed on (date)",
            ]),
        ],
    },
]
