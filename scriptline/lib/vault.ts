// Client-side Prompt Vault — saves, organizes, and reuses generation setups.
// Persisted to localStorage so saved prompts survive reloads.

import { MODES, type ModeId, type Platform } from "./modes";

const STORAGE_KEY = "scriptline-prompt-vault-v1";
// Older builds stored the vault under these keys; loadVault migrates them forward
// so nobody loses saved prompts when the app is renamed.
const LEGACY_STORAGE_KEYS = ["contentforge-prompt-vault-v1"];

// Tracks whether the most recent write to localStorage succeeded, so the UI can
// warn the user (e.g. storage full) instead of silently losing their data.
let lastWriteOk = true;
export function lastWriteSucceeded(): boolean {
  return lastWriteOk;
}

// A saved prompt captures the full generation setup plus the last output.
export interface VaultPrompt {
  id: string;
  name: string;
  mode: ModeId;
  platform: Platform;
  format: string;
  promoAngle?: string;
  topic: string;
  goal: string;
  hookStyle: string;
  extraContext?: string;
  output?: string;
  tags: string[];
  favorite: boolean;
  createdAt: number;
  updatedAt: number;
}

// The generation-setup fields a saved prompt loads back into the form.
export type VaultSetup = Omit<
  VaultPrompt,
  "id" | "name" | "tags" | "favorite" | "createdAt" | "updatedAt"
>;

function isBrowser(): boolean {
  return typeof window !== "undefined" && !!window.localStorage;
}

// Best-effort unique id without pulling in a dependency.
function makeId(): string {
  if (isBrowser() && "randomUUID" in crypto) return crypto.randomUUID();
  return `p_${Date.now().toString(36)}_${Math.floor(Math.random() * 1e6).toString(36)}`;
}

function readKey(key: string): VaultPrompt[] {
  try {
    const raw = window.localStorage.getItem(key);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) return [];
    return parsed.filter((p): p is VaultPrompt => !!p && typeof p.id === "string");
  } catch {
    return [];
  }
}

export function loadVault(): VaultPrompt[] {
  if (!isBrowser()) return [];
  const current = readKey(STORAGE_KEY);
  if (current.length > 0) return current;
  // One-time migration: pull prompts saved by an older build's key forward.
  for (const legacy of LEGACY_STORAGE_KEYS) {
    const old = readKey(legacy);
    if (old.length > 0) {
      persist(old);
      return old;
    }
  }
  return current;
}

function persist(prompts: VaultPrompt[]): boolean {
  if (!isBrowser()) {
    lastWriteOk = true;
    return true;
  }
  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(prompts));
    lastWriteOk = true;
    return true;
  } catch {
    // storage full or blocked — surface it so the caller can warn the user
    lastWriteOk = false;
    return false;
  }
}

// Add a new saved prompt and return the updated, newest-first list.
export function addPrompt(
  prompts: VaultPrompt[],
  name: string,
  tags: string[],
  setup: VaultSetup,
): VaultPrompt[] {
  const now = Date.now();
  const entry: VaultPrompt = {
    id: makeId(),
    name: name.trim() || "Untitled prompt",
    tags: normalizeTags(tags),
    favorite: false,
    createdAt: now,
    updatedAt: now,
    ...setup,
  };
  const next = [entry, ...prompts];
  persist(next);
  return next;
}

export function updatePrompt(
  prompts: VaultPrompt[],
  id: string,
  patch: Partial<VaultPrompt>,
): VaultPrompt[] {
  const next = prompts.map((p) =>
    p.id === id ? { ...p, ...patch, id: p.id, updatedAt: Date.now() } : p,
  );
  persist(next);
  return next;
}

export function removePrompt(prompts: VaultPrompt[], id: string): VaultPrompt[] {
  const next = prompts.filter((p) => p.id !== id);
  persist(next);
  return next;
}

export function toggleFavorite(prompts: VaultPrompt[], id: string): VaultPrompt[] {
  const next = prompts.map((p) =>
    p.id === id ? { ...p, favorite: !p.favorite, updatedAt: Date.now() } : p,
  );
  persist(next);
  return next;
}

