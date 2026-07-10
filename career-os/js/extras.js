/* =========================================================================
   CAREER OS — EXTRAS  (Phase 6: Settings · Help · Bonuses)
   -------------------------------------------------------------------------
   Three meta views rendered on demand. Settings are real and persisted via the
   `store`. Help and Bonuses are static, offline content. Loaded before app.js;
   app.js calls initExtras() once and routes here via navToView().
   ========================================================================= */

/* ---- SETTINGS ------------------------------------------------------------ */
function renderSettings(){
  $('#pageTitle').textContent = "Settings";
  $('#pageSub').textContent   = "Make it yours — saved on this device";

  const theme = document.documentElement.dataset.theme || 'light';
  const occ   = store.occ;
  const fs    = store.fontSize;
  const auto  = store.autosave;

  const seg = (set, options) => options.map(o =>
    `<button class="seg ${o.active?'is-on':''}" data-set="${set}" data-val="${o.val}">${o.label}</button>`).join("");

  const editions = Object.entries(OCCUPATIONS).map(([k,o]) =>
    `<button class="edpick ${k===occ?'is-on':''}" data-set="occ" data-val="${k}" title="${o.edition}">
       <span class="edpick-sw" style="background:linear-gradient(135deg,${o.accent},${o.accent2})"></span>
       <span class="edpick-nm">${o.name}</span>
     </button>`).join("");

  $('#view-settings').innerHTML = `
    <div class="settings-wrap">

      <div class="card set-card">
        <div class="rs-head"><span class="rs-no">I.</span><h3>Appearance</h3><span class="rule-dot"></span></div>

        <div class="set-row">
          <div class="set-label"><b>Edition</b><span>Day reads on parchment; Evening is leather-bound.</span></div>
          <div class="seg-group">${seg('theme',[
            {val:'light',label:'Day edition',  active:theme!=='dark'},
            {val:'dark', label:'Evening edition',active:theme==='dark'},
          ])}</div>
        </div>

        <hr class="rule"/>

        <div class="set-row col">
          <div class="set-label"><b>Accent &amp; occupation</b><span>The jewel accent that re-skins the whole app.</span></div>
          <div class="edpick-grid">${editions}</div>
        </div>

        <hr class="rule"/>

        <div class="set-row">
          <div class="set-label"><b>Text size</b><span>Comfortable by default; Large bumps reading text.</span></div>
          <div class="seg-group">${seg('fontsize',[
            {val:'comfortable',label:'Comfortable',active:fs!=='large'},
            {val:'large',      label:'Large',      active:fs==='large'},
          ])}</div>
        </div>

        <hr class="rule"/>

        <div class="set-row">
          <div class="set-label"><b>New here?</b><span>Replay the welcome tour — the three-thing orientation you saw on first launch.</span></div>
          <button class="btn-sm btn-link" data-action="welcome">Replay welcome tour</button>
        </div>
      </div>

      <div class="card set-card">
        <div class="rs-head"><span class="rs-no">II.</span><h3>Data &amp; privacy</h3><span class="rule-dot"></span></div>

        <div class="set-row">
          <div class="set-label"><b>Autosave</b><span>Save your entries on this device between visits. Turn off on a shared computer.</span></div>
          <div class="seg-group">${seg('autosave',[
            {val:'on', label:'On', active:auto},
            {val:'off',label:'Off',active:!auto},
          ])}</div>
        </div>

        <hr class="rule"/>

        <div class="set-row">
          <div class="set-label"><b>Everything stays on your device</b><span>Career OS is fully offline. Nothing you type is uploaded — it lives in this browser's local storage. Export your résumé and copy your tracker if you switch devices.</span></div>
          <button class="btn-danger" data-action="clear">Clear all saved data</button>
        </div>
      </div>

    </div>`;
}

