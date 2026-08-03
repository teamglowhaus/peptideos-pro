# Part V - Desire Clarity
# Content module for The Lion's Gate 8/8 Activation.
# Exports PAGES for the layout engine in lg/engine.py.

SECTION = "Desire Clarity"

PAGES = [

    # 1. Education: why clarity precedes manifestation
    {
        "family": "education",
        "section": SECTION,
        "title": "Wanting on Purpose",
        "subtitle": "Why clarity has to come first",
        "toc": True,
        "wash": True,
        "blocks": [
            ("p", "Manifestation, stripped of its glitter, is a discipline of attention: you get clear about "
                  "what you want, you practice being the woman who could hold it, and you take real steps "
                  "toward it, over and over. Every part of that sequence begins with clarity. A vague wish "
                  "cannot be planned for, practiced, or even recognized when it arrives."),
            ("h2", "Scattered wishes, chosen intentions"),
            ("p", "A scattered wish is reactive. It flares when you scroll past someone else's kitchen, "
                  "promotion, or relationship, and it fades by dinner. A chosen intention is deliberate: you "
                  "have examined it, traced its roots, and decided it belongs to you. The pages ahead exist "
                  "to turn the first kind of wanting into the second."),
            ("h2", "Desire as information"),
            ("p", "Your wants are data. Beneath almost every desire sits a value you hold or a need asking "
                  "to be met. Read this way, even an envious pang becomes useful: it points at something you "
                  "care about and have not yet given yourself full permission to pursue."),
            ("callout", "Before you begin",
                  "Nothing you write in this part is a promise or a prediction. It is an honest map of what "
                  "matters to you in this season, drawn so that your attention and your actions can finally "
                  "agree with each other."),
            ("quote", "Clarity is the first act of self-respect."),
        ],
    },

    # 2. Life-area satisfaction wheel
    {
        "family": "exercise",
        "section": SECTION,
        "title": "The Satisfaction Wheel",
        "blocks": [
            ("p", "Shade each slice from the center outward. A full slice means this area of life already "
                  "feels satisfying; a sliver means it is running on empty. Work quickly and honestly; your "
                  "first instinct is usually the true one."),
            ("wheel", ["Wealth", "Career", "Love", "Confidence", "Home", "Creativity", "Wellness", "Spirit"]),
            ("prompt", "Looking at the shape of my wheel, what catches my eye first is:", 2),
        ],
    },

    # 3. Desire brainstorm + sorting matrix
    {
        "family": "exercise",
        "section": SECTION,
        "title": "The Uncensored List",
        "blocks": [
            ("p", "Set a timer for five minutes and list everything you want. Do not rank, justify, or "
                  "shrink anything. Trivial and enormous belong on the same page: softer mornings, a paid "
                  "invoice, a great love, a bathtub worth lingering in."),
            ("lines", 8),
            ("h3", "Now sort"),
            ("p", "Reread your list slowly and move each item into one of the two columns below. Notice "
                  "which column fills faster; that, too, is information."),
            ("twocol", "Energizing to me", "Expected of me", 6),
        ],
    },

    # 4. Intrinsic vs externally influenced goals
    {
        "family": "exercise",
        "section": SECTION,
        "title": "Whose Desire Is This?",
        "toc": True,
        "blocks": [
            ("p", "Some desires are natively yours. Others were installed by family, algorithms, or an "
                  "older version of you who needed different things. Neither makes you foolish, but only an "
                  "intrinsic want can carry an intention through the long, boring middle of pursuing it."),
            ("callout", "The quiet test",
                  "Imagine you could have the outcome fully, but you could never post it, mention it, or be "
                  "admired for it. If the wanting survives the silence, it is yours."),
            ("prompt", "Would I still want this if no one ever saw it?", 4),
            ("prompt", "The desires on my list that arrived wearing someone else's handwriting are:", 3),
            ("prompt", "One want I am ready to hand back to its original owner is:", 3),
        ],
    },

    # 5. Goal -> feeling -> need
    {
        "family": "exercise",
        "section": SECTION,
        "title": "The Feeling Beneath, the Need Beneath That",
        "blocks": [
            ("p", "Goals are rarely about their objects. The salary, the ring, the finished book: each is a "
                  "delivery mechanism for a feeling, and under the feeling sits a need. Once you can name "
                  "the need, you stop being hostage to one single outcome, because there are usually many "
                  "ways to meet it."),
            ("callout", "A worked example",
                  "Goal: my own small design studio. Feeling underneath: sovereignty, answering to my own "
                  "taste. Need beneath that: self-trust and room to be fully expressed. Notice how many "
                  "paths could feed that need while the studio is still being built."),
            ("prompt", "The goal I am tracing down to its root is:", 2),
            ("prompt", "Underneath that goal, the feeling I keep reaching for is:", 3),
            ("prompt", "Beneath the feeling sits a need; named plainly, my need is:", 2),
            ("prompt", "One way to start feeding that need this week, before the goal arrives, is:", 2),
        ],
    },

    # 6. Values alignment + opportunity cost
    {
        "family": "exercise",
        "section": SECTION,
        "title": "Values and the Cost of Yes",
        "blocks": [
            ("p", "A desire that matches your values feels clean to pursue, even when the pursuit is hard. "
                  "A desire that fights your values leaks energy no matter how impressive it looks. Check "
                  "the fit, then read the price tag honestly: every real yes quietly closes other doors."),
            ("prompt", "The values this desire would let me live out loud are:", 2),
            ("twocol", "Saying yes to this means", "So I am saying no to", 5),
            ("prompt", "Succeeding here will genuinely cost me:", 2),
            ("prompt", "Despite my fears, it will not cost me:", 2),
        ],
    },

    # 7. One-year and three-year visions
    {
        "family": "exercise",
        "section": SECTION,
        "title": "One Year, Three Years",
        "toc": True,
        "blocks": [
            ("p", "Vision work is not prediction; it is rehearsal. You are teaching your attention what to "
                  "look for. Write both scenes in plain, confident detail, reporting rather than hoping."),
            ("h3", "Next August"),
            ("prompt", "It is August of next year and I am catching up with a dear friend; when she asks "
                       "about my year, the stories I tell first are:", 5),
            ("h3", "Three Augusts out"),
            ("prompt", "Three years past this gate, someone meeting me for the first time would never "
                       "guess that I once:", 5),
        ],
    },

    # 8. Ordinary ideal day scripting
    {
        "family": "exercise",
        "section": SECTION,
        "title": "An Ordinary Ideal Day",
        "blocks": [
            ("p", "Not a vacation, not a highlight reel: an unremarkable Tuesday in the life that fits you. "
                  "Ordinary days are where a life actually happens, which makes this the most practical "
                  "vision you will write. Move through the day in order and stay inside your senses: what "
                  "you hear, wear, smell, taste, and touch."),
            ("pi", "Write in the present tense, as if the day is happening now."),
            ("prompt", "My eyes open in that life; the first things I notice, the light, the sounds, the "
                       "feel of the room, are:", 3),
            ("linesfill",),
        ],
    },

    # 9. More-of / less-of + nonnegotiables
    {
        "family": "exercise",
        "section": SECTION,
        "title": "More of This, Less of That",
        "blocks": [
            ("p", "Desire is directional, and direction has two ends. Fill both columns quickly with "
                  "textures, people, obligations, habits, and inputs. Then circle the three entries in each "
                  "column with the strongest pull."),
            ("twocol", "More of this", "Less of that", 7),
            ("h3", "Nonnegotiables"),
            ("p", "Some things are not up for trade while you pursue anything at all. Name yours; they are "
                  "the guardrails around every intention in this book."),
            ("fields", ["Nonnegotiable one", "Nonnegotiable two", "Nonnegotiable three"]),
        ],
    },

    # 10a. Eight focused desire areas, part one
    {
        "family": "exercise",
        "section": SECTION,
        "title": "Eight Areas, One Want Each",
        "blocks": [
            ("p", "One sharp want per area, across this page and the next. Not everything you could want "
                  "there: the single desire with the most heat in it right now."),
            ("h3", "Wealth & financial stability"),
            ("prompt", "Money, handled on my terms, would quietly buy me:", 2),
            ("h3", "Career & business"),
            ("prompt", "Work that deserves the best hours of my day would look like:", 3),
            ("h3", "Love & relationships"),
            ("prompt", "In my closest relationships, the standard I am ready to raise is:", 2),
            ("h3", "Confidence & self-concept"),
            ("prompt", "The woman who enters rooms without shrinking quietly assumes:", 2),
        ],
    },

    # 10b. Eight focused desire areas, part two
    {
        "family": "exercise",
        "section": SECTION,
        "title": "Eight Areas, Continued",
        "blocks": [
            ("pi", "Keep the same rule: one want per area, the one with heat."),
            ("h3", "Home & lifestyle"),
            ("prompt", "A home that is unmistakably mine would feel like:", 3),
            ("h3", "Creativity & purpose"),
            ("prompt", "The project I would still make with no audience at all is:", 2),
            ("h3", "Wellness & energy"),
            ("prompt", "A week that leaves me resourced instead of drained includes:", 3),
            ("h3", "Spiritual connection"),
            ("prompt", "My sense of connection to something larger is strongest when:", 2),
        ],
    },

    # 11. Top-eight selection + final intention
    {
        "family": "exercise",
        "section": SECTION,
        "title": "Eight Desires, One Intention",
        "toc": True,
        "blocks": [
            ("p", "Reread everything you have written in this part. Choose the eight desires with the most "
                  "life in them, one per area if you can, and list them below. Narrowing is not abandoning; "
                  "it is deciding where this season's attention goes."),
            ("fields", ["Desire one", "Desire two", "Desire three", "Desire four",
                        "Desire five", "Desire six", "Desire seven", "Desire eight"]),
            ("h3", "The one you carry to the gate"),
            ("prompt", "Of these eight, the single intention I am bringing to my 8/8 ritual is:", 2),
            ("check", ["It is specific", "It is mine, not borrowed",
                       "It has a feeling I can name", "There is an action attached"]),
            ("aff", "I am allowed to want what I want, out loud and on paper."),
        ],
    },
]
