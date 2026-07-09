/* =========================================================================
   CAREER OS — ATS KEYWORD CHECKER  (Phase 9)
   -------------------------------------------------------------------------
   Real, offline keyword/phrase matching between a résumé and a job
   description — the one feature every paid "optimizer" tool (Jobscan,
   Rezi, Teal) leads with, and the single most-requested table-stakes
   feature this product lacked. No AI call: plain frequency-based keyword
   extraction + substring matching, same spirit as the Résumé Score.

   Deliberately honest about its limits — this is mechanical term matching,
   not the semantic analysis modern ATS software actually does — which is
   why the "ATS Audit" prompt tool (id:"ats" in modules.js) still exists
   alongside this for deeper, AI-assisted analysis.

   Custom view (like the other Phase 8/9 tools) — not driven by the prompt
   engine, since there's no "compose a prompt" step here, just live
   computation. Loaded before app.js; app.js calls initAtsCheck() once and
   navigates via showView('atscheck') + renderAtsCheck().
   ========================================================================= */

/* ---- Nav registration ------------------------------------------------------ */
const ATSCHECK_MODULE = {
  id:"atscheck", group:"Apply", name:"ATS Keyword Checker", tag:"Scan", custom:true,
  intro:"Real keyword/phrase matching against a job description — instant, offline, no AI call.",
  icon:'<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/><path d="M8 11h6"/>',
};

/* ---- keyword extraction ----------------------------------------------------
   Unigrams: any non-stopword token appearing at least once. Bigrams:
   two-word phrases that repeat (≥2x) to cut noise from incidental pairs.
   Ties (most unigrams appear once) break by first-seen order, which in a
   job description usually means title/duties before boilerplate.

   Two stopword lists, not one: ATS_HARD_STOPWORDS (pure function words) is
   used for bigrams; the broader ATS_STOPWORDS (adds generic workplace
   filler like "team"/"role"/"job") is used for unigrams only. Filtering
   "team" out of unigrams is right — it's noise on its own — but filtering
   it out of BIGRAMS too silently breaks legitimate role/title phrases like
   "team lead" or "product role", since one half would never pass. Bigram
   words also only need length > 1 (not > 2), so short domain acronyms
   ("ai engineer", "ux designer", "hr manager") can still form. */
