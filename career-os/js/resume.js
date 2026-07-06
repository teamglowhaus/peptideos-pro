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

/* ---- EXAMPLE RÉSUMÉS (Phase 7 — "Load example") ---------------------------
   One fully-written, occupation-aware example per edition. "Load example"
   drops a finished résumé into the builder so a buyer can see, edit, and
   export a real result immediately instead of starting from a blank form.
   No AI call, no network — this is plain bundled data, same as OCCUPATIONS. */
const RESUME_EXAMPLES = {
  general: Object.assign(defaultResume(), {
    name:"Jordan Avery Rivera", phone:"(555) 214-7790", email:"jordan.rivera@email.com", location:"Denver, CO",
    linkedin:"linkedin.com/in/jordanrivera",
    target:"Senior Project Manager",
    summary:"Senior Project Manager with 7 years leading cross-functional teams through complex, multi-stakeholder programs. Known for turning ambiguous initiatives into shipped results on time and under budget.",
    skills:"Stakeholder management, Agile & Scrum, budgeting & forecasting, risk management, roadmapping, cross-functional leadership",
    experience:[
      {title:"Senior Project Manager", company:"Meridian Partners", location:"Denver, CO", start:"Jun 2021", end:"Present",
        bullets:"Led a 12-person cross-functional team to launch a company-wide CRM migration 3 weeks ahead of schedule\nCut project cycle time 28% by introducing a lightweight Agile cadence across 4 departments\nManaged a $1.4M annual program budget with zero overruns across 9 concurrent initiatives"},
      {title:"Project Coordinator", company:"Northline Group", location:"Denver, CO", start:"Aug 2018", end:"May 2021",
        bullets:"Coordinated 15+ concurrent client projects, maintaining a 96% on-time delivery rate\nBuilt the team's first standardized intake process, cutting kickoff time from 2 weeks to 3 days"},
    ],
    education:[{degree:"B.A. Business Administration", school:"Front Range State University", location:"Boulder, CO", start:"2014", end:"2018", details:""}],
    certifications:[{name:"PMP", issuer:"Project Management Institute", date:"2022"}],
  }),
  nurse: Object.assign(defaultResume(), {
    name:"Jordan A. Rivera", phone:"(555) 213-8890", email:"jordan.rivera@email.com", location:"Austin, TX",
    linkedin:"linkedin.com/in/jrivera",
    target:"ICU Registered Nurse",
    summary:"ICU Registered Nurse with 6 years of critical-care experience across Level I trauma and cardiac units. Epic power user who mentors new-graduate nurses and leads rapid-response protocol.",
    skills:"Critical care, Epic/EHR, ACLS, BLS, ventilator management, patient & family advocacy",
    experience:[
      {title:"Senior ICU Registered Nurse", company:"Hill Country Medical Center", location:"Austin, TX", start:"Jun 2021", end:"Present",
        bullets:"Precepted 11 new-graduate nurses, cutting orientation time 30%\nLed rapid-response coverage on a 24-bed ICU, maintaining a 0.9 falls-per-1,000-patient-days rate\nPartnered with physicians on a sepsis-protocol update that cut time-to-antibiotics 22%"},
      {title:"Registered Nurse, Cardiac Step-Down", company:"Lakeside Regional Medical Center", location:"Austin, TX", start:"Jul 2018", end:"May 2021",
        bullets:"Managed a 5–6 patient acute cardiac caseload per shift with zero medication errors\nTrained 8 new hires on telemetry monitoring and post-op cardiac care protocols"},
    ],
    education:[{degree:"B.S. Nursing", school:"Bluebonnet State University", location:"Austin, TX", start:"2014", end:"2018", details:""}],
    certifications:[{name:"ACLS", issuer:"American Heart Association", date:"2024"},{name:"CCRN", issuer:"AACN", date:"2023"}],
  }),
  swe: Object.assign(defaultResume(), {
    name:"Alex Chen", phone:"(555) 640-2210", email:"alex.chen@email.com", location:"San Francisco, CA",
    website:"alexchen.dev", linkedin:"linkedin.com/in/alexchen",
    target:"Senior Software Engineer",
    summary:"Senior backend engineer with 8 years building distributed systems at scale. Specializes in turning slow, brittle services into fast, reliable ones — and the teams that run them into ones that move faster too.",
    skills:"Go, Python, Kubernetes, AWS, PostgreSQL, distributed systems, CI/CD",
    experience:[
      {title:"Senior Software Engineer", company:"Bridgeline Payments", location:"Remote", start:"Mar 2020", end:"Present",
        bullets:"Cut p99 checkout latency from 2.4s to 0.8s, lifting conversion 12%\nReduced cloud spend $40K/yr by right-sizing infrastructure and automating scale-down\nLed the migration of a 6-year-old monolith's billing path to a Go microservice with zero downtime"},
      {title:"Software Engineer", company:"Vertex Equity Systems", location:"San Francisco, CA", start:"Jul 2016", end:"Feb 2020",
        bullets:"Built the internal deploy pipeline, cutting release time from 45 to 8 minutes\nShipped a rate-limiting service now handling 50M+ requests/day"},
    ],
    education:[{degree:"B.S. Computer Science", school:"Pacific Coast State University", location:"Berkeley, CA", start:"2012", end:"2016", details:""}],
    projects:[{name:"ratelimit-go", role:"Creator & maintainer", link:"github.com/example-dev/ratelimit-go", description:"Open-source token-bucket rate limiter used by 3 mid-size startups\n400+ GitHub stars"}],
  }),
  teacher: Object.assign(defaultResume(), {
    name:"Morgan Ellis", phone:"(555) 402-1187", email:"morgan.ellis@email.com", location:"Portland, OR",
    linkedin:"linkedin.com/in/morganellis",
    target:"5th Grade Lead Teacher",
    summary:"5th grade lead teacher with 6 years raising reading and math proficiency through differentiated, data-driven instruction. Builds classrooms where every student, including those below grade level, makes measurable growth.",
    skills:"Differentiated instruction, SEL, formative assessment, IEP collaboration, classroom technology",
    experience:[
      {title:"5th Grade Lead Teacher", company:"Maple Grove Elementary", location:"Portland, OR", start:"Aug 2019", end:"Present",
        bullets:"Raised reading proficiency 22% in one school year through small-group, data-driven differentiation\nDesigned a peer-mentoring program adopted school-wide across 6 classrooms\nSecured a $15,000 grant for classroom technology, funding 1:1 devices for 28 students"},
      {title:"4th Grade Teacher", company:"Lincoln Elementary", location:"Portland, OR", start:"Aug 2016", end:"Jun 2019",
        bullets:"Led a classroom of 26 students to the highest math growth scores in the grade level two years running"},
    ],
    education:[{degree:"M.Ed. Elementary Education", school:"Cascade State University", location:"Portland, OR", start:"2014", end:"2016", details:""}],
    certifications:[{name:"Oregon Teaching License", issuer:"Oregon TSPC", date:"2016"}],
  }),
  exec: Object.assign(defaultResume(), {
    name:"Morgan Lee", phone:"(555) 305-9902", email:"morgan.lee@email.com", location:"Chicago, IL",
    linkedin:"linkedin.com/in/morganlee",
    target:"VP of Operations",
    summary:"Operations executive who scales teams and P&L. Led a turnaround that lifted output 40% while cutting cost, and has integrated two acquisitions without disrupting service.",
    skills:"P&L ownership, org design, M&A integration, lean operations, strategy",
    experience:[
      {title:"VP of Operations", company:"Northwind Logistics", location:"Chicago, IL", start:"Jan 2019", end:"Present",
        bullets:"Grew EBITDA 35% ($1.2M to $1.6M) via a network redesign across 8 distribution centers\nIntegrated two acquisitions worth $40M combined with zero service disruption\nBuilt and scaled the operations team from 3 directors to 15 while cutting attrition 30%"},
      {title:"Director of Operations", company:"Fairview Supply Co.", location:"Chicago, IL", start:"Feb 2014", end:"Dec 2018",
        bullets:"Turned around an underperforming region, lifting output 40% in two quarters\nCut operating costs $250K/yr by renegotiating vendor contracts"},
    ],
    education:[{degree:"MBA", school:"Lakeshore School of Management", location:"Evanston, IL", start:"2010", end:"2012", details:""}],
    awards:[{name:"Operational Excellence Award", issuer:"Northwind Logistics", date:"2023"}],
  }),
};

