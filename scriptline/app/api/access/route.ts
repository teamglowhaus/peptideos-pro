import { NextResponse } from "next/server";
import { accessGateEnabled, isValidAccessCode } from "@/lib/access";

// Tells the client whether an access code is required, and (if a code is sent)
// whether it's valid. Only returns booleans — never the codes themselves.
export async function POST(req: Request) {
  let body: { code?: string } = {};
  try {
    body = await req.json();
  } catch {
    // no body → treat as an empty code
  }
  const required = accessGateEnabled();
  const valid = required ? isValidAccessCode(body.code) : true;
  return NextResponse.json({ required, valid });
}
