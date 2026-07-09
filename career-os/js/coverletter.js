/* =========================================================================
   CAREER OS — COVER LETTER BUILDER  (Phase 8)
   -------------------------------------------------------------------------
   The Résumé Builder's companion: a dedicated form with a live one-page
   letter preview and the same three offline exports (Print/PDF, plain text,
   Word .doc). Distinct from the "Cover Letter" prompt tool in modules.js —
   that one composes a prompt for an AI to draft one; this one lets you
   write, edit, and export an actual letter yourself. Vanilla JS, no
   external libraries.

   Loaded before app.js (after resume.js, so downloadBlob/copyText/toast/$/
   newProfileId/escapeAttr/escapeHtml are guaranteed to exist by the time
   any of this runs). app.js calls initCoverLetterBuilder() once and
   navigates via showView('coverletter') + renderCoverLetter().
   ========================================================================= */

/* ---- Nav registration: a custom view, not a prompt tool ------------------ */
const COVERLETTER_MODULE = {
  id:"coverletter", group:"Build", name:"Cover Letter Builder", tag:"Build", custom:true,
  intro:"Write and format an actual cover letter with a live preview, print, text & Word export.",
  icon:'<path d="M4 4h16v16H4z"/><path d="m4 7 8 6 8-6"/><path d="M4 20l6-6M20 20l-6-6"/>',
};

/* ---- Data model ------------------------------------------------------------
   Multiple named, saved letters — mirrors the Résumé Builder's profile
   system exactly, so a letter can be kept per application/résumé profile
   instead of one overwriting the last. One namespaced key (`cos_coverletter`)
   holds every letter; `clData` always points at the ACTIVE letter's data
   object, so every existing function that reads/writes clData's properties
   in place (rather than reassigning the variable) keeps working unchanged. */
function defaultCoverLetter(){
  return {
    name:"", phone:"", email:"", location:"", linkedin:"",
    date:"", hiringManager:"", company:"", companyAddress:"", role:"",
    salutation:"", opening:"", body:"", closing:"", signoff:"Sincerely,",
  };
}
let clData = null;
let clStore = null;   // { activeId, profiles:[{id, name, isExample, data}] }

function activeCLProfile(){
  return clStore.profiles.find(p => p.id === clStore.activeId) || clStore.profiles[0];
}
function syncActiveCLData(){ clData = activeCLProfile().data; }

function createCLProfile(){
  const name = (prompt('Name this cover letter (e.g. "Acme Corp — PM role")', "Untitled letter") || "").trim();
  if(!name) return;
  const id = newProfileId();
  clStore.profiles.push({ id, name, isExample:false, data: defaultCoverLetter() });
  clStore.activeId = id;
  syncActiveCLData();
  saveCoverLetter();
  renderCoverLetter();
  toast("New cover letter created");
}
function duplicateCLProfile(){
  const src = activeCLProfile();
  const id = newProfileId();
  clStore.profiles.push({ id, name: src.name + " (copy)", isExample: !!src.isExample, data: JSON.parse(JSON.stringify(src.data)) });
  clStore.activeId = id;
  syncActiveCLData();
  saveCoverLetter();
  renderCoverLetter();
  toast("Cover letter duplicated");
}
function renameCLProfile(){
  const p = activeCLProfile();
  const name = (prompt("Rename this cover letter", p.name) || "").trim();
  if(!name) return;
  p.name = name;
  saveCoverLetter();
  renderCoverLetter();
}
function deleteCLProfile(){
  if(clStore.profiles.length <= 1){ toast("You need at least one cover letter"); return; }
  const p = activeCLProfile();
  if(!confirm(`Delete "${p.name}"? This can't be undone.`)) return;
  clStore.profiles = clStore.profiles.filter(x => x.id !== p.id);
  clStore.activeId = clStore.profiles[0].id;
  syncActiveCLData();
  saveCoverLetter();
  renderCoverLetter();
  toast("Cover letter deleted");
}

function hasCoverLetterContent(d){
  const has = v => v && String(v).trim() !== "";
  return has(d.name) || has(d.company) || has(d.salutation) || has(d.opening) || has(d.body) || has(d.closing);
}

