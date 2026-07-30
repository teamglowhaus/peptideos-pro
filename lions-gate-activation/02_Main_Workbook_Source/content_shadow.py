"""Part IV: Limiting Beliefs & Shadow Work.

Pages for identifying limiting beliefs, tracing their origins and costs
with compassion, honoring their protective purpose, and building
believable replacement beliefs.
"""

SECTION = "Beliefs & Shadow Work"

PAGES = [
    # ------------------------------------------------------------ 1. education
    {
        "family": "education",
        "section": SECTION,
        "title": "Meeting the Stories That Run You",
        "subtitle": "Limiting beliefs, shadow work, and how to do this gently",
        "toc": True,
        "wash": True,
        "blocks": [
            ("p", "A limiting belief is not a character flaw. It is a conclusion you reached, usually young, from the evidence you had at the time: *love has to be earned, wanting things is dangerous, people like me do not get to rest.* The conclusion once protected you. It may now be steering you."),
            ("h2", "Shadow work, in plain terms"),
            ("p", "In this workbook, shadow work simply means looking at the parts of yourself you usually avoid: the envy, the fear, the old shame, the qualities you tucked away to stay loved. Not to wallow in them, and not to exile them, but to see them clearly enough that they stop driving from the back seat."),
            ("p", "You do this with compassion or you do not do it at all. Self-attack teaches nothing new; it only re-runs the oldest lesson."),
            ("h3", "How this section moves"),
            ("p", "First you will learn to spot your patterns, then trace where they came from, what they have cost and what they were protecting. You will finish by building kinder beliefs you can actually believe."),
            ("callout", "Your boundaries for this work", "You decide how deep to go, and you may stop at any line on any page. If something here touches real trauma, close the workbook and come back when you feel resourced, ideally with support. These pages are reflection, not therapy, and they are not a substitute for care from a licensed professional."),
            ("quote", "What you can name gently, you no longer have to obey."),
        ],
    },
    # ---------------------------------------------------- 2. pattern field guide
    {
        "family": "exercise",
        "section": SECTION,
        "title": "A Field Guide to Familiar Patterns",
        "subtitle": "Old survival strategies wearing everyday clothes",
        "toc": True,
        "blocks": [
            ("p", "Read slowly and put a check in the first column beside every pattern that feels familiar. Most women recognize several; that is a map, not a diagnosis. Your most persistent pattern will be your companion through the rest of this section."),
            ("table",
                ["Me?", "Pattern", "How it often sounds"],
                [
                    ["", "Scarcity", "There is never quite enough, so I must grip."],
                    ["", "Fear of visibility", "If they really see me, I will be judged."],
                    ["", "Fear of success", "If I rise, I will be resented or exposed."],
                    ["", "Fear of failure", "If I try and miss, it proves the worst."],
                    ["", "Unworthiness", "Good things are for other people."],
                    ["", "Overgiving", "I earn my place by pouring myself out."],
                    ["", "Perfectionism", "It cannot go out until it is flawless."],
                    ["", "Procrastination", "I will start when I feel ready. I never do."],
                    ["", "Comparison", "Her progress means I am behind."],
                    ["", "Difficulty receiving", "Help, gifts and praise make me squirm."],
                    ["", "Hyper-independence", "Needing no one is the only safe way."],
                    ["", "People pleasing", "Their comfort comes before my truth."],
                    ["", "Money shame", "I should be further along by now."],
                    ["", "Attachment patterns", "I chase, or I retreat, when love gets close."],
                    ["", "Outgrowing others", "If I change, I will lose my people."],
                    ["", "Becoming someone new", "Who am I if not this story?"],
                ],
                (0.08, 0.26, 0.66)),
            ("prompt", "The pattern that showed up earliest in my life was probably:", 2),
        ],
    },
    # ---------------------------------------------------- 3. trigger-to-belief map
    {
        "family": "exercise",
        "section": SECTION,
        "title": "The Trigger-to-Belief Map",
        "subtitle": "Follow a sting down to its root",
        "blocks": [
            ("p", "Strong reactions are messengers. When a small comment lands like a slap, an old belief has usually been touched. Trace one recent trigger from the outside in."),
            ("callout", "A worked example", "Situation: my sister asked when my shop will finally make real money. Feeling: hot shame, tight chest. Automatic thought: she thinks I am playing pretend. Underlying belief: I am not someone whose work gets taken seriously."),
            ("h3", "Now trace your own"),
            ("fields", ["The situation, in one sentence", "The feeling, and where it sat in my body"]),
            ("prompt", "The automatic thought that ran through my mind:", 2),
            ("prompt", "Underneath that thought, the belief might be:", 2),
            ("h3", "A second round, if another sting comes to mind"),
            ("fields", ["Another situation", "What I felt then"]),
            ("lines", 2),
        ],
    },
    # ------------------------------------- 4. evidence + whose voice is this
    {
        "family": "exercise",
        "section": SECTION,
        "title": "Cross-Examining the Old Belief",
        "subtitle": "Evidence on both sides, and the voice behind it",
        "blocks": [
            ("p", "Put the belief from your map, or the pattern you marked most strongly, on the stand. Beliefs feel like facts right up until you ask them for their sources."),
            ("fields", ["The belief I am examining"]),
            ("twocol", "Evidence that seems to support it", "Evidence it conveniently ignores", 6),
            ("h2", "Whose voice is this?"),
            ("prompt", "When I hear this belief in my head, the voice sounds like (a person, a place, an era):", 2),
            ("prompt", "Where I first learned this conclusion, as best I can trace it:", 3),
        ],
    },
    # ------------------------------------------------- 5. inherited beliefs
    {
        "family": "exercise",
        "section": SECTION,
        "title": "The Beliefs You Inherited",
        "subtitle": "What was handed to you before you could choose",
        "blocks": [
            ("p", "Every family passes down beliefs along with recipes and photographs: about work, love, rest, safety and worth. Some are treasures. Some are burdens misfiled as truths. Listing them is not disloyal; it is how you decide what to keep."),
            ("prompt", "Messages about life I absorbed growing up, spoken or silent:", 4),
            ("h3", "The family money script"),
            ("prompt", "In my childhood home, money was treated as (tight, secret, shameful, easy, complicated):", 2),
            ("prompt", "A money sentence I heard often back then, and how it echoes in my choices now:", 3),
            ("note", "You are allowed to love the people who raised you and still retire the beliefs that no longer fit. Both can be true at once."),
        ],
    },
    # ---------------------------------------------- 6. cost of the old story
    {
        "family": "exercise",
        "section": SECTION,
        "title": "What the Old Story Has Cost",
        "subtitle": "An honest accounting, without blame",
        "toc": True,
        "blocks": [
            ("p", "This page is not about fault. You did the best you could inside the story you were given, and so did most of the people who gave it to you. Naming the cost simply shows you your reasons for choosing differently."),
            ("callout", "If grief shows up here", "Let it. Grieving what a belief has cost is often the exact moment it loses its grip. You are not behind; you are arriving."),
            ("prompt", "Choices I made smaller because this belief was steering:", 2),
            ("prompt", "Asks I swallowed instead of voicing:", 2),
            ("prompt", "Rest and softness I talked myself out of:", 3),
            ("prompt", "Joy I postponed until I felt more deserving:", 3),
        ],
    },
    # ------------------------------------------------ 7. protective purpose
    {
        "family": "exercise",
        "section": SECTION,
        "title": "The Protection It Offered",
        "subtitle": "Every old belief was once a bodyguard",
        "blocks": [
            ("p", "Beliefs persist because they pay. Somewhere along the line, this one kept you safe: from rejection, from disappointment, from standing out in a place where standing out was costly. Before you replace it, acknowledge the job it was doing."),
            ("prompt", "What this belief has been trying to protect me from:", 3),
            ("prompt", "How it once made sense, given what I knew or lived through then:", 3),
            ("h2", "Honoring the past without repeating it"),
            ("p", "Gratitude and goodbye can share a sentence. You can respect the strategy that carried you here and still decline to let it plan your future."),
            ("prompt", "A way I can thank that protective part of me while choosing differently now:", 4),
        ],
    },
    # ------------------------------------------------ 8. believable bridge
    {
        "family": "exercise",
        "section": SECTION,
        "title": "Building the Believable Bridge",
        "subtitle": "From the old line to one you can stand on",
        "toc": True,
        "blocks": [
            ("p", "Fake positivity fails because your nervous system can smell it. Leaping straight from *I am terrible with money* to *wealth flows effortlessly to me* only makes the old belief roll its eyes. A bridge belief is different: one honest step kinder, close enough to reach, true enough to repeat with a straight face."),
            ("steps", [
                ("Name the old line", "Write the belief exactly as it sounds in your head, in its own words."),
                ("Build the bridge", "Draft a replacement that is kinder and still believable. Phrases like *I am learning*, *I am becoming* and *it is possible that* do heavy lifting here."),
                ("Test it in your body", "Say it aloud. If your shoulders drop even slightly, it is close enough. If you cringe, soften it further."),
            ]),
            ("table",
                ["The old line", "A believable bridge"],
                [
                    ["I always give up on things.", "I am learning to finish at a pace I can sustain."],
                    ["Nobody takes my work seriously.", "Some people already do, and I can find more of them."],
                    ["I am bad with money.", "I am becoming a woman who looks at her numbers."],
                ],
                (0.42, 0.58)),
            ("prompt", "The bridge sentence I most want to test this week:", 2),
        ],
    },
    # ------------------------------------------- 9. new working beliefs
    {
        "family": "exercise",
        "section": SECTION,
        "title": "Your New Working Beliefs",
        "subtitle": "Draft three lines you can live inside",
        "blocks": [
            ("p", "Borrow, adapt or ignore the examples below. A working belief is one you are willing to rehearse in ordinary moments: while washing dishes, before sending the email, on the walk home."),
            ("cardaff", [
                "It is possible that things can be easier than they have been.",
                "I can want more and be grateful at the same time.",
                "My needs are information, not an imposition.",
                "I am allowed to be seen while I am still learning.",
                "Every ask I make is practice, whatever the answer.",
            ]),
            ("h3", "Now draft your own"),
            ("twocol", "The old belief", "My kinder, believable replacement", 6),
            ("prompt", "Reading my three new lines back, the one that feels most believable is:", 2),
            ("aff", "I can question an old story without betraying the girl who first believed it."),
        ],
    },
]
