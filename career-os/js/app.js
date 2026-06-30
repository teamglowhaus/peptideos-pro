/* =========================================================================
   CAREER OS — APP ENGINE
   -------------------------------------------------------------------------
   Two config objects (OCCUPATIONS, MODULES) drive ONE renderer. This file is
   the engine: a small localStorage `store`, the live occupation reskin, the
   nav/dashboard/module renderers, the prompt composer, and the view router.

   Load order (see index.html): occupations.js → modules.js → app.js.
   All three are classic scripts sharing one global scope.
   ========================================================================= */

/* ---- 1. STATE — one small store object wraps ALL localStorage access ----- */
const store = {
  get occ(){ return localStorage.getItem('cos_occ') || 'general'; },
  set occ(v){ localStorage.setItem('cos_occ', v); },

  get theme(){ return localStorage.getItem('cos_theme') || 'light'; },
  set theme(v){ localStorage.setItem('cos_theme', v); },

  // per-module field values, keyed by module id
  fields(id){ try { return JSON.parse(localStorage.getItem('cos_f_'+id) || '{}'); } catch { return {}; } },
  saveField(id, k, val){ const f = this.fields(id); f[k] = val; localStorage.setItem('cos_f_'+id, JSON.stringify(f)); },

  // completed-module list (drives the readiness ring + "drafts" stat)
  get done(){ try { return JSON.parse(localStorage.getItem('cos_done') || '[]'); } catch { return []; } },
  markDone(id){ const d = new Set(this.done); d.add(id); localStorage.setItem('cos_done', JSON.stringify([...d])); },

  // Resume Builder data — one namespaced key holds the whole résumé (Phase 3)
  get resume(){ try { return JSON.parse(localStorage.getItem('cos_resume') || 'null'); } catch { return null; } },
  set resume(v){ localStorage.setItem('cos_resume', JSON.stringify(v)); },

  // Job Tracker board — one namespaced key holds the whole board (Phase 4)
  get board(){ try { return JSON.parse(localStorage.getItem('cos_board') || 'null'); } catch { return null; } },
  set board(v){ localStorage.setItem('cos_board', JSON.stringify(v)); },
};

// All navigable tools, grouped in display order: Build (Resume Builder) →
// the prompt tools (Compose/Apply) → Track (Job Tracker). Custom views are
// guarded so app.js still works if a phase file isn't loaded.
function navModules(){
  const head = (typeof RESUME_MODULE !== 'undefined') ? [RESUME_MODULE] : [];
  const tail = (typeof TRACKER_MODULE !== 'undefined') ? [TRACKER_MODULE] : [];
  return head.concat(MODULES, tail);
}
function findNavModule(id){ return navModules().find(m => m.id === id); }

const $ = s => document.querySelector(s);
let currentModule = null;

/* ---- 2. APPLY EDITION (the live reskin — signature interaction) ---------- */
function applyOccupation(key){
  const o = OCCUPATIONS[key]; if(!o) return;
  store.occ = key;
  const r = document.documentElement.style;
  // Only the jewel accent changes — parchment + gold stay constant.
  r.setProperty('--accent',  o.accent);
  r.setProperty('--accent-2',o.accent2);
  r.setProperty('--accent-soft', o.accent + '14');
  r.setProperty('--accent-line', o.accent + '33');

  $('#seal').textContent       = o.seal;
  $('#heroMark').textContent   = o.seal;
  $('#brandEdition').textContent = o.edition;
  $('#occName').textContent    = o.name;
  $('#heroTitle').innerHTML    = o.greet;
  $('#pageSub').textContent    = o.tagline;

  // re-render the parts that carry edition-aware example text
  if(currentModule) renderModule(currentModule, false);
  renderQuickStart();
  markEditionActive(key);
}

function markEditionActive(key){
  document.querySelectorAll('.occ-opt').forEach(el =>
    el.classList.toggle('is-active', el.dataset.occ === key));
}