// One-time migration: buyers who saved a letter before profiles existed had
// a flat letter object under this same key — fold it into profile 1 instead
// of losing it (same pattern as loadResume()'s cos_resume migration).
function loadCoverLetter(){
  const saved = store.coverletter;
  if(saved && Array.isArray(saved.profiles) && saved.profiles.length){
    clStore = saved;
  } else {
    const legacy = saved && !Array.isArray(saved.profiles) ? saved : null;
    const id = newProfileId();
    const data = Object.assign(defaultCoverLetter(), legacy || {});
    clStore = { activeId:id, profiles:[{ id, name:"My Cover Letter", isExample:false, data }] };
    if(legacy) saveCoverLetter();
  }
  syncActiveCLData();
}
function saveCoverLetter(){ store.coverletter = clStore; }   // autosave through the one store

/* ---- EXAMPLE LETTERS (Phase 8 follow-up) -----------------------------------
   One fully-written, occupation-aware example per edition, addressed to a
   fictional target company (deliberately distinct from the Résumé Builder's
   example employers, since a cover letter is addressed to somewhere you
   DON'T already work). Same "no AI call, plain bundled data" approach as
   RESUME_EXAMPLES in resume.js. */
const COVERLETTER_EXAMPLES = {
  general: Object.assign(defaultCoverLetter(), {
    name:"Jordan Avery Rivera", phone:"(555) 214-7790", email:"jordan.rivera@email.com", location:"Denver, CO",
    linkedin:"linkedin.com/in/jordanrivera",
    date:"January 1, 2026", hiringManager:"Taylor Nguyen", company:"Solstice Consulting Group",
    companyAddress:"400 Wynkoop St, Denver, CO", role:"Senior Project Manager",
    salutation:"Dear Taylor,",
    opening:"When I saw Solstice Consulting Group's opening for a Senior Project Manager, it read like a description of the work I already love doing: turning ambiguous, multi-stakeholder initiatives into shipped results on time and under budget.",
    body:"At Meridian Partners, I led a 12-person cross-functional team through a company-wide CRM migration, delivering it three weeks ahead of schedule, and introduced a lightweight Agile cadence across four departments that cut project cycle time 28%. I'd bring that same combination of structure and speed to Solstice's client engagements.",
    closing:"I'd welcome the chance to talk through how I could contribute to your team. Thank you for considering my application — I'm looking forward to hearing from you.",
    signoff:"Sincerely,",
  }),
  nurse: Object.assign(defaultCoverLetter(), {
    name:"Jordan A. Rivera", phone:"(555) 213-8890", email:"jordan.rivera@email.com", location:"Austin, TX",
    linkedin:"linkedin.com/in/jrivera",
    date:"January 1, 2026", hiringManager:"Casey Whitfield", company:"Riverbend General Hospital",
    companyAddress:"2100 River Rd, Austin, TX", role:"ICU Registered Nurse",
    salutation:"Dear Casey,",
    opening:"I'm writing to apply for the ICU Registered Nurse position at Riverbend General Hospital. With six years of critical-care experience across Level I trauma and cardiac units, I'm drawn to Riverbend's reputation for clinical excellence and mentorship.",
    body:"At Hill Country Medical Center, I precepted 11 new-graduate nurses, cutting orientation time 30%, and helped lead a sepsis-protocol update that cut time-to-antibiotics 22%. I'd bring that same mix of bedside skill and mentorship to Riverbend's ICU team.",
    closing:"I'd welcome the opportunity to discuss how my background fits your unit's needs. Thank you for your time and consideration.",
    signoff:"Sincerely,",
  }),
  swe: Object.assign(defaultCoverLetter(), {
    name:"Alex Chen", phone:"(555) 640-2210", email:"alex.chen@email.com", location:"San Francisco, CA",
    linkedin:"linkedin.com/in/alexchen",
    date:"January 1, 2026", hiringManager:"Sam Okafor", company:"Fernbridge Technologies",
    companyAddress:"88 Mission St, San Francisco, CA", role:"Senior Software Engineer",
    salutation:"Dear Sam,",
    opening:"Fernbridge Technologies' Senior Software Engineer posting immediately caught my attention — I've spent eight years turning slow, brittle backend services into fast, reliable ones, and that's exactly the kind of problem your team is hiring for.",
    body:"At Bridgeline Payments, I cut p99 checkout latency from 2.4s to 0.8s, lifting conversion 12%, and led the migration of a six-year-old billing monolith to a Go microservice with zero downtime. I'd bring that same systems-first approach to Fernbridge's platform team.",
    closing:"I'd love the chance to talk through your team's roadmap and where I could help. Thanks for your consideration.",
    signoff:"Best,",
  }),
  teacher: Object.assign(defaultCoverLetter(), {
    name:"Morgan Ellis", phone:"(555) 402-1187", email:"morgan.ellis@email.com", location:"Portland, OR",
    linkedin:"linkedin.com/in/morganellis",
    date:"January 1, 2026", hiringManager:"Dr. Priya Ramesh", company:"Willowmere School District",
    companyAddress:"900 Willow Ave, Portland, OR", role:"5th Grade Lead Teacher",
    salutation:"Dear Dr. Ramesh,",
    opening:"I'm excited to apply for the 5th Grade Lead Teacher position at Willowmere School District. Over six years in the classroom, I've focused on one thing above all: making sure every student, including those below grade level, makes measurable growth.",
    body:"At Maple Grove Elementary, I raised reading proficiency 22% in a single school year through small-group, data-driven differentiation, and designed a peer-mentoring program that was later adopted school-wide across six classrooms. I'd bring that same data-driven approach to Willowmere.",
    closing:"I'd welcome the opportunity to discuss how I could contribute to your school community. Thank you for your consideration.",
    signoff:"Warm regards,",
  }),
  exec: Object.assign(defaultCoverLetter(), {
    name:"Morgan Lee", phone:"(555) 305-9902", email:"morgan.lee@email.com", location:"Chicago, IL",
    linkedin:"linkedin.com/in/morganlee",
    date:"January 1, 2026", hiringManager:"Board Search Committee", company:"Anchorpoint Industries",
    companyAddress:"1 Anchorpoint Plaza, Chicago, IL", role:"VP of Operations",
    salutation:"Dear Search Committee,",
    opening:"I'm writing to express my interest in the VP of Operations role at Anchorpoint Industries. I've spent my career scaling teams and P&L, and I'm drawn to the scope of the turnaround Anchorpoint is positioned for.",
    body:"At Northwind Logistics, I grew EBITDA 35% via a network redesign across eight distribution centers and integrated two acquisitions worth $40M combined with zero service disruption. I'd bring that same operational discipline to Anchorpoint's next chapter.",
    closing:"I'd welcome a conversation about how my background aligns with your goals. Thank you for your time.",
    signoff:"Sincerely,",
  }),
};

