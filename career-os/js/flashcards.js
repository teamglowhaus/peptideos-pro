/* =========================================================================
   CAREER OS — INTERVIEW FLASHCARDS  (Phase 8)
   -------------------------------------------------------------------------
   A self-quiz / flip-card practice mode — a genuinely different feature
   TYPE from the 40+ prompt composers: no AI call, no fields, just a bundled
   question bank you click through. Front = the question (or, for "Ask
   Them", the question YOU ask); back = a short coaching tip, not a
   scripted answer — this is practice, not a script to memorize.

   Custom view (like the Résumé Builder / Job Tracker) — not driven by the
   prompt engine. Loaded before app.js; app.js calls initFlashcards() once
   and navigates via showView('flashcards') + renderFlashcards().
   ========================================================================= */

/* ---- Nav registration ------------------------------------------------------ */
const FLASHCARDS_MODULE = {
  id:"flashcards", group:"Interview", name:"Interview Flashcards", tag:"Practice", custom:true,
  intro:"Flip through real interview questions and coaching tips — no AI needed.",
  icon:'<rect x="4" y="5" width="16" height="11" rx="1.5"/><path d="M8 20h8"/><path d="M9 8h6M9 11h4"/>',
};

/* ---- The bank --------------------------------------------------------------
   Deliberately occupation-agnostic (like the Bonuses library) so it's useful
   across every edition. Front = question; back = what it's really probing
   for and how to structure a strong answer — never a canned script. */
