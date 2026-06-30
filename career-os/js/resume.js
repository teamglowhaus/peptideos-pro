/* =========================================================================
   CAREER OS — RESUME BUILDER  (Phase 3)
   -------------------------------------------------------------------------
   The one genuinely custom module — NOT driven by the prompt engine. A
   dedicated multi-section form with a live one-page résumé preview, autosave
   to a single namespaced localStorage key, and three offline exports:
   Print/PDF (window.print), clean plain text (clipboard), and a Word-ready
   .doc download. Vanilla JS, no external libraries.

   Loaded before app.js; everything here is global. app.js calls
   initResumeBuilder() once (binds delegated events) and navigates to it via
   showView('resume') + renderResume().
   ========================================================================= */

/* ---- Nav registration: a custom view, not a prompt tool ------------------ */
const RESUME_MODULE = {
  id:"resume", group:"Build", name:"Resume Builder", tag:"Build", custom:true,
  intro:"Compose a clean one-page résumé with live preview, autosave, and print, text & Word export.",
  icon:'<rect x="5" y="3" width="14" height="18" rx="1.5"/><path d="M8 8h8M8 12h8M8 16h5"/>',
};

/* ---- Repeatable section schemas -----------------------------------------
   Each section is a list of entries; each entry has these fields. Adding a
   field here adds it to the form AND the preview automatically. `f` = whole
   width, `h` = half width (paired in a 2-col grid), `t` = textarea.        */
const RESUME_SECTIONS = {
  experience: { label:"Experience", entryLabel:"Position", fields:[
    {k:"title",  l:"Job title",   w:"h", ph:o=>o.roleEx},
    {k:"company",l:"Company",     w:"h"},
    {k:"location",l:"Location",   w:"h", ph:_=>"City, ST"},
    {k:"start",  l:"Start",       w:"h", ph:_=>"Jan 2022"},
    {k:"end",    l:"End",         w:"h", ph:_=>"Present"},
    {k:"bullets",l:"Highlights — one per line", w:"t", ph:_=>"Led … resulting in …\nImproved … by …%"},
  ]},
  education: { label:"Education", entryLabel:"Program", fields:[
    {k:"degree", l:"Degree / credential", w:"h", ph:_=>"B.S. Nursing"},
    {k:"school", l:"School",      w:"h"},
    {k:"location",l:"Location",   w:"h", ph:_=>"City, ST"},
    {k:"start",  l:"Start",       w:"h", ph:_=>"2016"},
    {k:"end",    l:"End",         w:"h", ph:_=>"2020"},
    {k:"details",l:"Details (optional)", w:"t", ph:_=>"GPA, honors, relevant coursework…"},
  ]},
  projects: { label:"Projects", entryLabel:"Project", fields:[
    {k:"name", l:"Project name", w:"h"},
    {k:"role", l:"Your role",    w:"h"},
    {k:"link", l:"Link (optional)", w:"f", ph:_=>"github.com/…"},
    {k:"description", l:"Description — one per line", w:"t"},
  ]},
  certifications: { label:"Certifications", entryLabel:"Certification", fields:[
    {k:"name",   l:"Certification", w:"h", ph:_=>"ACLS"},
    {k:"issuer", l:"Issuer",        w:"h", ph:_=>"American Heart Assoc."},
    {k:"date",   l:"Date",          w:"h", ph:_=>"2024"},
  ]},
  awards: { label:"Awards", entryLabel:"Award", fields:[
    {k:"name",   l:"Award", w:"h"},
    {k:"issuer", l:"Issuer / context", w:"h"},
    {k:"date",   l:"Date", w:"h", ph:_=>"2023"},
  ]},
  volunteer: { label:"Volunteer", entryLabel:"Role", fields:[
    {k:"role", l:"Role", w:"h"},
    {k:"org",  l:"Organization", w:"h"},
    {k:"start",l:"Start", w:"h", ph:_=>"2021"},
    {k:"end",  l:"End",   w:"h", ph:_=>"2023"},
    {k:"description", l:"Description — one per line", w:"t"},
  ]},
};
// order the repeatable sections appear in the form + preview
const RESUME_SECTION_ORDER = ["experience","education","projects","certifications","awards","volunteer"];

