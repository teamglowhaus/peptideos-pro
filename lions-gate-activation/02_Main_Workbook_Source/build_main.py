# -*- coding: utf-8 -*-
"""Build the four main workbook editions (US Letter, A4, Digital Letter, Digital A4)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lg import theme, engine

import content_front, content_orientation, content_understanding
import content_clearing, content_shadow, content_desire, content_selfconcept
import content_days1, content_days2, content_rituals, content_meditation
import content_scripting, content_abundance, content_love
import content_tarot, content_crystals, content_vision, content_affirm
import content_action, content_integration, content_reference

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TITLE = "The Lion's Gate 8/8 Activation"
SUBTITLE = "An Eight-Day Manifestation, Self-Concept and Aligned-Action Experience"

def divider(num, title, subtitle, motif, seed):
    return {"kind": "divider", "num": num, "title": title, "subtitle": subtitle,
            "motif": motif, "seed": seed, "toc_label": "Part %s · %s" % (num, title)}

def assemble():
    pages = []
    pages.append({"kind": "cover", "tagline": "Eight days · Eight intentions · One aligned plan"})
    fm = list(content_front.PAGES)
    pages.extend(fm[:8])                     # title ... format guidance
    pages.append({"kind": "toc"})            # contents
    pages.extend(fm[8:])                     # ownership, beginning check-in

    pages.append(divider("I", "Welcome & Orientation",
        "Choosing your path, gathering what you need, and arriving on purpose", "sun", 11))
    pages.extend(content_orientation.PAGES)

    pages.append(divider("II", "Understanding the Lion's Gate",
        "The stars, the eights, the stories, and what is honestly yours to keep", "arch", 12))
    pages.extend(content_understanding.PAGES)

    pages.append(divider("III", "Preparation & Clearing",
        "Making room, closing loops, and setting down what this season will not need", "botanical", 13))
    pages.extend(content_clearing.PAGES)

    pages.append(divider("IV", "Limiting Beliefs & Shadow Work",
        "Meeting the old stories with compassion, and choosing what replaces them", "moon", 14))
    pages.extend(content_shadow.PAGES)

    pages.append(divider("V", "Desire Clarity",
        "From scattered wishes to one intention you can say without flinching", "star", 15))
    pages.extend(content_desire.PAGES)

    pages.append(divider("VI", "Self-Concept & the Future Self",
        "The quiet engine underneath outcomes, and how to practice being her now", "constellation", 16))
    pages.extend(content_selfconcept.PAGES)

    pages.append(divider("VII", "The Eight-Day Activation",
        "Awareness, Release, Worthiness, Courage, Clarity, Embodiment, Action, Activation", "lion", 17))
    pages.extend(content_days1.PAGES)
    pages.extend(content_days2.PAGES)

    pages.append(divider("VIII", "The 8/8 Rituals & Meditation",
        "Three complete rituals, six adaptations, and a journey through the golden gate", "geometry", 18))
    pages.extend(content_rituals.PAGES)
    pages.extend(content_meditation.PAGES)

    pages.append(divider("IX", "Scripting, Abundance & Love",
        "Writing it real, money with clear eyes, and love without puppet strings", "infinity", 19))
    pages.extend(content_scripting.PAGES)
    pages.extend(content_abundance.PAGES)
    pages.extend(content_love.PAGES)

    pages.append(divider("X", "Reflective Tools",
        "Tarot spreads, crystals and symbols, vision work, and the 88 affirmations", "sun", 20))
    pages.extend(content_tarot.PAGES)
    pages.extend(content_crystals.PAGES)
    pages.extend(content_vision.PAGES)
    pages.extend(content_affirm.PAGES)

    pages.append(divider("XI", "The Aligned Action Plan",
        "Where intention meets calendar, kindly and on purpose", "star", 21))
    pages.extend(content_action.PAGES)

    pages.append(divider("XII", "Integration & Quick Reference",
        "The thirty days after the portal, and the whole system at a glance", "moon", 22))
    pages.extend(content_integration.PAGES)
    pages.extend(content_reference.PAGES)

    pages.append({"kind": "back",
                  "quote": "You did not wait for a door. You built one, and walked.",
                  "brand": "GlowHausDigital"})
    return pages

BUILDS = [
    ("letter",         os.path.join(ROOT, "03_Main_Workbook_PDFs", "Lions_Gate_Activation_US_Letter.pdf")),
    ("a4",             os.path.join(ROOT, "03_Main_Workbook_PDFs", "Lions_Gate_Activation_A4.pdf")),
    ("letter_digital", os.path.join(ROOT, "04_Digital_Editions", "Lions_Gate_Activation_Digital_US_Letter.pdf")),
    ("a4_digital",     os.path.join(ROOT, "04_Digital_Editions", "Lions_Gate_Activation_Digital_A4.pdf")),
]

if __name__ == "__main__":
    only = sys.argv[1:] or None
    for key, path in BUILDS:
        if only and key not in only:
            continue
        book = engine.Book(theme.spec(key), title=TITLE, subtitle=SUBTITLE)
        engine.make_anchor_hook(book)
        book.extend(assemble())
        n = book.build(path)
        print("%-16s %3d pages  %s" % (key, n, os.path.basename(path)))
