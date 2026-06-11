# Marie's Content Generator

A Next.js app that generates UGC, Instagram, TikTok, and SWC course promo content in Marie's voice — scripts, captions, and upload-ready images.

## What it does

- **4 creator modes** (tabs): UGC Video Creator, Instagram Creator, TikTok Creator, SWC Course Promo — each with its own color system, formats, and voice rules.
- **Script & copy generation** via the Anthropic API (server-side, key never exposed).
- **Pexels image search** baked in: after generating, the app fetches 3 relevant background images.
- **Visual preview panel** for static formats (Single Feed Post, Carousel, Stories): click an image, see your copy overlaid in bold white text, swipe carousel slides.
- **Download PNG**: renders the image + text overlay to a 1080×1080 (feed) or 1080×1920 (story) PNG, ready to upload directly to Instagram or TikTok.
- For video formats (Reels, TikToks, UGC) the 3 images are shown as labeled B-roll reference thumbnails.

## Setup

```bash
cd maries-content-generator
npm install
cp .env.example .env.local   # then fill in your keys
npm run dev
```

Required environment variables (server-side only):

| Variable | Where to get it |
|---|---|
| `ANTHROPIC_API_KEY` | https://platform.claude.com |
| `PEXELS_API_KEY` | https://www.pexels.com/api/ (free) |

## Deploy to Vercel

1. Import the repo in Vercel and set the **Root Directory** to `maries-content-generator`.
2. Add `ANTHROPIC_API_KEY` and `PEXELS_API_KEY` as environment variables.
3. Deploy.

## Workflow tip — turning scripts into video

The app produces upload-ready **text and images**. For actual video, pair the generated scripts with:

- **HeyGen** — paste the script, your AI avatar films it
- **Creatify / Arcads** — paste script + product URL for UGC-style video
- **CapCut** — film it yourself using the script + B-roll shot list
- **InVideo AI** — faceless videos from scripts
