// Client-side API-key settings — lets each user paste their own keys instead of
// requiring server-side env vars. Stored only in the user's browser (localStorage)
// and sent per-request to this app's own API routes, which forward them to
// Anthropic / Pexels. Server env vars still work and take precedence.

const STORAGE_KEY = "contentforge-settings-v1";

export interface Settings {
  anthropicKey: string;
  pexelsKey: string;
}

const EMPTY: Settings = { anthropicKey: "", pexelsKey: "" };

function isBrowser(): boolean {
  return typeof window !== "undefined" && !!window.localStorage;
}

export function loadSettings(): Settings {
  if (!isBrowser()) return { ...EMPTY };
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) return { ...EMPTY };
    const parsed = JSON.parse(raw);
    return {
      anthropicKey: typeof parsed?.anthropicKey === "string" ? parsed.anthropicKey : "",
      pexelsKey: typeof parsed?.pexelsKey === "string" ? parsed.pexelsKey : "",
    };
  } catch {
    return { ...EMPTY };
  }
}

export function saveSettings(settings: Settings): boolean {
  if (!isBrowser()) return false;
  try {
    window.localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify({
        anthropicKey: settings.anthropicKey.trim(),
        pexelsKey: settings.pexelsKey.trim(),
      }),
    );
    return true;
  } catch {
    return false;
  }
}

export function clearSettings(): void {
  if (!isBrowser()) return;
  try {
    window.localStorage.removeItem(STORAGE_KEY);
  } catch {
    // ignore
  }
}
