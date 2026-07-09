// Shared config for Scriptline — used by both the UI and API routes.

export type ModeId = "ugc" | "instagram" | "tiktok" | "swc";
export type Platform = "Instagram" | "TikTok";

export interface ModeTheme {
  bg: string;
  panel: string;
  accent: string;
  accent2: string;
  text: string;
}

export interface ModeConfig {
  id: ModeId;
  label: string;
  tagline: string;
  theme: ModeTheme;
  formatLabel: string;
  formats: string[];
}

export const INSTAGRAM_FORMATS = [
  "Reel 15-30s",
  "Reel 60-90s",
  "Reel 3-5 min",
  "Carousel (slide by slide)",
  "Single Feed Post",
  "Story Series 3-part",
  "Story Poll / Quiz",
  "Talking Head Reel",
  "GRWM Reel",
  "Collab Post",
  "UGC Ad Creative",
  "Broadcast Channel message",
];

export const TIKTOK_FORMATS = [
  "Hook & Scroll (15-30s)",
  "Storytime (60-90s)",
  "Talking Head",
  "Voiceover / Faceless",
  "Stitch or Duet Reply",
  "TikTok UGC Ad",
  "Day in My Life POV",
  "Tutorial / How-To",
  "Text Overlay Trend",
  "Green Screen",
  "TikTok Live outline",
  "Series Part (episode style)",
  "Trending Audio concept",
];

export const UGC_STYLES = [
  "Unboxing / First Reaction",
  "Honest Review (30-60s)",
  "Before & After",
  "Testimonial Style",
  "Product Demo / How-To",
  "GRWM featuring product",
  "POV: I tried this so you don't have to",
  "Aesthetic / Vibe only (no talking)",
  "Talking Head Ad (direct to camera)",
  "Skit / Funny concept",
];

export const SWC_ANGLES = [
  "I bought this and here's what's inside",
  "How I'm making money between night shifts",
  "Digital products explained for beginners",
  "You don't need to make it from scratch",
  "PLR / done-for-you products explainer",
  "This is how I'd start over if I lost everything",
  "No face no followers no problem",
  "What I wish I knew before I started",
  "Real talk: is this course worth it?",
  "Storytime: how I found this",
];

export const GOALS = [
  "Drive sales",
  "Build trust",
  "Entertain & go viral",
  "Product demo",
  "Testimonial",
  "Awareness",
];

export const HOOK_STYLES = [
  "Problem-pain",
  "Controversial take",
  "Nobody talks about this",
  "Before & after",
  "Hot take",
  "POV format",
  "I tested this so you don't have to",
  "Number hook (3 reasons...)",
  "Storytime opener",
  "Silent visual hook",
];

export const MODES: Record<ModeId, ModeConfig> = {
  ugc: {
    id: "ugc",
    label: "UGC Video Creator",
    tagline: "Real content for brands you genuinely use",
    theme: {
      bg: "#1a1015",
      panel: "#241620",
      accent: "#E066A0",
      accent2: "#fce4ec",
      text: "#fce4ec",
    },
    formatLabel: "UGC Style",
    formats: UGC_STYLES,
  },
  instagram: {
    id: "instagram",
    label: "Instagram Creator",
    tagline: "Platform-native IG energy",
    theme: {
      bg: "#0d0d1a",
      panel: "#161629",
      accent: "#9B59B6",
      accent2: "#E066A0",
      text: "#ece8f5",
    },
    formatLabel: "Format",
    formats: INSTAGRAM_FORMATS,
  },
  tiktok: {
    id: "tiktok",
    label: "TikTok Creator",
    tagline: "FYP rhythm, not a marketing deck",
    theme: {
      bg: "#0d0d0d",
      panel: "#181818",
      accent: "#69C9D0",
      accent2: "#EE1D52",
      text: "#f0f0f0",
    },
    formatLabel: "Format",
    formats: TIKTOK_FORMATS,
  },
  swc: {
    id: "swc",
    label: "Digital Product Promo",
    tagline: "Real been-there honesty, never hype",
    theme: {
      bg: "#0d1117",
      panel: "#1a2332",
      accent: "#F0C040",
      accent2: "#e8d9a0",
      text: "#ece4d0",
    },
    formatLabel: "Format",
    formats: [], // resolved from the selected platform
  },
};

// Formats that get a static-post visual preview (image + text overlay + download)
const STATIC_FORMATS = [
  "Single Feed Post",
  "Carousel (slide by slide)",
  "Story Series 3-part",
  "Story Poll / Quiz",
];

export function isStaticFormat(format: string): boolean {
  return STATIC_FORMATS.includes(format);
}

export function isStoryFormat(format: string): boolean {
  return format.startsWith("Story");
}

export function isCarouselFormat(format: string): boolean {
  return format.startsWith("Carousel");
}

// 9:16 vertical for stories and all TikTok content, square for feed/carousel
export function imageOrientation(mode: ModeId, platform: Platform, format: string): "portrait" | "square" {
  if (isStoryFormat(format)) return "portrait";
  if (isStaticFormat(format)) return "square";
  if (mode === "tiktok" || (mode === "swc" && platform === "TikTok")) return "portrait";
  return "portrait"; // video b-roll reference defaults to vertical
}

// Mode context keywords appended to the Pexels search
export const MODE_IMAGE_KEYWORDS: Record<ModeId, string> = {
  ugc: "lifestyle product aesthetic",
  instagram: "aesthetic lifestyle",
  tiktok: "candid lifestyle",
  swc: "laptop workspace hustle night",
};
