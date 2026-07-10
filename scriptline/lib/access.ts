// Server-side access gate.
//
// When the ACCESS_CODES env var is set (a comma-separated list), visitors must
// enter one of those codes before they can generate. This lets a seller host a
// single instance, put their own ANTHROPIC_API_KEY on the server (so they pay
// for usage), and hand each buyer a code — buyers just type the code and go, no
// keys or setup on their end.
//
// When ACCESS_CODES is unset, the gate is OFF and the app is open (useful for
// personal use or when each user brings their own key).

export function accessGateEnabled(): boolean {
  return !!process.env.ACCESS_CODES?.trim();
}

function validCodes(): string[] {
  const raw = process.env.ACCESS_CODES?.trim();
  if (!raw) return [];
  return raw
    .split(",")
    .map((c) => c.trim().toLowerCase())
    .filter(Boolean);
}

// Codes are matched case-insensitively so buyers don't get tripped up by caps.
export function isValidAccessCode(code: string | undefined | null): boolean {
  const codes = validCodes();
  if (codes.length === 0) return true; // no gate configured → allow everyone
  if (!code) return false;
  return codes.includes(code.trim().toLowerCase());
}
