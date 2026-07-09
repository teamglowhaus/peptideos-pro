"use client";

import { useEffect, useMemo, useState } from "react";
import {
  GOALS,
  HOOK_STYLES,
  INSTAGRAM_FORMATS,
  MODES,
  SWC_ANGLES,
  TIKTOK_FORMATS,
  imageOrientation,
  isCarouselFormat,
  isStaticFormat,
  isStoryFormat,
  type ModeId,
  type Platform,
} from "@/lib/modes";

interface Photo {
  id: number;
  alt: string;
  photographer: string;
  pageUrl: string;
  full: string;
  preview: string;
  thumb: string;
}

const MODE_ORDER: ModeId[] = ["ugc", "instagram", "tiktok", "swc"];

// ---- Output parsing -------------------------------------------------------

const HEADER_RE = /^([A-Z][A-Z0-9 &/'\-]{2,})(?: \d+)?:/;

function parseSections(text: string): Record<string, string> {
  const sections: Record<string, string> = {};
  let current = "";
  for (const line of text.split("\n")) {
    const m = line.match(/^([A-Z][A-Z0-9 &/'\-]{2,}(?: \d+)?):\s*(.*)$/);
    if (m) {
      current = m[1].trim();
      sections[current] = m[2] ?? "";
    } else if (current) {
      sections[current] += (sections[current] ? "\n" : "") + line;
    }
  }
  for (const k of Object.keys(sections)) sections[k] = sections[k].trim();
  return sections;
}

function overlayTextFor(format: string, sections: Record<string, string>, slide: number): string {
  if (isCarouselFormat(format)) {
    return sections[`SLIDE ${slide + 1}`] ?? sections["SLIDE 1"] ?? "";
  }
  if (isStoryFormat(format)) {
    return sections[`STORY ${slide + 1}`] ?? sections["STORY 1"] ?? "";
  }
  const caption = sections["CAPTION"] ?? "";
  const firstChunk = caption.split("\n").find((l) => l.trim()) ?? caption;
  return firstChunk.length > 160 ? firstChunk.slice(0, 157) + "…" : firstChunk;
}

function slideCountFor(format: string, sections: Record<string, string>): number {
  if (isCarouselFormat(format)) {
    let n = 0;
    while (sections[`SLIDE ${n + 1}`] !== undefined) n++;
    return Math.max(n, 1);
  }
  if (isStoryFormat(format)) return 3;
  return 1;
}

// ---- Canvas download ------------------------------------------------------

function wrapText(ctx: CanvasRenderingContext2D, text: string, maxWidth: number): string[] {
  const lines: string[] = [];
  for (const rawLine of text.split("\n")) {
    let line = "";
    for (const word of rawLine.split(" ")) {
      const probe = line ? `${line} ${word}` : word;
      if (ctx.measureText(probe).width > maxWidth && line) {
        lines.push(line);
        line = word;
      } else {
        line = probe;
      }
    }
    lines.push(line);
  }
  return lines;
}

async function downloadPng(photoUrl: string, text: string, portrait: boolean, filename: string) {
  const w = 1080;
  const h = portrait ? 1920 : 1080;
  const img = new Image();
  img.crossOrigin = "anonymous";
  await new Promise<void>((resolve, reject) => {
    img.onload = () => resolve();
    img.onerror = () => reject(new Error("Couldn't load the image for download (CORS)."));
    img.src = photoUrl;
  });

  const canvas = document.createElement("canvas");
  canvas.width = w;
  canvas.height = h;
  const ctx = canvas.getContext("2d")!;

  // cover-crop the photo
  const scale = Math.max(w / img.width, h / img.height);
  const dw = img.width * scale;
  const dh = img.height * scale;
  ctx.drawImage(img, (w - dw) / 2, (h - dh) / 2, dw, dh);

  // darken for readability
  const grad = ctx.createLinearGradient(0, 0, 0, h);
  grad.addColorStop(0, "rgba(0,0,0,0.18)");
  grad.addColorStop(1, "rgba(0,0,0,0.5)");
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, w, h);

  // bold white text with dark shadow, centered
  const fontSize = portrait ? 64 : 56;
  ctx.font = `800 ${fontSize}px -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`;
  ctx.fillStyle = "#fff";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.shadowColor = "rgba(0,0,0,0.85)";
  ctx.shadowBlur = 18;
  ctx.shadowOffsetY = 4;

  const lines = wrapText(ctx, text, w * 0.82);
  const lineHeight = fontSize * 1.3;
  const startY = h / 2 - ((lines.length - 1) * lineHeight) / 2;
  lines.forEach((line, i) => ctx.fillText(line, w / 2, startY + i * lineHeight));

  const blob = await new Promise<Blob | null>((resolve) => canvas.toBlob(resolve, "image/png"));
  if (!blob) throw new Error("Couldn't render the PNG.");
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = filename;
  a.click();
  URL.revokeObjectURL(a.href);
}

// ---- Page -----------------------------------------------------------------

export default function Home() {
  const [mode, setMode] = useState<ModeId>("ugc");
  const [platform, setPlatform] = useState<Platform>("Instagram");
  const [format, setFormat] = useState(MODES.ugc.formats[0]);
  const [promoAngle, setPromoAngle] = useState(SWC_ANGLES[0]);
  const [topic, setTopic] = useState("");
  const [goal, setGoal] = useState(GOALS[0]);
  const [hookStyle, setHookStyle] = useState(HOOK_STYLES[0]);
  const [extraContext, setExtraContext] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [output, setOutput] = useState("");
  const [photos, setPhotos] = useState<Photo[]>([]);
  const [imagesError, setImagesError] = useState("");
  const [selectedPhoto, setSelectedPhoto] = useState<Photo | null>(null);
  const [slide, setSlide] = useState(0);
  const [copied, setCopied] = useState(false);
  const [downloading, setDownloading] = useState(false);

  const cfg = MODES[mode];
  const formats = useMemo(() => {
    if (mode === "swc") return platform === "Instagram" ? INSTAGRAM_FORMATS : TIKTOK_FORMATS;
    return cfg.formats;
  }, [mode, platform, cfg]);

  // apply per-mode theme
  useEffect(() => {
    const r = document.documentElement.style;
    r.setProperty("--bg", cfg.theme.bg);
    r.setProperty("--panel", cfg.theme.panel);
    r.setProperty("--accent", cfg.theme.accent);
    r.setProperty("--accent2", cfg.theme.accent2);
    r.setProperty("--text", cfg.theme.text);
  }, [cfg]);

  // keep format valid when mode/platform changes
  useEffect(() => {
    if (!formats.includes(format)) setFormat(formats[0]);
  }, [formats, format]);

  const sections = useMemo(() => parseSections(output), [output]);
  const staticFormat = isStaticFormat(format);
  const portrait = imageOrientation(mode, platform, format) === "portrait";
  const totalSlides = slideCountFor(format, sections);
  const overlayText = overlayTextFor(format, sections, slide);

  async function fetchImages() {
    setImagesError("");
    setPhotos([]);
    setSelectedPhoto(null);
    try {
      const res = await fetch("/api/images", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          topic,
          mode,
          orientation: imageOrientation(mode, platform, format),
        }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error ?? `Image search failed (${res.status})`);
      setPhotos(data.photos);
      if (data.photos.length > 0) setSelectedPhoto(data.photos[0]);
    } catch (e) {
      setImagesError(e instanceof Error ? e.message : String(e));
    }
  }

  async function generate() {
    if (!topic.trim()) {
      setError("Add a product or topic first.");
      return;
    }
    setLoading(true);
    setError("");
    setOutput("");
    setSlide(0);
    try {
      const res = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mode, format, platform, promoAngle, topic, goal, hookStyle, extraContext }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error ?? `Generation failed (${res.status})`);
      setOutput(data.content);
      fetchImages(); // kick off image search after the script lands
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setLoading(false);
    }
  }

  async function copyOutput() {
    await navigator.clipboard.writeText(output);
    setCopied(true);
    setTimeout(() => setCopied(false), 1600);
  }

  async function handleDownload() {
    if (!selectedPhoto) return;
    setDownloading(true);
    try {
      const suffix = totalSlides > 1 ? `-slide${slide + 1}` : "";
      await downloadPng(
        selectedPhoto.full,
        overlayText,
        portrait,
        `scriptline-post${suffix}.png`,
      );
    } catch (e) {
      setImagesError(e instanceof Error ? e.message : String(e));
    } finally {
      setDownloading(false);
    }
  }

  // render output with highlighted section headers
  const renderedOutput = useMemo(() => {
    return output.split("\n").map((line, i) => {
      if (HEADER_RE.test(line)) {
        return (
          <span key={i}>
            <span className="section-head">{line}</span>
          </span>
        );
      }
      return <span key={i}>{line + "\n"}</span>;
    });
  }, [output]);

  return (
    <main className="app">
      <h1 className="app-title">
        Script<span>line</span>
      </h1>
      <p className="app-sub">{cfg.tagline}</p>

      <div className="tabs">
        {MODE_ORDER.map((id) => (
          <button
            key={id}
            className={`tab ${mode === id ? "active" : ""}`}
            onClick={() => setMode(id)}
          >
            {MODES[id].label}
            <small>{MODES[id].tagline}</small>
          </button>
        ))}
      </div>

      <div className="panel">
        <div className="grid">
          {mode === "swc" && (
            <>
              <div className="field">
                <label>Platform</label>
                <select value={platform} onChange={(e) => setPlatform(e.target.value as Platform)}>
                  <option>Instagram</option>
                  <option>TikTok</option>
                </select>
              </div>
              <div className="field">
                <label>Promo Angle</label>
                <select value={promoAngle} onChange={(e) => setPromoAngle(e.target.value)}>
                  {SWC_ANGLES.map((a) => (
                    <option key={a}>{a}</option>
                  ))}
                </select>
              </div>
            </>
          )}

          <div className="field">
            <label>{cfg.formatLabel}</label>
            <select value={format} onChange={(e) => setFormat(e.target.value)}>
              {formats.map((f) => (
                <option key={f}>{f}</option>
              ))}
            </select>
          </div>

          <div className="field">
            <label>Goal</label>
            <select value={goal} onChange={(e) => setGoal(e.target.value)}>
              {GOALS.map((g) => (
                <option key={g}>{g}</option>
              ))}
            </select>
          </div>

          <div className="field">
            <label>Hook Style</label>
            <select value={hookStyle} onChange={(e) => setHookStyle(e.target.value)}>
              {HOOK_STYLES.map((h) => (
                <option key={h}>{h}</option>
              ))}
            </select>
          </div>

          <div className="field full">
            <label>Product or Topic</label>
            <input
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="e.g. lavender pillow spray, a digital course, vitamin C serum…"
            />
          </div>

          <div className="field full">
            <label>Extra Context (optional)</label>
            <textarea
              value={extraContext}
              onChange={(e) => setExtraContext(e.target.value)}
              placeholder="Anything the writer should know — brand details, your story, what to avoid…"
            />
          </div>
        </div>

        <button className="btn btn-primary" onClick={generate} disabled={loading}>
          {loading ? "Writing your script…" : "Generate Content"}
        </button>
      </div>

      {error && <div className="error-box">{error}</div>}

      {loading && (
        <div className="loading">
          <div className="dots">
            <span />
            <span />
            <span />
          </div>
          Stopping the scroll…
        </div>
      )}

      {output && !loading && (
        <div className="panel">
          <div className="output-toolbar">
            <button className="btn btn-ghost" onClick={copyOutput}>
              {copied ? "Copied ✓" : "Copy to clipboard"}
            </button>
            <button className="btn btn-ghost" onClick={generate}>
              Regenerate
            </button>
          </div>
          <div className="output">{renderedOutput}</div>

          {/* ---- Images ---- */}
          {(photos.length > 0 || imagesError) && (
            <>
              <div className="section-title">
                {staticFormat
                  ? "Pick a background image"
                  : "Suggested background / B-roll reference images"}
              </div>
              {imagesError && <div className="error-box">{imagesError}</div>}
              <div className="image-grid">
                {photos.map((p) => (
                  <button
                    key={p.id}
                    className={`image-card ${staticFormat && selectedPhoto?.id === p.id ? "selected" : ""}`}
                    onClick={() => staticFormat && setSelectedPhoto(p)}
                    title={p.alt}
                  >
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img src={p.thumb} alt={p.alt} />
                    <span className="image-credit">📷 {p.photographer} · Pexels</span>
                  </button>
                ))}
              </div>
            </>
          )}

          {/* ---- Visual preview for static posts ---- */}
          {staticFormat && selectedPhoto && (
            <>
              <div className="section-title">
                Visual preview {portrait ? "(9:16 story)" : "(1:1 feed post)"}
              </div>
              <div className="preview-wrap">
                <div className={`preview-frame ${portrait ? "portrait" : "square"}`}>
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img src={selectedPhoto.preview} alt={selectedPhoto.alt} />
                  <div className="preview-overlay">
                    <p>{overlayText}</p>
                  </div>
                </div>

                {totalSlides > 1 && (
                  <div className="carousel-nav">
                    <button
                      className="btn btn-ghost"
                      onClick={() => setSlide((s) => Math.max(0, s - 1))}
                      disabled={slide === 0}
                    >
                      ‹ Prev
                    </button>
                    <span>
                      Slide {slide + 1} / {totalSlides}
                    </span>
                    <button
                      className="btn btn-ghost"
                      onClick={() => setSlide((s) => Math.min(totalSlides - 1, s + 1))}
                      disabled={slide === totalSlides - 1}
                    >
                      Next ›
                    </button>
                  </div>
                )}

                <button className="btn btn-ghost" onClick={handleDownload} disabled={downloading}>
                  {downloading ? "Rendering…" : "⬇ Download PNG (upload-ready)"}
                </button>
              </div>
            </>
          )}
        </div>
      )}

      <footer className="footer">
        <b>Scriptline</b> · content that stops the scroll
      </footer>
    </main>
  );
}