function loadExampleCoverLetter(){
  const example = COVERLETTER_EXAMPLES[store.occ] || COVERLETTER_EXAMPLES.general;
  if(hasCoverLetterContent(clData) &&
     !confirm("Replace your current cover letter with a filled-in example? You can edit every field afterward. This can't be undone.")) return;
  Object.assign(clData, JSON.parse(JSON.stringify(example)));
  activeCLProfile().isExample = true;
  saveCoverLetter();
  renderCoverLetter();
  toast("Example loaded — every name and detail is fictional, replace it all before you send this anywhere");
}

function renderCLExampleBanner(){
  const el = $('#clExampleBanner'); if(!el) return;
  const isExample = !!(clStore && activeCLProfile().isExample);
  el.innerHTML = !isExample ? "" : `
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 9v4M12 17h.01M10.3 3.9 2.5 17a2 2 0 0 0 1.7 3h15.6a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/></svg>
    <span><b>Sample content.</b> Every name, employer, and result here is fictional — replace all of it before exporting or sending this letter anywhere.</span>`;
}

/* ---- FORM RENDER ----------------------------------------------------------- */
function renderCoverLetter(){
  if(!clData) loadCoverLetter();
  const o = OCCUPATIONS[store.occ];
  $('#pageTitle').textContent = "Cover Letter Builder";
  $('#pageSub').textContent   = o.tagline;

  const F = (k, l, val, ph, type) => {
    const v = escapeAttr(val || "");
    const p = escapeAttr(ph || "");
    const ctrl = type === "t"
      ? `<textarea data-clf="${k}" placeholder="${p}">${escapeHtml(val||"")}</textarea>`
      : `<input data-clf="${k}" value="${v}" placeholder="${p}"/>`;
    return `<div class="field"><label>${l}</label>${ctrl}</div>`;
  };

  // 0) Letter switcher — multiple named, saved letters (mirrors résumé profiles)
  let html = `<div class="card rs-card rs-profile-bar">
    <select id="clProfileSelect" aria-label="Cover letter">
      ${clStore.profiles.map(p => `<option value="${escapeAttr(p.id)}" ${p.id===clStore.activeId?'selected':''}>${escapeHtml(p.name)}</option>`).join("")}
    </select>
    <div class="rs-profile-actions">
      <button class="btn-sm btn-link" id="clpNew">+ New</button>
      <button class="btn-sm btn-link" id="clpDuplicate">Duplicate</button>
      <button class="btn-sm btn-link" id="clpRename">Rename</button>
      <button class="btn-sm btn-link" id="clpDelete" ${clStore.profiles.length<=1?'disabled':''}>Delete</button>
    </div>
  </div>`;

  html += `<div class="card rs-card">
    <div class="rs-head"><span class="rs-no">I.</span><h3>Your details</h3><span class="rule-dot"></span></div>
    ${F("name","Full name",clData.name,"Jordan Avery Rivera")}
    <div class="rs-grid2">
      ${F("phone","Phone",clData.phone,"(555) 123-4567")}
      ${F("email","Email",clData.email,"you@email.com")}
      ${F("location","Location",clData.location,"City, ST")}
      ${F("linkedin","LinkedIn (optional)",clData.linkedin,"linkedin.com/in/you")}
    </div>
  </div>`;

  html += `<div class="card rs-card">
    <div class="rs-head"><span class="rs-no">II.</span><h3>Recipient &amp; role</h3><span class="rule-dot"></span></div>
    ${F("date","Date",clData.date,"January 1, 2026")}
    ${F("role","Role &amp; company",clData.role,o.roleEx+" at [Company]")}
    <div class="rs-grid2">
      ${F("hiringManager","Hiring manager (optional)",clData.hiringManager,"Jordan Lee")}
      ${F("company","Company",clData.company,"Company name")}
    </div>
    ${F("companyAddress","Company address (optional)",clData.companyAddress,"123 Main St, City, ST")}
  </div>`;

  html += `<div class="card rs-card">
    <div class="rs-head"><span class="rs-no">III.</span><h3>The letter</h3><span class="rule-dot"></span></div>
    ${F("salutation","Salutation",clData.salutation,'Dear Hiring Manager,')}
    ${F("opening","Opening hook",clData.opening,"Why this role, why now — one strong opening line.","t")}
    ${F("body","Proof paragraph",clData.body,"The one result you're proud of that fits this role.","t")}
    ${F("closing","Closing",clData.closing,"A confident, low-pressure call to action.","t")}
    ${F("signoff","Sign-off",clData.signoff,"Sincerely,")}
  </div>`;

  $('#clForm').innerHTML = html;
  renderCoverLetterPreview();
}

