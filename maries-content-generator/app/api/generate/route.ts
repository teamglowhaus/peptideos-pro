import Anthropic from "@anthropic-ai/sdk";
import { NextResponse } from "next/server";
import { buildSystemPrompt, buildUserPrompt, type GenerateParams } from "@/lib/prompts";
import { MODES, type ModeId } from "@/lib/modes";

export const maxDuration = 60;

export async function POST(req: Request) {
  if (!process.env.ANTHROPIC_API_KEY) {
    return NextResponse.json(
      { error: "ANTHROPIC_API_KEY is not set on the server." },
      { status: 500 },
    );
  }
  const client = new Anthropic(); // reads ANTHROPIC_API_KEY server-side

  let params: GenerateParams;
  try {
    params = await req.json();
  } catch {
    return NextResponse.json({ error: "Invalid JSON body." }, { status: 400 });
  }

  if (!params.topic?.trim()) {
    return NextResponse.json({ error: "Product or topic is required." }, { status: 400 });
  }
  if (!MODES[params.mode as ModeId]) {
    return NextResponse.json({ error: `Unknown mode: ${params.mode}` }, { status: 400 });
  }

  try {
    const response = await client.messages.create({
      model: "claude-opus-4-8",
      max_tokens: 4096,
      system: buildSystemPrompt(params),
      messages: [{ role: "user", content: buildUserPrompt(params) }],
    });

    const text = response.content
      .filter((b): b is Anthropic.TextBlock => b.type === "text")
      .map((b) => b.text)
      .join("\n");

    return NextResponse.json({ content: text });
  } catch (error) {
    if (error instanceof Anthropic.APIError) {
      return NextResponse.json(
        { error: `Anthropic API error (${error.status}): ${error.message}` },
        { status: error.status ?? 500 },
      );
    }
    const message = error instanceof Error ? error.message : String(error);
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
