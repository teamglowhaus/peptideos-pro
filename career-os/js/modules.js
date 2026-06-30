/* =========================================================================
   CAREER OS — MODULES  (the tool definitions)
   -------------------------------------------------------------------------
   ONE renderer drives every tool. A tool is a single object in this array.
   The renderer reads `fields[]` to draw the form, and calls `buildPrompt()`
   on Generate. Adding a 34th tool = one new object below. No view code ever
   changes — that is the whole product.

   ----- HOW TO ADD A NEW MODULE (copy an entry, edit the values) -----
   {
     id        unique slug (used in nav, routing, localStorage).
     group     section it lives under in the sidebar ("Compose", "Apply"…).
     name      label shown in nav, quick-start, and the module header.
     tag       tiny mono badge ("Draft", "Scan").
     icon      inline SVG path string — drawn inside a 24×24 stroked <svg>.
     intro     one-line description shown under the title + on quick-start.
     fields    [] of form controls. Each field is:
                 { key, label, type:'input'|'textarea', ph:(occupation)=>string }
                 `ph` is a function so placeholders can be edition-aware
                 (e.g. ph:o=>o.roleEx shows the current edition's example role).
     buildPrompt(values, occupation) -> string
                 THE DELIVERABLE. Assembles an expert-persona prompt from the
                 user's inputs. `values` is { key: userText }; `occupation` is
                 the active OCCUPATIONS entry, so prompts are edition-aware.
                 Always provide a sensible fallback for empty inputs.
   }

   The prompt is hidden by default — the output panel shows a "Prompt composed"
   success state with Copy / Open Claude / Open ChatGPT and a "View prompt"
   disclosure. The buyer never writes a prompt and isn't shown one unless asked.
   ========================================================================= */

const MODULES = [

  /* ---- COMPOSE -------------------------------------------------------- */

  {
    id:"bullets", group:"Compose", name:"Resume Bullets", tag:"Draft",
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
    id:"summary", group:"Compose", name:"Professional Summary", tag:"Draft",
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
    id:"skills", group:"Compose", name:"Skills Section", tag:"Draft",
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

  /* ---- APPLY ---------------------------------------------------------- */

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
];
