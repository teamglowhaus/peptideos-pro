# -*- coding: utf-8 -*-
"""Part X continued — The 88 Affirmations: teaching + the complete collection."""

from affirmations import AFFIRMATIONS

SEC = "The 88 Affirmations"

def _aff_pages():
    """Two families per page -> four collection pages."""
    fams = list(AFFIRMATIONS.items())
    pages = []
    for i in range(0, 8, 2):
        (n1, l1), (n2, l2) = fams[i], fams[i + 1]
        pages.append({
            "family": "education", "section": SEC,
            "title": "%s · %s" % (n1, n2), "toc": False, "wash": True,
            "blocks": [
                ("h2", n1), ("cardaff", l1),
                ("h2", n2), ("cardaff", l2),
            ],
        })
    return pages

PAGES = [

{
 "family": "education", "section": SEC, "title": "Eighty-Eight Affirmations That Do Not Lie to You", "toc": True,
 "subtitle": "How to choose one, how to soften one, how to make one yours",
 "blocks": [
    ("p", "An affirmation is not a spell; it is a rehearsal. Repeated often enough, a sentence becomes a lens, and lenses change what you notice and what you attempt. That only works when the sentence is one your nervous system will sign off on. If your shoulders rise when you say it, the sentence is writing checks your body refuses to cash."),
    ("h2", "Choosing"),
    ("p", "Read a family that matches your season and notice which line makes you exhale. Choose that one, even if a shinier one sits beside it. One line, spoken for a week, outworks eleven skimmed once."),
    ("h2", "Softening the unbelievable"),
    ("p", "When a line feels like a costume, walk it back to the edge of believable. I am wealthy becomes I am learning to handle money like a woman who keeps it. I love my body becomes my body and I are renegotiating, kindly. A bridge affirmation names the direction and the practice, not the finished state, and that honesty is what lets you repeat it with a straight face."),
    ("callout", "The believability test", "Say the line aloud once. If your body stays quiet, keep it. If it argues, add one of these hinges: I am learning to... I am becoming someone who... I am practicing... It is getting easier to..."),
    ("h2", "A tiny daily liturgy"),
    ("bullets", [
      "Morning: say your line once before your phone gets a vote. Let it set the day's posture.",
      "Evening: say it again, then name one moment the day gave you that rhymed with it, however small.",
    ]),
 ],
},
]

PAGES += _aff_pages()

PAGES += [
{
 "family": "exercise", "section": SEC, "title": "The Affirmation Builder", "toc": True,
 "subtitle": "Write the line only you could write",
 "blocks": [
    ("p", "The strongest affirmation in this book is the one that is not in this book yet. Build it from your own materials."),
    ("fields", [
      "The belief I am replacing",
      "What I want to be true, stated plainly",
      "The hinge that makes it believable today",
    ]),
    ("prompt", "My line, first draft (present tense, my own vocabulary, no borrowed shine):", 2),
    ("scale", "Believability when I say it aloud"),
    ("prompt", "Softened or sharpened until my body signs off, final version:", 2),
    ("h2", "Put it to work"),
    ("check", [
      "Written where I will see it tomorrow morning",
      "Attached to an existing habit (kettle, commute, skincare)",
      "Paired with one action that gives it evidence this week",
    ]),
    ("note", "Revisit the line every Sunday of this season. As the evidence grows, let the sentence grow with it."),
 ],
},
]