/* ---- PREVIEW RENDER (cheap; called on every keystroke) --------------------- */
function renderCoverLetterPreview(){
  const d = clData;
  const has = v => v && String(v).trim() !== "";
  const E = escapeHtml;

  renderCLExampleBanner();

  if(!hasCoverLetterContent(d)){
    $('#clSheet').innerHTML = `<div class="r-empty">Your cover letter previews here as you type.</div>`;
    return;
  }

  const contact = [d.phone, d.email, d.location, d.linkedin].filter(has).map(x => `<span>${E(x)}</span>`).join("");
  const recipient = [d.hiringManager, d.company, d.companyAddress].filter(has).map(x => `<div>${E(x)}</div>`).join("");
  const para = v => has(v) ? `<p>${E(v).split("\n").filter(Boolean).join("</p><p>")}</p>` : "";

  $('#clSheet').innerHTML = `
    <div class="cl-header">
      ${has(d.name) ? `<div class="r-name">${E(d.name)}</div>` : ""}
      ${contact ? `<div class="r-contact">${contact}</div>` : ""}
    </div>
    ${has(d.date) ? `<div class="cl-date">${E(d.date)}</div>` : ""}
    ${recipient ? `<div class="cl-recipient">${recipient}</div>` : ""}
    <div class="cl-body">
      ${has(d.salutation) ? `<p>${E(d.salutation)}</p>` : ""}
      ${para(d.opening)}
      ${para(d.body)}
      ${para(d.closing)}
    </div>
    <div class="cl-signoff">
      ${has(d.signoff) ? `<p>${E(d.signoff)}</p>` : ""}
      ${has(d.name) ? `<p>${E(d.name)}</p>` : ""}
    </div>`;
}