// flat (non-repeatable) contact fields, rendered in a 2-col grid
const RESUME_CONTACT = [
  {k:"phone",    l:"Phone",    ph:_=>"(555) 123-4567"},
  {k:"email",    l:"Email",    ph:_=>"you@email.com"},
  {k:"location", l:"Location", ph:_=>"City, ST"},
  {k:"website",  l:"Website / portfolio", ph:_=>"yoursite.com"},
  {k:"linkedin", l:"LinkedIn", ph:_=>"linkedin.com/in/you"},
];

/* ---- Data model ---------------------------------------------------------- */
function blankEntry(sec){ const o = {}; RESUME_SECTIONS[sec].fields.forEach(f => o[f.k] = ""); return o; }
function defaultResume(){
  return {
    name:"", phone:"", email:"", location:"", website:"", linkedin:"",
    target:"", summary:"", skills:"", languages:"", references:"",
    experience:[], education:[], projects:[], certifications:[], awards:[], volunteer:[],
  };
}
let resumeData = null;

function loadResume(){
  const saved = store.resume;            // single namespaced key (see app.js store.resume)
  resumeData = Object.assign(defaultResume(), saved || {});
  // guarantee every repeatable section is an array (forward-compatible)
  RESUME_SECTION_ORDER.forEach(s => { if(!Array.isArray(resumeData[s])) resumeData[s] = []; });
}
function saveResume(){ store.resume = resumeData; }   // autosave through the one store

/* ---- FORM RENDER (rebuilt on structural change only) --------------------- */
function renderResume(){
  if(!resumeData) loadResume();
  const o = OCCUPATIONS[store.occ];
  $('#pageTitle').textContent = "Resume Builder";
  $('#pageSub').textContent   = o.tagline;

  const F = (k, l, val, ph, type) => {
    const v = escapeAttr(val || "");
    const p = escapeAttr(ph || "");
    const ctrl = type === "t"
      ? `<textarea data-f="${k}" placeholder="${p}">${escapeHtml(val||"")}</textarea>`
      : `<input data-f="${k}" value="${v}" placeholder="${p}"/>`;
    return `<div class="field"><label>${l}</label>${ctrl}</div>`;
  };

  // 1) Identity + contact
  let html = `<div class="card rs-card">
    <div class="rs-head"><span class="rs-no">I.</span><h3>Identity</h3><span class="rule-dot"></span></div>
    ${F("name","Full name",resumeData.name,"Jordan Avery Rivera")}
    ${F("target","Target position",resumeData.target,o.roleEx)}
    <div class="rs-grid2">
      ${RESUME_CONTACT.map(f => F(f.k,f.l,resumeData[f.k],f.ph(o))).join("")}
    </div>
  </div>`;

  // 2) Professional summary
  html += `<div class="card rs-card">
    <div class="rs-head"><span class="rs-no">II.</span><h3>Professional Summary</h3><span class="rule-dot"></span></div>
    ${F("summary","Summary",resumeData.summary,"3–4 lines that frame who you are and your strongest proof.","t")}
  </div>`;

  // 3) Repeatable sections
  let roman = 3;
  RESUME_SECTION_ORDER.forEach(sec => {
    const cfg = RESUME_SECTIONS[sec], rows = resumeData[sec];
    html += `<div class="card rs-card">
      <div class="rs-head"><span class="rs-no">${toRoman(roman++)}.</span><h3>${cfg.label}</h3><span class="rule-dot"></span></div>
      ${rows.map((row, i) => entryHtml(sec, cfg, row, i, rows.length)).join("")}
      <button class="rs-add" data-add="${sec}">+ Add ${cfg.entryLabel.toLowerCase()}</button>
    </div>`;
  });

  // 4) Skills / Languages / References
  html += `<div class="card rs-card">
    <div class="rs-head"><span class="rs-no">${toRoman(roman++)}.</span><h3>Skills &amp; More</h3><span class="rule-dot"></span></div>
    ${F("skills","Skills — comma or line separated",resumeData.skills,o.skillEx,"t")}
    ${F("languages","Languages",resumeData.languages,"English (native), Spanish (fluent)","t")}
    ${F("references","References",resumeData.references,"Available upon request","t")}
  </div>`;

  $('#resumeForm').innerHTML = html;
  renderResumePreview();
}

