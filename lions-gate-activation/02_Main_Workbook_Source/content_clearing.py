"""Part III: Preparation & Clearing.

Pages for the pre-activation clearing work: space reset, open loops,
boundaries, quick money/habit/self-talk audits, cleansing ritual menu,
release letter and a fire-free symbolic release ceremony.
"""

SECTION = "Preparation & Clearing"

PAGES = [
    # ------------------------------------------------------------ 1. education
    {
        "family": "education",
        "section": SECTION,
        "title": "Clearing the Ground",
        "subtitle": "Why making room comes before calling anything in",
        "toc": True,
        "wash": True,
        "blocks": [
            ("p", "An intention set on top of clutter has to shout to be heard. Before your eight days begin, this section helps you clear a little room: in your home, your inbox, your relationships and your self-talk, so that whatever you choose on August 8 lands somewhere ready to hold it."),
            ("h2", "Why clearing works"),
            ("p", "There is nothing mystical about this part, although you are welcome to treat it as sacred. Preparation changes three practical things about how your mind treats a new beginning."),
            ("kv", [
                ("Attention", "A cleared surface, screen or schedule stops tugging at your focus, which leaves more of it available for what you actually want to build."),
                ("Closure", "Naming and finishing open loops quiets the background hum of the unfinished. Ending things well makes beginning things easier."),
                ("The fresh-start effect", "Research on temporal landmarks suggests we pursue goals more readily after a date that feels like a clean line: a new year, a birthday, or a chosen day like 8/8."),
            ]),
            ("callout", "Clearing is not purging", "You are not required to minimize your life or throw anything away. Clear only what obscures your view. A little more room is enough."),
            ("quote", "You are not making space because your life is wrong. You are making space because something new is arriving."),
        ],
    },
    # -------------------------------------------------- 2. space reset checklists
    {
        "family": "exercise",
        "section": SECTION,
        "title": "The Space Reset",
        "subtitle": "A room and a screen can both hold old weather",
        "blocks": [
            ("p", "Choose a handful of these, not all of them. Twenty minutes of honest clearing beats a whole weekend of overwhelmed reorganizing."),
            ("h3", "Physical space reset"),
            ("check", [
                "Clear one surface completely: desk, nightstand or kitchen table",
                "Wash or change your bedding",
                "Open the windows and let the air move for ten minutes",
                "Carry stray cups, papers and laundry out of your main room",
                "Move one object you dislike out of sight",
                "Set up one small spot that will hold this workbook and a pen",
                "Add one living or beautiful thing: a plant, a flower, a bowl of water",
            ]),
            ("h3", "Digital declutter"),
            ("check", [
                "Archive or answer the emails that have been sitting open",
                "Unfollow five accounts that leave you feeling behind",
                "Silence nonessential notifications for the eight days",
                "Pare your phone's home screen down to what you actually use",
                "Unsubscribe from three mailing lists you never read",
                "Delete screenshots and downloads you no longer need",
                "Choose a phone-free window around your morning practice",
            ]),
            ("prompt", "One corner of my home I will reset before the eight days begin, and what belongs there instead:", 4),
        ],
    },
    # ------------------------------------- 3. emotional inventory + open loops
    {
        "family": "exercise",
        "section": SECTION,
        "title": "Open Loops and Unfinished Business",
        "subtitle": "What is still running in the background",
        "toc": True,
        "blocks": [
            ("p", "Unfinished things do not disappear when you ignore them; they idle quietly and burn attention you could be spending on your own life. An open loop is anything begun and not concluded: a conversation, a task, a decision you keep postponing."),
            ("scale", "How heavy does my mental load feel as I begin this page?"),
            ("prompt", "Feelings that have been visiting me most often this month, whether or not they make sense:", 3),
            ("h2", "The open-loop list"),
            ("p", "List what is unfinished, then sort each item: **close it** (do it or say it), **schedule it** (give it a date), or **release it** (decide, on purpose, that it will not happen)."),
            ("table",
                ["Open loop", "Close, schedule or release?", "Next step or date"],
                [["1.", "", ""], ["2.", "", ""], ["3.", "", ""], ["4.", "", ""],
                 ["5.", "", ""], ["6.", "", ""], ["7.", "", ""]],
                (0.46, 0.28, 0.26)),
            ("note", "Releasing counts as finishing. A loop closed by an honest decision stops draining you just as surely as one closed by doing."),
        ],
    },
    # ------------------------------------------- 4. boundaries + relationships
    {
        "family": "exercise",
        "section": SECTION,
        "title": "Boundary Check",
        "subtitle": "Where your energy actually goes",
        "blocks": [
            ("p", "Relationships are part of your inner landscape. Without ranking anyone's worth, notice which interactions leave you fuller and which leave you scraped thin. This is information about fit and pacing, not a verdict on the people involved."),
            ("twocol", "Interactions that fill me", "Interactions that drain me", 5),
            ("prompt", "One boundary I am ready to practice this week, with whom, and around what:", 3),
            ("prompt", "How I will say it, kindly and without a paragraph of apology:", 2),
            ("callout", "A boundary is not a wall", "It is a door with a handle on your side. You can love someone deeply and still decline the role they have assigned you."),
        ],
    },
    # ------------------------------- 5. money temperature + habit + self-talk
    {
        "family": "exercise",
        "section": SECTION,
        "title": "Money Feelings, Habits and Self-Talk",
        "subtitle": "Three quick audits before the deeper work",
        "blocks": [
            ("p", "This page only takes a temperature. The deeper money story, with its history and its rewrites, has a section of its own later in this workbook."),
            ("prompt", "When I think about my money situation today, the honest feeling underneath is:", 2),
            ("note", "No fixing yet. Just name what is true right now, without an improvement plan attached."),
            ("h3", "Habit audit"),
            ("twocol", "A daily habit that supports me", "A daily habit that quietly costs me", 4),
            ("h3", "Self-talk audit"),
            ("prompt", "A phrase I often catch myself saying about myself, out loud or silently:", 2),
            ("prompt", "Is that phrase fully true? What would I say to a friend who believed it about herself?", 3),
        ],
    },
    # -------------------------------------------------- 6. cleansing ritual menu
    {
        "family": "ritual",
        "section": SECTION,
        "title": "A Menu of Cleansing Rituals",
        "subtitle": "Choose one, adapt freely, or invent your own",
        "toc": True,
        "blocks": [
            ("p", "A cleansing ritual is a physical way of telling yourself that one chapter is ending. None of these carry power beyond the meaning you bring to them, and none are required. Pick whichever suits your home, your senses and your evening."),
            ("kv", [
                ("Water", "Shower or bathe slowly, imagining the residue of the season rinsing away. Salts and oils are lovely; plain water works just as well."),
                ("Smoke-free clearing", "Open every window wide for ten minutes, or mist a favorite room spray, and let moving air do the work."),
                ("Sound", "A bell, a chime, a sung note, or one favorite song played through every room."),
                ("Candle", "Light a single candle, sit with it for five quiet minutes, then blow it out with one sentence of thanks."),
                ("Candle-free glow", "A lamp, a string of lights or the sunset itself can hold the same role as a flame."),
                ("No supplies at all", "Wash your hands slowly under warm water and say silently: I am setting this season down."),
            ]),
            ("note", "Fire safety: never leave a lit candle unattended, keep it well away from fabric, paper and hair, and set it on a stable, heat-proof surface out of reach of children and pets."),
            ("prompt", "The clearing ritual I am choosing, and the evening I will give it:", 2),
        ],
    },
    # -------------------------- 7. stop carrying + mine / not mine
    {
        "family": "exercise",
        "section": SECTION,
        "title": "What I Am Ready to Stop Carrying",
        "subtitle": "Sorting the load before the gate",
        "blocks": [
            ("p", "Some weight is worth carrying and some has simply been in your arms so long you forgot you could put it down. Name it plainly here."),
            ("prompt", "I am ready to stop carrying:", 4),
            ("h2", "What is mine, and what is not?"),
            ("p", "Part of your load belongs to you: your choices, your healing, your next step. Part of it never did: other people's moods, opinions, outcomes and old predictions about who you would become. Sort honestly."),
            ("twocol", "Mine to carry", "Not mine to carry", 6),
            ("prompt", "Something I have been holding that was never mine to fix:", 2),
        ],
    },
    # ------------------------------------------------------- 8. release letter
    {
        "family": "exercise",
        "section": SECTION,
        "title": "The Release Letter",
        "subtitle": "For a pattern, story or season you are completing",
        "blocks": [
            ("p", "Write to whatever you are finishing with, and address it directly: *Dear exhaustion. Dear old story about being behind. Dear season of waiting.* Say what living with it was like, what it taught you, and why you are done. You will never send this letter; it exists so the words can finally leave your head."),
            ("bullets", [
                "Name it honestly: what it was, how long it stayed, what it cost",
                "Thank it if thanks are true; skip that part if they are not",
                "End with a clear goodbye sentence in your own words",
            ]),
            ("aff", "What I set down does not need me to carry it any further."),
            ("fields", ["Dear"]),
            ("linesfill",),
        ],
    },
    # ------------------------------------------- 9. symbolic release ceremony
    {
        "family": "ritual",
        "section": SECTION,
        "title": "A Symbolic Release Ceremony",
        "subtitle": "No fire required",
        "toc": True,
        "blocks": [
            ("p", "Once the letter is written, let your body finish what your mind began. A small physical act gives the release an ending your memory can point to."),
            ("kv", [
                ("Tear it", "Rip the letter into small pieces, slowly, and let the recycling take them."),
                ("Bury it", "Fold the page and tuck it into garden soil or a potted plant, returning the old story to the ground."),
                ("Dissolve it", "Rest the paper in a bowl of water and watch it soften; pour everything away when you are ready."),
                ("Delete it", "If you wrote digitally, read the letter once aloud, then delete the note and empty the trash."),
            ]),
            ("steps", [
                ("Ground first", "Feel your feet on the floor, lengthen one exhale, and name where you are: room, day, year."),
                ("Release", "Perform your chosen act slowly, saying your goodbye sentence once."),
                ("Return", "Drink some water, stretch your arms overhead, and stand by a window for three breaths."),
            ]),
            ("note", "Keep this ceremony flame-free. Burning paper indoors is never worth the risk, and tearing works on every level that matters."),
            ("prompt", "What I noticed in my body after letting it go:", 3),
        ],
    },
]
