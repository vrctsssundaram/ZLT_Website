# V24 — High-Resolution Semiconductor Cinematic Media

## Objective
Replace the short explanatory hero sequence with a longer, self-explanatory semiconductor technology film while preserving truthful positioning around Zepto Logic's actual work.

## Hero media contract
- 64-second master loop that repeats indefinitely in the browser
- 1920×1080 desktop master
- 720×1280 portrait mobile derivation from the high-resolution master
- WebM + MP4 fallbacks
- high-quality static posters for reduced-motion and load fallback
- no chapter HUD, process labels, duration labels, watermark, third-party logo or stock-media dependency
- discreet Pause / Play motion control remains

The visual sequence moves from broad semiconductor-industry context into the company's direct engineering domain: digital architecture, routed logic, FPGA hardware, secure compute and connected/edge system concepts. Fabrication imagery is visual context only; the commercial copy continues to position Zepto Logic around semiconductor IP, front-end design, verification, FPGA engineering and applied R&D.

## Technical page films
Products, Engineering, Applications and R&D use higher-resolution 1280×720 domain films at approximately 24 seconds each. Film metadata overlays have been removed; adjacent copy explains the engineering proposition instead of narrating the animation.

## Quality and compatibility
- mobile receives a portrait crop rather than a stretched landscape file
- desktop uses the 1080p master
- object-fit and poster fallbacks cover intermediate device sizes
- reduced-motion uses static posters
- section films start only when near the viewport
- Save-Data starts optional section films paused while preserving explicit user opt-in
- active page media remains locally hosted

## V24 cleanup
- retired hero chapter HUD removed from HTML, CSS and runtime synchronization
- obsolete section-film labels removed
- duplicated V23 runtime block removed
- sticky page-nav active-chip tracking changed to horizontal-only movement to prevent layout instability
- browser QA validates actual decoded duration and intrinsic resolution
