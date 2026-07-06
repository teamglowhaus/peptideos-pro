// Client-side Prompt Vault — saves, organizes, and reuses generation setups.
// Persisted to localStorage so Marie's saved prompts survive reloads.

import type { ModeId, Platform } from "./modes";

const STORAGE_KEY = "maries-prompt-vault-v1";

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

export function loadVault(): VaultPrompt[] {
  if (!isBrowser()) return [];
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) return [];
    return parsed.filter((p): p is VaultPrompt => !!p && typeof p.id === "string");
  } catch {
    return [];
  }
}

function persist(prompts: VaultPrompt[]): void {
  if (!isBrowser()) return;
  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(prompts));
  } catch {
    // storage full or blocked — nothing we can do beyond failing silently
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
