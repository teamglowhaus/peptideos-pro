/* =========================================================================
   CAREER OS — COVER LETTER BUILDER  (Phase 8)
   -------------------------------------------------------------------------
   The Résumé Builder's companion: a dedicated form with a live one-page
   letter preview and the same three offline exports (Print/PDF, plain text,
   Word .doc). Distinct from the "Cover Letter" prompt tool in modules.js —
   that one composes a prompt for an AI to draft one; this one lets you
   write, edit, and export an actual letter yourself. Vanilla JS, no
   external libraries.

   Loaded before app.js (after resume.js, so downloadBlob/copyText/toast/$
   are guaranteed to exist by the time any of this runs). app.js calls
   initCoverLetterBuilder() once and navigates via showView('coverletter')
   + renderCoverLetter().
   ========================================================================= */

/* ---- Nav registration: a custom view, not a prompt tool ------------------ */
const COVERLETTER_MODULE = {
  id:"coverletter", group:"Build", name:"Cover Letter Builder", tag:"Build", custom:true,
  intro:"Write and format an actual cover letter with a live preview, print, text & Word export.",
  icon:'<path d="M4 4h16v16H4z"/><path d="m4 7 8 6 8-6"/><path d="M4 20l6-6M20 20l-6-6"/>',
};

/* ---- Data model ------------------------------------------------------------
   One namespaced key holds one letter (no profiles yet — the Résumé
   Builder's profile switcher is the natural next step if this needs it). */
function defaultCoverLetter(){
  return {
    name:"", phone:"", email:"", location:"", linkedin:"",
    date:"", hiringManager:"", company:"", companyAddress:"", role:"",
    salutation:"", opening:"", body:"", closing:"", signoff:"Sincerely,",
  };
}
let clData = null;

function loadCoverLetter(){
  const saved = store.coverletter;
  clData = Object.assign(defaultCoverLetter(), saved || {});
}
function saveCoverLetter(){ store.coverletter = clData; }   // autosave through the one store

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

  let html = `<div class="card rs-card">
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

  const anything = has(d.name) || has(d.company) || has(d.salutation) || has(d.opening) || has(d.body) || has(d.closing);
  if(!anything){
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
   loads first, so they're already global by the time this ever runs). */
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
    saveCoverLetter();
    renderCoverLetterPreview();
  });

  $('#clPrint').addEventListener("click", () => window.print());
  $('#clCopy').addEventListener("click",  () => copyText(coverLetterToText(), "Cover letter text copied"));
  $('#clDoc').addEventListener("click",   () => { downloadBlob(coverLetterToDoc(), coverLetterFilename("doc"), "application/msword"); toast("Word document downloaded"); });
}
