/* =========================================================================
   CAREER OS — JOB TRACKER  (Phase 4)
   -------------------------------------------------------------------------
   A Kanban board: Wishlist · Applied · Interview · Offer · Rejected. Cards
   drag between columns with native HTML5 drag events (no libraries). Add /
   edit / delete via a modal, search by company/role, filter by column. The
   whole board autosaves to one namespaced localStorage key and restores every
   card in its column and order on reload.

   Custom view (like the Resume Builder) — not driven by the prompt engine.
   Loaded before app.js; app.js calls initJobTracker() once and navigates via
   showView('tracker') + renderTracker().
   ========================================================================= */

/* ---- Nav registration ---------------------------------------------------- */
const TRACKER_MODULE = {
  id:"tracker", group:"Track", name:"Job Tracker", tag:"Track", custom:true,
  intro:"A drag-and-drop board to track every application from wishlist to offer.",
  icon:'<rect x="3" y="4" width="5" height="16" rx="1"/><rect x="10" y="4" width="5" height="11" rx="1"/><rect x="17" y="4" width="4" height="7" rx="1"/>',
};

/* ---- Columns (status keys are stored on each card) ----------------------- */
const TRACKER_COLUMNS = [
  { key:"wishlist",  label:"Wishlist"  },
  { key:"applied",   label:"Applied"   },
  { key:"interview", label:"Interview" },
  { key:"offer",     label:"Offer"     },
  { key:"rejected",  label:"Rejected"  },
];
const TRACKER_DEFAULT_STATUS = "wishlist";

/* ---- Editable fields on a job card --------------------------------------- */
const JOB_FIELDS = [
  {k:"company",  l:"Company",        w:"h"},
  {k:"role",     l:"Role",           w:"h"},
  {k:"location", l:"Location",       w:"h", ph:_=>"City, ST / Remote"},
  {k:"comp",     l:"Salary / comp",  w:"h", ph:_=>"$120k–140k"},
  {k:"link",     l:"Link to posting",w:"f", ph:_=>"https://…"},
  {k:"notes",    l:"Notes",          w:"t", ph:_=>"Recruiter name, next step, impressions…"},
];

/* ---- Data model — one namespaced key ------------------------------------- */
function defaultBoard(){ return { jobs: [] }; }   // jobs: [{id, status, added, ...JOB_FIELDS}]
let board = null;
let trackerSearch = "";          // live search text (data is never deleted by search)
let trackerFilter = "all";       // "all" or a column key
let editingId = null;            // job id being edited, or null when adding

function loadBoard(){
  board = store.board || defaultBoard();
  if(!Array.isArray(board.jobs)) board.jobs = [];
}

/* ---- CSV EXPORT (Phase 8) -------------------------------------------------
   A real backup/portability option — Excel/Sheets-openable, not just
   "print the page." Reuses downloadBlob() (defined in resume.js, loaded
   first, so it's already a global by the time this ever runs). */
function csvCell(v){
  const s = String(v == null ? "" : v);
  return /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
}
function boardToCsv(){
  const statusLabel = s => (TRACKER_COLUMNS.find(c => c.key === s) || {}).label || s;
  const header = ["Company","Role","Status","Location","Salary / Comp","Link","Added","Notes"];
  const rows = board.jobs.map(j => [j.company, j.role, statusLabel(j.status), j.location, j.comp, j.link, j.added, j.notes]);
  // UTF-8 BOM so Excel renders accented characters correctly instead of mojibake
  return "\uFEFF" + [header, ...rows].map(r => r.map(csvCell).join(",")).join("\r\n");
}
// autosave through the one store; also refreshes the Dashboard's live counts
function saveBoard(){ store.board = board; if(typeof renderStats === 'function') renderStats(); }
function getJob(id){ return board.jobs.find(j => j.id === id); }
function newId(){
  if(window.crypto && crypto.randomUUID) return crypto.randomUUID();
  return "job_" + Date.now().toString(36) + Math.random().toString(36).slice(2,7);
}

/* ---- Move/reorder a card (single global array; column = filter by status)
   Removing then re-inserting before `beforeId` (same column) or appending
   keeps per-column order stable across reloads. ------------------------------ */
