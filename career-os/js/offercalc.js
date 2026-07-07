/* =========================================================================
   CAREER OS — OFFER COMPARISON CALCULATOR  (Phase 8)
   -------------------------------------------------------------------------
   Real arithmetic, not an AI estimate — the numeric companion to the
   "Offer Comparison" prompt tool (id:"offercompare" in modules.js), which
   handles the qualitative trade-offs (culture, growth, stability) instead.
   Custom view (like the other Phase 8 tools) — not driven by the prompt
   engine. No tax modeling: total comp only, clearly labeled as such,
   since accurate take-home pay depends on jurisdiction data this product
   doesn't have and shouldn't guess at.
   ========================================================================= */

/* ---- Nav registration ------------------------------------------------------ */
const OFFERCALC_MODULE = {
  id:"offercalc", group:"Track", name:"Offer Comparison Calculator", tag:"Decide", custom:true,
  intro:"Real math on two offers — base, bonus, equity, benefits — side by side.",
  icon:'<path d="M4 21V10M12 21V3M20 21v-7"/><path d="M2 21h20"/>',
};

/* ---- Data model — two offers, not persisted (recompute fresh each visit) -- */
function defaultOffer(){ return { label:"", base:"", signing:"", bonus:"", equityTotal:"", equityYears:"", benefits:"", col:"", pto:"" }; }
let ocOffers = null;   // { a: {...}, b: {...} }

const OC_FIELDS = [
  {k:"label",       l:"Company / label",              ph:"e.g. Offer A — Acme Corp"},
  {k:"base",        l:"Base salary",                  ph:"$120,000"},
  {k:"signing",     l:"Signing bonus (one-time)",     ph:"$10,000"},
  {k:"bonus",       l:"Annual target bonus",          ph:"$8,000 or 10%"},
  {k:"equityTotal", l:"Total equity grant value",     ph:"$80,000"},
  {k:"equityYears", l:"Vesting period (years)",       ph:"4"},
  {k:"benefits",    l:"Benefits — annual value estimate", ph:"$12,000"},
  {k:"col",         l:"Cost-of-living index (optional)", ph:"1.0 = baseline"},
  {k:"pto",         l:"PTO (days/yr, informational)", ph:"20"},
];

/* ---- number parsing — accepts "$120,000", "120000", "120k", "10%" -------- */
function ocNum(v){
  const s = String(v||"").trim().toLowerCase().replace(/[$,\s]/g,"").replace(/%$/,"");
  if(!s) return 0;
  const m = s.match(/^(-?\d+(\.\d+)?)(k|m)?$/);
  if(!m) return 0;
  let n = parseFloat(m[1]);
  if(m[3] === 'k') n *= 1000;
  if(m[3] === 'm') n *= 1000000;
  return isNaN(n) ? 0 : n;
}
function ocFmt(n){ return "$" + Math.round(n).toLocaleString("en-US"); }

function ocLoad(){ ocOffers = { a: defaultOffer(), b: defaultOffer() }; }

/* ---- MATH ------------------------------------------------------------------
   Total comp only — no tax modeling (jurisdiction-dependent, out of scope).
   Equity is amortized straight-line over the vesting period (default 4 yrs)
   to get an annual-equivalent figure; this ignores cliffs/back-loading. */
function ocCompute(o){
  const base = ocNum(o.base), signing = ocNum(o.signing), bonus = ocNum(o.bonus),
        equityTotal = ocNum(o.equityTotal), equityYears = ocNum(o.equityYears) || 4,
        benefits = ocNum(o.benefits), col = ocNum(o.col), pto = ocNum(o.pto);
  const equityAnnual = equityYears > 0 ? equityTotal / equityYears : 0;
  const ongoing = base + bonus + equityAnnual + benefits;
  const year1 = ongoing + signing;
  return { base, signing, bonus, equityAnnual, equityYears, benefits, col, pto, year1, ongoing,
    colAdjusted: col > 0 ? ongoing / col : null };
}