// Checks EVERY field on the résumé (not a curated subset) — used to decide
// whether "Load example" needs to confirm before it overwrites anything.
function hasResumeContent(d){
  const has = v => v && String(v).trim() !== "";
  return Object.keys(defaultResume()).some(k => {
    const v = d[k];
    return Array.isArray(v) ? v.some(r => Object.values(r).some(has)) : has(v);
  });
}

// True while the builder holds unedited example data. Every field's every
// name/company/school is fictional, but it's polished enough to look like a
// finished, submittable résumé — so we keep a persistent banner (not just a
// toast) up until the user actually edits something, to head off someone
// exporting it as-is.
let exampleActive = false;

// Deep-clone so edits to the loaded example never mutate the shared template.
function loadExampleResume(){
  const example = RESUME_EXAMPLES[store.occ] || RESUME_EXAMPLES.general;
  if(hasResumeContent(resumeData) &&
     !confirm("Replace your current résumé with a filled-in example? You can edit every field afterward. This can't be undone.")) return;
  resumeData = JSON.parse(JSON.stringify(example));
  RESUME_SECTION_ORDER.forEach(s => { if(!Array.isArray(resumeData[s])) resumeData[s] = []; });
  exampleActive = true;
  saveResume();
  renderResume();
  toast("Example loaded — every name and detail is fictional, replace it all before you send this anywhere");
}