function moveJob(id, status, beforeId){
  if(id === beforeId) return;
  const i = board.jobs.findIndex(j => j.id === id);
  if(i < 0) return;
  const [job] = board.jobs.splice(i, 1);
  job.status = status;
  if(beforeId){
    const bi = board.jobs.findIndex(j => j.id === beforeId);
    if(bi >= 0) board.jobs.splice(bi, 0, job); else board.jobs.push(job);
  } else {
    board.jobs.push(job);   // end of array → end of its column when filtered
  }
  saveBoard();
  renderBoard();
}

/* ---- RENDER -------------------------------------------------------------- */
function renderTracker(){
  $('#pageTitle').textContent = "Job Tracker";
  $('#pageSub').textContent   = OCCUPATIONS[store.occ].tagline;
  if(!board) loadBoard();
  // sync filter control to state
  const f = $('#trackerFilter'); if(f) f.value = trackerFilter;
  renderBoard();
}

function renderBoard(){
  const q = trackerSearch.trim().toLowerCase();
  const matches = j => !q || (j.company||"").toLowerCase().includes(q) || (j.role||"").toLowerCase().includes(q);

  const cols = TRACKER_COLUMNS
    .filter(c => trackerFilter === "all" || trackerFilter === c.key)
    .map(c => {
      const all = board.jobs.filter(j => j.status === c.key);   // column total (for the count)
      const shown = all.filter(matches);                         // search only hides, never deletes
      const cards = shown.map(cardHtml).join("");
      const bodyInner = cards || `<div class="tcol-empty">Drop jobs here</div>`;
      return `<div class="tcol" data-col="${c.key}">
        <div class="tcol-head">
          <span class="tcol-dot"></span>
          <span class="tcol-name">${c.label}</span>
          <span class="tcol-count">${all.length}</span>
        </div>
        <div class="tcol-body" data-col="${c.key}">${bodyInner}</div>
      </div>`;
    }).join("");

  $('#trackerBoard').innerHTML = cols;
}

// Only allow http(s) links to reach an href — blocks a javascript:/data: URI
// typed into the "Link to posting" field from executing when the card is clicked.
function safeJobLink(raw){
  const s = String(raw||"").trim();
  if(!s) return "";
  try{
    const u = new URL(/^[a-z][a-z0-9+.-]*:/i.test(s) ? s : "https://" + s);
    return (u.protocol === "http:" || u.protocol === "https:") ? u.href : "";
  } catch { return ""; }
}

function cardHtml(j){
  const E = escapeHtml, A = escapeAttr;
  const meta = [];
  if(j.location) meta.push(`<span>${E(j.location)}</span>`);
  if(j.comp)     meta.push(`<span>${E(j.comp)}</span>`);
  if(j.added)    meta.push(`<span>${E(j.added)}</span>`);
  const href = safeJobLink(j.link);
  if(href)       meta.push(`<a href="${A(href)}" target="_blank" rel="noopener" data-noedit>Posting ↗</a>`);
  return `<div class="tcard" draggable="true" data-id="${A(j.id)}">
    <div class="tc-company">${E(j.company||"Untitled")}</div>
    ${j.role?`<div class="tc-role">${E(j.role)}</div>`:""}
    ${meta.length?`<div class="tc-meta">${meta.join("")}</div>`:""}
  </div>`;
}

/* ---- MODAL (add / edit) -------------------------------------------------- */
function openJobModal(id){
  editingId = id || null;
  const job = id ? getJob(id) : null;
  const o = OCCUPATIONS[store.occ];
  $('#jobModalTitle').textContent = id ? "Edit job" : "Add a job";
  $('#jobModalFields').innerHTML = JOB_FIELDS.map(f => {
    const v = job ? (job[f.k]||"") : "";
    const ph = escapeAttr(f.ph ? f.ph(o) : "");
    const ctrl = f.w === "t"
      ? `<textarea data-jk="${f.k}" placeholder="${ph}">${escapeHtml(v)}</textarea>`
      : `<input data-jk="${f.k}" value="${escapeAttr(v)}" placeholder="${ph}"/>`;
    return `<div class="field" style="${f.w==='h'?'':'grid-column:1/-1'}"><label>${f.l}</label>${ctrl}</div>`;
  }).join("");
  $('#jobDelete').style.display = id ? "" : "none";
  $('#jobModal').classList.add("open");
  const first = $('#jobModalFields [data-jk]'); if(first) first.focus();
}
function closeJobModal(){ $('#jobModal').classList.remove("open"); editingId = null; }