/* ---- EXPORTS ---------------------------------------------------------------
   Reuses downloadBlob() and copyText() (both defined in resume.js, which
   loads first, so they're already global by the time this ever runs). All
   three are guarded on hasCoverLetterContent() so an empty letter can't be
   printed/copied/downloaded as the "previews here as you type" placeholder. */
function coverLetterToText(){
  const d = clData, out = [], has = v => v && String(v).trim() !== "";
  if(has(d.name)) out.push(d.name);
  const contact = [d.phone, d.email, d.location, d.linkedin].filter(has).join("  |  ");
  if(contact) out.push(contact);
  out.push("");
  if(has(d.date)) out.push(d.date, "");
  [d.hiringManager, d.company, d.companyAddress].filter(has).forEach(l => out.push(l));
  out.push("");
  if(has(d.salutation)) out.push(d.salutation, "");
  [d.opening, d.body, d.closing].filter(has).forEach(p => { out.push(p, ""); });
  if(has(d.signoff)) out.push(d.signoff);
  if(has(d.name)) out.push(d.name);
  return out.join("\n").replace(/\n{3,}/g, "\n\n").trim();
}

function coverLetterToDoc(){
  const sheet = $('#clSheet').innerHTML;
  const css = `body{font-family:Calibri,Arial,sans-serif;color:#1f1a12;font-size:11pt;line-height:1.5}
    .r-name{font-size:16pt;font-weight:bold}
    .r-contact span{margin-right:14px;font-size:9.5pt;color:#444}
    .cl-date{margin-top:16pt}
    .cl-recipient{margin-top:10pt}
    .cl-body{margin-top:16pt}
    .cl-body p{margin-bottom:12pt}
    .cl-signoff{margin-top:6pt}
    .cl-signoff p{margin:0}`;
  return `<!DOCTYPE html><html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word'>
<head><meta charset="utf-8"><title>Cover Letter</title><style>${css}</style></head>
<body>${sheet}</body></html>`;
}

function coverLetterFilename(ext){
  return ((clData.name||"cover-letter").trim().replace(/[^\w]+/g,"_").replace(/^_+|_+$/g,"") || "cover_letter") + "_cover_letter." + ext;
}

/* ---- INIT: bind delegated events once -------------------------------------- */
function initCoverLetterBuilder(){
  loadCoverLetter();
  const form = $('#clForm');

  form.addEventListener("input", e => {
    const t = e.target;
    if(t.dataset.clf === undefined) return;
    clData[t.dataset.clf] = t.value;
    activeCLProfile().isExample = false;
    saveCoverLetter();
    renderCoverLetterPreview();
  });

  form.addEventListener("click", e => {
    if(e.target.closest("#clpNew"))       { createCLProfile();     return; }
    if(e.target.closest("#clpDuplicate")) { duplicateCLProfile();  return; }
    if(e.target.closest("#clpRename"))    { renameCLProfile();     return; }
    if(e.target.closest("#clpDelete"))    { deleteCLProfile();     return; }
  });

  form.addEventListener("change", e => {
    if(e.target.id !== "clProfileSelect") return;
    clStore.activeId = e.target.value;
    syncActiveCLData();
    saveCoverLetter();
    renderCoverLetter();
  });

  $('#clExample').addEventListener("click", loadExampleCoverLetter);
  $('#clPrint').addEventListener("click", () => {
    if(!hasCoverLetterContent(clData)){ toast("Add some content first"); return; }
    window.print();
  });
  $('#clCopy').addEventListener("click", () => {
    if(!hasCoverLetterContent(clData)){ toast("Add some content first"); return; }
    copyText(coverLetterToText(), "Cover letter text copied");
  });
  $('#clDoc').addEventListener("click", () => {
    if(!hasCoverLetterContent(clData)){ toast("Add some content first"); return; }
    downloadBlob(coverLetterToDoc(), coverLetterFilename("doc"), "application/msword");
    toast("Word document downloaded");
  });
}
