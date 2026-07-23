#!/usr/bin/env python3
"""Build the 10–15s Etsy flip-through video.

Silent flip-through of vault pages ending on the before/after listing image,
with one on-screen caption line (per Optimization Kit section 5).
Pipeline: render frame HTMLs -> screenshot at 1440x1080 (render_frames.mjs)
          -> h264 mp4 via imageio-ffmpeg (this script, --encode).
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FRAMES = os.path.join(HERE, "video_frames")
DIST = os.path.join(HERE, "..", "dist")
CAPTION = "108 prompts that make AI actually work for you."

# (source image, seconds on screen)
PAGE_SEQ = [(1, 1.6), (3, 0.8), (5, 0.8), (6, 0.9), (7, 1.0), (13, 0.8), (25, 0.8),
            (30, 1.0), (37, 0.8), (41, 0.8), (44, 0.9), (46, 1.0)]
FINAL_HOLD = 3.2  # before/after image

FRAME_CSS = """
@font-face { font-family:'Space Mono'; font-weight:700;
  src:url('../../assets/fonts/spacemono-700.woff2') format('woff2'); }
*{ margin:0; padding:0; box-sizing:border-box; }
body{ width:1440px; height:1080px; background:#0b0b11; overflow:hidden; position:relative; }
.stage{ position:absolute; top:24px; bottom:110px; left:0; right:0;
  display:flex; align-items:center; justify-content:center; }
.stage img{ max-height:100%; max-width:92%; border-radius:8px;
  box-shadow:0 30px 80px rgba(0,0,0,.8); }
.stage img.full{ max-width:100%; border-radius:0; box-shadow:none; }
.caption{ position:absolute; left:0; right:0; bottom:0; height:110px; background:#0b0b11;
  display:flex; align-items:center; justify-content:center; font-family:'Space Mono',monospace;
  font-weight:700; font-size:30px; color:#c6ff00; letter-spacing:.06em; border-top:4px solid #c6ff00; }
"""


def write_frames():
    os.makedirs(FRAMES, exist_ok=True)
    os.makedirs(os.path.join(HERE, "pagepng"), exist_ok=True)
    # make sure every needed page png exists
    import fitz
    doc = fitz.open(os.path.join(DIST, "Claude_Prompt_Vault_108_Prompts.pdf"))
    for n, _ in PAGE_SEQ:
        out = os.path.join(HERE, "pagepng", f"p{n:02d}.png")
        if not os.path.exists(out):
            doc[n - 1].get_pixmap(dpi=150).save(out)

    specs = [(f"f{i:02d}.html", f"../pagepng/p{n:02d}.png", "")
             for i, (n, _) in enumerate(PAGE_SEQ)]
    specs.append((f"f{len(PAGE_SEQ):02d}.html", "../../dist/etsy/02_before_after.png", "full"))
    for name, img, cls in specs:
        with open(os.path.join(FRAMES, name), "w") as f:
            f.write(f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{FRAME_CSS}</style></head>
<body><div class="stage"><img class="{cls}" src="{img}"></div>
<div class="caption">{CAPTION}</div></body></html>""")
    print(f"wrote {len(specs)} frame html files")


def encode():
    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    durations = [d for _, d in PAGE_SEQ] + [FINAL_HOLD]
    concat = os.path.join(FRAMES, "concat.txt")
    with open(concat, "w") as f:
        for i, d in enumerate(durations):
            f.write(f"file 'f{i:02d}.png'\nduration {d}\n")
        f.write(f"file 'f{len(durations)-1:02d}.png'\n")  # concat demuxer quirk: repeat last
    out = os.path.join(DIST, "etsy", "video_flipthrough.mp4")
    subprocess.run([ff, "-y", "-f", "concat", "-safe", "0", "-i", concat,
                    "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-preset", "medium",
                    "-crf", "18", "-movflags", "+faststart", out], check=True)
    total = sum(durations)
    print(f"wrote {out} ({total:.1f}s)")


if __name__ == "__main__":
    if "--encode" in sys.argv:
        encode()
    else:
        write_frames()
