Career OS — Local Fonts
=======================

These fonts are bundled so the product runs 100% offline (no Google Fonts / CDN).

Files (latin subset, .woff2):
  fraunces-roman.woff2    Fraunces, variable (opsz 9–144, wght 500–700)
  fraunces-italic.woff2   Fraunces italic, variable
  jost.woff2              Jost, variable (wght 400–600)
  spacemono-400.woff2     Space Mono, regular
  spacemono-700.woff2     Space Mono, bold

@font-face declarations live in fonts.css (linked from index.html before style.css).

Fallback: if any face fails to load, style.css degrades to system stacks:
  display  ->  Fraunces, "Iowan Old Style", "Palatino Linotype", Georgia, serif
  body     ->  Jost, -apple-system, "Segoe UI", Roboto, system-ui, sans-serif
  mono     ->  "Space Mono", ui-monospace, "SFMono-Regular", Menlo, monospace

Licensing: Fraunces, Jost, and Space Mono are licensed under the SIL Open Font
License 1.1, which permits bundling and redistribution with this product.
Source: Google Fonts.