function renderExampleBanner(){
  const el = $('#resumeExampleBanner'); if(!el) return;
  el.innerHTML = !exampleActive ? "" : `
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 9v4M12 17h.01M10.3 3.9 2.5 17a2 2 0 0 0 1.7 3h15.6a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/></svg>
    <span><b>Sample content.</b> Every name, employer, and result here is fictional — replace all of it before exporting or sending this résumé anywhere.</span>`;
}

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

  renderExampleBanner();

  // contact line
  const contact = [d.phone, d.email, d.location, d.website, d.linkedin].filter(has)
    .map(x => `<span>${E(x)}</span>`).join("");

  let body = "";
  const anything = has(d.name) || has(d.summary) || contact ||
    RESUME_SECTION_ORDER.some(s => d[s].some(r => Object.values(r).some(has))) ||
    has(d.skills) || has(d.languages) || has(d.references);

  if(!anything){
    $('#resumeSheet').innerHTML = `<div class="r-empty">Your résumé previews here as you type.</div>`;
    renderResumeScore();
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
  renderResumeScore();

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
const ICO_CHECK= '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>';
const ICO_DOT  = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="3"/></svg>';

/* ---- RÉSUMÉ SCORE (Phase 7) ------------------------------------------------
   A live, fully offline checklist — the same rules taught in the Bonuses'
   "Résumé Checklist", now checked against the résumé actually being built.
   No AI call: plain pattern checks over resumeData. Recomputed on every
   preview render (cheap — a handful of small arrays). */
function bulletLines(rows){
  return (rows||[]).flatMap(r => String(r.bullets||"").split("\n").map(s => s.trim()).filter(Boolean));
}
const RESUME_CHECKS = [
  {label:"Contact info complete", test:d => {
    const has = v => v && String(v).trim() !== "";
    return has(d.name) && (has(d.phone) || has(d.email)) && has(d.location);
  }},
  {label:"Target position set", test:d => !!String(d.target||"").trim()},
  {label:"Professional summary written", test:d => String(d.summary||"").trim().length >= 40},
  {label:"At least one role with highlights", test:d => bulletLines(d.experience).length > 0},
  // The next two checks assess the QUALITY of highlights that already exist —
  // they pass vacuously when there are none, so "no highlights yet" shows up
  // as exactly one failing check (above), not three.
  {label:"Highlights show measurable impact", test:d => {
    const bullets = bulletLines(d.experience);
    if(!bullets.length) return true;
    return bullets.filter(b => /\d/.test(b)).length / bullets.length >= 0.5;
  }},
  {label:'No "Responsible for" openers', test:d => {
    const bullets = bulletLines(d.experience);
    if(!bullets.length) return true;
    return !bullets.some(b => /^responsible for/i.test(b));
  }},
  {label:"Skills listed", test:d => !!String(d.skills||"").trim()},
  {label:"Education listed", test:d => (d.education||[]).some(r => Object.values(r).some(v => v && String(v).trim() !== ""))},
  {label:"LinkedIn or portfolio link added", test:d => {
    const has = v => v && String(v).trim() !== "";
    return has(d.linkedin) || has(d.website);
  }},
];

function renderResumeScore(){
  const el = $('#resumeScore'); if(!el) return;
  const results = RESUME_CHECKS.map(c => ({ label:c.label, pass: c.test(resumeData) }));
  const passed = results.filter(r => r.pass).length;
  const pct = Math.round(passed / results.length * 100);
  el.innerHTML = `
    <div class="resume-score-head"><b>Résumé Score</b><span>${passed} / ${results.length}</span></div>
    <div class="resume-score-bar"><div class="resume-score-fill" style="width:${pct}%"></div></div>
    <p class="resume-score-note">A quick mechanical self-check, not a guarantee — your judgment still matters most.</p>
    <div class="rs-check-list">${results.map(r => `
      <div class="rs-check ${r.pass ? 'pass' : ''}">
        <span class="mark">${r.pass ? ICO_CHECK : ICO_DOT}</span>
        <span><span class="sr-only">${r.pass ? 'Passed: ' : 'Not yet: '}</span>${escapeHtml(r.label)}</span>
      </div>`).join("")}</div>`;
}

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
    exampleActive = false;
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
    exampleActive = false;
    saveResume();
    renderResume();
  });

  // exports
  $('#rsExample').addEventListener("click", loadExampleResume);
  $('#rsPrint').addEventListener("click", () => window.print());
  $('#rsCopy').addEventListener("click",  () => copyText(resumeToText(), "Résumé text copied"));
  $('#rsDoc').addEventListener("click",   () => { downloadBlob(resumeToDoc(), resumeFilename("doc"), "application/msword"); toast("Word document downloaded"); });
}