/* ---- RENDER ----------------------------------------------------------------- */
function renderOfferCalc(){
  $('#pageTitle').textContent = "Offer Comparison Calculator";
  $('#pageSub').textContent   = "Real numbers, side by side — no AI, no guessing";
  if(!ocOffers) ocLoad();

  const F = (offerKey, f) => {
    const val = ocOffers[offerKey][f.k];
    return `<div class="field"><label>${f.l}</label><input data-oc="${offerKey}" data-k="${f.k}" value="${escapeAttr(val)}" placeholder="${escapeAttr(f.ph)}"/></div>`;
  };
  const offerCard = (key, title) => `<div class="card rs-card oc-offer">
    <div class="rs-head"><span class="rs-no">${key.toUpperCase()}.</span><h3>${title}</h3><span class="rule-dot"></span></div>
    ${OC_FIELDS.map(f => F(key, f)).join("")}
  </div>`;

  $('#ocForm').innerHTML = `<div class="oc-grid">${offerCard("a","Offer A")}${offerCard("b","Offer B")}</div>`;
  renderOfferResult();
}

function renderOfferResult(){
  const a = ocCompute(ocOffers.a), b = ocCompute(ocOffers.b);
  const labelA = ocOffers.a.label.trim() || "Offer A", labelB = ocOffers.b.label.trim() || "Offer B";
  const has = a.base || a.signing || a.bonus || a.equityTotal || a.benefits ||
              b.base || b.signing || b.bonus || b.equityTotal || b.benefits;

  const el = $('#ocResult');
  if(!has){
    el.innerHTML = `<div class="r-empty">Fill in either offer to see the comparison.</div>`;
    return;
  }

  const row = (label, va, vb, fmt) => `<div class="oc-row"><span>${escapeHtml(label)}</span><b>${fmt(va)}</b><b>${fmt(vb)}</b></div>`;
  const money = n => ocFmt(n);
  const days  = n => n ? n + " days" : "—";

  const diff = b.ongoing - a.ongoing;
  const winner = diff === 0 ? null : (diff > 0 ? labelB : labelA);
  const diffAbs = Math.abs(diff);

  let colLine = "";
  if(a.colAdjusted != null || b.colAdjusted != null){
    const ca = a.colAdjusted != null ? a.colAdjusted : a.ongoing;
    const cb = b.colAdjusted != null ? b.colAdjusted : b.ongoing;
    const cdiff = cb - ca, cwinner = cdiff === 0 ? null : (cdiff > 0 ? labelB : labelA);
    colLine = `<p class="oc-verdict">Cost-of-living adjusted: <b>${cwinner ? escapeHtml(cwinner) + " is ahead by " + money(Math.abs(cdiff)) + "/yr" : "even"}</b>.</p>`;
  }

  el.innerHTML = `
    <div class="oc-head"><span class="oc-h-label"></span><span class="oc-h-a">${escapeHtml(labelA)}</span><span class="oc-h-b">${escapeHtml(labelB)}</span></div>
    ${row("Base salary", a.base, b.base, money)}
    ${row("Signing bonus (year 1 only)", a.signing, b.signing, money)}
    ${row("Annual target bonus", a.bonus, b.bonus, money)}
    ${row("Equity (annualized over " + (a.equityYears||4) + "/" + (b.equityYears||4) + " yrs)", a.equityAnnual, b.equityAnnual, money)}
    ${row("Benefits (annual value)", a.benefits, b.benefits, money)}
    <div class="oc-row oc-row-total"><span>Year 1 total</span><b>${money(a.year1)}</b><b>${money(b.year1)}</b></div>
    <div class="oc-row oc-row-total"><span>Ongoing annual total</span><b>${money(a.ongoing)}</b><b>${money(b.ongoing)}</b></div>
    ${row("PTO (informational)", a.pto, b.pto, days)}
    <p class="oc-verdict">${winner ? escapeHtml(winner) + "'s ongoing annual total is <b>" + money(diffAbs) + "/yr</b> higher." : "The two offers are even on ongoing annual total."}</p>
    ${colLine}
    <p class="oc-note">Total compensation only — this doesn't model taxes, healthcare premiums you'd pay, or vesting cliffs/back-loading. Use the "Offer Comparison" prompt tool for the qualitative trade-offs (culture, growth, stability).</p>`;
}

/* ---- INIT: bind delegated events once -------------------------------------- */
function initOfferCalc(){
  ocLoad();
  $('#ocForm').addEventListener("input", e => {
    const t = e.target;
    if(t.dataset.oc === undefined) return;
    ocOffers[t.dataset.oc][t.dataset.k] = t.value;
    renderOfferResult();
  });
}