/* ---- HELP CENTER --------------------------------------------------------- */
function renderHelp(){
  $('#pageTitle').textContent = "Help Center";
  $('#pageSub').textContent   = "Everything you need to get the most from Career OS";

  const faqs = [
    ["Do I need the internet?",
     "No. Career OS is a fully offline product — fonts, styles, and all 33 tools run from the files on your device. The only time you go online is when you click Open Claude or Open ChatGPT to run a prompt you've copied."],
    ["How do the prompt tools work?",
     "Pick a tool, fill in a few fields, and press Compose. Career OS assembles an expert-grade prompt for you behind the scenes. Hit Copy prompt, then Open Claude or Open ChatGPT and paste. You never have to write a prompt yourself — though you can press View prompt to see it."],
    ["Where is my data saved?",
     "In your browser's local storage on this device only. Nothing is uploaded. If you clear your browser data or use a different device/browser, your entries won't follow you — so export your résumé (PDF / text / Word) and keep a copy of anything important."],
    ["How do I switch to my profession?",
     "Use the edition switcher at the top right (or Settings → Accent & occupation). It re-skins the app and tailors every tool's examples and keywording to your field. Your entries are kept as you switch."],
    ["The résumé print includes the app — help?",
     "Use the Print / PDF button inside the Résumé Builder. The print stylesheet hides the app and prints only the résumé sheet. In your browser's print dialog, choose 'Save as PDF' and make sure 'Background graphics' is off for a crisp page."],
    ["Copy isn't working from a downloaded file.",
     "Some browsers limit clipboard access when opening files directly (file://). Career OS falls back automatically, but if a copy ever fails, press View prompt and select the text manually. Serving the folder over http (or opening in a normal browser tab) removes the limitation."],
  ];

  const steps = [
    ["Start on the Dashboard","Your Career Readiness grows as you use tools. Tap a Quick start card or any tool in the sidebar."],
    ["Build your résumé","Open the Résumé Builder, fill it in, watch the live preview, then export to PDF, text, or Word. It autosaves."],
    ["Compose with the tools","Each tool turns your inputs into an expert prompt. Copy it into Claude or ChatGPT to get the finished writing."],
    ["Track your search","Add roles to the Job Tracker and drag them across Wishlist → Applied → Interview → Offer."],
  ];

  $('#view-help').innerHTML = `
    <div class="help-wrap">
      <div class="card help-card help-hero">
        <span class="eyebrow">Quick start</span>
        <h2>Four steps to a sharper search</h2>
        <ol class="help-steps">
          ${steps.map((s,i)=>`<li><span class="hs-no">${i+1}</span><div><b>${s[0]}</b><p>${s[1]}</p></div></li>`).join("")}
        </ol>
      </div>

      <div class="card help-card">
        <div class="rs-head"><span class="rs-no">?</span><h3>Frequently asked</h3><span class="rule-dot"></span></div>
        ${faqs.map(([q,a])=>`<details class="faq"><summary>${q}</summary><p>${a}</p></details>`).join("")}
      </div>

      <div class="card help-card">
        <div class="rs-head"><span class="rs-no">✦</span><h3>Power-user note</h3><span class="rule-dot"></span></div>
        <p class="help-note">Career OS is config-driven: every tool is one object in <code>js/modules.js</code>, and every edition is one object in <code>js/occupations.js</code>. To add a tool or a whole occupation edition, copy an existing entry and edit the values — no other code changes. See the README for the full guide.</p>
      </div>
    </div>`;
}