function entryHtml(sec, cfg, row, i, total){
  const fields = cfg.fields.map(f => {
    const v = escapeAttr(row[f.k] || ""), p = escapeAttr(f.ph ? f.ph(OCCUPATIONS[store.occ]) : "");
    const ctrl = f.w === "t"
      ? `<textarea data-sec="${sec}" data-i="${i}" data-k="${f.k}" placeholder="${p}">${escapeHtml(row[f.k]||"")}</textarea>`
      : `<input data-sec="${sec}" data-i="${i}" data-k="${f.k}" value="${v}" placeholder="${p}"/>`;
    const cls = f.w === "t" ? "field" : "field";
    return `<div class="${cls}" style="${f.w==='h'?'':'grid-column:1/-1'}"><label>${f.l}</label>${ctrl}</div>`;
  }).join("");
  return `<div class="rs-entry">
    <div class="rs-entry-head">
      <span class="rs-entry-label">${cfg.entryLabel} ${i+1}</span>
      <div class="rs-entry-tools">
        <button class="rs-iconbtn" title="Move up" data-up="${sec}" data-i="${i}" ${i===0?"disabled":""}>${ICO_UP}</button>
        <button class="rs-iconbtn" title="Move down" data-down="${sec}" data-i="${i}" ${i===total-1?"disabled":""}>${ICO_DOWN}</button>
        <button class="rs-iconbtn danger" title="Remove" data-del="${sec}" data-i="${i}">${ICO_X}</button>
      </div>
    </div>
    <div class="rs-grid2">${fields}</div>
  </div>`;
}

/* ---- PREVIEW RENDER (cheap; called on every keystroke) ------------------- */
function renderResumePreview(){
  const d = resumeData;
  const has = v => v && String(v).trim() !== "";
  const lines = v => String(v||"").split("\n").map(s => s.trim()).filter(Boolean);
  const E = escapeHtml;

  // contact line
  const contact = [d.phone, d.email, d.location, d.website, d.linkedin].filter(has)
    .map(x => `<span>${E(x)}</span>`).join("");

  let body = "";
  const anything = has(d.name) || has(d.summary) || contact ||
    RESUME_SECTION_ORDER.some(s => d[s].some(r => Object.values(r).some(has))) ||
    has(d.skills) || has(d.languages) || has(d.references);

  if(!anything){
    $('#resumeSheet').innerHTML = `<div class="r-empty">Your résumé previews here as you type.</div>`;
    return;
  }

  // header
  body += `<div class="r-head-block">
    ${has(d.name) ? `<div class="r-name">${E(d.name)}</div>` : ""}
    ${has(d.target) ? `<div class="r-target">${E(d.target)}</div>` : ""}
    ${contact ? `<div class="r-contact">${contact}</div>` : ""}
  </div>`;

  if(has(d.summary)) body += section("Summary", `<div class="r-summary">${E(d.summary)}</div>`);

  // Experience
  body += repeatable(d.experience, "Experience", r => itemBlock({
    role: r.title, org: [r.company, r.location].filter(has).join(" · "),
    meta: [r.start, r.end].filter(has).join(" – "), bullets: lines(r.bullets),
  }));
  // Education
  body += repeatable(d.education, "Education", r => itemBlock({
    role: r.degree, org: [r.school, r.location].filter(has).join(" · "),
    meta: [r.start, r.end].filter(has).join(" – "), bullets: lines(r.details),
  }));
  // Projects
  body += repeatable(d.projects, "Projects", r => itemBlock({
    role: r.name, org: [r.role, r.link].filter(has).join(" · "),
    meta: "", bullets: lines(r.description),
  }));
  // Certifications (compact inline)
  body += repeatable(d.certifications, "Certifications", r => itemBlock({
    role: r.name, org: r.issuer, meta: r.date, bullets: [],
  }));
  // Awards
  body += repeatable(d.awards, "Awards", r => itemBlock({
    role: r.name, org: r.issuer, meta: r.date, bullets: [],
  }));
  // Volunteer
  body += repeatable(d.volunteer, "Volunteer", r => itemBlock({
    role: r.role, org: r.org, meta: [r.start, r.end].filter(has).join(" – "), bullets: lines(r.description),
  }));

  // Skills / Languages / References (inline, separated)
  const inline = v => E(String(v).split(/[\n,]/).map(s=>s.trim()).filter(Boolean).join("  ·  "));
  if(has(d.skills))     body += section("Skills", `<div class="r-inline">${inline(d.skills)}</div>`);
  if(has(d.languages))  body += section("Languages", `<div class="r-inline">${inline(d.languages)}</div>`);
  if(has(d.references)) body += section("References", `<div class="r-inline">${E(d.references)}</div>`);

  $('#resumeSheet').innerHTML = body;

  // helpers (closures)
  function section(title, inner){ return `<div class="r-section"><h4>${title}</h4>${inner}</div>`; }
  function repeatable(rows, title, fn){
    const valid = rows.filter(r => Object.values(r).some(has));
    if(!valid.length) return "";
    return section(title, valid.map(fn).join(""));
  }
  function itemBlock({role, org, meta, bullets}){
    return `<div class="r-item">
      <div class="r-item-top">
        <div>${has(role)?`<span class="r-role">${E(role)}</span>`:""}${has(org)?` <span class="r-org">— ${E(org)}</span>`:""}</div>
        ${has(meta)?`<span class="r-meta">${E(meta)}</span>`:""}
      </div>
      ${bullets.length?`<ul>${bullets.map(b=>`<li>${E(b)}</li>`).join("")}</ul>`:""}
    </div>`;
  }
}