const FLASHCARDS = [
  // Behavioral
  {cat:"Behavioral", q:"Tell me about a time you disagreed with a manager or teammate.",
    tip:"They're testing how you handle conflict without burning bridges. Use STAR (Situation, Task, Action, Result), stay factual about the disagreement, and end on how it was resolved — not on who was right."},
  {cat:"Behavioral", q:"Describe a time you failed or made a mistake.",
    tip:"Own it plainly, no excuses or blame-shifting. The story lands or falls on what you changed afterward — that's the part to spend the most time on."},
  {cat:"Behavioral", q:"Tell me about a time you had to persuade someone to see things your way.",
    tip:"Show you listened first. The strongest version of this story is one where you built the case around THEIR interests, not just yours."},
  {cat:"Behavioral", q:"Describe a time you had too much on your plate at once.",
    tip:"Show your prioritization method — what you protected, what you dropped, and how you communicated the trade-off to others."},
  {cat:"Behavioral", q:"Tell me about a time you received tough feedback.",
    tip:"Show you didn't get defensive in the moment. The concrete change you made afterward matters more than how the feedback felt."},
  {cat:"Behavioral", q:"Give an example of when you went above and beyond.",
    tip:"Pick something with a measurable result, not just extra hours worked. \"I stayed late\" isn't a story — what changed because you did?"},
  {cat:"Behavioral", q:"Tell me about a time you had to learn something quickly.",
    tip:"Walk through your actual learning process (how you got up to speed), not just the happy outcome. Process is what they're evaluating."},

  // Motivation & Fit
  {cat:"Motivation & Fit", q:"Why do you want to work here?",
    tip:"Needs 2–3 specific, researched reasons tied to THIS company — a product, a mission, recent news. \"Great culture\" or \"growth opportunity\" alone reads as generic."},
  {cat:"Motivation & Fit", q:"Why are you leaving your current role?",
    tip:"Frame it forward — what you're moving toward, not what you're escaping. Never trash a current or former employer, even if it's true."},
  {cat:"Motivation & Fit", q:"Where do you see yourself in five years?",
    tip:"Show ambition that grows logically FROM this role, not past it or sideways from it. It should sound like this job is a real step, not a placeholder."},
  {cat:"Motivation & Fit", q:"What do you know about our company?",
    tip:"Should reference something recent or specific — a product launch, a stated value, a piece of news — not just a paraphrase of the \"About\" page."},
  {cat:"Motivation & Fit", q:"Why should we hire you over other candidates?",
    tip:"One sharp differentiator backed by proof beats a list of flattering adjectives. Pick the ONE thing you want them to remember."},
  {cat:"Motivation & Fit", q:"What are you looking for in your next role?",
    tip:"Match your answer to what THIS role genuinely offers — don't describe your dream job if it isn't the job in front of you."},
  {cat:"Motivation & Fit", q:"How did you hear about this position?",
    tip:"Quick and honest, then pivot fast into why you're excited. This question is a warm-up, not the main event — don't over-invest in it."},

  // Strengths & Growth
  {cat:"Strengths & Growth", q:"What's your greatest strength?",
    tip:"Pick one relevant to the role and back it with a specific result — the label alone (\"I'm a hard worker\") doesn't prove anything."},
  {cat:"Strengths & Growth", q:"What's your greatest weakness?",
    tip:"A real weakness plus a concrete step you're taking on it. Avoid disguised strengths (\"I work too hard\") — interviewers hear that one constantly."},
  {cat:"Strengths & Growth", q:"How do you handle stress or pressure?",
    tip:"Give a specific method you actually use, not just \"I stay calm.\" What do you DO differently when things get intense?"},
  {cat:"Strengths & Growth", q:"What motivates you at work?",
    tip:"Connect it to something evidenced by your actual work history, not an abstraction. If you say \"impact,\" have a story that shows it."},
  {cat:"Strengths & Growth", q:"How do you prioritize when everything feels urgent?",
    tip:"Give a real method — impact vs. effort, who's blocked, hard deadlines — not just \"I make a list.\""},
  {cat:"Strengths & Growth", q:"What kind of manager gets the best out of you?",
    tip:"Be honest but constructive. Describing your worst boss (even without naming them) reads as a red flag, not self-awareness."},

  // Curveballs
  {cat:"Curveballs", q:"What's a controversial opinion you hold about your field?",
    tip:"Show independent thinking, but keep it professional and defensible — this isn't the place for something that reads as reckless or offensive."},
  {cat:"Curveballs", q:"How would you handle an unreasonable deadline?",
    tip:"Show negotiation, not blind compliance or flat refusal. A strong answer proposes trade-offs (scope, resources, timeline) rather than just saying yes or no."},
  {cat:"Curveballs", q:"If you could redo one decision in your career, what would it be?",
    tip:"Pick something real but not disqualifying, and spend most of the answer on the lesson it taught you, not the mistake itself."},
  {cat:"Curveballs", q:"Sell me this pen (or similar prompt-selling exercise).",
    tip:"Ask a clarifying question first (\"what do you need a pen for?\"), then tie features to what they just told you. Selling before listening is the trap."},
  {cat:"Curveballs", q:"What would your last manager say your growth area is?",
    tip:"Should roughly match what you'd say yourself about your weakness — inconsistency between the two is what interviewers are quietly checking for."},
  {cat:"Curveballs", q:"Walk me through your résumé in two minutes.",
    tip:"Rehearse this one specifically — it often sets the tone for the whole interview. Hit the through-line, not every job title."},

  // Ask Them (the flip side — questions YOU ask, tip = why it's a strong one to ask)
  {cat:"Ask Them", q:"What does success look like in this role after six months?",
    tip:"Shows you're already thinking about impact, not just getting hired. A vague answer from them can also be a mild red flag worth noting."},
  {cat:"Ask Them", q:"What's the biggest challenge someone in this role would face right now?",
    tip:"Surfaces the real, current pain point — often more honest than anything in the job description."},
  {cat:"Ask Them", q:"How would you describe the team's working style?",
    tip:"A concrete, specific answer (vs. generic \"collaborative and fast-paced\") tells you a lot about how self-aware the team is."},
  {cat:"Ask Them", q:"What's changed most about this role or team in the last year?",
    tip:"Reveals growth, churn, or reorg history that isn't in any posting — listen for whether the change sounds positive or exhausted."},
  {cat:"Ask Them", q:"What made you decide to join this company?",
    tip:"Personal, low-pressure, and often gets a genuinely candid answer — a good read on culture from someone who isn't reciting talking points."},
  {cat:"Ask Them", q:"What would make you excited about a candidate after this interview?",
    tip:"A bold, senior-feeling closer — it signals you're evaluating fit both ways, and gives you one last chance to address anything unspoken."},
];
const FLASHCARD_CATEGORIES = ["Behavioral","Motivation & Fit","Strengths & Growth","Curveballs","Ask Them"];