/* ---- BONUSES LIBRARY ----------------------------------------------------- */
/* Real, useful, offline resources. Each opens to reveal copy-ready content.   */
const BONUSES = [
  { title:"500 Power Verbs", tag:"Reference",
    intro:"Twenty categories of strong résumé verbs. Never open two bullets the same way.",
    body:
`LEADERSHIP & OWNERSHIP: Led, Directed, Spearheaded, Orchestrated, Owned, Championed, Oversaw, Drove, Headed, Piloted, Chaired, Governed, Commanded, Mobilized, Galvanized, Steered, Presided, Founded, Instituted, Pioneered, Marshaled, Helmed, Stewarded, Established, Initiated

BUILDING & CREATING: Built, Created, Designed, Developed, Launched, Engineered, Architected, Formulated, Devised, Produced, Constructed, Assembled, Crafted, Composed, Forged, Prototyped, Authored, Originated, Shaped, Fabricated, Generated, Conceived, Drafted, Modeled, Configured

IMPROVING & OPTIMIZING: Improved, Optimized, Streamlined, Enhanced, Refined, Upgraded, Overhauled, Modernized, Simplified, Standardized, Automated, Strengthened, Elevated, Revitalized, Sharpened, Tuned, Perfected, Retooled, Reengineered, Consolidated, Harmonized, Rationalized, Fortified, Transformed, Renovated

GROWTH & INCREASE: Grew, Increased, Expanded, Scaled, Boosted, Amplified, Accelerated, Multiplied, Doubled, Tripled, Maximized, Advanced, Extended, Broadened, Propelled, Escalated, Compounded, Widened, Ramped, Enlarged, Surged, Bolstered, Augmented, Uplifted, Catapulted

REVENUE & COST: Generated, Earned, Captured, Monetized, Grossed, Netted, Reduced, Cut, Saved, Lowered, Trimmed, Slashed, Decreased, Minimized, Eliminated, Recouped, Recovered, Reclaimed, Contained, Curbed, Offset, Funded, Financed, Budgeted, Forecasted

DELIVERING & ACHIEVING: Delivered, Achieved, Completed, Executed, Exceeded, Surpassed, Attained, Secured, Won, Shipped, Finalized, Fulfilled, Accomplished, Realized, Landed, Clinched, Closed, Reached, Notched, Sustained, Outperformed, Yielded, Banked, Nailed, Hit

MANAGING PEOPLE & MENTORING: Managed, Mentored, Coached, Trained, Supervised, Onboarded, Cultivated, Guided, Empowered, Motivated, Unified, Inspired, Fostered, Nurtured, Recruited, Hired, Staffed, Delegated, Counseled, Upskilled, Retained, Aligned, Energized, Enabled, Groomed

PROBLEM-SOLVING & FIXING: Solved, Resolved, Diagnosed, Troubleshot, Fixed, Remediated, Debugged, Untangled, Prevented, Mitigated, Addressed, Corrected, Repaired, Restored, Rectified, Reconciled, Averted, Defused, Neutralized, Countered, Patched, Salvaged, Overcame, Cracked, Redressed

COMMUNICATION & PERSUASION: Presented, Communicated, Persuaded, Influenced, Negotiated, Pitched, Articulated, Conveyed, Advocated, Lobbied, Briefed, Educated, Clarified, Translated, Documented, Reported, Wrote, Edited, Publicized, Promoted, Evangelized, Facilitated, Moderated, Narrated, Corresponded

ANALYSIS & RESEARCH: Analyzed, Researched, Assessed, Evaluated, Audited, Investigated, Examined, Measured, Quantified, Benchmarked, Projected, Mapped, Segmented, Surveyed, Tested, Validated, Verified, Calculated, Interpreted, Synthesized, Appraised, Inspected, Profiled, Tracked, Monitored

TECHNICAL & ENGINEERING: Programmed, Coded, Deployed, Integrated, Migrated, Scripted, Provisioned, Implemented, Installed, Maintained, Refactored, Instrumented, Containerized, Virtualized, Hardened, Encrypted, Networked, Compiled, Rearchitected, Automated, Debugged, Configured, Administered, Patched, Documented

OPERATIONS & PROCESS: Coordinated, Operated, Administered, Scheduled, Dispatched, Processed, Expedited, Systematized, Handled, Regulated, Balanced, Allocated, Arranged, Prioritized, Sequenced, Synchronized, Routed, Logged, Ran, Facilitated, Managed, Supervised, Executed, Standardized, Oversaw

SALES & BUSINESS DEVELOPMENT: Sold, Prospected, Closed, Negotiated, Upsold, Cross-sold, Acquired, Renewed, Converted, Qualified, Sourced, Signed, Positioned, Partnered, Brokered, Penetrated, Won, Retained, Expanded, Exceeded, Pitched, Cultivated, Onboarded, Forecasted, Landed

MARKETING & BRAND: Marketed, Branded, Positioned, Launched, Promoted, Advertised, Publicized, Segmented, Targeted, Personalized, Optimized, Ranked, Grew, Engaged, Converted, Nurtured, Amplified, Curated, Storyboarded, Rebranded, Messaged, Campaigned, Localized, Syndicated, Activated

PLANNING & STRATEGY: Planned, Strategized, Forecasted, Roadmapped, Prioritized, Aligned, Scoped, Charted, Envisioned, Blueprinted, Modeled, Projected, Budgeted, Allocated, Positioned, Structured, Sequenced, Balanced, Anticipated, Formulated, Defined, Set, Established, Framed, Calibrated

CHANGE & TRANSFORMATION: Transformed, Modernized, Revamped, Restructured, Reorganized, Realigned, Reengineered, Digitized, Integrated, Consolidated, Merged, Migrated, Transitioned, Standardized, Centralized, Decentralized, Rebuilt, Redesigned, Repositioned, Revitalized, Overhauled, Streamlined, Unified, Scaled, Turned around

QUALITY, RISK & COMPLIANCE: Ensured, Enforced, Audited, Inspected, Verified, Validated, Certified, Standardized, Documented, Complied, Safeguarded, Secured, Protected, Reduced, Mitigated, Controlled, Monitored, Reviewed, Reconciled, Corrected, Prevented, Assured, Accredited, Governed, Regulated

TEACHING, CARE & SUPPORT: Taught, Instructed, Trained, Coached, Mentored, Facilitated, Educated, Advised, Counseled, Guided, Supported, Assisted, Cared, Treated, Rehabilitated, Assessed, Diagnosed, Administered, Monitored, Comforted, Empowered, Tutored, Demonstrated, Explained, Nurtured

ORGANIZATION & ADMINISTRATION: Organized, Cataloged, Compiled, Consolidated, Filed, Recorded, Maintained, Updated, Processed, Arranged, Coordinated, Scheduled, Tracked, Logged, Documented, Archived, Systematized, Standardized, Streamlined, Prepared, Reconciled, Balanced, Audited, Verified, Managed

INITIATIVE & IMPACT: Initiated, Launched, Pioneered, Introduced, Established, Founded, Instituted, Championed, Drove, Led, Delivered, Achieved, Improved, Increased, Reduced, Created, Built, Solved, Won, Exceeded, Transformed, Accelerated, Generated, Secured, Spearheaded

RULE: never start two bullets with the same verb, and never with "Responsible for". Match the verb to the result that follows it.` },

  { title:"ATS Formatting Rules", tag:"Checklist",
    intro:"What keeps your résumé readable to applicant-tracking software.",
    body:
`DO
- Use a single-column layout. Multi-column and text boxes confuse parsers.
- Use standard section headers: Summary, Experience, Education, Skills.
- Use a common font (the résumé sheet here is already ATS-safe).
- Save and submit as PDF unless the posting asks for .docx.
- Spell out then abbreviate the first time: "Registered Nurse (RN)".
- Mirror the exact keywords from the job description where they're true.
- Keep dates consistent: "Jan 2022 – Present".

DON'T
- No tables, columns, headers/footers, or images for key content.
- No graphics, icons, or charts to convey skills or ratings.
- Don't hide keywords in white text — modern ATS and recruiters catch it.
- Don't use uncommon section names ("Where I've Made Magic").
- Don't cram 10pt text edge-to-edge; whitespace helps humans who read after the ATS.

RULE OF THUMB: if it would break when pasted into a plain text box, an ATS may choke on it.` },

  { title:"Networking Message Templates", tag:"Templates",
    intro:"Four short messages that get replies. Swap the [brackets].",
    body:
`COLD CONNECT (LinkedIn, <300 chars)
Hi [Name] — I follow [company]'s work in [area] and your path from [X] to [Y] stood out. I'm exploring [role/field] and would value being connected. No ask — just genuinely interested in how you got there.

INFORMATIONAL CHAT
Hi [Name], I'm a [your role] moving toward [target]. I admire [specific thing about them]. Could I borrow 15 minutes to hear how you broke into [field]? Happy to work around your schedule — and no, I'm not asking you for a job, just perspective.

REFERRAL ASK (someone you know)
Hi [Name], hope you're well! I'm applying for [role] at [company] and saw you're connected there. Would you be comfortable referring me or pointing me to the right person? I'll send a tailored resume and a 2-line blurb you can forward — easy to say no if it's not a fit.

FOLLOW-UP AFTER APPLYING
Subject: Following up — [Role], [Name]
Hi [Name], I applied for [role] on [date] and wanted to reaffirm my interest. [One sentence: strongest relevant proof.] Happy to share anything that would help. Thanks for your time.` },

  { title:"Interview Day Checklist", tag:"Checklist",
    intro:"The 60 minutes before, and what to have ready.",
    body:
`THE NIGHT BEFORE
- Re-read the job description and your own résumé.
- Prepare 3 STAR stories you can flex to many questions.
- Write 4 questions to ask them (role success, team, growth, one bold one).
- Lay out clothes; test video/audio if remote.

60 MINUTES BEFORE
- Quiet space, water, notepad, copy of résumé and the job description.
- Re-read your "Tell me about yourself" once, out loud.
- Power pose / walk / breathe — get your energy up, not jittery.

HAVE OPEN (remote)
- Résumé, the JD, your question list, and your 30-60-90 notes.
- Close noisy apps and notifications.

DURING
- Smile on the first answer; it sets your tone.
- Use specifics and numbers; pause before answering hard questions.
- Ask your questions — interviews are two-way.

WITHIN 24 HOURS
- Send a tailored thank-you that references something specific you discussed.` },

  { title:"Salary Research & Negotiation Scripts", tag:"Guide",
    intro:"Know your number — and the exact words to hold it.",
    body:
`WHERE TO LOOK (triangulate at least 3)
- Levels.fyi (tech), Glassdoor, LinkedIn Salary, Payscale, Salary.com.
- Government data: the U.S. Bureau of Labor Statistics (BLS) for role + region.
- Professional associations and union scales (esp. nursing, education, trades).
- Real humans: ask 2–3 people in the role what a fair range is.

ADJUST FOR
- Location / cost of living and remote vs. on-site.
- Years of experience and specialization.
- Company size and stage (startup equity vs. enterprise base).

BUILD YOUR RANGE
- Floor: the number below which you'd say no.
- Target: the well-supported market number for your level.
- Reach: 10–15% above target — your opening anchor.

WHEN ASKED "WHAT ARE YOUR EXPECTATIONS?"
"Based on the role and market data for this level, I'm targeting [range]. I'm sure we can find a number that works if it's the right fit."

ALWAYS counter once, politely. Most first offers have room.

--- NEGOTIATION SCRIPTS (swap the [brackets]) ---

COUNTER (email)
"Thank you so much — I'm excited about [role] and the team. Based on the scope and market data for this level, I was targeting [$target]. Is there flexibility to close that gap? I'm confident we can find a number that works."

WHEN THEY NAME A NUMBER FIRST (verbal)
"I appreciate that. Given [my specialization / competing interest / the responsibilities], I was hoping for something closer to [$target]. How much room is there?" — then stop talking.

"THAT'S THE MAX WE CAN DO"
"I understand budgets have limits. If base is fixed, could we look at a signing bonus, an earlier review, extra PTO, or [title]? I want to make this work."

"WE DON'T USUALLY NEGOTIATE"
"Totally understand. I'm weighing this seriously, and [$target] would make it an easy yes. Is there anything you can do?"

ACCEPTING
"That works for me — I'm thrilled to accept. Could you send the written offer so I can review and sign? Looking forward to starting on [date]."

DECLINING GRACEFULLY
"Thank you for the offer and your time. After careful thought I've decided to pursue another opportunity that's a closer fit right now. I'd love to stay in touch."` },

  { title:"LinkedIn Profile Audit", tag:"Checklist",
    intro:"A 12-point pass to make recruiters stop scrolling.",
    body:
`PHOTO & BANNER
1. Clear, friendly headshot; simple background.
2. Banner that signals your field (or a clean brand color).

HEADLINE & ABOUT
3. Headline names your role + value, not just "Open to work".
4. About is first-person, opens with a hook, and ends with who you help.
5. Keywords for your target role appear naturally (recruiters search them).

EXPERIENCE
6. Each role has 2–4 achievement bullets with numbers — not duties.
7. Most recent role is the most detailed.
8. Skills section lists the top 10 for your target role; pin the best 3.

PROOF & ACTIVITY
9. Featured section pins your best work, résumé, or a post.
10. Recommendations: at least 2, ideally from managers.
11. You post or comment occasionally — active profiles rank higher.

SETTINGS
12. "Open to work" set (recruiters-only if discreet); location and headline match your target market.` },

  { title:"Achievement Library", tag:"Reference",
    intro:"Ready-made achievement bullets by function — swap the [numbers] for yours.",
    body:
`LEADERSHIP / MANAGEMENT
- Led a team of [8] to deliver [project] [2] weeks ahead of schedule and [10]% under budget.
- Built and scaled a department from [3] to [15] while cutting attrition [30]%.
- Turned around an underperforming unit, lifting output [40]% in [two quarters].

REVENUE / SALES
- Grew territory revenue [35]% YoY ([$1.2M] → [$1.6M]) by [reworking the pipeline].
- Closed [$800K] in new business in [6 months], [120]% of quota.
- Improved renewal rate from [78]% to [91]% via a proactive check-in cadence.

COST / EFFICIENCY
- Cut operating costs [$250K]/yr by renegotiating [vendor contracts].
- Reduced process cycle time [45]% by automating [manual reporting].
- Eliminated [12] hrs/week of rework through a new [QA checklist].

CUSTOMER / SERVICE
- Raised CSAT from [4.1] to [4.7] across [3,000+] monthly tickets.
- Cut average response time [60]% while volume grew [25]%.

OPERATIONS / PROJECT
- Delivered [15] concurrent projects at [98]% on-time with zero budget overruns.
- Standardized [onboarding], cutting ramp time from [6] to [3] weeks.

TECHNICAL
- Reduced page load [2.4s] → [0.8s], lifting conversion [12]%.
- Cut cloud spend [$40K]/yr by right-sizing [infrastructure].
- Improved deploy frequency from [weekly] to [daily] with a new CI/CD pipeline.

HEALTHCARE
- Maintained a [0.9] fall rate per [1,000] patient-days on a [24]-bed unit.
- Precepted [11] new-grad nurses, cutting orientation time [30]%.

EDUCATION
- Raised student proficiency [22]% through data-driven differentiation.
- Secured [$15K] in grants for [classroom technology].

FORMULA: Action verb + what you did + tool/method + measurable result. If you lack a number, estimate conservatively and mark it [like this] until confirmed.` },

  { title:"Résumé Checklist", tag:"Checklist",
    intro:"A final pass before you hit submit.",
    body:
`CONTENT
- Every bullet starts with a strong, varied verb (no "Responsible for").
- At least half of your bullets carry a number (%, $, time, scale, quality).
- Top third of page 1 shows your strongest, most relevant proof.
- Summary is specific to the target role — not a generic objective.
- Keywords from the job description appear where they're true.
- No duties-only lines; every bullet implies a result.

LENGTH & FORMAT
- 1 page (<10 yrs experience) or 2 pages (senior); federal is the exception.
- Consistent dates ("Jan 2022 – Present"), tenses, and punctuation.
- One clean, ATS-safe font; single column; no tables/text boxes/images.
- Adequate white space; nothing crammed edge to edge.

PROOF & POLISH
- Contact info correct; LinkedIn URL customized.
- File saved as PDF named "First-Last-Resume.pdf".
- Zero typos — read it backwards, and out loud, once.
- Tailored to THIS role, not a one-size-fits-all copy.

REMOVE
- References line ("available on request" is assumed).
- Photo, birthdate, marital status (US résumés).
- High-school info once you have a degree.
- Clichés: "hardworking", "team player", "detail-oriented" (show it instead).` },

  { title:"Professional Email Templates", tag:"Templates",
    intro:"Copy, fill the [brackets], send. Covers the whole search.",
    body:
`APPLICATION FOLLOW-UP
Subject: Following up — [Role], [Your Name]
Hi [Name], I applied for [role] on [date] and wanted to reaffirm my interest. [One line: strongest relevant proof.] I'd welcome the chance to discuss how I can help [team/goal]. Thank you for your time.

THANK-YOU AFTER INTERVIEW
Subject: Thank you — [Role]
Hi [Name], thank you for the conversation today. I especially enjoyed [specific topic]. It reinforced my excitement about [role] — [one line tying your strength to their need]. Happy to share anything else that would help.

ACCEPTING AN OFFER
Subject: Offer Acceptance — [Your Name]
Hi [Name], I'm delighted to accept the [role] offer at [salary/terms]. Thank you for the opportunity and your confidence. Please send any onboarding paperwork — I look forward to starting on [date].

DECLINING AN OFFER
Hi [Name], thank you for the offer and for the time your team invested. After careful consideration I've decided to accept another opportunity that's a closer fit right now. I hope our paths cross again — I have great respect for [company].

RESCHEDULING AN INTERVIEW
Hi [Name], I'm looking forward to our conversation. Something unavoidable has come up at our scheduled time — could we move to [option A] or [option B]? Apologies for the shuffle, and thank you for your flexibility.

REQUESTING A REFERENCE
Hi [Name], I'm applying for [role] and would be grateful to list you as a reference — you saw my work on [project] firsthand. If you're comfortable, I'll send the role details and a couple of points to emphasize. Totally fine to say no.

RECONNECTING (cold-ish)
Hi [Name], it's been a while since [shared context]! I'm exploring [field/role] and thought of you. No agenda beyond catching up — and I'd value your take on [topic] if you have 15 minutes sometime.` },

  { title:"Career Planning Workbook", tag:"Workbook",
    intro:"A guided self-assessment to point the search in the right direction.",
    body:
`Work through these in a notebook. Be honest — this is for you, not a recruiter.

1. VALUES (what a job must give you)
- Rank: compensation, growth, stability, flexibility, impact, autonomy, prestige, people.
- Top 3 non-negotiables: __________
- Deal-breakers you'll walk away from: __________

2. STRENGTHS & ENERGY
- 3 things people consistently praise in your work: __________
- Tasks that energize you (you lose track of time): __________
- Tasks that drain you (minimize these): __________

3. STORY & PROOF
- 5 accomplishments you're proud of + the result of each: __________
- The through-line they reveal about you: __________

4. TARGET
- Ideal role title(s): __________
- Industries / company types / size: __________
- Must-have vs nice-to-have in the next role: __________

5. GAPS
- Skills/credentials the target role expects that you lack: __________
- Fastest way to close or signal each: __________

6. GOALS (make them SMART)
- 90-day goal: __________
- 12-month goal: __________
- Success signal for each: __________

7. WEEKLY PLAN
- Hours/week for the search: ____
- Split across: applying / networking / tailoring / interview prep / skill-building.
- One action to take TODAY: __________

Revisit monthly. Adjust the target as you learn — clarity comes from motion, not just reflection.` },
];