/* ---- 3. NAV + DASHBOARD -------------------------------------------------- */
function renderNav(){
  // Group modules by their `group` field, preserving first-seen order.
  // The Resume Builder is included first (its own "Build" group).
  const groups = {};
  navModules().forEach(m => { (groups[m.group] ||= []).push(m); });

  const dash = `<button class="nav-item active" data-view="dashboard">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><rect x="3" y="3" width="7" height="9" rx="1"/><rect x="14" y="3" width="7" height="5" rx="1"/><rect x="14" y="12" width="7" height="9" rx="1"/><rect x="3" y="16" width="7" height="5" rx="1"/></svg>Atelier</button>`;

  const gh = Object.entries(groups).map(([g, items]) => `
    <div class="nav-group"><div class="nav-label">${g}</div>
      ${items.map(m => `<button class="nav-item" data-mod="${m.id}">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">${m.icon}</svg>${m.name}</button>`).join('')}
    </div>`).join('');

  $('#nav').innerHTML = dash + gh;
}

function renderStats(){
  const done = store.done.length;
  const stats = [
    {b:done, s:"Drafts composed", i:'<path d="M4 6h16M4 12h16M4 18h10"/>'},
    {b:"12", s:"Applications",    i:'<path d="M4 4h16v16H4z"/><path d="m4 8 8 5 8-5"/>'},
    {b:"3",  s:"Interviews",      i:'<path d="M8 2v4M16 2v4M3 10h18M5 6h14v14H5z"/>'},
    {b:"1",  s:"Offers",          i:'<path d="m12 2 3 7h7l-5.5 4 2 7L12 17l-6.5 3 2-7L2 9h7z"/>'},
  ];
  $('#statRow').innerHTML = stats.map((s,i) => `<div class="card stat">
    <span class="card-idx">0${i+1}</span>
    <div class="ico" style="color:var(--accent)"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">${s.i}</svg></div>
    <b>${s.b}</b><span>${s.s}</span></div>`).join('');
}

function renderRing(){
  // Readiness = share of modules completed (with a small head-start once any
  // draft exists, so the first composition feels rewarding).
  const pct = Math.min(100, store.done.length / MODULES.length * 100 + (store.done.length ? 22 : 0));
  const circ = 2 * Math.PI * 59;
  $('#ring').setAttribute('stroke-dasharray', circ.toFixed(0));
  // defer so the transition runs from full offset → target
  setTimeout(() => $('#ring').setAttribute('stroke-dashoffset', (circ * (1 - pct/100)).toFixed(0)), 140);
  // count-up numeral
  let n = 0;
  const t = setInterval(() => {
    n += Math.ceil(pct/24);
    if(n >= pct){ n = Math.round(pct); clearInterval(t); }
    $('#ringNum').textContent = n;
  }, 28);
  $('#ringHint').textContent = pct >= 80 ? "Interview-ready" : pct > 0 ? "A strong beginning" : "Compose drafts to raise it";
}

function renderQuickStart(){
  // Resume Builder first (the flagship), then the next two prompt tools.
  $('#qsGrid').innerHTML = navModules().slice(0,3).map((m,i) => `
    <div class="card qs-card" data-mod="${m.id}">
      <span class="qs-tag">${m.tag}</span>
      <span class="qs-num">0${i+1}</span>
      <div class="qs-divider"></div>
      <h3>${m.name}</h3><p>${m.intro}</p>
    </div>`).join('');
}

/* ---- 4. MODULE RENDERER (reads fields[] — never bespoke per tool) -------- */
function renderModule(mod, switchView = true){
  currentModule = mod;
  const o = OCCUPATIONS[store.occ], saved = store.fields(mod.id);

  $('#modIdx').textContent     = '№ ' + String(MODULES.indexOf(mod)+1).padStart(2,'0');
  $('#modEyebrow').textContent = mod.group + ' · ' + o.name;
  $('#modTitle').textContent   = mod.name;
  $('#modIntro').textContent   = mod.intro;
  $('#pageTitle').textContent  = mod.name;
  $('#pageSub').textContent    = o.tagline;

  $('#modForm').innerHTML = mod.fields.map(f => {
    const ph = f.ph(o), val = (saved[f.key] || '');
    const ctrl = f.type === 'textarea'
      ? `<textarea data-k="${f.key}" placeholder="${escapeAttr(ph)}">${escapeHtml(val)}</textarea>`
      : `<input data-k="${f.key}" value="${escapeAttr(val)}" placeholder="${escapeAttr(ph)}"/>`;
    return `<div class="field"><label>${f.label}</label>${ctrl}</div>`;
  }).join('');

  // persist every keystroke through the store (no scattered localStorage calls)
  $('#modForm').querySelectorAll('[data-k]').forEach(el =>
    el.addEventListener('input', e => store.saveField(mod.id, e.target.dataset.k, e.target.value)));

  if(switchView){ resetOutput(); showView('module'); }
}

function resetOutput(){
  $('#outShell').innerHTML = `<div class="out-empty">
    <div class="mark"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M7 8h10M7 12h10M7 16h6"/><rect x="3" y="3" width="18" height="18" rx="1"/></svg></div>
    <h3>Your composed prompt appears here</h3>
    <p>Fill the form and compose. We assemble an expert-level prompt for you to copy into your AI.</p></div>`;
}

/* ---- 5. COMPOSE (buildPrompt is the hidden deliverable) ------------------ */
function generate(){
  const mod = currentModule; if(!mod) return;
  const o = OCCUPATIONS[store.occ], vals = {};
  $('#modForm').querySelectorAll('[data-k]').forEach(el => vals[el.dataset.k] = el.value.trim());

  const prompt = mod.buildPrompt(vals, o);
  store.markDone(mod.id);

  $('#outShell').innerHTML = `<div class="result">
    <div class="result-top">
      <span class="result-stamp">✓</span>
      <div><b>Prompt composed</b><span>Copy it, then paste into Claude or ChatGPT</span></div>
    </div>
    <div class="result-actions">
      <button class="btn-sm btn-copy" id="copyBtn"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><rect x="9" y="9" width="11" height="11" rx="1.5"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/></svg>Copy prompt</button>
      <a class="btn-sm btn-link" href="https://claude.ai/new" target="_blank" rel="noopener">Open Claude</a>
      <a class="btn-sm btn-link" href="https://chat.openai.com" target="_blank" rel="noopener">Open ChatGPT</a>
      <button class="btn-disclose" id="discloseBtn">View prompt</button>
    </div>
    <div class="prompt-raw" id="promptRaw"><pre id="promptText"></pre></div>
  </div>`;

  $('#promptText').textContent = prompt;            // textContent = no HTML injection
  $('#copyBtn').onclick = () => copyPrompt(prompt);
  $('#discloseBtn').onclick = e => {
    const raw = $('#promptRaw'); const open = raw.classList.toggle('show');
    e.currentTarget.textContent = open ? 'Hide prompt' : 'View prompt';
  };

  renderStats(); renderRing();
}

function copyPrompt(text){ copyText(text, 'Copied to clipboard'); }

// Generic clipboard copy with an offline (file://) fallback. Reused by the
// prompt composer and the Resume Builder's "Copy text" export.
function copyText(text, msg){
  const done = () => toast(msg || 'Copied to clipboard');
  if(navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(text).then(done).catch(() => fallbackCopy(text, done));
  } else { fallbackCopy(text, done); }
}
function fallbackCopy(text, done){
  // works offline / from file:// where the async clipboard API may be blocked
  const ta = document.createElement('textarea');
  ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
  document.body.appendChild(ta); ta.select();
  try { document.execCommand('copy'); done(); } catch { toast('Copy failed — select & copy manually'); }
  document.body.removeChild(ta);
}

/* ---- 6. ROUTER + EVENTS -------------------------------------------------- */
function showView(name){
  $('#view-dashboard').hidden = name !== 'dashboard';
  $('#view-module').hidden    = name !== 'module';
  $('#view-resume').hidden    = name !== 'resume';
  $('#view-tracker').hidden   = name !== 'tracker';
  if(name === 'dashboard'){
    $('#pageTitle').textContent = 'Atelier';
    $('#pageSub').textContent   = OCCUPATIONS[store.occ].tagline;
    renderRing();
  }
  $('.scroll').scrollTop = 0;
}
function setActiveNav(el){ document.querySelectorAll('.nav-item').forEach(n => n.classList.toggle('active', n === el)); }
function navTo(mod){
  if(!mod) return;
  setActiveNav(document.querySelector(`.nav-item[data-mod="${mod.id}"]`));
  if(mod.custom && mod.id === 'resume'){ renderResume(); showView('resume'); }
  else if(mod.custom && mod.id === 'tracker'){ renderTracker(); showView('tracker'); }
  else renderModule(mod);
  closeDrawer();
}
function toast(m){ const t = $('#toast'); t.textContent = m; t.classList.add('show'); setTimeout(() => t.classList.remove('show'), 1900); }

/* mobile drawer */
function openDrawer(){ document.body.classList.add('nav-open'); }
function closeDrawer(){ document.body.classList.remove('nav-open'); }

document.addEventListener('click', e => {
  // nav: dashboard or a module
  const nav = e.target.closest('[data-view],[data-mod]');
  if(nav){
    if(nav.dataset.view === 'dashboard'){ setActiveNav(nav); showView('dashboard'); closeDrawer(); }
    else if(nav.dataset.mod){ navTo(findNavModule(nav.dataset.mod)); }
  }
  // hero / section CTAs
  const go = e.target.closest('[data-go]');
  if(go){ navTo(findNavModule(go.dataset.go)); }
  if(e.target.closest('[data-go-first]')){ e.preventDefault(); navTo(navModules()[0]); }

  // occupation switcher open/close + selection
  if(e.target.closest('#occBtn')) $('#occMenu').classList.toggle('open');
  else if(!e.target.closest('#occMenu')) $('#occMenu').classList.remove('open');
  const opt = e.target.closest('.occ-opt');
  if(opt){ applyOccupation(opt.dataset.occ); $('#occMenu').classList.remove('open'); toast(OCCUPATIONS[opt.dataset.occ].edition + ' applied'); }

  // mobile drawer
  if(e.target.closest('#menuBtn')) openDrawer();
  if(e.target.closest('#scrim'))   closeDrawer();
});

/* ---- 7. THEME (Day / Evening edition) ------------------------------------ */
function applyTheme(t){
  document.documentElement.dataset.theme = t;
  store.theme = t;
  const lbl = $('#themeLabel'); if(lbl) lbl.textContent = t === 'dark' ? 'Day edition' : 'Evening edition';
}
function bindStaticEvents(){
  $('#genBtn').addEventListener('click', generate);
  $('#themeToggle').addEventListener('click', () => applyTheme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark'));
  document.addEventListener('keydown', e => {
    if((e.shiftKey && e.key.toLowerCase() === 'd') && !/input|textarea/i.test(e.target.tagName)) $('#themeToggle').click();
    if(e.key === 'Escape'){ $('#occMenu').classList.remove('open'); closeDrawer(); }
  });
}

/* ---- 8. EDITION MENU (built from OCCUPATIONS) ---------------------------- */
function renderEditionMenu(){
  $('#occMenu').innerHTML = '<div class="mhead">Choose an edition</div>' +
    Object.entries(OCCUPATIONS).map(([k,o]) => `
      <button class="occ-opt" data-occ="${k}">
        <span class="swatch" style="background:linear-gradient(135deg,${o.accent},${o.accent2})"></span>
        <span><b>${o.name}</b><small>${o.edition}</small></span>
      </button>`).join('');
}

/* ---- helpers: escape user text before it enters markup ------------------- */
function escapeHtml(s){ return String(s).replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c])); }
function escapeAttr(s){ return String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c])); }

/* ---- 9. INIT ------------------------------------------------------------- */
(function init(){
  applyTheme(store.theme);
  renderNav();
  renderStats();
  renderEditionMenu();
  applyOccupation(store.occ);   // sets accent + edition-aware text, renders quick-start
  renderRing();
  bindStaticEvents();
  initResumeBuilder();          // Phase 3 — binds the Resume Builder's events once
  initJobTracker();             // Phase 4 — binds the Job Tracker's events once
})();
