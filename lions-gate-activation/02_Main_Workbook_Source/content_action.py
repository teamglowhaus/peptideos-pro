# The Aligned Action Plan (content module)
# Family: action / Kicker: Aligned Action

PAGES = [

    # 1 — Education: Where Intention Meets Calendar
    {
        "family": "action",
        "section": "Aligned Action",
        "title": "Where Intention Meets Calendar",
        "subtitle": "The part of manifestation that most workbooks skip",
        "toc": True,
        "wash": True,
        "blocks": [
            ("p", "In this workbook, manifestation is a practical sequence: clarity about what you want, a self-concept spacious enough to hold it, repetition that keeps it in view, and real action that moves it forward. The first three change how you see. This section changes what you do, and that is where the outside world starts cooperating."),
            ("h2", "Why action changes identity"),
            ("p", "Affirmations describe the woman you are becoming. Kept promises prove her. Every time you tell yourself *I will do this by Thursday* and then actually do it, you hand your own mind a piece of evidence, and identity shifts far faster on evidence than on repetition alone. Self-trust is not a mood; it is a track record, built one small kept promise at a time."),
            ("h2", "Aligned action, not forced action"),
            ("p", "Not all effort is equal. Forced action comes from fear of falling behind. Aligned action has three markers:"),
            ("bullets", [
                "It moves toward your values, not just away from your anxiety",
                "It is right-sized: ambitious in direction, modest in daily dose",
                "It is honest: you would still choose it if nobody was watching",
            ]),
            ("h2", "The map you are about to draw"),
            ("kv", [
                ("Intention", "The direction you have chosen, named in your own words."),
                ("Outcome", "What real would look like by a specific date."),
                ("Milestone", "A checkpoint you could photograph or point to."),
                ("Action", "A step small enough to finish on an ordinary Tuesday."),
            ]),
            ("quote", "The calendar is where the wish learns to walk."),
        ],
    },

    # 2 — Intention-to-outcome map
    {
        "family": "action",
        "section": "Aligned Action",
        "title": "The Intention-to-Outcome Map",
        "subtitle": "From a felt direction to something you could point to",
        "toc": True,
        "blocks": [
            ("p", "Vague intentions produce vague weeks. Here you translate your chosen intention into outcomes with dates on them, then lay stepping stones between today and there."),
            ("prompt", "My intention for this season, written as one honest sentence:", 2),
            ("h2", "What real would look like"),
            ("prompt", "In thirty days, I would know this was becoming real because:", 3),
            ("prompt", "In six months, the visible difference in my ordinary life would be:", 3),
            ("h2", "Milestone stepping stones"),
            ("note", "Work backward from the six-month picture. Each milestone should be concrete enough that a kind friend could confirm you reached it."),
            ("fields", [
                "Milestone one, the nearest stepping stone",
                "Milestone two, the middle of the crossing",
                "Milestone three, the stone closest to the outcome",
            ]),
        ],
    },

    # 3 — Milestone-to-action worksheet
    {
        "family": "action",
        "section": "Aligned Action",
        "title": "One Milestone, Tuesday-Sized",
        "subtitle": "Break a single milestone into pieces you can actually lift",
        "blocks": [
            ("p", "A milestone is too big to do in a day; that is its job. Your job is to keep cutting it down until each piece fits inside a normal week, between the laundry and the life."),
            ("fields", ["The milestone I am breaking down"]),
            ("steps", [
                ("List the moving parts", "Write everything this milestone requires, messy and unordered is fine."),
                ("Find the true first move", "Circle the one piece that unlocks the others, not the one that merely looks productive."),
                ("Cut until it fits a Tuesday", "If a piece needs more than about an hour, split it again. Repeat without shame."),
            ]),
            ("fields", [
                "Piece one, the true first move",
                "Piece two",
                "Piece three",
                "Piece four",
                "Piece five, optional",
            ]),
            ("prompt", "The piece I keep avoiding, and what would make it smaller:", 2),
            ("lines", 2),
        ],
    },

    # 4 — First Eight Actions (fresh framing: numbered checklist with date column)
    {
        "family": "action",
        "section": "Aligned Action",
        "title": "First Eight Actions",
        "subtitle": "Eight moves in thirty days, each finishable in one sitting",
        "blocks": [
            ("p", "Momentum is manufactured, not found. In honor of the eight, choose eight actions you can complete within the next thirty days and give every one of them a deadline. An action qualifies when you could answer *done or not done* without needing to explain."),
            ("table",
             ["", "The action, finishable in one sitting", "Done by"],
             [["1.", "", ""], ["2.", "", ""], ["3.", "", ""], ["4.", "", ""],
              ["5.", "", ""], ["6.", "", ""], ["7.", "", ""], ["8.", "", ""]],
             [0.07, 0.68, 0.25]),
            ("note", "Check the number when it is complete. Nothing on this list should depend on anyone else saying yes first."),
            ("prompt", "The action on this list I am secretly most excited about, and why:", 2),
            ("prompt", "The action I am most likely to postpone, and what I will trade to protect it:", 2),
        ],
    },

    # 5 — Time-horizon commitments
    {
        "family": "action",
        "section": "Aligned Action",
        "title": "Four Horizons",
        "subtitle": "One commitment for each distance",
        "blocks": [
            ("p", "Different horizons do different work. The near ones break inertia; the far ones require a calendar and a little faith in your own follow-through."),
            ("kv", [
                ("The 24-hour action", "So small it is almost funny. Its only job is to break the seal."),
                ("The 72-hour action", "Rides the early energy while the ritual is still warm in your body."),
                ("The eight-day action", "Closes your activation window with proof, not just poetry."),
                ("The 30-day action", "Far enough out to need scheduling, close enough to stay real."),
            ]),
            ("fields", [
                "Within 24 hours I will",
                "Within 72 hours I will",
                "Within eight days I will",
                "Within thirty days I will",
            ]),
            ("prompt", "What I will say to myself if one of these horizons slips:", 2),
            ("lines", 3),
        ],
    },

    # 6 — Obstacle forecast + if-then planning
    {
        "family": "action",
        "section": "Aligned Action",
        "title": "The Obstacle Forecast",
        "subtitle": "Plan for the weather, not just the destination",
        "blocks": [
            ("p", "Obstacles are not omens; they are logistics. Psychologists call the tool below an if-then plan: you decide your response before the obstacle arrives, so the decision is already made when your willpower is tired."),
            ("callout", "A worked example",
             "Obstacle: my sister visits and my morning slot collapses. If my morning disappears, then I will do the ten-minute version at lunch and count it as fully done."),
            ("table",
             ["Likely obstacle", "If this happens", "Then I will"],
             [["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""]],
             [0.30, 0.32, 0.38]),
            ("prompt", "The obstacle most likely to be me, and how I will meet myself kindly when it shows up:", 3),
            ("lines", 2),
        ],
    },

    # 7 — Support structures
    {
        "family": "action",
        "section": "Aligned Action",
        "title": "Support Structures",
        "subtitle": "Make the aligned thing the easy thing",
        "blocks": [
            ("h3", "Accountability"),
            ("prompt", "Who knows about this plan, and what exactly have I asked them to do?", 3),
            ("h3", "Environment"),
            ("p", "Your space votes on your behavior every day. Notice what it is currently voting for."),
            ("twocol", "In my space, this makes action easier", "This quietly makes it harder", 4),
            ("h3", "Habit stacking"),
            ("p", "Attach the new action to a habit that already runs on autopilot: after I pour my coffee, I will open the notebook."),
            ("table",
             ["After I (existing habit)", "I will (new action)"],
             [["", ""], ["", ""], ["", ""]],
             [0.5, 0.5]),
        ],
    },

    # 8 — Momentum: evidence log, course correction, celebration, calendar
    {
        "family": "action",
        "section": "Aligned Action",
        "title": "Keeping the Momentum",
        "subtitle": "Evidence, adjustment, and the unglamorous middle",
        "toc": True,
        "blocks": [
            ("p", "From today on, keep a running record of proof: actions completed, conversations opened, tiny shifts in how you carry yourself. Progress you never write down is progress your doubt gets to deny later. Start the record here:"),
            ("lines", 3),
            ("h3", "Course-correct without abandoning yourself"),
            ("p", "When something is not working, adjust the plan, not your worth. A revised deadline is maintenance; it is not a verdict on you."),
            ("prompt", "My celebration practice, how I will mark small wins so they register:", 2),
            ("prompt", "On the day this stops feeling magical, I will:", 2),
            ("aff", "I keep promises to myself in sizes I can carry."),
            ("h3", "Thirty days at a glance"),
            ("note", "Shade each day you took any aligned action, however small. A visible chain is its own motivation."),
            ("grid", ["Week 1", "Week 2", "Week 3", "Week 4"], ["M", "T", "W", "T", "F", "S", "S"]),
        ],
    },
]