function renderBonuses(){
  $('#pageTitle').textContent = "Bonuses";
  $('#pageSub').textContent   = "A library of extras to sharpen every step";
  $('#view-bonuses').innerHTML = `
    <div class="bonus-grid">
      ${BONUSES.map((b,i)=>`
        <details class="card bonus-card">
          <summary>
            <span class="bonus-tag">${b.tag}</span>
            <h3>${escapeHtml(b.title)}</h3>
            <p>${escapeHtml(b.intro)}</p>
            <span class="bonus-open">View ▾</span>
          </summary>
          <div class="bonus-body">
            <button class="btn-sm btn-copy bonus-copy" data-bonus="${i}"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><rect x="9" y="9" width="11" height="11" rx="1.5"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/></svg>Copy</button>
            <pre>${escapeHtml(b.body)}</pre>
          </div>
        </details>`).join("")}
    </div>`;
}

/* ---- INIT: bind delegated events once ------------------------------------ */
function initExtras(){
  // Settings controls (delegation on the persistent view container)
  $('#view-settings').addEventListener("click", e => {
    const ctl = e.target.closest("[data-set]");
    if(ctl){
      const { set, val } = ctl.dataset;
      if(set === 'theme')    applyTheme(val);
      if(set === 'occ')    { applyOccupation(val); toast(OCCUPATIONS[val].edition + ' applied'); }
      if(set === 'fontsize') applyFontSize(val);
      if(set === 'autosave'){ store.autosave = (val === 'on'); toast('Autosave ' + val); }
      renderSettings();
      return;
    }
    if(e.target.closest("[data-action='clear']")){
      if(confirm("Clear all saved data on this device? Your résumé, job board, saved entries, and preferences will be erased. This can't be undone.")){
        store.clearAll();
        toast("All saved data cleared");
        setTimeout(() => location.reload(), 600);
      }
    }
    if(e.target.closest("[data-action='welcome']")) openWelcomeModal();
  });

  // Bonuses copy buttons
  $('#view-bonuses').addEventListener("click", e => {
    const c = e.target.closest("[data-bonus]");
    if(c){ e.preventDefault(); copyText(BONUSES[+c.dataset.bonus].body, "Copied to clipboard"); }
  });
}
