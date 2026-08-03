import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lg import theme, engine

s = theme.spec("letter")
b = engine.Book(s, title="The Lion's Gate 8/8 Activation",
                subtitle="An Eight-Day Manifestation, Self-Concept and Aligned-Action Experience")
engine.make_anchor_hook(b)
b.add({"kind": "cover", "tagline": "Eight days · Eight intentions · One aligned plan"})
b.add({"kind": "toc"})
b.add({"kind": "divider", "num": "I", "title": "Understanding the Lion's Gate",
       "subtitle": "What this date means, where the story comes from, and how to make it your own",
       "motif": "arch", "toc_label": "Part I — Understanding"})
b.add({"family": "education", "section": "Understanding the Lion's Gate", "title": "Why August 8?",
       "blocks": [
           ("p", "In modern spiritual practice, the eighth day of the eighth month is treated as a doorway. Many practitioners associate this window with the star *Sirius*, with Leo season, and with the number eight, which has long symbolized abundance, cycles and renewal."),
           ("h2", "Symbol, not certainty"),
           ("p", "None of this is scientific fact, and this workbook will never pretend otherwise. What the date offers is a **shared moment of attention**, the way a new year or a birthday does."),
           ("callout", "A grounding note", "You do not need to believe anything in particular for this work to be useful. Reflection, clarity and action stand on their own."),
           ("quote", "A symbolic date is simply a door you agree to walk through on purpose."),
           ("bullets", ["Leo season emphasizes courage and visibility", "The number 8 is associated with abundance and balance", "Sirius has been honored in many traditions"]),
       ]})
b.add({"family": "exercise", "section": "Desire Clarity", "title": "The Feeling Beneath the Goal",
       "blocks": [
           ("p", "Choose one desire from your brainstorm and follow it downward. The goal is the surface; the feeling is the root."),
           ("prompt", "The desire I am exploring is:", 2),
           ("prompt", "When I imagine it already present in my life, the feeling underneath is:", 3),
           ("scale", "How available does this feeling seem to me right now?"),
           ("twocol", "What this desire would give me", "What I fear it might cost", 5),
           ("lines", 4),
       ]})
b.add({"family": "exercise", "section": "Desire Clarity", "title": "Life-Area Satisfaction Wheel",
       "blocks": [
           ("p", "Shade each slice from the center outward: the fuller the slice, the more satisfied you feel today. There are no wrong answers, only information."),
           ("wheel", ["Wealth", "Career", "Love", "Confidence", "Home", "Creativity", "Wellness", "Spirit"]),
           ("prompt", "The slice that most wants my attention this season is:", 2),
       ]})
b.add({"family": "day", "section": "The Eight-Day Activation", "title": "",
       "blocks": [
           ("daymark", 1, "Awareness", "August 1 · or whenever your eight days begin"),
           ("p", "Before anything can shift, it helps to see clearly what is actually here. Today is an honest inventory, taken with kindness."),
           ("h2", "Morning grounding"),
           ("p", "Sit somewhere comfortable, breathe slowly for one minute, and name three things that are true about this season of your life."),
           ("prompt", "What is present in my life right now that I have not fully acknowledged?", 4),
           ("aff", "I can look at my life honestly and kindly at the same time."),
           ("check", ["Morning grounding", "Journal prompts", "Embodiment practice", "Evening reflection"]),
       ]})
b.add({"family": "action", "section": "Aligned Action", "title": "First Eight Actions",
       "blocks": [
           ("p", "Small enough to begin, real enough to matter. List eight actions you can complete within thirty days."),
           ("steps", [("Name it", "Write the action as a single, finishable sentence."),
                       ("Schedule it", "Give it a day and a rough time."),
                       ("Shrink it", "If you feel resistance, cut the action in half.")]),
           ("fields", ["Action one", "Action two", "Action three", "Action four"]),
           ("grid", ["Action 1", "Action 2", "Action 3"], ["D1","D2","D3","D4","D5","D6","D7","D8"]),
       ]})
b.add({"family": "meditation", "section": "Guided Meditation", "title": "Through the Golden Gate", "wash": True,
       "blocks": [
           ("p", "Read slowly, or record yourself reading and play it back with your eyes closed. Pause wherever you see a small star."),
           ("quote", "Let your breath arrive before you do."),
           ("p", "Settle into your seat. Feel the places where your body meets what holds it."),
           ("lines", 3),
       ]})
b.add({"kind": "back", "quote": "You are allowed to build a life that fits you.", "brand": "GlowHausDigital"})
n = b.build("/tmp/claude-0/-home-user-peptideos-pro/a1845c3c-b1b4-5807-bd49-43cd11990094/scratchpad/smoke.pdf")
print("pages:", n)
