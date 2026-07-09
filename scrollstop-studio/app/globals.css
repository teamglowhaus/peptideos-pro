* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

:root {
  --bg: #0d0d1a;
  --panel: #161629;
  --accent: #9b59b6;
  --accent2: #e066a0;
  --text: #ece8f5;
  --muted: rgba(255, 255, 255, 0.55);
  --border: rgba(255, 255, 255, 0.1);
}

html,
body {
  background: var(--bg);
  color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica,
    Arial, sans-serif;
  min-height: 100vh;
  transition: background 0.35s ease;
}

.app {
  max-width: 1100px;
  margin: 0 auto;
  padding: 24px 16px 60px;
}

.app-title {
  font-size: 1.6rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  margin-bottom: 4px;
}

.app-title span {
  color: var(--accent);
}

.app-sub {
  color: var(--muted);
  font-size: 0.9rem;
  margin-bottom: 20px;
}

/* ---- Tabs ---- */
.tabs {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 24px;
}

.tab {
  flex: 1 1 140px;
  padding: 12px 10px;
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 12px;
  color: var(--muted);
  font-size: 0.85rem;
  font-weight: 700;
  cursor: pointer;
  text-align: center;
  transition: all 0.2s ease;
}

.tab.active {
  color: var(--text);
  border-color: var(--accent);
  box-shadow: 0 0 0 1px var(--accent), 0 4px 20px -6px var(--accent);
}

.tab small {
  display: block;
  font-weight: 400;
  font-size: 0.7rem;
  margin-top: 3px;
  opacity: 0.7;
}

/* ---- Form ---- */
.panel {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 20px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 14px;
}

.field label {
  display: block;
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--accent);
  margin-bottom: 6px;
}

.field input,
.field select,
.field textarea {
  width: 100%;
  background: rgba(0, 0, 0, 0.35);
  border: 1px solid var(--border);
  border-radius: 10px;
  color: var(--text);
  padding: 11px 12px;
  font-size: 0.92rem;
  font-family: inherit;
}

.field textarea {
  resize: vertical;
  min-height: 70px;
}

.field input:focus,
.field select:focus,
.field textarea:focus {
  outline: none;
  border-color: var(--accent);
}

.field.full {
  grid-column: 1 / -1;
}

/* ---- Buttons ---- */
.btn {
  border: none;
  border-radius: 10px;
  font-weight: 700;
  cursor: pointer;
  font-size: 0.92rem;
  padding: 13px 22px;
  transition: transform 0.12s ease, opacity 0.2s ease;
}

.btn:active {
  transform: scale(0.98);
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-primary {
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  color: #fff;
  width: 100%;
  margin-top: 16px;
  font-size: 1rem;
}

.btn-ghost {
  background: transparent;
  border: 1px solid var(--accent);
  color: var(--accent);
  padding: 9px 16px;
  font-size: 0.82rem;
}

/* ---- Output ---- */
.output-toolbar {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.output {
  white-space: pre-wrap;
  font-size: 0.95rem;
  line-height: 1.65;
}

.output .section-head {
  display: block;
  margin-top: 18px;
  font-weight: 800;
  color: var(--accent);
  letter-spacing: 0.04em;
}

.output .section-head:first-child {
  margin-top: 0;
}

.error-box {
  background: rgba(255, 60, 60, 0.12);
  border: 1px solid rgba(255, 80, 80, 0.5);
  color: #ff9b9b;
  border-radius: 12px;
  padding: 14px 16px;
  font-size: 0.9rem;
  margin-bottom: 20px;
  word-break: break-word;
}

/* ---- Loading ---- */
.loading {
  display: flex;
  align-items: center;
  gap: 12px;
  justify-content: center;
  padding: 40px 0;
  color: var(--muted);
  font-size: 0.92rem;
}

.dots {
  display: flex;
  gap: 6px;
}

.dots span {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: var(--accent);
  animation: bounce 1.2s infinite ease-in-out;
}

.dots span:nth-child(2) {
  animation-delay: 0.15s;
}

.dots span:nth-child(3) {
  animation-delay: 0.3s;
}

@keyframes bounce {
  0%,
  80%,
  100% {
    transform: scale(0.6);
    opacity: 0.4;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

/* ---- Images ---- */
.section-title {
  font-size: 0.78rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--accent);
  margin: 26px 0 12px;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 12px;
}

.image-card {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  border: 2px solid transparent;
  cursor: pointer;
  background: rgba(0, 0, 0, 0.3);
  padding: 0;
}

.image-card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  display: block;
}

.image-card.selected {
  border-color: var(--accent);
  box-shadow: 0 0 0 2px var(--accent);
}

.image-credit {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  font-size: 0.65rem;
  padding: 4px 8px;
  background: rgba(0, 0, 0, 0.65);
  color: rgba(255, 255, 255, 0.8);
}

/* ---- Preview ---- */
.preview-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 14px;
}

.preview-frame {
  position: relative;
  width: 100%;
  max-width: 360px;
  border-radius: 14px;
  overflow: hidden;
  background: #000;
}

.preview-frame.square {
  aspect-ratio: 1 / 1;
}

.preview-frame.portrait {
  aspect-ratio: 9 / 16;
}

.preview-frame img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.preview-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 8%;
  background: linear-gradient(rgba(0, 0, 0, 0.15), rgba(0, 0, 0, 0.45));
}

.preview-overlay p {
  color: #fff;
  font-weight: 800;
  font-size: 1.15rem;
  line-height: 1.35;
  text-align: center;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.85), 0 0 2px rgba(0, 0, 0, 0.9);
  white-space: pre-wrap;
  word-break: break-word;
}

.carousel-nav {
  display: flex;
  align-items: center;
  gap: 14px;
  font-size: 0.85rem;
  color: var(--muted);
}

/* ---- Footer ---- */
.footer {
  margin-top: 48px;
  text-align: center;
  color: var(--muted);
  font-size: 0.82rem;
}

.footer b {
  color: var(--accent);
}

@media (max-width: 600px) {
  .tab {
    flex: 1 1 45%;
  }
  .image-card img {
    height: 150px;
  }
}
