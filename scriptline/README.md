# Scriptline

A Next.js app that generates UGC, Instagram, TikTok, and digital-product promo content in your voice — scripts, captions, and upload-ready images.

## What it does

- **4 creator modes** (tabs): UGC Video Creator, Instagram Creator, TikTok Creator, Digital Product Promo — each with its own color system, formats, and voice rules.
- **Prompt Vault**: save any generation setup (mode, format, topic, goal, hook, extra context) plus the copy it produced, then search, tag, favorite, and reload/reuse it any time. Persisted client-side in the browser.
- **Script & copy generation** via the Anthropic API (server-side, key never exposed).
- **Pexels image search** baked in: after generating, the app fetches 3 relevant background images.
- **Visual preview panel** for static formats (Single Feed Post, Carousel, Stories): click an image, see your copy overlaid in bold white text, swipe carousel slides.
- **Download PNG**: renders the image + text overlay to a 1080×1080 (feed) or 1080×1920 (story) PNG, ready to upload directly to Instagram or TikTok.
- For video formats (Reels, TikToks, UGC) the 3 images are shown as labeled B-roll reference thumbnails.

## Using your API keys

There are **two ways** to supply the keys the app needs — pick whichever is easier:

1. **In the app (no setup).** Open the app, click the **⚙️ Settings** button, and paste your
   keys. They're stored only in your browser and used to talk directly to Anthropic / Pexels.
   This is the easiest option and requires no server configuration or redeploy.
2. **As server environment variables** (best if you're the only operator, or want the keys
   set for everyone). See below.

| Key | Where to get it | Needed for |
|---|---|---|
| `ANTHROPIC_API_KEY` | https://platform.claude.com → Billing → API Keys | Generating content (required) |
| `PEXELS_API_KEY` | https://www.pexels.com/api/ (free) | Background image search (optional) |

If a server env var is set it takes precedence; otherwise the app uses the key saved in Settings.

## Selling access with access codes (hosted model)

If you want to host one instance and sell **access** (buyers just open a link and type a code —
no keys or setup on their end), set two server environment variables:

| Env var | What it does |
|---|---|
| `ANTHROPIC_API_KEY` | Your key. The server uses it for everyone, so **you** pay for usage. |
| `ACCESS_CODES` | Comma-separated list of codes, e.g. `sunrise-42,vip-panda,launch-code`. Visitors must enter one to unlock the app. |

How it works:

- When `ACCESS_CODES` is set, visitors see a **lock screen** and must enter a valid code before
  they can generate anything. Codes are matched case-insensitively.
- Give each buyer a code with their purchase (e.g. deliver "link + code" via Etsy/Gumroad).
- To revoke access, remove or change a code in `ACCESS_CODES` and redeploy.
- When `ACCESS_CODES` is **not** set, the gate is off and the app is open (personal use).

The access gate is enforced server-side on every generation request, so it can't be bypassed by
editing the page. (One shared code list — for unique per-buyer codes you'd add a backend.)

## Local setup

```bash
cd scriptline
npm install
cp .env.example .env.local   # optional — or just use the in-app Settings
npm run dev
```

## Deploy to Vercel

1. Import the repo in Vercel and set the **Root Directory** to `scriptline`.
2. Add `ANTHROPIC_API_KEY` and `PEXELS_API_KEY` as environment variables.
3. Deploy.

## Workflow tip — turning scripts into video

The app produces upload-ready **text and images**. For actual video, pair the generated scripts with:

- **HeyGen** — paste the script, your AI avatar films it
- **Creatify / Arcads** — paste script + product URL for UGC-style video
- **CapCut** — film it yourself using the script + B-roll shot list
- **InVideo AI** — faceless videos from scripts
