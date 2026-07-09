# Scriptline — Setup Guide

From downloaded ZIP to a live, working app in about 15 minutes. No coding
background needed — just copy, paste, and follow along.

## What you'll need

- [ ] **Node.js installed** — the engine that runs the app on your computer. Free, one-time install. (2 min)
- [ ] **A Vercel account** — free hosting, this is where your app actually lives online. (1 min)
- [ ] **An Anthropic API key** — powers the writing. Pay-as-you-go; around $5 covers hundreds of generations. (3 min)
- [ ] **A Pexels API key** — powers the background images. Completely free. (2 min)

## 1. Unzip and open a terminal here

Unzip the file you downloaded. You'll get a folder called `scriptline`.

**Mac:** Right-click the `scriptline` folder → *New Terminal at Folder* (or open Terminal, type `cd `, drag the folder in, press Enter).

**Windows:** Open the `scriptline` folder in File Explorer, click the address bar, type `cmd`, press Enter.

## 2. Install Node.js (skip if you already have it)

```
node -v
```

If you see a version number like `v20.11.0`, skip to step 3. If you see "command not found," install Node from [nodejs.org](https://nodejs.org) (choose the **LTS** version), restart your terminal, and try again.

## 3. Get your Anthropic API key

This is what writes your scripts and captions.

1. Go to [platform.claude.com](https://platform.claude.com) → sign in
2. Left sidebar → **API Keys** → **Create Key** → copy it (starts with `sk-ant-`)
3. Left sidebar → **Billing** → add $5 of credit

> **A Claude chat subscription does not cover this.** The API is billed separately, per generation — a few cents each. $5 lasts a long time.

## 4. Get your free Pexels key

This is what finds background images for your posts.

Go to [pexels.com/api](https://www.pexels.com/api/) → sign up (free) → copy your key.

## 5. Install and deploy

Two ways to get this live — pick one.

**Recommended — deploy from your terminal (fastest, no GitHub needed):**

```bash
npm install
```

```bash
npx vercel login
# opens your browser — log in or create a free Vercel account
```

```bash
npx vercel
# answer the prompts — defaults are correct, just press Enter:
# Set up and deploy? Y
# Link to existing project? N
# Project name? [press Enter]
# Directory? [press Enter]
```

**Alternative — GitHub + Vercel dashboard:** push the folder to a new GitHub repo, then import it at vercel.com/new. Set **Root Directory** in Project Settings to `scriptline`.

## 6. Add your keys and go live

```bash
npx vercel env add ANTHROPIC_API_KEY production
# paste your sk-ant-... key when asked
```

```bash
npx vercel env add PEXELS_API_KEY production
# paste your Pexels key when asked
```

```bash
npx vercel --prod
# builds and deploys your live app — about a minute
```

When it finishes, the terminal prints your live URL — something like `scriptline-yourname.vercel.app`. Open it in your browser.

## You're live 🎬

Pick a mode, type a product or topic, and hit Generate.

## If something goes wrong

**Generation fails with a credit or billing error** — your Anthropic account needs API credit added separately from any Claude subscription. Go to `platform.claude.com → Billing` and add funds.

**Images never load** — double-check your Pexels key has no extra spaces. Re-run `npx vercel env add PEXELS_API_KEY production` to replace it, then `npx vercel --prod` again.

**Terminal says "command not found: npm" or "npx"** — Node.js isn't installed yet, or your terminal needs restarting after install. Revisit step 2.

**I changed something in the code — how do I update the live site?** — save your changes, then run `npx vercel --prod` again from the project folder.

---

See [LICENSE.md](./LICENSE.md) for usage terms.
