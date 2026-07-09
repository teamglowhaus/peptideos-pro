/* =========================================================================
   CAREER OS — MODULES  (the tool definitions)
   -------------------------------------------------------------------------
   ONE renderer drives every tool. A tool is a single object in this array.
   The renderer reads `fields[]` to draw the form, and calls `buildPrompt()`
   on Generate. Adding another tool = one new object below. No view code
   ever changes — that is the whole product.

   ----- HOW TO ADD A NEW MODULE (copy an entry, edit the values) -----
   {
     id        unique slug (used in nav, routing, localStorage).
     group     section it lives under in the sidebar:
                 "Build"     — résumé / profile content
                 "Apply"     — outreach & application materials
                 "Interview" — interview preparation
                 "Track"     — offers, planning & career management
     name      label shown in nav, quick-start, and the module header.
     tag       tiny mono badge ("Draft", "Scan", "Prep"…).
     icon      inline SVG path string — drawn inside a 24×24 stroked <svg>.
     intro     one-line description shown under the title + on quick-start.
     fields    [] of form controls. Each field is:
                 { key, label, type:'input'|'textarea', ph:(occupation)=>string }
                 `ph` is a function so placeholders can be edition-aware
                 (e.g. ph:o=>o.roleEx shows the current edition's example role).
     buildPrompt(values, occupation) -> string
                 THE DELIVERABLE. Assembles a world-class, expert-persona
                 prompt from the user's inputs. `values` is { key: userText };
                 `occupation` is the active OCCUPATIONS entry, so every prompt
                 is edition-aware (persona, role examples, ATS keywording).
                 Always provide a sensible fallback for empty inputs.
   }

   The prompt is hidden by default — the output panel shows a "Prompt composed"
   success state with Copy / Open Claude / Open ChatGPT and a "View prompt"
   disclosure. The buyer never writes a prompt and isn't shown one unless asked.

   Convention used below: o.name = edition label (e.g. "Nursing"),
   o.roleEx = an example role, o.skillEx = example skills. Lean on these for
   occupation-aware keywording so one config serves every edition.
   ========================================================================= */

