"""Validate a content module: build it standalone at Letter and Pocket sizes.

Usage: python3 validate_content.py content_desire [content_selfconcept ...]
Renders to scratch PDFs, reports page counts and any crash, checks for banned
phrases and duplicate prompts.
"""
import sys, os, re, importlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lg import theme, engine

BANNED = [
    "embark on a transformative", "unlock your limitless", "step into your highest self",
    "harness cosmic", "quantum leap", "the universe will deliver", "dream life is inevitable",
    "simply believe", "everything happens for a reason", "magnet for millions",
    "fast-paced world", "dive into", "unleash", "take a moment",
]

def texts_of(pages):
    out = []
    def walk(x):
        if isinstance(x, str):
            out.append(x)
        elif isinstance(x, (list, tuple)):
            for y in x:
                walk(y)
        elif isinstance(x, dict):
            for y in x.values():
                walk(y)
    walk(pages)
    return out

def main(names):
    ok = True
    all_prompts = {}
    for name in names:
        mod = importlib.import_module(name)
        pages = mod.PAGES
        texts = texts_of(pages)
        joined = " ||| ".join(texts).lower()
        for b in BANNED:
            if b in joined:
                print(f"[{name}] BANNED PHRASE: {b!r}")
                ok = False
        # duplicate prompts across modules
        for pg in pages:
            for blk in pg.get("blocks", []):
                if blk and blk[0] == "prompt":
                    key = re.sub(r"\W+", " ", blk[1].lower()).strip()
                    if key in all_prompts:
                        print(f"[{name}] DUPLICATE PROMPT (also in {all_prompts[key]}): {blk[1][:60]!r}")
                        ok = False
                    all_prompts[key] = name
        for size in ("letter", "pocket"):
            b = engine.Book(theme.spec(size), title="validate")
            b.extend(pages)
            b.add({"kind": "back", "quote": "test"})
            out = f"/tmp/claude-0/-home-user-peptideos-pro/a1845c3c-b1b4-5807-bd49-43cd11990094/scratchpad/val_{name}_{size}.pdf"
            n = b.build(out)
            print(f"[{name}] {size}: {n} pages -> {out}")
    print("OK" if ok else "PROBLEMS FOUND")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