function saveJobFromModal(){
  const vals = {};
  document.querySelectorAll('#jobModalFields [data-jk]').forEach(el => vals[el.dataset.jk] = el.value.trim());
  if(!vals.company && !vals.role){ toast("Add a company or role first"); return; }
  if(editingId){
    Object.assign(getJob(editingId), vals);
  } else {
    board.jobs.push(Object.assign({ id:newId(), status:TRACKER_DEFAULT_STATUS, added:todayStr() }, vals));
  }
  saveBoard(); closeJobModal(); renderBoard();
}
function deleteEditingJob(){
  if(!editingId) return;
  const i = board.jobs.findIndex(j => j.id === editingId);
  if(i >= 0) board.jobs.splice(i, 1);
  saveBoard(); closeJobModal(); renderBoard();
}
function todayStr(){
  const d = new Date();
  return d.toLocaleDateString(undefined, { month:"short", day:"numeric", year:"numeric" });
}

/* ---- INIT: bind delegated events once ------------------------------------ */
let dragId = null;
function initJobTracker(){
  loadBoard();
  const boardEl = $('#trackerBoard');

  // --- click: open editor (ignore clicks on the posting link) ---
  boardEl.addEventListener("click", e => {
    if(e.target.closest("[data-noedit]")) return;
    const card = e.target.closest(".tcard");
    if(card) openJobModal(card.dataset.id);
  });

  // --- native HTML5 drag-and-drop ---
  boardEl.addEventListener("dragstart", e => {
    const card = e.target.closest(".tcard"); if(!card) return;
    dragId = card.dataset.id;
    e.dataTransfer.effectAllowed = "move";
    e.dataTransfer.setData("text/plain", dragId);
    requestAnimationFrame(() => card.classList.add("dragging"));
  });
  boardEl.addEventListener("dragend", e => {
    const card = e.target.closest(".tcard"); if(card) card.classList.remove("dragging");
    boardEl.querySelectorAll(".drop-target").forEach(el => el.classList.remove("drop-target"));
    dragId = null;
  });
  boardEl.addEventListener("dragover", e => {
    const col = e.target.closest(".tcol"); if(!col) return;
    e.preventDefault();                       // allow drop
    e.dataTransfer.dropEffect = "move";
    boardEl.querySelectorAll(".drop-target").forEach(el => { if(el !== col) el.classList.remove("drop-target"); });
    col.classList.add("drop-target");
  });
  boardEl.addEventListener("drop", e => {
    const col = e.target.closest(".tcol"); if(!col) return;
    e.preventDefault();
    const id = dragId || e.dataTransfer.getData("text/plain");
    if(!id) return;
    // insert before the card we dropped onto (if any), else append to the column
    const overCard = e.target.closest(".tcard");
    const beforeId = (overCard && overCard.dataset.id !== id) ? overCard.dataset.id : null;
    moveJob(id, col.dataset.col, beforeId);
  });

  // --- toolbar: add / search / filter ---
  $('#trackerAdd').addEventListener("click", () => openJobModal(null));
  $('#trackerSearch').addEventListener("input", e => { trackerSearch = e.target.value; renderBoard(); });
  $('#trackerFilter').addEventListener("change", e => { trackerFilter = e.target.value; renderBoard(); });
  $('#trackerExport').addEventListener("click", () => {
    if(!board.jobs.length){ toast("Add a job before exporting"); return; }
    downloadBlob(boardToCsv(), "job-tracker-" + todayStr().replace(/[^\w]+/g, "-") + ".csv", "text/csv");
    toast("Job tracker exported");
  });

  // --- modal ---
  $('#jobSave').addEventListener("click", saveJobFromModal);
  $('#jobDelete').addEventListener("click", deleteEditingJob);
  $('#jobModalClose').addEventListener("click", closeJobModal);
  $('#jobModalScrim').addEventListener("click", closeJobModal);
  $('#jobModal').addEventListener("keydown", e => {
    if(e.key === "Escape") closeJobModal();
    if(e.key === "Enter" && (e.metaKey || e.ctrlKey)) saveJobFromModal();
  });
}