/* ---- EXPORTS ------------------------------------------------------------- */
// Clean plain text (clipboard + the basis for the .doc body)
function resumeToText(){
  const d = resumeData, out = [], has = v => v && String(v).trim() !== "";
  const lines = v => String(v||"").split("\n").map(s=>s.trim()).filter(Boolean);
  if(has(d.name)) out.push(d.name.toUpperCase());
  if(has(d.target)) out.push(d.target);
  const contact = [d.phone,d.email,d.location,d.website,d.linkedin].filter(has).join("  |  ");
  if(contact) out.push(contact);
  const head = t => { out.push("", t.toUpperCase(), "—".repeat(t.length+2)); };
  if(has(d.summary)){ head("Summary"); out.push(d.summary); }

  const sec = (rows, title, fmt) => {
    const valid = rows.filter(r => Object.values(r).some(has));
    if(!valid.length) return;
    head(title);
    valid.forEach(r => fmt(r, lines));
  };
  sec(d.experience,"Experience",(r,L)=>{
    out.push(`${[r.title,r.company,r.location].filter(has).join(" — ")}${has(r.start)||has(r.end)?`  (${[r.start,r.end].filter(has).join(" – ")})`:""}`);
    L(r.bullets).forEach(b=>out.push(`  • ${b}`));
  });
  sec(d.education,"Education",(r,L)=>{
    out.push(`${[r.degree,r.school,r.location].filter(has).join(" — ")}${has(r.start)||has(r.end)?`  (${[r.start,r.end].filter(has).join(" – ")})`:""}`);
    L(r.details).forEach(b=>out.push(`  • ${b}`));
  });
  sec(d.projects,"Projects",(r,L)=>{
    out.push([r.name,r.role,r.link].filter(has).join(" — "));
    L(r.description).forEach(b=>out.push(`  • ${b}`));
  });
  sec(d.certifications,"Certifications",(r)=>out.push(`${[r.name,r.issuer].filter(has).join(" — ")}${has(r.date)?`  (${r.date})`:""}`));
  sec(d.awards,"Awards",(r)=>out.push(`${[r.name,r.issuer].filter(has).join(" — ")}${has(r.date)?`  (${r.date})`:""}`));
  sec(d.volunteer,"Volunteer",(r,L)=>{
    out.push(`${[r.role,r.org].filter(has).join(" — ")}${has(r.start)||has(r.end)?`  (${[r.start,r.end].filter(has).join(" – ")})`:""}`);
    L(r.description).forEach(b=>out.push(`  • ${b}`));
  });
  const inline = v => String(v).split(/[\n,]/).map(s=>s.trim()).filter(Boolean).join(", ");
  if(has(d.skills)){ head("Skills"); out.push(inline(d.skills)); }
  if(has(d.languages)){ head("Languages"); out.push(inline(d.languages)); }
  if(has(d.references)){ head("References"); out.push(d.references); }
  return out.join("\n");
}