export function normalizeTags(tags: string[]): string[] {
  const seen = new Set<string>();
  const out: string[] = [];
  for (const t of tags) {
    const clean = t.trim().toLowerCase();
    if (clean && !seen.has(clean)) {
      seen.add(clean);
      out.push(clean);
    }
  }
  return out;
}

export function parseTagInput(raw: string): string[] {
  return normalizeTags(raw.split(","));
}

// Every distinct tag across the vault, sorted, for filter chips.
export function allTags(prompts: VaultPrompt[]): string[] {
  const set = new Set<string>();
  for (const p of prompts) for (const t of p.tags) set.add(t);
  return [...set].sort();
}

// Serialize the whole vault into a downloadable backup file.
export function exportVault(prompts: VaultPrompt[]): string {
  return JSON.stringify(prompts, null, 2);
}

// Coerce one untrusted backup entry into a well-formed VaultPrompt, or null if
// it's unusable. Critically, rejects unknown modes — MODES[mode] is read during
// render, so an invalid mode would otherwise crash the whole vault view.
function sanitizePrompt(raw: unknown): VaultPrompt | null {
  if (!raw || typeof raw !== "object") return null;
  const p = raw as Record<string, unknown>;
  if (typeof p.id !== "string" || !p.id) return null;
  if (typeof p.mode !== "string" || !(p.mode in MODES)) return null;
  const now = Date.now();
  const str = (v: unknown, fallback = "") => (typeof v === "string" ? v : fallback);
  return {
    id: p.id,
    name: str(p.name, "Untitled prompt"),
    mode: p.mode as ModeId,
    platform: p.platform === "TikTok" ? "TikTok" : "Instagram",
    format: str(p.format),
    promoAngle: typeof p.promoAngle === "string" ? p.promoAngle : undefined,
    topic: str(p.topic),
    goal: str(p.goal),
    hookStyle: str(p.hookStyle),
    extraContext: typeof p.extraContext === "string" ? p.extraContext : undefined,
    output: typeof p.output === "string" ? p.output : undefined,
    tags: normalizeTags(
      Array.isArray(p.tags) ? (p.tags as unknown[]).filter((t): t is string => typeof t === "string") : [],
    ),
    favorite: p.favorite === true,
    createdAt: typeof p.createdAt === "number" ? p.createdAt : now,
    updatedAt: typeof p.updatedAt === "number" ? p.updatedAt : now,
  };
}

// Merge a backup file into the current vault, skipping ids already present.
// Returns the merged list and how many new prompts were added (or an error).
export function importVault(
  prompts: VaultPrompt[],
  json: string,
): { prompts: VaultPrompt[]; added: number; error?: string } {
  let parsed: unknown;
  try {
    parsed = JSON.parse(json);
  } catch {
    return { prompts, added: 0, error: "That file isn't valid JSON." };
  }
  // Accept either a raw array or a { prompts: [...] } envelope (forward-compat).
  const list = Array.isArray(parsed)
    ? parsed
    : parsed && typeof parsed === "object" && Array.isArray((parsed as { prompts?: unknown }).prompts)
      ? ((parsed as { prompts: unknown[] }).prompts)
      : null;
  if (!list) {
    return { prompts, added: 0, error: "That backup file isn't in the expected format." };
  }

  const existing = new Set(prompts.map((p) => p.id));
  const seen = new Set<string>();
  const incoming: VaultPrompt[] = [];
  for (const raw of list) {
    const clean = sanitizePrompt(raw);
    if (!clean || existing.has(clean.id) || seen.has(clean.id)) continue;
    seen.add(clean.id);
    incoming.push(clean);
  }

  if (incoming.length === 0) {
    return {
      prompts,
      added: 0,
      error: list.length
        ? "No new prompts to import — they're already in your vault, or the file is invalid."
        : "No prompts found in that file.",
    };
  }

  const next = [...incoming, ...prompts];
  if (!persist(next)) {
    return {
      prompts,
      added: 0,
      error:
        "Couldn't save the import — your browser's storage may be full. Export a backup and remove old prompts first.",
    };
  }
  return { prompts: next, added: incoming.length };
}
