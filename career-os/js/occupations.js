/* =========================================================================
   CAREER OS — OCCUPATIONS  (the edition definitions)
   -------------------------------------------------------------------------
   ONE config object controls every edition. Switching occupation only:
     • overwrites four CSS custom properties (the jewel accent), and
     • swaps example placeholder text + the greeting / tagline / seal letter.

   The parchment + gold identity NEVER changes, so all editions feel like one
   line. To ship "Career OS — Healthcare Edition" you duplicate the folder and
   change the default in js/app.js — you do NOT touch any view code.

   ----- HOW TO ADD A NEW EDITION (copy an entry, change the values) -----
   key:  { name, edition, seal, accent, accent2, tagline, greet, roleEx, skillEx }

     key      short id used internally + saved to localStorage (lowercase).
     name     label shown in the switcher + topbar ("General", "Healthcare"…).
     edition  the stamped sub-title under the brand ("Clinical Edition").
     seal     ONE letter shown in the brand seal + hero watermark.
     accent   the jewel accent hex — the ONLY color that changes per edition.
     accent2  a lighter pair, used for the switcher swatch gradient.
     tagline  mono sub-line in the topbar / dashboard.
     greet    hero headline — wrap ONE word in <em>…</em> to italicise it.
     roleEx   example job title, used as a field placeholder.
     skillEx  example skills list, used as a field placeholder.

   Accents are the kickoff's jewel set: parchment + gold stay fixed.
   ========================================================================= */

const OCCUPATIONS = {
  // General — oxblood / claret. The default, broadest edition.
  general: {
    name: "General",    edition: "General Edition",   seal: "C",
    accent: "#73263A",  accent2: "#9A3450",
    tagline: "Your career command room",
    greet: "Built to get you <em>hired</em>.",
    roleEx: "Senior Project Manager",
    skillEx: "stakeholder management, Agile, budgeting",
  },

  // Healthcare — deep peacock.
  nurse: {
    name: "Healthcare", edition: "Clinical Edition",  seal: "N",
    accent: "#0E5A57",  accent2: "#15807A",
    tagline: "Composed for clinical careers",
    greet: "Land the <em>unit</em> you actually want.",
    roleEx: "ICU Registered Nurse",
    skillEx: "critical care, Epic/EHR, patient advocacy",
  },

  // Software / Tech — ink indigo.
  swe: {
    name: "Technology", edition: "Technical Edition", seal: "T",
    accent: "#283A78",  accent2: "#3C52A0",
    tagline: "Composed for engineers & IT",
    greet: "A resume that <em>passes</em> the screen.",
    roleEx: "Senior Software Engineer",
    skillEx: "React, distributed systems, CI/CD",
  },

  // Teaching / Education — cognac.
  teacher: {
    name: "Education",  edition: "Educator Edition",  seal: "E",
    accent: "#8A4A24",  accent2: "#B0622F",
    tagline: "Composed for teachers",
    greet: "Turn classroom impact into <em>offers</em>.",
    roleEx: "5th Grade Lead Teacher",
    skillEx: "differentiated instruction, SEL, assessment",
  },

  // Executive — graphite espresso.
  exec: {
    name: "Executive",  edition: "Executive Edition", seal: "X",
    accent: "#2C2723",  accent2: "#4A4038",
    tagline: "Composed for senior leaders",
    greet: "Position yourself for the <em>C-suite</em>.",
    roleEx: "VP of Operations",
    skillEx: "P&L ownership, org design, M&A integration",
  },
};
