Career OS — Icons
=================

Icons are inline SVG, defined as path strings on each module's `icon` field in
js/modules.js and drawn by the renderer inside a 24×24 stroked <svg>. Nav,
stat, and UI icons are inlined directly in index.html / js/app.js.

Keeping icons inline (rather than as files here) means zero extra network
requests and full offline support. This folder is reserved for any future
raster/exported icon assets; the placeholder set ships inline.