/* ---- State (not persisted — this is a practice session, not saved data) --- */
let fcDeck = [];       // current filtered (and possibly shuffled) working set
let fcIndex = 0;
let fcRevealed = false;
let fcCategory = "all";

function buildDeck(){
  fcDeck = fcCategory === "all" ? FLASHCARDS.slice() : FLASHCARDS.filter(c => c.cat === fcCategory);
  fcIndex = 0;
  fcRevealed = false;
}
function shuffleDeck(){
  for(let i = fcDeck.length - 1; i > 0; i--){
    const j = Math.floor(Math.random() * (i + 1));
    [fcDeck[i], fcDeck[j]] = [fcDeck[j], fcDeck[i]];
  }
  fcIndex = 0;
  fcRevealed = false;
}

/* ---- RENDER ---------------------------------------------------------------- */
function renderFlashcards(){
  $('#pageTitle').textContent = "Interview Flashcards";
  $('#pageSub').textContent   = "Practice out loud — no AI, no account, just the questions";
  if(!fcDeck.length) buildDeck();
  renderFlashcardsToolbar();
  renderFlashcardCard();
}

function renderFlashcardsToolbar(){
  $('#fcCategory').innerHTML = `<option value="all">All categories (${FLASHCARDS.length})</option>` +
    FLASHCARD_CATEGORIES.map(c => `<option value="${escapeAttr(c)}" ${c===fcCategory?'selected':''}>${escapeHtml(c)} (${FLASHCARDS.filter(f=>f.cat===c).length})</option>`).join("");
}

function renderFlashcardCard(){
  const el = $('#fcCard');
  if(!fcDeck.length){
    el.innerHTML = `<div class="r-empty">No cards in this category.</div>`;
    $('#fcCount').textContent = "0 / 0";
    return;
  }
  const card = fcDeck[fcIndex];
  $('#fcCount').textContent = (fcIndex + 1) + " / " + fcDeck.length;
  el.innerHTML = `
    <span class="fc-tag">${escapeHtml(card.cat)}</span>
    ${!fcRevealed
      ? `<p class="fc-question">${escapeHtml(card.q)}</p><span class="fc-hint">Tap to reveal the coaching tip</span>`
      : `<p class="fc-question fc-question-small">${escapeHtml(card.q)}</p><p class="fc-tip">${escapeHtml(card.tip)}</p>`}
  `;
  el.classList.toggle("revealed", fcRevealed);
  $('#fcPrev').disabled = fcIndex === 0;
  $('#fcNext').disabled = fcIndex === fcDeck.length - 1;
}

/* ---- INIT: bind delegated events once -------------------------------------- */
function initFlashcards(){
  buildDeck();

  $('#fcCategory').addEventListener("change", e => { fcCategory = e.target.value; buildDeck(); renderFlashcardCard(); });
  $('#fcShuffle').addEventListener("click", () => { shuffleDeck(); renderFlashcardCard(); toast("Shuffled"); });
  $('#fcCard').addEventListener("click", () => { fcRevealed = !fcRevealed; renderFlashcardCard(); });
  $('#fcCard').addEventListener("keydown", e => {
    if(e.key !== "Enter" && e.key !== " " && e.key !== "Spacebar") return;
    e.preventDefault();
    fcRevealed = !fcRevealed;
    renderFlashcardCard();
  });
  $('#fcPrev').addEventListener("click", () => { if(fcIndex > 0){ fcIndex--; fcRevealed = false; renderFlashcardCard(); } });
  $('#fcNext').addEventListener("click", () => { if(fcIndex < fcDeck.length - 1){ fcIndex++; fcRevealed = false; renderFlashcardCard(); } });
}