const ATS_HARD_STOPWORDS = new Set([
  "the","and","of","to","a","in","for","with","on","is","are","as","that","this","will","you","your",
  "we","our","be","been","being","have","has","had","an","or","at","by","from","which","who","it","its",
  "their","they","he","she","i","but","not","if","can","may","also","other","such","into","about","across",
  "per","each","all","any","more","most","some","these","those","than","then","so","do","does","did","was",
  "were","would","could","should","must","shall","us","ours","one","two","etc","new",
]);
const ATS_STOPWORDS = new Set([...ATS_HARD_STOPWORDS,
  "work","working","role","job","team","teams","including","include","includes","using","used","use",
  "strong","excellent","ability",
]);
function atsNormalize(s){
  return " " + String(s||"").toLowerCase().replace(/[^a-z0-9\s+#./-]/g," ").replace(/\s+/g," ").trim() + " ";
}
function atsTokenize(s){
  return String(s||"").toLowerCase().replace(/[^a-z0-9\s+#./-]/g," ").split(/\s+/)
    // strip leading/trailing punctuation (sentence-ending periods, stray
    // hyphens/slashes) picked up by the char class above, while keeping it
    // when internal — "node.js" and "cross-functional" stay intact, "role."
    // becomes "role"
    .map(w => w.replace(/^[.\-/+#]+|[.\-/+#]+$/g, ""))
    .filter(Boolean);
}
// Returns every extracted term, sorted by frequency, unsliced — callers cap
// for display themselves so they can report how many were cut, if any.
function atsKeywords(jdText){
  const raw = atsTokenize(jdText);
  const isRealUni = w => w.length > 2 && !ATS_STOPWORDS.has(w) && !/^\d+$/.test(w);
  const isRealBi  = w => w.length > 1 && !ATS_HARD_STOPWORDS.has(w) && !/^\d+$/.test(w);
  const uniFreq = {};
  raw.forEach(w => { if(isRealUni(w)) uniFreq[w] = (uniFreq[w]||0) + 1; });
  const biFreq = {};
  for(let i = 0; i < raw.length - 1; i++){
    const a = raw[i], b = raw[i+1];
    if(isRealBi(a) && isRealBi(b)){ const phrase = a + " " + b; biFreq[phrase] = (biFreq[phrase]||0) + 1; }
  }
  const uni = Object.entries(uniFreq).map(([term,count]) => ({term, count}));
  const bi  = Object.entries(biFreq).filter(([,c]) => c >= 2).map(([term,count]) => ({term, count}));
  return uni.concat(bi).sort((a,b) => b.count - a.count).map(x => x.term);
}
function atsIncludes(haystack, term){
  return atsNormalize(haystack).includes(atsNormalize(term));
}

/* ---- RENDER ------------------------------------------------------------------ */
function renderAtsCheck(){
  $('#pageTitle').textContent = "ATS Keyword Checker";
  $('#pageSub').textContent   = "Paste both sides — no AI, no upload, nothing leaves this device";
  renderAtsUseResumeButton();
  renderAtsResult();
}

function renderAtsUseResumeButton(){
  const btn = $('#atsUseResume'); if(!btn) return;
  const hasResumeBuilder = typeof activeProfile === 'function' && typeof resumesStore !== 'undefined' && resumesStore;
  btn.style.display = hasResumeBuilder ? "" : "none";
  if(hasResumeBuilder) btn.textContent = 'Use my "' + (activeProfile().name || "résumé") + '"';
}

function renderAtsResult(){
  const panel = $('#atsResultPanel'); if(!panel) return;
  const resumeText = $('#atsResume').value.trim();
  const jdText = $('#atsJD').value.trim();

  if(!resumeText || !jdText){
    panel.innerHTML = `<div class="out-empty">
      <div class="mark"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg></div>
      <h3>Your missing keywords appear here</h3>
      <p>Paste your résumé text and a job description — this updates instantly as you type.</p></div>`;
    return;
  }

  const KEYWORD_CAP = 25;
  const allKeywords = atsKeywords(jdText);
  const keywords = allKeywords.slice(0, KEYWORD_CAP);
  const matched = keywords.filter(k => atsIncludes(resumeText, k));
  const missing = keywords.filter(k => !atsIncludes(resumeText, k));
  const pct = keywords.length ? Math.round(matched.length / keywords.length * 100) : 0;
  const E = escapeHtml;

  // Missing list leads — it's the actionable part. Coverage is a secondary,
  // small label (not "ATS score") so a high number can't read as a quality
  // judgment: this is mechanical term-presence, and stuffing matched words
  // into a résumé without real content would trivially max it out.
  panel.innerHTML = `<div class="result">
    <div class="result-top">
      <div><b>Missing keywords to review</b><span>Coverage: ${pct}% (${matched.length} of ${keywords.length} terms found)</span></div>
    </div>
    ${allKeywords.length > KEYWORD_CAP ? `<p class="ats-cap-note">Showing top ${KEYWORD_CAP} of ${allKeywords.length} extracted terms.</p>` : ""}
    <div class="ats-cols">
      <div class="ats-col">
        <h4>Missing — consider adding if true (${missing.length})</h4>
        ${missing.length ? `<ul class="ats-list ats-list-fail">${missing.map(k => `<li>${E(k)}</li>`).join("")}</ul>` : `<p class="ats-empty">None — every extracted term appears in your résumé.</p>`}
      </div>
      <div class="ats-col">
        <h4>Found (${matched.length})</h4>
        ${matched.length ? `<ul class="ats-list ats-list-pass">${matched.map(k => `<li>${E(k)}</li>`).join("")}</ul>` : `<p class="ats-empty">None yet.</p>`}
      </div>
    </div>
    <p class="ats-note">Mechanical keyword/phrase matching, not true semantic analysis — modern ATS software reads context, not just exact words. This can't recognize synonyms or abbreviations ("RN" vs. "Registered Nurse", "JS" vs. "JavaScript"), so a "missing" term may already be covered by different wording in your résumé — double-check before adding anything. Use the "ATS Audit" prompt tool for deeper, AI-assisted analysis.</p>
  </div>`;
}

/* ---- INIT: bind delegated events once -------------------------------------- */
function initAtsCheck(){
  $('#atsResume').addEventListener("input", renderAtsResult);
  $('#atsJD').addEventListener("input", renderAtsResult);
  $('#atsUseResume').addEventListener("click", () => {
    if(typeof resumeToText !== 'function') return;
    $('#atsResume').value = resumeToText();
    renderAtsResult();
  });
}
