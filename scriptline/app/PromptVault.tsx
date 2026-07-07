"use client";

import { useMemo, useRef, useState } from "react";
import { MODES } from "@/lib/modes";
import { allTags, parseTagInput, type VaultPrompt } from "@/lib/vault";

interface Props {
  prompts: VaultPrompt[];
  onLoad: (prompt: VaultPrompt) => void;
  onDelete: (id: string) => void;
  onToggleFavorite: (id: string) => void;
  onUpdate: (id: string, patch: { name: string; tags: string[] }) => void;
  onStartCreating: () => void;
  onExport: () => void;
  onImport: (text: string) => { added: number; error?: string };
}

type ModeFilter = "all" | "favorites" | keyof typeof MODES;

function timeAgo(ts: number): string {
  const diff = Date.now() - ts;
  const mins = Math.round(diff / 60000);
  if (mins < 1) return "just now";
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.round(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  const days = Math.round(hrs / 24);
  if (days < 30) return `${days}d ago`;
  const months = Math.round(days / 30);
  return `${months}mo ago`;
}

function firstLine(output?: string): string {
  if (!output) return "";
  const line = output.split("\n").find((l) => l.trim() && !/^[A-Z][A-Z0-9 &/'\-]{2,}:/.test(l));
  return (line ?? output.split("\n").find((l) => l.trim()) ?? "").trim();
}

export default function PromptVault({
  prompts,
  onLoad,
  onDelete,
  onToggleFavorite,
  onUpdate,
  onStartCreating,
  onExport,
  onImport,
}: Props) {
  const [query, setQuery] = useState("");
  const [modeFilter, setModeFilter] = useState<ModeFilter>("all");
  const [tagFilter, setTagFilter] = useState<string | null>(null);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editName, setEditName] = useState("");
  const [editTags, setEditTags] = useState("");
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const [importNote, setImportNote] = useState("");
  const fileInputRef = useRef<HTMLInputElement>(null);

  const tags = useMemo(() => allTags(prompts), [prompts]);

  async function handleImportFile(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    e.target.value = ""; // allow re-importing the same file later
    if (!file) return;
    try {
      const text = await file.text();
      const res = onImport(text);
      setImportNote(
        res.error
          ? res.error
          : `Imported ${res.added} prompt${res.added === 1 ? "" : "s"}.`,
      );
    } catch {
      setImportNote("Couldn't read that file.");
    }
    setTimeout(() => setImportNote(""), 4000);
  }

  const backupBar = (
    <div className="vault-backup">
      <input
        ref={fileInputRef}
        type="file"
        accept="application/json,.json"
        onChange={handleImportFile}
        style={{ display: "none" }}
      />
      {prompts.length > 0 && (
        <button className="btn btn-ghost" onClick={onExport}>
          ⬇ Export backup
        </button>
      )}
      <button className="btn btn-ghost" onClick={() => fileInputRef.current?.click()}>
        ⬆ Import backup
      </button>
      {importNote && <span className="vault-import-note">{importNote}</span>}
    </div>
  );

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return prompts
      .filter((p) => {
        if (modeFilter === "favorites") return p.favorite;
        if (modeFilter !== "all") return p.mode === modeFilter;
        return true;
      })
      .filter((p) => (tagFilter ? p.tags.includes(tagFilter) : true))
      .filter((p) => {
        if (!q) return true;
        const haystack = [p.name, p.topic, p.format, p.extraContext ?? "", p.output ?? "", ...p.tags]
          .join(" ")
          .toLowerCase();
        return haystack.includes(q);
      })
      .sort((a, b) => {
        if (a.favorite !== b.favorite) return a.favorite ? -1 : 1;
        return b.updatedAt - a.updatedAt;
      });
  }, [prompts, query, modeFilter, tagFilter]);

  function startEdit(p: VaultPrompt) {
    setEditingId(p.id);
    setEditName(p.name);
    setEditTags(p.tags.join(", "));
  }

  function saveEdit(id: string) {
    onUpdate(id, { name: editName, tags: parseTagInput(editTags) });
    setEditingId(null);
  }

  async function copyOutput(p: VaultPrompt) {
    if (!p.output) return;
    await navigator.clipboard.writeText(p.output);
    setCopiedId(p.id);
    setTimeout(() => setCopiedId((c) => (c === p.id ? null : c)), 1600);
  }

  if (prompts.length === 0) {
    return (
      <div className="panel vault-empty">
        <div className="vault-empty-icon">📥</div>
        <h2>Your Prompt Vault is empty</h2>
        <p>
          Generate some content, then hit <b>Save to Vault</b> to stash the setup here. Saved
          prompts remember the mode, format, topic, and the copy you generated — so you can reload
          and reuse them any time.
        </p>
        <button className="btn btn-primary vault-empty-btn" onClick={onStartCreating}>
          Create your first one
        </button>
        <div className="vault-empty-backup">{backupBar}</div>
      </div>
    );
  }

  const MODE_KEYS = Object.keys(MODES) as (keyof typeof MODES)[];

  return (
    <div className="panel">
      {backupBar}
      <div className="vault-controls">
        <input
          className="vault-search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="🔎 Search saved prompts by name, topic, tag, or copy…"
        />
        <div className="vault-filters">
          <button
            className={`chip ${modeFilter === "all" ? "active" : ""}`}
            onClick={() => setModeFilter("all")}
          >
            All ({prompts.length})
          </button>
          <button
            className={`chip ${modeFilter === "favorites" ? "active" : ""}`}
            onClick={() => setModeFilter("favorites")}
          >
            ★ Favorites
          </button>
          {MODE_KEYS.map((id) => (
            <button
              key={id}
              className={`chip ${modeFilter === id ? "active" : ""}`}
              onClick={() => setModeFilter(id)}
            >
              {MODES[id].label}
            </button>
          ))}
        </div>
        {tags.length > 0 && (
          <div className="vault-filters vault-tagrow">
            <span className="vault-tagrow-label">Tags:</span>
            {tags.map((t) => (
              <button
                key={t}
                className={`chip chip-tag ${tagFilter === t ? "active" : ""}`}
                onClick={() => setTagFilter((cur) => (cur === t ? null : t))}
              >
                #{t}
              </button>
            ))}
          </div>
        )}
      </div>

      {filtered.length === 0 ? (
        <p className="vault-noresults">No saved prompts match those filters.</p>
      ) : (
        <div className="vault-grid">
          {filtered.map((p) => {
            const theme = MODES[p.mode].theme;
            const preview = firstLine(p.output);
            const isEditing = editingId === p.id;
            return (
              <div className="vault-card" key={p.id}>
                <div className="vault-card-top">
                  <span
                    className="vault-badge"
                    style={{ background: theme.accent, color: "#fff" }}
                  >
                    {MODES[p.mode].label}
                  </span>
                  <button
                    className={`vault-star ${p.favorite ? "on" : ""}`}
                    onClick={() => onToggleFavorite(p.id)}
                    title={p.favorite ? "Unfavorite" : "Favorite"}
                    aria-label={p.favorite ? "Unfavorite" : "Favorite"}
                  >
                    {p.favorite ? "★" : "☆"}
                  </button>
                </div>

                {isEditing ? (
                  <div className="vault-edit">
                    <input
                      className="vault-edit-input"
                      value={editName}
                      onChange={(e) => setEditName(e.target.value)}
                      placeholder="Prompt name"
                    />
                    <input
                      className="vault-edit-input"
                      value={editTags}
                      onChange={(e) => setEditTags(e.target.value)}
                      placeholder="Tags, comma separated"
                    />
                    <div className="vault-card-actions">
                      <button className="btn btn-ghost" onClick={() => saveEdit(p.id)}>
                        Save
                      </button>
                      <button className="btn btn-ghost" onClick={() => setEditingId(null)}>
                        Cancel
                      </button>
                    </div>
                  </div>
                ) : (
                  <>
                    <h3 className="vault-card-name">{p.name}</h3>
                    <div className="vault-meta">
                      {p.format}
                      {p.mode === "swc" ? ` · ${p.platform}` : ""} · {timeAgo(p.updatedAt)}
                    </div>
                    <div className="vault-topic">{p.topic}</div>
                    {preview && <div className="vault-preview">{preview}</div>}
                    {p.tags.length > 0 && (
                      <div className="vault-tags">
                        {p.tags.map((t) => (
                          <span key={t} className="vault-tag">
                            #{t}
                          </span>
                        ))}
                      </div>
                    )}
                    <div className="vault-card-actions">
                      <button className="btn btn-ghost" onClick={() => onLoad(p)}>
                        ↺ Load & reuse
                      </button>
                      {p.output && (
                        <button className="btn btn-ghost" onClick={() => copyOutput(p)}>
                          {copiedId === p.id ? "Copied ✓" : "Copy copy"}
                        </button>
                      )}
                      <button className="btn btn-ghost" onClick={() => startEdit(p)}>
                        Edit
                      </button>
                      <button
                        className="btn btn-ghost vault-delete"
                        onClick={() => onDelete(p.id)}
                      >
                        Delete
                      </button>
                    </div>
                  </>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
