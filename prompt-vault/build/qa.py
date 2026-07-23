#!/usr/bin/env python3
"""QA pass for the vault relaunch (handoff brief, Step 5). Writes dist/QA_REPORT.md."""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, "..", "dist")
sys.path.insert(0, HERE)

import fitz  # PyMuPDF
import vault_data as v

results = []


def check(name, ok, detail=""):
    results.append((name, ok, detail))
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail else ""))


# ---- PDF ----
pdf_path = os.path.join(DIST, "Claude_Prompt_Vault_108_Prompts.pdf")
doc = fitz.open(pdf_path)
text = "\n".join(p.get_text() for p in doc)

check("PDF page count is 48", doc.page_count == 48, f"got {doc.page_count}")
check("PDF page size is US Letter", abs(doc[0].rect.width - 612) < 1 and abs(doc[0].rect.height - 792) < 1)

nums = sorted(set(int(m) for m in re.findall(r"#(\d{3})\b", text)))
check("108 numbered prompt boxes (#001–#108)", nums == list(range(1, 109)),
      f"found {len(nums)} unique, min {nums[0] if nums else '-'}, max {nums[-1] if nums else '-'}")

utw = len(re.findall(r"USE THIS WHEN:", text))
check("USE THIS WHEN tag on every prompt box (108)", utw >= 108, f"found {utw} occurrences")

for i in range(12):
    lo = i * 9 + 1
    sec_nums = [n for n in nums if lo <= n <= lo + 8]
    if len(sec_nums) != 9:
        check(f"Section {i+1} has 9 prompts", False, f"found {len(sec_nums)}")
        break
else:
    check("All 12 sections have exactly 9 prompts", True)

placeholder = "[ADD YOUR GOOGLE DOC LINK]" in text
check("Companion-doc link is set (no placeholder)", not placeholder,
      "placeholder still present — rebuild with: python3 build_vault.py --companion-url <link> && node render_pdf.mjs"
      if placeholder else "")

# every prompt body present verbatim (whitespace-normalized)
flat = re.sub(r"\s+", " ", text)
missing = [n for n, t, u, b in v.PROMPTS if re.sub(r"\s+", " ", b)[:60] not in flat]
check("All 108 prompt bodies present verbatim", not missing, f"missing: {missing[:5]}" if missing else "")

# ---- Companion doc ----
try:
    import docx
    cdoc = docx.Document(os.path.join(DIST, "Claude_Prompt_Vault_Companion_Doc.docx"))
    paras = [p.text for p in cdoc.paragraphs]
    titles = [p for p in paras if re.match(r"^\d{3} — ", p)]
    check("Companion doc has 108 numbered prompts", len(titles) == 108, f"got {len(titles)}")
    check("Companion doc has 12 section headers",
          sum(1 for p in paras if p.startswith("SECTION ")) == 12)
    check("Companion doc has no manual line breaks in prompts",
          not any("\n" in p or "\x0b" in p for p in paras))
except ImportError:
    check("Companion doc checks", False, "python-docx not installed (pip3 install python-docx)")

# ---- Images ----
try:
    from PIL import Image
    expected = ["01_hero", "02_before_after", "03_whats_inside", "04_page_spread",
                "05_click_to_copy", "06_hidden_tease", "07_who_for", "08_how_it_works",
                "09_cheat_sheet", "10_value_stack"]
    bad = []
    for name in expected:
        p = os.path.join(DIST, "etsy", name + ".png")
        if not os.path.exists(p):
            bad.append(name + " missing")
            continue
        w, h = Image.open(p).size
        if (w, h) != (2700, 2025):
            bad.append(f"{name} is {w}x{h}")
    check("10 listing images present at 2700x2025", not bad, "; ".join(bad))
    check("Hero thumbnail QA preview exists",
          os.path.exists(os.path.join(DIST, "etsy", "qa_hero_thumbnail_570px.png")))
except ImportError:
    check("Image checks", False, "pillow not installed (pip3 install pillow)")

# ---- Video ----
vid = os.path.join(DIST, "etsy", "video_flipthrough.mp4")
check("Flip-through video exists", os.path.exists(vid),
      f"{os.path.getsize(vid)//1024} KB" if os.path.exists(vid) else "")

# ---- Report ----
ok = all(r[1] for r in results)
lines = ["# QA Report — Claude Prompt Vault Relaunch", "",
         f"Overall: {'ALL CHECKS PASS' if ok else 'FAILURES PRESENT — see below'}", ""]
for name, passed, detail in results:
    lines.append(f"- [{'x' if passed else ' '}] {'PASS' if passed else 'FAIL'} — {name}"
                 + (f" ({detail})" if detail else ""))
lines += ["", "Manual checks that cannot be automated:",
          "- Companion Google Doc created, shared as 'anyone with link can view', copy-paste tested on mobile",
          "- PDF rebuilt with the real companion link before uploading to Etsy",
          "- Title/description proofread on the live listing",
          "- Images previewed at Etsy thumbnail size (see dist/etsy/qa_hero_thumbnail_570px.png)"]
with open(os.path.join(DIST, "QA_REPORT.md"), "w") as f:
    f.write("\n".join(lines) + "\n")
print("\nwrote dist/QA_REPORT.md")
sys.exit(0 if ok else 1)
