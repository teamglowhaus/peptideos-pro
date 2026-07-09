import { NextResponse } from "next/server";
import { MODE_IMAGE_KEYWORDS, type ModeId } from "@/lib/modes";

export const maxDuration = 30;

const STOP_WORDS = new Set([
  "the", "a", "an", "and", "or", "for", "with", "my", "your", "our", "of",
  "to", "in", "on", "at", "is", "it", "this", "that", "new", "how", "i",
]);

// Pull 2-3 meaningful keywords out of the product/topic input
function extractKeywords(topic: string): string {
  return topic
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, " ")
    .split(/\s+/)
    .filter((w) => w.length > 2 && !STOP_WORDS.has(w))
    .slice(0, 3)
    .join(" ");
}

export async function POST(req: Request) {
  const apiKey = process.env.PEXELS_API_KEY;
  if (!apiKey) {
    return NextResponse.json(
      { error: "PEXELS_API_KEY is not set on the server." },
      { status: 500 },
    );
  }

  let body: { topic?: string; mode?: ModeId; orientation?: "portrait" | "square" | "landscape" };
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: "Invalid JSON body." }, { status: 400 });
  }

  const topic = body.topic?.trim();
  if (!topic) {
    return NextResponse.json({ error: "topic is required." }, { status: 400 });
  }

  const modeKeywords = body.mode ? MODE_IMAGE_KEYWORDS[body.mode] ?? "" : "";
  const query = `${extractKeywords(topic)} ${modeKeywords}`.trim() || topic;
  const orientation = body.orientation ?? "portrait";

  const url = new URL("https://api.pexels.com/v1/search");
  url.searchParams.set("query", query);
  url.searchParams.set("per_page", "3");
  url.searchParams.set("orientation", orientation);

  try {
    const res = await fetch(url, { headers: { Authorization: apiKey } });
    if (!res.ok) {
      const detail = await res.text().catch(() => "");
      return NextResponse.json(
        { error: `Pexels API error (${res.status}): ${detail || res.statusText}` },
        { status: res.status },
      );
    }
    const data = await res.json();
    const photos = (data.photos ?? []).map(
      (p: {
        id: number;
        alt: string;
        photographer: string;
        url: string;
        src: { large2x: string; large: string; medium: string };
      }) => ({
        id: p.id,
        alt: p.alt,
        photographer: p.photographer,
        pageUrl: p.url,
        full: p.src.large2x || p.src.large,
        preview: p.src.large,
        thumb: p.src.medium,
      }),
    );
    return NextResponse.json({ photos, query });
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
