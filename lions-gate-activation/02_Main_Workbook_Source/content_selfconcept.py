# Part VI - Self-Concept & the Future Self
# Content module for The Lion's Gate 8/8 Activation.
# Exports PAGES for the layout engine in lg/engine.py.

SECTION = "Self-Concept & Future Self"

PAGES = [

    # 1a. Education: what self-concept is, identity-based habits
    {
        "family": "education",
        "section": SECTION,
        "title": "The Self You Assume",
        "subtitle": "Where identity comes from, and how it changes",
        "toc": True,
        "wash": True,
        "blocks": [
            ("p", "Your self-concept is the collection of things you assume are true about you: I am bad "
                  "with money, I am the reliable one, I always quit in the middle. These assumptions feel "
                  "like facts because you have gathered years of evidence for them. But they began as "
                  "conclusions, and conclusions can be revised."),
            ("h2", "Behavior votes for identity"),
            ("p", "Habit researchers describe a simple loop: every action is a small vote for a version of "
                  "you. Send the invoice, and you vote for a woman who handles her money. Keep one tiny "
                  "promise to yourself, and you vote for someone trustworthy. No single vote decides the "
                  "election; the running count does."),
            ("h2", "Why this matters for 8/8"),
            ("p", "In this workbook, manifestation means clarity plus self-concept plus repetition plus "
                  "real action. You have named what you want. This part works on the assumptions of the "
                  "woman who could receive it, and keep it."),
            ("callout", "A grounding note",
                  "You are not broken and being repaired. You are revising a draft of yourself that was "
                  "written under old conditions."),
            ("quote", "You do not talk yourself into a new identity. You out-vote the old one."),
        ],
    },

    # 1b. Education: embodiment without pretending
    {
        "family": "education",
        "section": SECTION,
        "title": "Acting As If, Without Pretending",
        "blocks": [
            ("p", "Somewhere along the way, acting as if got confused with faking it. They are different "
                  "skills. Pretending denies the facts: the balance, the diagnosis, the deadline. "
                  "Embodiment accepts every fact and changes your posture toward them: how you decide, "
                  "speak, rest, and follow through."),
            ("kv", [
                ("Confidence", "Knowing the facts and trusting yourself to handle them."),
                ("Denial", "Refusing the facts and hoping momentum will cover for you."),
            ]),
            ("h2", "What acting as if is not"),
            ("bullets", [
                "Spending money your future self would actually flinch at",
                "Ignoring bills, symptoms, or red flags because attention feels negative",
                "Performing certainty you do not feel instead of building competence",
            ]),
            ("h2", "What it looks like instead"),
            ("bullets", [
                "Answering email like a woman whose time is valuable",
                "Keeping your word to yourself in small, cheap ways first",
                "Deciding from the person you are becoming, not the mood you are in",
            ]),
            ("note", "Embodiment is a reflective practice, not a financial strategy, and never a "
                     "substitute for medical, legal, or financial advice."),
        ],
    },

    # 2. Current-self inventory
    {
        "family": "exercise",
        "section": SECTION,
        "title": "A Kind and Honest Inventory",
        "blocks": [
            ("p", "Before drawing the future self, take stock of the current one in the tone you would use "
                  "for a friend: honest about the facts, gentle about the person. Nothing here is a "
                  "verdict. It is a starting photograph."),
            ("prompt", "The strengths I lean on, even on my hardest days, are:", 3),
            ("prompt", "The habits currently steering my weeks, helpful and not, include:", 3),
            ("prompt", "Lately, the voice in my head speaks to me like:", 2),
            ("prompt", "My surroundings, home, phone, people, are mostly feeding me:", 2),
        ],
    },

    # 3a. Future-self profile, page one
    {
        "family": "exercise",
        "section": SECTION,
        "title": "The Future Self, Page One",
        "subtitle": "Her values, boundaries and rhythms",
        "toc": True,
        "blocks": [
            ("p", "She is not a stranger and not a celebrity. She is you, a few thousand votes from now. "
                  "Describe her specifically enough that you could recognize her decisions in the wild."),
            ("h3", "Her values"),
            ("fields", ["The value she will not trade, even for approval",
                        "The value that decides how she spends money",
                        "The value people sense within minutes of meeting her"]),
            ("h3", "Her boundaries"),
            ("prompt", "The boundary she keeps without a speech or an apology is:", 2),
            ("h3", "Her rhythms"),
            ("twocol", "Anchors of her weekdays", "Anchors of her weekends", 6),
        ],
    },

    # 3b. Future-self profile, page two
    {
        "family": "exercise",
        "section": SECTION,
        "title": "The Future Self, Page Two",
        "subtitle": "Money, love, spaces and words",
        "blocks": [
            ("p", "Keep describing her where daily life actually happens: at the bank balance, in the hard "
                  "conversation, in the rooms she lives in."),
            ("prompt", "When money arrives, her first move is:", 2),
            ("prompt", "Her relationships meet a clear standard, and that standard is:", 2),
            ("fields", ["Her phone is arranged so that",
                        "Her most-lived-in room makes it easy to"]),
            ("prompt", "When something true is hard to say, she says it by:", 2),
            ("prompt", "Before any real decision, the question she runs it through is:", 2),
        ],
    },

    # 4. Identity bridge
    {
        "family": "exercise",
        "section": SECTION,
        "title": "The Identity Bridge",
        "blocks": [
            ("p", "Becoming her is not a demolition. Most of who you are crosses the bridge with you. Name "
                  "what stays, what softens, and what gets practiced until it is second nature."),
            ("pi", "She keeps her warmth. She keeps her humor. She keeps the way she loves her people."),
            ("prompt", "Crossing the bridge, the parts of me that come along untouched are:", 3),
            ("prompt", "The stories and habits that soften and fall behind as I cross are:", 3),
            ("prompt", "Skills she practices until they look effortless from the outside include:", 4),
        ],
    },

    # 5. Evidence log + smallest believable shift
    {
        "family": "exercise",
        "section": SECTION,
        "title": "Proof I Am Already Becoming Her",
        "blocks": [
            ("p", "Identity change gathers speed when it is noticed. Somewhere in the past month you "
                  "already acted like her: kept a boundary, told the truth, finished something quietly. "
                  "Log the evidence; small entries count double here."),
            ("prompt", "Moments from recent weeks, however minor, when I already acted like her:", 7),
            ("h3", "The smallest believable shift"),
            ("p", "Overnight reinvention collapses because your nervous system refuses to sign off on it. "
                  "Choose a shift so small that believing in it takes no effort at all."),
            ("prompt", "The smallest shift I genuinely believe I could make this week is:", 3),
        ],
    },

    # 6. Daily embodiment menu + decision prompt
    {
        "family": "exercise",
        "section": SECTION,
        "title": "The Daily Embodiment Menu",
        "blocks": [
            ("p", "Choose one or two per day, never all of them. Embodiment is a seasoning, not a second "
                  "job."),
            ("check", [
                "Dress for the day she would expect to have",
                "Answer one message with her calm directness",
                "Tidy one surface to her standard",
                "Eat one meal at the pace she eats",
                "Decline one thing she would decline",
                "Put one dollar, or ten, where she would put it",
                "Walk into one room the way she enters rooms",
                "Rest for twenty minutes without earning it first",
                "Speak about yourself the way she would allow",
                "Close the day by naming one vote you cast for her",
            ]),
            ("h3", "Her next move"),
            ("p", "Whenever you are stuck between options, borrow her eyes for a minute. The choice "
                  "usually simplifies."),
            ("prompt", "What would she do next, in the exact situation I am standing in today?", 4),
            ("note", "Keep this question light. It is a lens to look through, not another standard to "
                     "fall short of."),
        ],
    },

    # 7. Letter from the future self
    {
        "family": "exercise",
        "section": SECTION,
        "title": "A Letter From Her",
        "toc": True,
        "blocks": [
            ("p", "Let your future self write back to you. Do not compose; transcribe. Begin with one of "
                  "the starters below, keep the pen moving, and let her be kinder and more matter-of-fact "
                  "than you expect."),
            ("bullets", [
                "Dear you: I am writing from a morning that once seemed unlikely...",
                "The thing I most want to thank you for is...",
                "You will laugh at what became completely normal for us...",
            ]),
            ("linesfill",),
        ],
    },

    # 8. Letter to the future self
    {
        "family": "exercise",
        "section": SECTION,
        "title": "A Letter to Her",
        "blocks": [
            ("p", "Now write in the other direction. This letter is a send-off, not a wish list: tell her "
                  "what you are doing on her behalf, ask her what you have been wanting to know, and make "
                  "her one honest promise."),
            ("bullets", [
                "While you are becoming, I am the one who...",
                "What I hope you remember about this year is...",
                "The promise I am keeping on your behalf is...",
            ]),
            ("linesfill",),
        ],
    },

    # 9. Identity statement + affirmation builder
    {
        "family": "exercise",
        "section": SECTION,
        "title": "The Statement She Lives By",
        "toc": True,
        "blocks": [
            ("p", "An affirmation works when your body does not argue with it. Build yours from the "
                  "identity up, then test it for believability and adjust until it settles."),
            ("prompt", "I am the kind of woman who:", 3),
            ("h3", "Believability check"),
            ("scale", "How true does that sentence feel in my body right now?"),
            ("p", "Anything under a seven needs softening, not forcing. Add 'I am learning to' or 'more "
                  "and more' until the sentence earns a quiet yes, then let it firm up over the weeks."),
            ("prompt", "Adjusted until my body agrees, my working statement is:", 2),
            ("aff", "I keep small promises to myself, and they are adding up."),
        ],
    },

    # 10. Future-self decision filter card
    {
        "family": "reference",
        "section": SECTION,
        "title": "The Future-Self Filter",
        "subtitle": "Three questions before any real choice",
        "blocks": [
            ("p", "Copy these three questions somewhere you actually look: a card in your wallet, a note "
                  "pinned on your phone, the inside cover of your planner. Run any real choice through "
                  "them before you answer."),
            ("kv", [
                ("Direction", "Does this match the woman I am becoming, or only the person I am by default?"),
                ("Motive", "Am I choosing this from self-respect, or from fear of disappointing someone?"),
                ("Horizon", "Will the me who is one year past the gate be glad I decided it this way?"),
            ]),
            ("note", "A filter is not a cage. Some days you will choose comfort anyway; note it kindly "
                     "and keep the card."),
            ("quote", "Decisions are where identity stops being theoretical."),
        ],
    },
]