// Word-openable .doc (HTML body + msword MIME). Opens & saves as .docx in Word,
// Google Docs, Pages — no library needed.
function resumeToDoc(){
  const sheet = $('#resumeSheet').innerHTML;
  const css = `body{font-family:Calibri,Arial,sans-serif;color:#1f1a12;font-size:11pt;line-height:1.4}
    .r-name{font-size:20pt;font-weight:bold}
    .r-target{font-size:10pt;letter-spacing:1px;text-transform:uppercase;color:#555}
    .r-contact span{margin-right:14px;font-size:9.5pt;color:#444}
    .r-section{margin-top:14pt}
    .r-section h4{font-size:11pt;text-transform:uppercase;border-bottom:1px solid #999;padding-bottom:2pt;margin:0 0 6pt}
    .r-item{margin-bottom:8pt}.r-role{font-weight:bold}.r-org{color:#555}
    .r-meta{color:#777;font-size:9.5pt;float:right}
    ul{margin:4pt 0 0 16pt;padding:0}li{font-size:10pt;margin-bottom:1pt}
    .r-summary,.r-inline{font-size:10pt}`;
  return `<!DOCTYPE html><html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word'>
<head><meta charset="utf-8"><title>Résumé</title><style>${css}</style></head>
<body>${sheet}</body></html>`;
}

function downloadBlob(content, filename, mime){
  const blob = new Blob([content], { type: mime });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url; a.download = filename;
  document.body.appendChild(a); a.click();
  document.body.removeChild(a);
  setTimeout(() => URL.revokeObjectURL(url), 1500);
}
function resumeFilename(ext){ return ((resumeData.name||"resume").trim().replace(/[^\w]+/g,"_").replace(/^_+|_+$/g,"") || "resume") + "." + ext; }

/* ---- helpers -------------------------------------------------------------- */
function toRoman(n){
  const map = [[10,"X"],[9,"IX"],[5,"V"],[4,"IV"],[1,"I"]];
  let s = ""; for(const [v,sym] of map){ while(n>=v){ s+=sym; n-=v; } } return s;
}

/* ---- icons --------------------------------------------------------------- */
const ICO_UP   = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 14 6-6 6 6"/></svg>';
const ICO_DOWN = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 10 6 6 6-6"/></svg>';
const ICO_X    = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M18 6 6 18M6 6l12 12"/></svg>';

/* ---- INIT: bind delegated events once ------------------------------------ */
function initResumeBuilder(){
  loadResume();
  const form = $('#resumeForm');

  // typing → update model, autosave, refresh preview (NOT the form, to keep focus)
  form.addEventListener("input", e => {
    const t = e.target;
    if(t.dataset.f !== undefined){ resumeData[t.dataset.f] = t.value; }
    else if(t.dataset.sec !== undefined){ resumeData[t.dataset.sec][+t.dataset.i][t.dataset.k] = t.value; }
    else return;
    saveResume();
    renderResumePreview();
  });

  // structural actions → mutate arrays, autosave, full re-render
  form.addEventListener("click", e => {
    const add = e.target.closest("[data-add]");
    const del = e.target.closest("[data-del]");
    const up  = e.target.closest("[data-up]");
    const dn  = e.target.closest("[data-down]");
    if(add){ resumeData[add.dataset.add].push(blankEntry(add.dataset.add)); }
    else if(del){ resumeData[del.dataset.del].splice(+del.dataset.i, 1); }
    else if(up){ const s=up.dataset.up, i=+up.dataset.i; if(i>0) [resumeData[s][i-1],resumeData[s][i]]=[resumeData[s][i],resumeData[s][i-1]]; }
    else if(dn){ const s=dn.dataset.down, i=+dn.dataset.i; const a=resumeData[s]; if(i<a.length-1) [a[i+1],a[i]]=[a[i],a[i+1]]; }
    else return;
    saveResume();
    renderResume();
  });

  // exports
  $('#rsPrint').addEventListener("click", () => window.print());
  $('#rsCopy').addEventListener("click",  () => copyText(resumeToText(), "Résumé text copied"));
  $('#rsDoc').addEventListener("click",   () => { downloadBlob(resumeToDoc(), resumeFilename("doc"), "application/msword"); toast("Word document downloaded"); });
}