const MODULES = [

  /* ===================================================================== */
  /*  BUILD — résumé & profile content                                     */
  /* ===================================================================== */

  {
    id:"bullets", group:"Build", name:"Resume Bullets", tag:"Draft",
    icon:'<path d="M9 6h11M9 12h11M9 18h11M4 6h.01M4 12h.01M4 18h.01"/>',
    intro:"Turn a flat job duty into three metric-driven, recruiter-grade lines.",
    fields:[
      {key:"role", label:"Your role / title", type:"input",    ph:o=>o.roleEx},
      {key:"duty", label:"What you did",        type:"textarea", ph:_=>"e.g. Managed onboarding for new hires"},
      {key:"tools",label:"Scope, tools or numbers (optional)", type:"input", ph:_=>"e.g. team of 8, Workday, cut ramp time"},
    ],
    buildPrompt:(v,o)=>
`You are an elite executive resume writer and former Fortune 500 recruiter.

Rewrite the work activity below into THREE distinct, ATS-optimized resume bullet points for a ${v.role||o.roleEx}.

Activity: "${v.duty||'[describe what you did]'}"
Context / tools / scope: ${v.tools||'(none — infer conservative specifics; mark any invented number with [ ])'}

Rules:
- Start each with a strong, varied past-tense power verb (never "Responsible for").
- Quantify impact with a metric, %, $, time saved, or scale wherever credible.
- Formula: Action verb + task + tool/method + measurable result.
- One line each, under 30 words, no first person.
- Mirror language a ${o.name.toLowerCase()} hiring manager and an ATS scan for.

Return only the three bullets as a clean list.`
  },

  {
    id:"summary", group:"Build", name:"Professional Summary", tag:"Draft",
    icon:'<path d="M4 6h16M4 12h16M4 18h10"/>',
    intro:"A 3–4 line summary that hooks a recruiter in the first six seconds.",
    fields:[
      {key:"role",  label:"Target position", type:"input",    ph:o=>o.roleEx},
      {key:"years", label:"Years of experience", type:"input", ph:_=>"e.g. 8"},
      {key:"wins",  label:"Top achievements", type:"textarea", ph:_=>"e.g. grew revenue 40%, led a team of 12"},
      {key:"skills",label:"Core skills", type:"input", ph:o=>o.skillEx},
    ],
    buildPrompt:(v,o)=>
`You are a senior career strategist who writes resume summaries that get interviews.

Write a 3–4 sentence professional summary for a ${v.role||o.roleEx} with ${v.years||'X'} years of experience.

Signature achievements: ${v.wins||'[your biggest wins]'}
Core skills to weave in: ${v.skills||o.skillEx}

Rules:
- Open with a strong professional identity, not "Seeking a role where...".
- Lead with value and proof. Show, don't claim.
- Embed 4–6 keywords a ${o.name.toLowerCase()} ATS targets.
- Confident, specific, human — never buzzword soup.
- Third person implied (no "I").

Return three variations: (1) Standard, (2) Achievement-led, (3) Leadership-forward.`
  },

  {
    id:"skills", group:"Build", name:"Skills Section", tag:"Draft",
    icon:'<path d="M12 2 4 7v6c0 5 3.5 7.5 8 9 4.5-1.5 8-4 8-9V7z"/>',
    intro:"A balanced, ATS-friendly hard + soft skills section for your target role.",
    fields:[
      {key:"role", label:"Target position", type:"input", ph:o=>o.roleEx},
      {key:"have", label:"Skills you already have", type:"textarea", ph:o=>o.skillEx},
    ],
    buildPrompt:(v,o)=>
`Act as an ATS optimization specialist.

For a ${v.role||o.roleEx}, build a complete skills section.
Skills I already have: ${v.have||o.skillEx}

Deliver:
1. 8–10 HARD skills most scanned for this role (prioritize mine, then credible adjacents).
2. 5–6 SOFT skills phrased the way job descriptions phrase them.
3. 6 high-value KEYWORDS to place elsewhere in the resume.

Flag any skill I listed that's outdated for a ${o.name.toLowerCase()} role and suggest a modern replacement.`
  },

  {
    id:"achievements", group:"Build", name:"Achievement Quantifier", tag:"Draft",
    icon:'<path d="M8 21h8M12 17v4M7 4h10v3a5 5 0 0 1-10 0z"/><path d="M5 5H3v1a3 3 0 0 0 3 3M19 5h2v1a3 3 0 0 1-3 3"/>',
    intro:"Convert vague responsibilities into quantified, results-first achievements.",
    fields:[
      {key:"role", label:"Your role / title", type:"input", ph:o=>o.roleEx},
      {key:"resp", label:"Responsibilities (one per line)", type:"textarea", ph:_=>"Handled customer escalations\nTrained new staff"},
      {key:"context", label:"Any numbers you know (optional)", type:"input", ph:_=>"team size, budget, volume, time"},
    ],
    buildPrompt:(v,o)=>
`You are a resume impact analyst who turns ordinary duties into quantified achievements that recruiters remember.

For a ${v.role||o.roleEx}, transform each responsibility below into a results-first achievement.

Responsibilities:
${v.resp||'[list your responsibilities, one per line]'}
Known numbers: ${v.context||'(none — propose realistic metrics I could measure, wrapped in [brackets])'}

For each line, return:
- A rewritten achievement using the CAR formula (Challenge → Action → Result) in ONE bullet.
- The metric it leans on (%, $, time, volume, quality, satisfaction). If I gave no number, suggest the single most credible metric a ${o.name.toLowerCase()} role would track and mark it [like this].
- Vary the power verbs; never reuse one and never start with "Responsible for".

End with the 3 strongest bullets ranked, and one sentence on why each lands.`
  },

  {
    id:"tailor", group:"Build", name:"Resume Tailor", tag:"Scan",
    icon:'<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4 8.1 15.9M14.5 14.5 20 20M8.1 8.1 12 12"/>',
    intro:"Re-point your existing resume at one specific job description.",
    fields:[
      {key:"resume", label:"Your current resume / bullets", type:"textarea", ph:_=>"Paste your resume or key bullets…"},
      {key:"jd",     label:"Target job description", type:"textarea", ph:_=>"Paste the job posting…"},
    ],
    buildPrompt:(v,o)=>
`You are an ATS strategist and recruiter who tailors resumes to specific roles for a living.

Tailor my resume to this exact ${o.name.toLowerCase()} job description — without inventing experience.

=== MY RESUME ===
${v.resume||'[paste resume]'}

=== TARGET JOB DESCRIPTION ===
${v.jd||'[paste job description]'}

Deliver, in order:
1. ALIGNMENT SNAPSHOT — what already matches strongly.
2. REWRITE — up to 6 of my bullets rephrased to mirror the JD's language and priorities (keep them truthful; show before → after).
3. KEYWORDS TO ADD — exact terms from the JD I'm missing, with where to place each.
4. RE-ORDER — how to reorder sections/bullets so the most relevant proof is read first.
5. ONE-LINE SUMMARY rewritten for this specific role.

Be specific and surgical. Flag anything I should NOT claim without evidence.`
  },

  {
    id:"linkedin", group:"Build", name:"LinkedIn Optimizer", tag:"Profile",
    icon:'<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M7 10v7M7 7v.01M11 17v-4a2 2 0 0 1 4 0v4M11 17v-7"/>',
    intro:"A scroll-stopping LinkedIn headline and About section that gets you found.",
    fields:[
      {key:"role",  label:"Current or target role", type:"input", ph:o=>o.roleEx},
      {key:"about", label:"A few things about you", type:"textarea", ph:_=>"What you do, who you help, a proud result"},
      {key:"skills",label:"Specialties / skills", type:"input", ph:o=>o.skillEx},
    ],
    buildPrompt:(v,o)=>
`You are a LinkedIn personal-branding strategist who has grown senior ${o.name.toLowerCase()} profiles to recruiter-magnet status.

Build my LinkedIn profile copy as a ${v.role||o.roleEx}.
About me: ${v.about||'[a few details about your work and wins]'}
Specialties: ${v.skills||o.skillEx}

Deliver:
1. HEADLINE — 3 options under 220 characters, each keyword-rich for recruiter search and written for a human, not a robot.
2. ABOUT — a first-person About section (3 short paragraphs): hook, proof with specifics, and a clear "here's who I help / what's next" close.
3. SKILLS — the 10 skills to list for ${o.name.toLowerCase()} recruiter search, ranked.
4. FEATURED — 3 ideas for what to pin to the Featured section.

Confident, warm, specific. No "results-driven professional" clichés.`
  },

  {
    id:"brand", group:"Build", name:"Personal Brand Statement", tag:"Draft",
    icon:'<path d="M12 2 4 6v6c0 5 3.5 7.5 8 9 4.5-1.5 8-4 8-9V6z"/><path d="m9 12 2 2 4-4"/>',
    intro:"A one-line value proposition that says exactly why you, in seconds.",
    fields:[
      {key:"role",     label:"Your role / field", type:"input", ph:o=>o.roleEx},
      {key:"strength", label:"Your edge / strengths", type:"textarea", ph:_=>"What you're known for; what you do better than most"},
      {key:"audience", label:"Who you want to reach", type:"input", ph:_=>"e.g. hiring managers at mid-size hospitals"},
    ],
    buildPrompt:(v,o)=>
`You are an executive brand strategist who distills careers into one unforgettable line.

Craft a personal brand statement for a ${v.role||o.roleEx} aiming to reach ${v.audience||'hiring managers in my field'}.
My edge: ${v.strength||'[what you do better than most]'}

Deliver:
1. THE STATEMENT — one sentence (under 20 words) that names who I help, the outcome I create, and what makes me distinct.
2. THREE VARIATIONS — (a) bold, (b) warm, (c) understated-credible.
3. A 2-line "elevator" expansion of the strongest one.
4. Where to use it (resume header, LinkedIn, intros).

Make it specific to ${o.name.toLowerCase()} — no generic "passionate professional" filler.`
  },

  {
    id:"careerchange", group:"Build", name:"Career Change Translator", tag:"Pivot",
    icon:'<path d="M4 7h13l-3-3M20 17H7l3 3"/>',
    intro:"Translate experience from one field into the language of the one you want.",
    fields:[
      {key:"from", label:"Coming from (role/field)", type:"input", ph:_=>"e.g. classroom teacher"},
      {key:"to",   label:"Moving toward (role/field)", type:"input", ph:o=>o.roleEx},
      {key:"exp",  label:"What you've done", type:"textarea", ph:_=>"Key responsibilities, wins, projects"},
    ],
    buildPrompt:(v,o)=>
`You are a career-pivot coach who helps people move into ${o.name.toLowerCase()} roles from adjacent fields.

I'm moving FROM ${v.from||'[current field]'} TO ${v.to||o.roleEx}.
What I've done: ${v.exp||'[your experience]'}

Deliver:
1. TRANSFERABLE SKILLS MAP — for each relevant thing I've done, the equivalent value in the target field, in their words.
2. REFRAMED BULLETS — 4 resume bullets rewritten to read as if I belong in the new field (truthful, just re-languaged).
3. THE NARRATIVE — a 3-sentence "why I'm making this move" story that turns the pivot into a strength.
4. GAPS — the 2–3 most important things to learn or show to be credible, and the fastest way to signal each.

Be honest about what transfers and what doesn't.`
  },

  {
    id:"gaps", group:"Build", name:"Employment Gap Explainer", tag:"Draft",
    icon:'<rect x="3" y="4" width="18" height="17" rx="2"/><path d="M3 9h18M8 2v4M16 2v4M9 14h2M15 14h.01"/>',
    intro:"Confident, honest ways to frame a gap on the resume and in interviews.",
    fields:[
      {key:"reason", label:"Reason for the gap", type:"input", ph:_=>"e.g. caregiving, layoff, health, study"},
      {key:"length", label:"How long", type:"input", ph:_=>"e.g. 14 months"},
      {key:"during", label:"What you did during it (optional)", type:"textarea", ph:_=>"Courses, freelance, volunteering, skills kept current"},
    ],
    buildPrompt:(v,o)=>
`You are a career coach and former hiring manager who has placed many ${o.name.toLowerCase()} candidates with employment gaps.

Help me address a ${v.length||'[length]'} gap caused by: ${v.reason||'[reason]'}.
What I did during it: ${v.during||'(little to add — help me frame it honestly anyway)'}

Deliver:
1. RESUME — one neutral, confident line to place the gap (and whether to list it at all).
2. COVER LETTER — one sentence that addresses it briefly and pivots to value.
3. INTERVIEW — a 30-second spoken answer: honest, brief, no over-apologizing, ending forward-looking.
4. REFRAME — the genuine strengths or growth this period gave me that are relevant to a ${o.name.toLowerCase()} role.

Never advise lying. Keep it dignified and matter-of-fact.`
  },

  {
    id:"promotion", group:"Build", name:"Promotion & Raise Case", tag:"Draft",
    icon:'<path d="M3 17l6-6 4 4 7-7M14 8h6v6"/>',
    intro:"Build the evidence-based business case for a promotion or raise.",
    fields:[
      {key:"role", label:"Current role", type:"input", ph:o=>o.roleEx},
      {key:"wins", label:"What you've delivered", type:"textarea", ph:_=>"Results, scope growth, problems solved"},
      {key:"ask",  label:"The ask", type:"input", ph:_=>"e.g. promotion to Senior, +12% salary"},
    ],
    buildPrompt:(v,o)=>
`You are a compensation and promotion coach who prepares ${o.name.toLowerCase()} professionals for these conversations.

Build my case as a ${v.role||o.roleEx}. My ask: ${v.ask||'[promotion / raise]'}.
What I've delivered: ${v.wins||'[your results and expanded scope]'}

Deliver:
1. THE CASE — a one-page business case: scope I've grown into, quantified impact, and how I already operate at the next level.
2. EVIDENCE LIST — the 4–5 strongest proof points, each tied to business value.
3. THE SCRIPT — exactly how to open the conversation and state the ask with confidence.
4. OBJECTION HANDLING — responses to "not in the budget", "not yet", and "let's revisit later".

Anchor on value delivered, not tenure or need. Keep it collaborative, not combative.`
  },

  {
    id:"professional-bio", group:"Build", name:"Professional Bio", tag:"Draft",
    icon:'<circle cx="12" cy="8" r="4"/><path d="M4 20a8 8 0 0 1 16 0"/><path d="M2 12h3M19 12h3"/>',
    intro:"A polished bio in three lengths — for LinkedIn, a website, or a speaker intro.",
    fields:[
      {key:"name", label:"Name & role", type:"input", ph:o=>"Jordan Rivera, "+o.roleEx},
      {key:"use",  label:"Where it'll be used", type:"input", ph:_=>"e.g. LinkedIn, company site, conference intro"},
      {key:"highlights", label:"Highlights to include", type:"textarea", ph:_=>"Signature wins, expertise, credentials, a human detail"},
    ],
    buildPrompt:(v,o)=>
`You are a professional bio writer who crafts credible, human bios for ${o.name.toLowerCase()} professionals.

Write a bio for: ${v.name||'[name & role]'}, to be used on ${v.use||'[LinkedIn / website / intro]'}.
Highlights: ${v.highlights||'[your wins, expertise, credentials, a human detail]'}

Deliver THREE lengths, all in third person:
1. SHORT (~50 words) — a crisp one-paragraph bio.
2. MEDIUM (~100 words) — adds proof and specialty.
3. LONG (~200 words) — full story: what I do, who I help, signature results, credentials, and a closing human note.

Rules: open with a strong identity line (not "X is a…dedicated professional"), lead with value, weave in credible specifics, and keep the voice warm and confident. End the long version with one personable detail.`
  },

  /* ===================================================================== */
  /*  RÉSUMÉS — role-specific résumé builders                              */
  /* ===================================================================== */

  {
    id:"resume-careerchange", group:"Résumés", name:"Career Change Résumé", tag:"Résumé",
    icon:'<path d="M4 7h11M10 3 6 7l4 4M20 17H9M14 13l4 4-4 4"/>',
    intro:"A functional/hybrid résumé that reframes your past for a new field.",
    fields:[
      {key:"from", label:"Current field / role", type:"input", ph:_=>"e.g. classroom teacher"},
      {key:"to",   label:"Target role / field", type:"input", ph:o=>o.roleEx},
      {key:"exp",  label:"Experience & wins", type:"textarea", ph:_=>"Roles, responsibilities, results, projects"},
    ],
    buildPrompt:(v,o)=>
`You are a career-change résumé writer who gets people hired in new fields without relevant titles.

Build a full résumé moving FROM ${v.from||'[current field]'} TO ${v.to||o.roleEx}.
My experience: ${v.exp||'[roles, responsibilities, results]'}

Deliver a complete, truthful hybrid résumé:
1. TARGET TITLE + 3-line summary that frames me for the new field.
2. CORE SKILLS — the transferable skills that matter in ${v.to||o.roleEx}, in that field's language.
3. EXPERIENCE — my roles rewritten as achievement bullets emphasizing transferable impact (mark any invented metric with [ ]).
4. A short "Relevant Projects / Additional Qualifications" section to bridge gaps.
Explain in one line why the hybrid format helps me here. Keep it honest — reframe, don't fabricate.`
  },

  {
    id:"resume-executive", group:"Résumés", name:"Executive Résumé", tag:"Résumé",
    icon:'<path d="M3 20h18M6 20V10M18 20V10M4 10l8-6 8 6M9 20v-5h6v5"/>',
    intro:"A board-ready résumé built around leadership scope and P&L impact.",
    fields:[
      {key:"role",  label:"Target executive role", type:"input", ph:_=>"e.g. VP of Operations, COO"},
      {key:"scope", label:"Scope you own", type:"input", ph:_=>"team size, budget/P&L, regions, functions"},
      {key:"wins",  label:"Signature results", type:"textarea", ph:_=>"Transformations, growth, turnarounds, exits"},
    ],
    buildPrompt:(v,o)=>
`You are an executive résumé writer for C-suite and VP candidates.

Build a senior, board-ready résumé for a ${v.role||'[executive role]'}.
Scope I own: ${v.scope||'[team, budget/P&L, regions]'}
Signature results: ${v.wins||'[transformations, growth, turnarounds]'}

Deliver:
1. EXECUTIVE SUMMARY — a 3–4 line leadership brand statement (identity, scope, signature impact).
2. CORE COMPETENCIES — 8–10 executive competencies (P&L, org design, strategy, M&A, etc. as relevant).
3. EXPERIENCE — achievement bullets that lead with business outcomes ($, %, scale) and show scope of leadership, not tasks.
4. A "Selected Highlights" band of 3 marquee results.
Tone: confident, understated, quantified. No buzzword soup. Mark invented figures with [ ].`
  },

  {
    id:"resume-federal", group:"Résumés", name:"Federal Résumé", tag:"Résumé",
    icon:'<path d="M3 21h18M5 21V10M19 21V10M4 10l8-5 8 5M9 21v-6M12 21v-6M15 21v-6"/>',
    intro:"A USAJOBS-style federal résumé that mirrors the announcement.",
    fields:[
      {key:"series", label:"Job series / grade (if known)", type:"input", ph:_=>"e.g. 0343, GS-12"},
      {key:"announce", label:"Duties / announcement text", type:"textarea", ph:_=>"Paste key duties & qualifications from the posting"},
      {key:"exp", label:"Your experience", type:"textarea", ph:_=>"Roles, dates, hours/week, duties, results"},
    ],
    buildPrompt:(v,o)=>
`You are a federal résumé specialist who writes USAJOBS-compliant résumés that pass HR screening.

Build a federal résumé${v.series?` targeting ${v.series}`:''}.
Announcement duties/qualifications:
${v.announce||'[paste key duties & qualifications]'}
My experience: ${v.exp||'[roles, dates, hours/week, duties, results]'}

Deliver a federal-format résumé:
1. For each role: Title, Employer, Location, Month/Year–Month/Year, Hours per week, and (if applicable) Salary/Grade — then detailed duty + accomplishment statements.
2. Mirror the announcement's key words and required competencies explicitly (federal HR matches literally).
3. Include a "Specialized Experience" paragraph that maps my background to the qualification requirements.
4. Note anything I must add to be rated eligible (hours, dates, KSAs).
Federal résumés are detailed and long — do NOT trim to one page. Flag missing items with [ ].`
  },

  {
    id:"resume-healthcare", group:"Résumés", name:"Healthcare Résumé", tag:"Résumé",
    icon:'<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M12 8v8M8 12h8"/>',
    intro:"A clinical résumé that leads with licensure, units, and outcomes.",
    fields:[
      {key:"role", label:"Target role", type:"input", ph:_=>"e.g. ICU Registered Nurse"},
      {key:"creds", label:"Licenses & certifications", type:"input", ph:_=>"e.g. RN, BSN, ACLS, BLS, CCRN"},
      {key:"exp", label:"Clinical experience", type:"textarea", ph:_=>"Units, patient population, systems (EHR), results"},
    ],
    buildPrompt:(v,o)=>
`You are a healthcare résumé writer who places clinicians in competitive roles.

Build a clinical résumé for a ${v.role||'[clinical role]'}.
Licenses/certifications: ${v.creds||'[RN, BSN, ACLS…]'}
Experience: ${v.exp||'[units, patient population, EHR, results]'}

Deliver:
1. A LICENSURE & CERTIFICATIONS block up top (this gets read first in healthcare).
2. SUMMARY — 3 lines framing specialty, setting, and strengths.
3. CLINICAL EXPERIENCE — bullets naming unit/setting, patient acuity & ratios, systems (e.g. Epic/Cerner), and measurable outcomes (fall rates, satisfaction, throughput).
4. SKILLS — clinical + technical competencies employers scan for.
Keep it credible and specifics-driven. Mark any invented number with [ ].`
  },

  {
    id:"resume-it", group:"Résumés", name:"IT / Tech Résumé", tag:"Résumé",
    icon:'<rect x="3" y="4" width="18" height="13" rx="2"/><path d="M8 21h8M9 9l-2 2 2 2M15 9l2 2-2 2M12 21v-4"/>',
    intro:"An impact-first tech résumé tuned for ATS and engineering hiring.",
    fields:[
      {key:"role", label:"Target role", type:"input", ph:_=>"e.g. Senior Backend Engineer"},
      {key:"stack", label:"Tech stack / skills", type:"input", ph:_=>"languages, frameworks, cloud, tools"},
      {key:"exp", label:"Experience & projects", type:"textarea", ph:_=>"What you built, scale, impact"},
    ],
    buildPrompt:(v,o)=>
`You are a technical résumé writer who gets engineers past ATS and technical screens.

Build a résumé for a ${v.role||'[tech role]'}.
Stack/skills: ${v.stack||'[languages, frameworks, cloud, tools]'}
Experience & projects: ${v.exp||'[what you built, scale, impact]'}

Deliver:
1. SUMMARY — 3 lines: level, domain strengths, signature impact.
2. TECHNICAL SKILLS — grouped (Languages / Frameworks / Cloud & Infra / Data / Tools) and ATS-friendly.
3. EXPERIENCE — bullets in "accomplished X by doing Y, measured by Z" form: latency, throughput, uptime, cost, scale, users, deploy frequency.
4. PROJECTS — 2–3 with stack + outcome.
Prioritize quantified impact over task lists. Mark invented metrics with [ ].`
  },

  {
    id:"resume-teacher", group:"Résumés", name:"Teacher Résumé", tag:"Résumé",
    icon:'<path d="M3 7l9-4 9 4-9 4-9-4z"/><path d="M21 7v5M7 9v5c0 1 2.2 2.5 5 2.5s5-1.5 5-2.5V9"/>',
    intro:"An education résumé built on certification, pedagogy, and student outcomes.",
    fields:[
      {key:"role", label:"Role & level", type:"input", ph:_=>"e.g. 5th Grade Lead Teacher"},
      {key:"certs", label:"Certifications & endorsements", type:"input", ph:_=>"e.g. State cert, ESL endorsement"},
      {key:"exp", label:"Teaching experience", type:"textarea", ph:_=>"Grades/subjects, methods, results, initiatives"},
    ],
    buildPrompt:(v,o)=>
`You are an education résumé writer who helps teachers land the classrooms they want.

Build a résumé for a ${v.role||'[teaching role]'}.
Certifications/endorsements: ${v.certs||'[state cert, endorsements]'}
Experience: ${v.exp||'[grades/subjects, methods, results]'}

Deliver:
1. A CERTIFICATIONS & LICENSURE block near the top.
2. SUMMARY — 3 lines: level/subject, teaching philosophy in action, signature strength.
3. TEACHING EXPERIENCE — bullets showing grade/subject, instructional methods (differentiation, SEL, data-driven instruction), and measurable student outcomes (growth %, proficiency, engagement).
4. SKILLS/HIGHLIGHTS — curriculum, assessment, tech, family engagement, leadership.
Show classroom impact with specifics. Mark invented numbers with [ ].`
  },

  {
    id:"resume-student", group:"Résumés", name:"Student & New-Grad Résumé", tag:"Résumé",
    icon:'<path d="M4 5a2 2 0 0 1 2-2h11v16H6a2 2 0 0 0-2 2z"/><path d="M17 3v16"/>',
    intro:"An education-forward résumé that turns projects and internships into proof.",
    fields:[
      {key:"target", label:"Target role / field", type:"input", ph:o=>o.roleEx},
      {key:"edu", label:"Degree, school, grad date", type:"input", ph:_=>"e.g. B.S. Marketing, State U, 2026"},
      {key:"exp", label:"Projects, internships, activities", type:"textarea", ph:_=>"Coursework, projects, jobs, clubs, leadership"},
    ],
    buildPrompt:(v,o)=>
`You are an early-career résumé coach who helps students and new grads with little formal experience stand out.

Build a résumé targeting ${v.target||o.roleEx}.
Education: ${v.edu||'[degree, school, grad date]'}
Experience: ${v.exp||'[projects, internships, jobs, activities]'}

Deliver:
1. EDUCATION near the top (degree, school, grad date, relevant coursework, honors, GPA if strong).
2. SUMMARY — 2–3 lines framing potential + strongest proof (no "hardworking recent grad" clichés).
3. EXPERIENCE & PROJECTS — turn internships, class projects, part-time jobs, and leadership into achievement bullets with results.
4. SKILLS — the tools and abilities the target role scans for.
Lead with capability and evidence, not apology for limited experience. Mark invented metrics with [ ].`
  },

  {
    id:"resume-military", group:"Résumés", name:"Military Transition Résumé", tag:"Résumé",
    icon:'<path d="M8 4h8l-1 5a4 4 0 0 1-6 0z"/><path d="M12 13v4M9 21l3-2 3 2"/>',
    intro:"Translate service experience into civilian language employers understand.",
    fields:[
      {key:"service", label:"Branch, rank, MOS/rating", type:"input", ph:_=>"e.g. Army, SSG, 25B"},
      {key:"target", label:"Target civilian role", type:"input", ph:o=>o.roleEx},
      {key:"exp", label:"Duties, leadership & results", type:"textarea", ph:_=>"What you led, managed, maintained, achieved"},
    ],
    buildPrompt:(v,o)=>
`You are a military-to-civilian résumé translator who helps service members land civilian roles.

Build a civilian résumé. Background: ${v.service||'[branch, rank, MOS/rating]'}.
Target civilian role: ${v.target||o.roleEx}
Duties, leadership & results: ${v.exp||'[what you led, managed, achieved]'}

Deliver:
1. SUMMARY — 3 lines positioning me for the civilian role (no unexplained acronyms).
2. TRANSLATION — for each key duty/MOS responsibility, the plain-English civilian equivalent and the transferable skill it proves (leadership, logistics, ops, security, training).
3. EXPERIENCE — achievement bullets in civilian terms with scope (people led, budget/equipment value, readiness, outcomes).
4. A short note on how to phrase clearances/awards for a civilian employer.
Decode ALL jargon. Emphasize leadership and measurable impact. Mark invented figures with [ ].`
  },

  /* ===================================================================== */
  /*  APPLY — outreach & application materials                             */
  /* ===================================================================== */

  {
    id:"ats", group:"Apply", name:"ATS Audit", tag:"Scan",
    icon:'<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>',
    intro:"Paste your resume and a job posting. Get a keyword gap report and an action plan.",
    fields:[
      {key:"resume", label:"Your resume text", type:"textarea", ph:_=>"Paste your full resume…"},
      {key:"jd",     label:"Job description",  type:"textarea", ph:_=>"Paste the job posting…"},
    ],
    buildPrompt:(v,o)=>
`You are an ATS auditor used by corporate recruiters.

Compare my resume against this job description and produce a recruiter-grade gap report.

=== MY RESUME ===
${v.resume||'[paste resume]'}

=== JOB DESCRIPTION ===
${v.jd||'[paste job description]'}

Produce in order:
1. ESTIMATED ATS MATCH SCORE (0–100) + one line on the reasoning.
2. MISSING KEYWORDS — exact JD terms absent from my resume.
3. WEAK BULLETS — up to 5 vague/unquantified lines, each with a stronger rewrite.
4. MISSING SKILLS the role expects that I haven't shown.
5. ACTION PLAN — 5 prioritized fixes I can make in under an hour.

Be blunt and specific. No filler.`
  },

  {
    id:"cover", group:"Apply", name:"Cover Letter", tag:"Draft",
    icon:'<path d="M4 4h16v16H4z"/><path d="m4 7 8 6 8-6"/>',
    intro:"A tailored, non-robotic cover letter built from the role and one story.",
    fields:[
      {key:"role",  label:"Role & company", type:"input", ph:_=>"e.g. Marketing Lead at Notion"},
      {key:"why",   label:"Why this company?", type:"textarea", ph:_=>"What draws you to them specifically"},
      {key:"proof", label:"One proof story", type:"textarea", ph:_=>"A result you're proud of that fits"},
    ],
    buildPrompt:(v,o)=>
`You are a conversion copywriter who writes cover letters that sound human and get callbacks.

Write a cover letter for: ${v.role||'[role & company]'}.
Why I want them: ${v.why||'[your reason]'}
My proof story: ${v.proof||'[your story]'}

Rules:
- 3 short paragraphs, under 250 words.
- Open with a real hook — never "I am writing to apply for…".
- Paragraph 2 = the proof story with a measurable result.
- Warm, confident, specific to THIS company. No clichés.
- Sound like a sharp ${o.name.toLowerCase()} professional wrote it.

End with a confident, low-pressure call to action.`
  },

  {
    id:"followup", group:"Apply", name:"Application Follow-Up", tag:"Outreach",
    icon:'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    intro:"A polite, value-adding nudge after you've applied or interviewed.",
    fields:[
      {key:"role", label:"Role & company", type:"input", ph:_=>"e.g. RN, ICU at Mercy Health"},
      {key:"when", label:"How long since you applied/interviewed", type:"input", ph:_=>"e.g. 10 days"},
      {key:"note", label:"Anything to add (optional)", type:"input", ph:_=>"new cert, mutual contact, recent win"},
    ],
    buildPrompt:(v,o)=>
`You are a job-search coach who writes follow-ups recruiters actually reply to.

Write a follow-up email for the ${v.role||'[role & company]'} application, about ${v.when||'[time]'} after applying/interviewing.
Something to add: ${v.note||'(nothing new — keep it brief and gracious)'}

Rules:
- Under 120 words. Subject line included.
- Reaffirm specific interest and one reason I'm a strong ${o.name.toLowerCase()} fit.
- Add value or a light new detail if I gave one; otherwise stay short and warm.
- No guilt-tripping, no "just checking in" with nothing behind it.
- End with an easy next step.

Give one email plus one shorter variation.`
  },

  {
    id:"recruiter", group:"Apply", name:"Recruiter Outreach", tag:"Outreach",
    icon:'<circle cx="10" cy="8" r="4"/><path d="M3 20a7 7 0 0 1 13 0"/><circle cx="18" cy="15" r="3"/><path d="m20.4 17.4 1.6 1.6"/>',
    intro:"A cold message to a recruiter that earns a reply, not a ghost.",
    fields:[
      {key:"role",  label:"Role you're targeting", type:"input", ph:o=>o.roleEx},
      {key:"pitch", label:"Your 1-line pitch", type:"textarea", ph:_=>"Who you are + strongest proof"},
      {key:"name",  label:"Recruiter name (optional)", type:"input", ph:_=>"e.g. Priya"},
    ],
    buildPrompt:(v,o)=>
`You are a recruiter who receives dozens of cold messages a day and you know which ones get a reply.

Write a cold outreach message to ${v.name||'a recruiter'} about a ${v.role||o.roleEx} opportunity.
My pitch: ${v.pitch||'[who you are and your strongest proof]'}

Rules:
- Under 90 words. Skimmable in 5 seconds.
- Lead with relevance to a ${o.name.toLowerCase()} role and ONE concrete proof point.
- Make the ask small and specific (a quick chat, or whether they're hiring for X).
- No flattery dump, no life story, no "I'd be a great fit" without evidence.

Give a LinkedIn-DM version (under 300 characters) and a slightly longer email version with a subject line.`
  },

  {
    id:"referral", group:"Apply", name:"Referral Request", tag:"Outreach",
    icon:'<circle cx="9" cy="8" r="3.2"/><path d="M3 20a6 6 0 0 1 12 0"/><path d="M16 11h5M18.5 8.5 21 11l-2.5 2.5"/>',
    intro:"Ask a contact for a referral without making it awkward.",
    fields:[
      {key:"name", label:"Who you're asking", type:"input", ph:_=>"e.g. former manager, ex-colleague"},
      {key:"role", label:"Role & company", type:"input", ph:_=>"e.g. Staff Engineer at Stripe"},
      {key:"rel",  label:"Your relationship / context", type:"textarea", ph:_=>"How you know them; when you last spoke"},
    ],
    buildPrompt:(v,o)=>
`You are a networking coach who helps ${o.name.toLowerCase()} professionals ask for referrals gracefully.

Write a referral request to ${v.name||'[contact]'} for the ${v.role||'[role & company]'} position.
Our relationship: ${v.rel||'[how you know them]'}

Rules:
- Warm, specific, and easy to say yes (or no) to — no pressure.
- Remind them briefly of our connection and ONE thing that makes me a credible fit.
- Make it effortless for them: offer to send my resume and a 2-line blurb they can forward.
- Under 130 words.

Give the message plus the 2-line blurb they could paste into a referral.`
  },

  {
    id:"connect", group:"Apply", name:"Connection Note", tag:"Outreach",
    icon:'<path d="M9 12h6"/><path d="M10 8H7a4 4 0 0 0 0 8h3M14 8h3a4 4 0 0 1 0 8h-3"/>',
    intro:"A LinkedIn connection note people actually accept.",
    fields:[
      {key:"who",    label:"Who they are", type:"input", ph:_=>"e.g. Director of Nursing at a hospital you admire"},
      {key:"reason", label:"Why you're reaching out", type:"textarea", ph:_=>"Shared interest, their work, a genuine reason"},
    ],
    buildPrompt:(v,o)=>
`You are a networking strategist who writes connection notes with a high accept rate.

Write a LinkedIn connection note to ${v.who||'[the person]'}.
Genuine reason: ${v.reason||'[why you want to connect]'}

Rules:
- Under 300 characters (LinkedIn's limit). No fluff.
- Specific and personal — reference them, not a template.
- No pitch, no ask for a job — just an authentic reason to connect.
- Sound like a real ${o.name.toLowerCase()} peer, warm and concise.

Give two variations: one professional, one slightly more personable.`
  },

  {
    id:"jobdecoder", group:"Apply", name:"Job Posting Decoder", tag:"Scan",
    icon:'<path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h7"/><path d="M14 3v5h5"/><circle cx="16.5" cy="16.5" r="2.5"/><path d="m19 19 2 2"/>',
    intro:"Read between the lines of a job description before you apply.",
    fields:[
      {key:"jd", label:"Job description", type:"textarea", ph:_=>"Paste the full posting…"},
    ],
    buildPrompt:(v,o)=>
`You are a former ${o.name.toLowerCase()} recruiter who wrote and screened postings like this one. Decode what it really means.

=== JOB DESCRIPTION ===
${v.jd||'[paste the posting]'}

Deliver:
1. MUST-HAVES vs NICE-TO-HAVES — separate the true dealbreakers from the wish-list.
2. HIDDEN PRIORITIES — what the wording reveals they actually care most about.
3. KEYWORDS TO MIRROR — exact phrases to echo in my resume and interview.
4. RED / YELLOW FLAGS — signs of churn, scope creep, unrealistic expectations, or budget issues.
5. SMART QUESTIONS — 3 questions that show I read between the lines.

Be candid. If something reads as a red flag, say so plainly.`
  },

  {
    id:"whycompany", group:"Apply", name:"Company Research Brief", tag:"Prep",
    icon:'<rect x="4" y="3" width="12" height="18" rx="1"/><path d="M8 7h.01M12 7h.01M8 11h.01M12 11h.01M8 15h4"/>',
    intro:"A research plan and talking points so 'why us?' is never a stumble.",
    fields:[
      {key:"company", label:"Company", type:"input", ph:_=>"e.g. Cleveland Clinic"},
      {key:"role",    label:"Role", type:"input", ph:o=>o.roleEx},
    ],
    buildPrompt:(v,o)=>
`You are an interview-prep researcher. Build a company research brief for my interview at ${v.company||'[company]'} for a ${v.role||o.roleEx} role.

Using what you know (and clearly flagging anything I should verify on their site / recent news):
1. SNAPSHOT — what they do, who they serve, and how a ${o.name.toLowerCase()} role contributes to their mission.
2. WHY THEM — three specific, non-generic reasons to want THIS company, phrased as I could say them.
3. TALKING POINTS — recent moves, values, or challenges I can reference to sound informed.
4. WATCH-OUTS — anything publicly known I should be aware of.
5. VERIFY LIST — the 4 things to confirm myself before the interview (recent news, leadership, products, glassdoor themes).

Make "why this company?" answerable in 30 confident seconds.`
  },

  {
    id:"networking", group:"Apply", name:"Coffee Chat Request", tag:"Outreach",
    icon:'<path d="M4 8h14v4a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5z"/><path d="M18 9h2a2 2 0 0 1 0 4h-2M7 2v2M11 2v2M15 2v2"/>',
    intro:"Ask for a short informational chat that people are glad to say yes to.",
    fields:[
      {key:"who",    label:"Who you're asking", type:"input", ph:_=>"e.g. someone in a role you want"},
      {key:"common", label:"Common ground", type:"input", ph:_=>"same school, shared field, their post"},
      {key:"ask",    label:"What you hope to learn", type:"textarea", ph:_=>"Their path, the team, advice on breaking in"},
    ],
    buildPrompt:(v,o)=>
`You are a networking coach. Write a short message asking ${v.who||'[the person]'} for a 15-minute informational chat.
Common ground: ${v.common||'[shared connection or interest]'}
What I hope to learn: ${v.ask||'[their path / advice]'}

Rules:
- Under 110 words. Respect their time explicitly (15 minutes, their convenience).
- Lead with the genuine common ground, not the ask.
- Be clear I want insight/advice, NOT a job — that's what makes people say yes.
- Frame it around a ${o.name.toLowerCase()} interest so it feels relevant.

Give the message plus a one-line follow-up to send if they don't reply in a week.`
  },

  /* ===================================================================== */
  /*  INTERVIEW — preparation                                              */
  /* ===================================================================== */

  {
    id:"predict", group:"Interview", name:"Question Predictor", tag:"Prep",
    icon:'<circle cx="12" cy="10" r="7"/><path d="M9.6 9a2.4 2.4 0 0 1 4.8 0c0 1.5-2.4 2-2.4 3.4M12 16h.01M6 20h12"/>',
    intro:"The questions you're most likely to get — and why they're asked.",
    fields:[
      {key:"role",  label:"Role you're interviewing for", type:"input", ph:o=>o.roleEx},
      {key:"level", label:"Level / seniority (optional)", type:"input", ph:_=>"e.g. mid-level, senior, lead"},
      {key:"jd",    label:"Job description (optional)", type:"textarea", ph:_=>"Paste it for sharper predictions…"},
    ],
    buildPrompt:(v,o)=>
`You are an interview coach and hiring manager who has run hundreds of ${o.name.toLowerCase()} interviews.

Predict the questions I'm most likely to face for a ${v.role||o.roleEx}${v.level?` (${v.level})`:''}.
${v.jd?`Job description:\n${v.jd}`:'(No JD provided — base it on the role.)'}

Deliver 12 likely questions, grouped:
- BEHAVIORAL (4)
- ROLE / TECHNICAL specific to ${o.name.toLowerCase()} work (4)
- MOTIVATION & FIT (2)
- CURVEBALLS (2)

For each: one line on WHY they ask it and what a strong answer signals. Rank the 3 most important to prepare first.`
  },

  {
    id:"star", group:"Interview", name:"STAR Story Builder", tag:"Prep",
    icon:'<path d="m12 3 2.5 5.5L20 9l-4 4 1 6-5-3-5 3 1-6-4-4 5.6-.5z"/>',
    intro:"Turn one experience into a tight, compelling behavioral answer.",
    fields:[
      {key:"competency", label:"What it should demonstrate", type:"input", ph:_=>"e.g. leadership under pressure"},
      {key:"story", label:"The experience", type:"textarea", ph:_=>"What happened, what you did, how it ended"},
    ],
    buildPrompt:(v,o)=>
`You are a behavioral interview coach who builds crisp STAR answers for ${o.name.toLowerCase()} candidates.

Shape my experience into a STAR answer that demonstrates: ${v.competency||'[the trait/skill]'}.
The experience: ${v.story||'[describe what happened]'}

Deliver:
1. The polished answer, labeled Situation / Task / Action / Result — spoken-length (60–90 seconds), with a quantified or concrete Result.
2. A 20-second condensed version for when time is short.
3. The ONE follow-up question an interviewer is likely to ask next, and how to answer it.
4. Two phrases to cut if my draft rambles.

Keep it natural and confident — not robotic. If my Result is vague, suggest the strongest credible outcome marked [like this].`
  },

  {
    id:"pitch", group:"Interview", name:"\"Tell Me About Yourself\"", tag:"Prep",
    icon:'<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M6 11a6 6 0 0 0 12 0M12 17v4M9 21h6"/>',
    intro:"The 60-second answer that frames the whole interview in your favor.",
    fields:[
      {key:"role", label:"Role you're interviewing for", type:"input", ph:o=>o.roleEx},
      {key:"background", label:"Your background in brief", type:"textarea", ph:_=>"Where you are now, key wins, what's next"},
    ],
    buildPrompt:(v,o)=>
`You are an interview coach. Write my answer to "Tell me about yourself" for a ${v.role||o.roleEx} interview.
My background: ${v.background||'[your background and best wins]'}

Use the Present → Past → Future structure:
- PRESENT: who I am professionally now and a proof point.
- PAST: the most relevant experience that built me toward this role.
- FUTURE: why THIS ${o.name.toLowerCase()} role is the logical next step.

Rules:
- 60–90 seconds spoken (roughly 130–180 words). Conversational, not a recited resume.
- Open with a strong first line that isn't "So, I graduated from…".
- End by handing the conversation back to them.

Give the main version plus a 30-second short version.`
  },

  {
    id:"tough", group:"Interview", name:"Tough Questions Coach", tag:"Prep",
    icon:'<path d="M12 2 4 6v6c0 5 3.5 7.5 8 9 4.5-1.5 8-4 8-9V6z"/><path d="M10.4 9.4a1.6 1.6 0 0 1 3.2 0c0 1.1-1.6 1.4-1.6 2.6M12 15h.01"/>',
    intro:"Honest, non-defensive answers to the questions that trip people up.",
    fields:[
      {key:"role",  label:"Role", type:"input", ph:o=>o.roleEx},
      {key:"tricky",label:"The tricky question / topic", type:"textarea", ph:_=>"e.g. greatest weakness, why you left, a gap, why so many jobs"},
    ],
    buildPrompt:(v,o)=>
`You are an interview coach who specializes in the answers candidates dread.

For a ${v.role||o.roleEx} interview, help me handle: ${v.tricky||'[the tough question or topic]'}

Deliver:
1. STRATEGY — what the interviewer is really probing for, and the trap to avoid.
2. ANSWER — a sample spoken answer that is honest, brief, and ends on growth or strength (no over-apologizing, no canned "I'm a perfectionist").
3. THE PIVOT — the exact sentence that turns the answer toward value I bring.
4. TWO DON'TS — phrasings that would hurt me here.

Keep it authentic to a ${o.name.toLowerCase()} context. Confidence without spin.`
  },

  {
    id:"negotiate", group:"Interview", name:"Salary Negotiation Script", tag:"Script",
    icon:'<path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>',
    intro:"Word-for-word scripts to negotiate an offer with confidence.",
    fields:[
      {key:"role",   label:"Role", type:"input", ph:o=>o.roleEx},
      {key:"offer",  label:"Current offer", type:"input", ph:_=>"e.g. $95,000 base"},
      {key:"target", label:"Your target", type:"input", ph:_=>"e.g. $108,000"},
      {key:"leverage",label:"Your leverage (optional)", type:"textarea", ph:_=>"competing offer, in-demand skills, market data"},
    ],
    buildPrompt:(v,o)=>
`You are a compensation negotiation expert who coaches ${o.name.toLowerCase()} professionals to better offers without burning bridges.

The role: ${v.role||o.roleEx}. Current offer: ${v.offer||'[offer]'}. My target: ${v.target||'[target]'}.
My leverage: ${v.leverage||'(help me find credible leverage from market value and my strengths)'}

Deliver:
1. THE NUMBER — a brief on whether my target is reasonable and how to anchor it.
2. EMAIL SCRIPT — a counter-offer email: appreciative, specific, justified by value.
3. VERBAL SCRIPT — what to say live, including the pause after stating my number.
4. PUSHBACK — responses to "that's the max we can do", "it's not in budget", and "we don't usually negotiate".
5. BEYOND BASE — other levers to ask for (sign-on, PTO, title, start date, review timing).

Collaborative tone throughout. Never ultimatums unless I have a real competing offer.`
  },

  {
    id:"askthem", group:"Interview", name:"Questions to Ask Them", tag:"Prep",
    icon:'<path d="M21 12a8 8 0 0 1-11.6 7.1L3 21l1.9-6.4A8 8 0 1 1 21 12z"/><path d="M9.6 10a2.4 2.4 0 0 1 4.8 0c0 1.4-2.4 1.9-2.4 3M12 16h.01"/>',
    intro:"Sharp questions that show you're evaluating them, too.",
    fields:[
      {key:"role",    label:"Role", type:"input", ph:o=>o.roleEx},
      {key:"company", label:"Company (optional)", type:"input", ph:_=>"e.g. a startup, a hospital, a school"},
      {key:"who",     label:"Who you're meeting (optional)", type:"input", ph:_=>"e.g. hiring manager, future peer, exec"},
    ],
    buildPrompt:(v,o)=>
`You are an interview strategist. Give me the questions to ASK in a ${v.role||o.roleEx} interview${v.company?` at ${v.company}`:''}${v.who?`, meeting ${v.who}`:''}.

Deliver 8 questions, grouped:
- THE ROLE & SUCCESS (what 'great' looks like in 6–12 months)
- THE TEAM & MANAGER
- GROWTH & CHALLENGES
- ONE BOLD question that signals senior thinking

For each, one line on what a strong answer (or a dodge) tells me. Tailor them to ${o.name.toLowerCase()} work. Avoid anything easily Googled and avoid only asking about perks.`
  },

  {
    id:"mock", group:"Interview", name:"Mock Interview Simulator", tag:"Practice",
    icon:'<path d="M4 5h16v10H9l-4 4v-4H4z"/><path d="M8 9h8M8 12h5"/>',
    intro:"Turn your AI into a live interviewer that asks, then critiques.",
    fields:[
      {key:"role",  label:"Role", type:"input", ph:o=>o.roleEx},
      {key:"focus", label:"What to focus on (optional)", type:"input", ph:_=>"behavioral, technical, leadership, the whole loop"},
    ],
    buildPrompt:(v,o)=>
`You are an experienced ${o.name.toLowerCase()} hiring manager. Run a realistic mock interview with me for a ${v.role||o.roleEx} role${v.focus?`, focused on ${v.focus}`:''}.

Rules for how you run it:
- Ask ONE question at a time and WAIT for my answer before continuing. Do not answer for me.
- Start with a brief warm-up, then progress from behavioral to role-specific to a curveball.
- After each of my answers: give tight feedback (what landed, what to sharpen) and a score out of 5, then ask the next question.
- Stay in character as the interviewer; keep it realistic but supportive.
- After ~6 questions, stop and give an overall debrief: top 2 strengths, top 2 fixes, and a model answer for my weakest response.

Begin now with your first question.`
  },

  {
    id:"thanks", group:"Interview", name:"Thank-You Note", tag:"Outreach",
    icon:'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    intro:"A post-interview thank-you that keeps you top of mind.",
    fields:[
      {key:"who",  label:"Interviewer name/role", type:"input", ph:_=>"e.g. Dana, the hiring manager"},
      {key:"role", label:"Role & company", type:"input", ph:_=>"e.g. RN at Mercy Health"},
      {key:"moment", label:"A moment from the conversation", type:"textarea", ph:_=>"Something they said or you discussed"},
    ],
    buildPrompt:(v,o)=>
`You are a career coach who writes thank-you notes that subtly re-sell the candidate.

Write a post-interview thank-you email to ${v.who||'[interviewer]'} for the ${v.role||'[role & company]'} interview.
A moment to reference: ${v.moment||'(reference our discussion generally if I gave nothing specific)'}

Rules:
- Send-ready, under 130 words, with a subject line.
- Reference something specific from the conversation so it's clearly not a template.
- Reinforce ONE reason I'm a strong ${o.name.toLowerCase()} fit, briefly.
- Warm, genuine, confident — not gushing.

Give one version for the hiring manager and a shorter one for a peer interviewer.`
  },

  /* ===================================================================== */
  /*  TRACK — offers, planning & career management                         */
  /* ===================================================================== */

  {
    id:"offercompare", group:"Track", name:"Offer Comparison", tag:"Decide",
    icon:'<path d="M12 3v18M5 7h14M7 7l-3 6a3 3 0 0 0 6 0zM17 7l-3 6a3 3 0 0 0 6 0z"/>',
    intro:"Weigh two offers on more than just the base salary.",
    fields:[
      {key:"a", label:"Offer A", type:"textarea", ph:_=>"Company, base, bonus, equity, benefits, role, location, vibe"},
      {key:"b", label:"Offer B", type:"textarea", ph:_=>"Company, base, bonus, equity, benefits, role, location, vibe"},
      {key:"priorities", label:"What matters most to you", type:"input", ph:_=>"e.g. growth, pay, stability, flexibility"},
    ],
    buildPrompt:(v,o)=>
`You are a career and compensation advisor helping a ${o.name.toLowerCase()} professional choose between two offers.

OFFER A: ${v.a||'[details]'}
OFFER B: ${v.b||'[details]'}
What matters most to me: ${v.priorities||'(weigh growth, comp, stability, and quality of life evenly)'}

Deliver:
1. TOTAL COMP — estimate the real value of each (base + bonus + equity + benefits + cost-of-living), flagging assumptions.
2. SIDE-BY-SIDE — a table across pay, growth, role scope, stability, flexibility, and culture signals.
3. TRADE-OFFS — the honest 2–3 tensions between them, tied to MY priorities.
4. DECISION FRAME — questions to resolve the call, and what each answer points to.
5. WHAT TO CLARIFY — anything missing I should ask each employer before deciding.

Give a recommendation lean, but make the reasoning mine to own.`
  },

  {
    id:"plan306090", group:"Track", name:"30-60-90 Day Plan", tag:"Plan",
    icon:'<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5"/>',
    intro:"A first-90-days plan — for onboarding or to wow them in the interview.",
    fields:[
      {key:"role",    label:"Role", type:"input", ph:o=>o.roleEx},
      {key:"company", label:"Company / context", type:"input", ph:_=>"e.g. a 30-bed ICU, a Series B startup"},
      {key:"goals",   label:"Known goals / priorities (optional)", type:"textarea", ph:_=>"What success looks like, if you know"},
    ],
    buildPrompt:(v,o)=>
`You are an onboarding strategist who builds 30-60-90 day plans for ${o.name.toLowerCase()} roles.

Build a 30-60-90 day plan for a ${v.role||o.roleEx}${v.company?` at ${v.company}`:''}.
Known goals: ${v.goals||'(infer sensible priorities for this role)'}

Structure each phase with: FOCUS, KEY ACTIONS, PEOPLE TO BUILD TRUST WITH, and a measurable WIN.
- DAYS 1–30 — Learn: absorb, listen, build relationships, quick wins.
- DAYS 31–60 — Contribute: own real work, propose improvements.
- DAYS 61–90 — Lead: deliver measurable impact and set the next horizon.

Make it specific to ${o.name.toLowerCase()} work, realistic, and outcome-oriented. Add one line on how to present this in an interview as a "here's my plan" closer.`
  },

  {
    id:"searchplan", group:"Track", name:"Job-Search Plan", tag:"Plan",
    icon:'<path d="M9 7h7M9 12h7M9 17h5M5 7h.01M5 12h.01M5 17h.01"/>',
    intro:"A focused weekly plan so the search doesn't sprawl into burnout.",
    fields:[
      {key:"role",  label:"Target role(s)", type:"input", ph:o=>o.roleEx},
      {key:"hours", label:"Hours per week you can give", type:"input", ph:_=>"e.g. 8"},
      {key:"timeline", label:"Timeline / urgency", type:"input", ph:_=>"e.g. need a role in 3 months"},
    ],
    buildPrompt:(v,o)=>
`You are a job-search strategist who keeps ${o.name.toLowerCase()} candidates focused and sane.

Build a weekly job-search plan for someone targeting ${v.role||o.roleEx}, with ${v.hours||'[X]'} hours/week and this timeline: ${v.timeline||'[timeline]'}.

Deliver:
1. WEEKLY CADENCE — how to split the hours across applying, networking, tailoring, interview prep, and skill-building (with rough time per block).
2. TARGETS — realistic weekly numbers (quality applications, outreach messages, conversations) given my hours.
3. PIPELINE METRICS — what to track to know it's working, and the typical funnel ratios to expect.
4. ANTI-BURNOUT — 3 rules to avoid the spray-and-pray spiral.
5. WEEK-ONE CHECKLIST — exactly what to do first.

Prioritize quality and networking over mass-applying. Keep it doable.`
  },

  {
    id:"resign", group:"Track", name:"Resignation Letter", tag:"Draft",
    icon:'<path d="M14 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4M10 12H3m0 0 3-3m-3 3 3 3"/>',
    intro:"A professional, bridge-preserving resignation letter.",
    fields:[
      {key:"role", label:"Your role & company", type:"input", ph:_=>"e.g. Staff Nurse at Mercy Health"},
      {key:"last", label:"Last working day", type:"input", ph:_=>"e.g. two weeks from today"},
      {key:"tone", label:"Tone (optional)", type:"input", ph:_=>"warm, neutral, or strictly formal"},
    ],
    buildPrompt:(v,o)=>
`You are an HR-savvy career coach. Write a resignation letter for my role: ${v.role||'[role & company]'}.
Last working day: ${v.last||'[date]'}. Tone: ${v.tone||'warm but professional'}.

Rules:
- Short and gracious: state that I'm resigning, my last day, and brief genuine thanks.
- Offer to help with a smooth transition.
- No grievances, no over-explaining why I'm leaving.
- Leave the door open — I may need these references.

Give the formal letter plus a 2–3 line version I could send by email or message to my manager first.`
  },

  {
    id:"references", group:"Track", name:"Reference Sheet", tag:"Draft",
    icon:'<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="11" r="2.4"/><path d="M5.5 17a3.5 3.5 0 0 1 7 0M15 9h4M15 13h4"/>',
    intro:"A polished reference sheet plus how to prep your references.",
    fields:[
      {key:"role", label:"Role you're applying for", type:"input", ph:o=>o.roleEx},
      {key:"refs", label:"Your references", type:"textarea", ph:_=>"Name, title, company, how they know you (one per line)"},
    ],
    buildPrompt:(v,o)=>
`You are a career coach. Help me prepare references for a ${v.role||o.roleEx} application.

My references:
${v.refs||'[name, title, company, relationship — one per line]'}

Deliver:
1. REFERENCE SHEET — a clean, professionally formatted list (name, title, company, contact placeholder, and relationship line) ready to hand over.
2. WHO TO USE WHEN — which reference best speaks to which strength for a ${o.name.toLowerCase()} role.
3. BRIEFING NOTE — a short message to send each reference to prep them (the role, 2 strengths to emphasize, the timeline).
4. ASK SCRIPT — one line to confirm they're comfortable being a strong reference.

Keep formatting recruiter-ready and the briefing respectful of their time.`
  },

  {
    id:"skillsgap", group:"Track", name:"Skills Gap Analysis", tag:"Plan",
    icon:'<path d="M5 20V12M10 20V6M15 20v-9M20 20v-5"/>',
    intro:"See exactly what to learn to land the role you want next.",
    fields:[
      {key:"have",   label:"Skills you have now", type:"textarea", ph:o=>o.skillEx},
      {key:"target", label:"Role you're aiming for", type:"input", ph:o=>o.roleEx},
    ],
    buildPrompt:(v,o)=>
`You are a career development coach who builds focused upskilling plans for ${o.name.toLowerCase()} professionals.

My current skills: ${v.have||o.skillEx}
Target role: ${v.target||o.roleEx}

Deliver:
1. GAP ANALYSIS — the skills/credentials the target role expects that I don't yet show, split into "must-have" and "edge".
2. ALREADY THERE — strengths I have that I'm probably underselling.
3. LEARNING PLAN — a prioritized path (what to learn first → last), with the TYPE of resource for each (course, cert, project, mentorship) and a rough time estimate.
4. PROOF — for each gap, the fastest way to demonstrate it to an employer (a project, a cert, a portfolio piece).
5. 30-DAY START — the three highest-leverage things to do this month.

Prioritize by impact-per-hour. Be concrete about what "good enough to list" looks like.`
  },

  {
    id:"goal-planner", group:"Track", name:"Career Goal Planner", tag:"Plan",
    icon:'<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5"/><path d="M12 3v3M21 12h-3"/>',
    intro:"Turn a career goal into a dated plan with milestones and weekly actions.",
    fields:[
      {key:"now",  label:"Where you are now", type:"input", ph:o=>o.roleEx},
      {key:"goal", label:"Your goal", type:"input", ph:_=>"e.g. Senior role in 12 months / switch into UX"},
      {key:"constraints", label:"Constraints & context", type:"textarea", ph:_=>"time per week, timeline, budget, obligations"},
    ],
    buildPrompt:(v,o)=>
`You are a career coach who turns vague ambitions into concrete, dated plans for ${o.name.toLowerCase()} professionals.

Where I am: ${v.now||o.roleEx}. My goal: ${v.goal||'[your goal]'}.
Constraints: ${v.constraints||'(assume ~5 hrs/week; ask nothing — make reasonable assumptions)'}

Deliver:
1. GOAL, SHARPENED — restate my goal as a SMART goal (specific, measurable, time-bound).
2. MILESTONE MAP — 30 / 90 / 180 / 365-day milestones, each with a clear success signal.
3. SKILLS & PROOF — what to learn or demonstrate at each stage, and how to show it.
4. WEEKLY CADENCE — a realistic weekly routine given my constraints.
5. METRICS & CHECK-INS — what to track and when to course-correct.
Keep it motivating but grounded. Front-load the highest-leverage moves.`
  },

];
