---
name: scrollcraft
description: >
  Design, build, and verify premium scroll-driven websites in Codex. Use for
  scrollytelling, Apple-style scroll experiences, video scrubbing, pinned
  narrative sections, horizontal rails, continuous-world scroll journeys,
  interactive product stories, technical 3D-style presentations, and requests
  for a landing page that should feel like an experience rather than a document.
  The skill interviews the user, selects a page grammar, protects factual and
  geometric truth, chooses between pre-rendered scrub media and real WebGL 3D,
  builds semantic production code in the project's existing stack, and verifies
  the result across desktop, mobile, reduced-motion, and scroll states.
license: MIT
metadata:
  owner: THE-AI-SHIFT
  port: codex-native
  package-version: 1.0.0
  upstream: https://github.com/nateherkai/scroll-craft
  upstream-version-reviewed: 0.2.0
---

# Scrollcraft

Build scroll experiences as a combination of **narrative architecture, interaction design, visual craft, factual integrity, and runtime verification**.

The page is not a long animation with text pasted on top. Scroll is a timeline, but different parts of the timeline should use different interaction devices unless the user explicitly wants one continuous world.

## Deliverables

For every serious build, produce:

- `BRIEF.md` — user intent and constraints in the user's words.
- `SOURCE_OF_TRUTH.md` — required when the page communicates technical, architectural, product, financial, scientific, or regulated facts.
- `PLAN.md` — journey, grammar, feeling curve, peak, signature move, device score, asset plan, performance budget.
- production page/app code in the project's existing stack.
- `VALIDATION.md` — what was tested, failures found, fixes made, and anything not verified.
- screenshots/contact sheet when browser automation is available.
- one fingerprint row appended to the workspace registry after the build is accepted.

## Codex operating rules

1. **Use the current project stack unless there is a concrete reason not to.**
   - Existing Next.js/React/Vite/Astro project: integrate into it.
   - No framework: semantic HTML/CSS/JS is acceptable and often preferable.
   - Do not rewrite a working app into another framework merely to use this skill.
2. **Real markup is mandatory.** Headings, paragraphs, links, buttons, lists, tables, and accessible labels stay as DOM text. Never bake important copy into generated imagery or video.
3. **Do not generate the whole page from a config object.** Shared mechanisms are fine. The page structure itself must remain authored markup/components so projects do not collapse into one template.
4. **Do not assume tool names.** Codex environments vary. Use available shell/filesystem/browser/MCP/plugin tools. If a capability is missing, say so and use a documented fallback.
5. **External media generation is opt-in.** Never upload private/local client assets to a third-party provider merely because a key or MCP server exists. Explain the provider and request approval before first external upload.
6. **Never hardcode credentials.** Use environment variables, connected MCP/apps, or user-approved secret stores.
7. **Technical truth outranks visual drama.** If a generated image changes geometry, construction layers, dimensions, product details, logos, labels, or claims, reject it.

## Phase 0 — Preflight, no spend and no external upload

Run:

```bash
node <skill>/scripts/doctor.mjs
```

The preflight checks local capabilities only: Node, ffmpeg, browser automation, Chrome/Edge/Chromium, workspace resolution, and likely project stack. It must not call paid APIs or upload assets.

If required dependencies are missing, state exactly what is missing. Do not silently weaken verification.

## Phase 1 — Interview the user

Ask one compact set of questions. Reuse facts already present in the conversation or repository instead of making the user repeat them.

Capture:

1. **What is being sold or communicated, and to whom?**
2. **What must the visitor believe by the end?** One primary belief.
3. **What should the visitor do next?** One primary action and label.
4. **Vibe in 3–5 words**, plus up to three references from any medium.
5. **The intended scroll journey** in the user's words.
6. **Energy and feeling curve.** Where should it feel calm, technical, surprising, urgent, luxurious, etc.?
7. **The one moment the visitor should remember.** This becomes the engineered peak.
8. **Continuous world or distinct scenes?** Do not default one way or the other.
9. **What assets already exist?** Photos, renders, video, CAD/3D, brand kit, diagrams, technical drawings.
10. **What must never change?** Geometry, dimensions, brand marks, products, technical details, legal language, approved claims.

Write the answers to `<workspace>/builds/<name>/BRIEF.md`.

If the user is not available and the run is truly autonomous, create a self-authored brief and mark it clearly as `Self-authored, not interviewed`.

## Phase 2 — Establish the source of truth

Use this phase whenever the page is more than pure mood/brand work.

Create `SOURCE_OF_TRUTH.md` with three tables:

### A. Locked facts
Facts that may be displayed without modification.

Examples: dimensions, materials, product names, construction sequence, legal names, measured performance, approved prices.

### B. Locked geometry / appearance
Things image or video generation may not reinterpret.

Examples: roof form, facade openings, module proportions, wall layers, product silhouette, logo placement, colorway.

### C. Claims requiring verification
Anything plausible but not yet proven.

Never turn an unverified claim into a stat counter, headline, badge, technical annotation, or comparison.

For technical or architectural work, prefer real drawings, CAD exports, approved section views, and source photos over synthetic reconstruction.

## Phase 3 — Choose the 3D/media route

Read `references/3d-routing.md` before choosing a technology.

Use **pre-rendered scrub media** when:

- the narrative is linear;
- camera choreography matters more than object manipulation;
- the visitor does not need to rotate, inspect, or configure the object freely;
- photorealism and mobile performance matter most.

Use **real WebGL 3D** (Three.js / React Three Fiber / existing project engine) when:

- the visitor must rotate, inspect, explode, isolate, configure, or select parts;
- camera motion depends on live pointer/scroll input in more than one axis;
- the scene must react to changing product data;
- a pre-rendered clip would prevent meaningful interaction.

Use a **hybrid** when a photoreal scrub is the hero but one later section needs a real 3D technical explorer.

Do not call a video scrub “real-time 3D.” It is a cinematic scroll interaction, not an interactive 3D model.

## Phase 4 — Pick a page grammar

A grammar decides what the page *is*, not merely how it looks. Read `references/grammars.md`.

Choose exactly one primary grammar:

- filmic one-shot
- chaptered editorial
- live surface
- continuous world
- typographic poster
- gallery / catalog
- split stage
- rhythmic cutlist

A grammar has explicit bans. Respect them.

If choosing filmic one-shot, explain why the other grammars were worse for the brief; it is the easiest default to overuse.

## Phase 5 — Invent the signature move

Every build needs one interaction that belongs to that project alone.

A signature move is not:

- the same spotlight with a different color;
- a slightly different tilt strength;
- a generic magnetic button;
- a standard horizontal rail.

It should translate something specific about the brand/product into interaction.

Examples:

- a modular building assembles from structural frame to finished envelope as scroll advances;
- a product cutaway opens only when the pointer crosses a material seam;
- a hospitality development expands from one unit into an entire site plan;
- a data product lets the page's real telemetry become navigation.

Keep bespoke code in the page/project. Do not fork the shared engine for one project.

## Phase 6 — Fingerprint gate

Resolve the workspace:

```bash
node <skill>/scripts/workspace.mjs --ensure
```

Compare the plan against every row in `FINGERPRINTS.md` on six axes:

1. grammar
2. navigation treatment
3. hero device
4. act-sequence shape
5. close pattern
6. signature move

Require at least **4 of 6 dimensions different** from every existing row. If it fails, change the plan, not the registry.

## Phase 7 — Feeling curve and scroll score

Write the feeling curve **before** selecting devices.

For each beat, write:

`emotion → what on screen causes it`

Two adjacent beats with the same feeling usually indicate filler.

Choose one engineered peak. It receives:

- the strongest asset;
- the largest meaningful scroll span;
- quieter pacing immediately before it;
- the most memorable interaction or reveal.

Then assign a device per beat. Read `references/devices.md`.

Rules:

- usually 4+ device families on a multi-act page;
- never the same family twice in a row unless the grammar itself requires it;
- usually no more than two heavy video-scrub acts;
- every scroll span must change something visible or intentionally hold a meaningful state;
- total page length should be justified, not maximized.

Write the result to `PLAN.md`.

## Phase 8 — Asset pipeline

Read `references/assets.md`.

Priority order:

1. approved client assets;
2. CAD/3D renders or real photography produced for the project;
3. connected media provider approved by the user (for example a Krea MCP server if available);
4. another connected image/video provider approved by the user;
5. optional API script explicitly configured by the user;
6. placeholders only when the user requests a prototype.

### Provider-neutral asset manifest

For every generated/processed asset, record in `assets/manifest.json`:

- source / provider
- generation or processing type
- prompt or transformation summary
- reference assets used
- whether external upload occurred
- approval status
- technical-truth status: `verified`, `visual-only`, or `reject`

### Consistency rule

Write one **style preamble** per visual family and reuse it verbatim. For the same physical building/product, also write one **geometry lock block** describing elements that must not move or mutate.

### Scrub encoding

Use:

```bash
node <skill>/scripts/encode.mjs input.mp4 output.mp4
node <skill>/scripts/encode.mjs input.mp4 output-mobile.mp4 --mobile
```

Dense keyframes are intentional. Normal web video may play smoothly while seeking poorly.

## Phase 9 — Build

Use the existing project architecture.

### Vanilla / static

Copy:

```bash
cp <skill>/engine/scrollcraft.js ./scrollcraft.js
cp <skill>/engine/scrollcraft.css ./scrollcraft.css
```

Use semantic markup with `data-sc-*` attributes.

### React / Next / other component frameworks

- Keep the same semantic DOM and `data-sc-*` contract.
- Mount the engine after the relevant DOM exists.
- Clean up listeners/observers on unmount.
- Avoid server/client hydration mismatches.
- Respect framework image/font optimization only when it does not break scrub behavior.
- Lazy-load heavy 3D/video sections below the fold.

### Real WebGL 3D

If the route in Phase 3 selected WebGL:

- use the project's existing 3D stack where possible;
- isolate the renderer in one component/module;
- publish scroll progress through CSS custom properties or a small state adapter;
- cap DPR on mobile;
- dispose geometries/materials/textures on teardown;
- provide a static or video fallback for reduced motion and unsupported devices;
- do not make textual content dependent on WebGL rendering.

## Phase 10 — Design floor

Read `references/design-floor.md` before final styling.

Required qualities:

- coherent type scale and readable measure;
- intentional spacing rhythm;
- functional color roles with accessible contrast;
- depth from composition, not generic glow;
- motion that uses transforms/opacity where possible;
- copy anchors vary across acts;
- mobile is designed, not merely shrunk;
- reduced-motion still communicates the full argument.

Avoid obvious AI-site tropes: repeated feature-card grids, fake stats, generic purple gradients, gradient text, endless centered copy, decorative scroll cues, and identical section choreography.

## Phase 11 — Verify

Read `references/verify.md`.

Serve locally:

```bash
node <skill>/scripts/serve.mjs --root . --port 4500
```

When browser automation is available:

```bash
npm i -D playwright-core
node <skill>/scripts/shoot.mjs --url http://localhost:4500 --out lab/desktop
node <skill>/scripts/shoot.mjs --url http://localhost:4500 --out lab/mobile --width 390 --height 844
node <skill>/scripts/shoot.mjs --url http://localhost:4500 --out lab/reduced --reduced-motion
```

Check at minimum:

- no dead scroll;
- no cue that is permanently half-visible;
- videos actually decode and advance;
- no horizontal overflow;
- no layout shift from media/font loading;
- readable contrast over the brightest/darkest relevant media frames;
- keyboard focus order and visible focus;
- reduced-motion mode keeps meaning and CTA;
- mobile touch/scroll does not trap or jitter;
- technical geometry and annotations still match `SOURCE_OF_TRUTH.md`;
- page close resolves and holds.

If a real phone is available, test it. A headless desktop browser is not a substitute for iOS/Android decoder, autoplay, low-power, and touch behavior.

Write `VALIDATION.md` with what was actually verified. Do not write “fully tested” when real-device testing did not occur.

## Performance budget

Set explicit budgets in `PLAN.md`. Default starting targets for a premium landing page:

- LCP target: < 2.5 s on a representative mobile profile when practical;
- CLS: < 0.1;
- avoid large main-thread work during scroll;
- lazy-load below-fold video and WebGL;
- desktop scrub clips should be compressed and bounded; mobile receives dedicated smaller media;
- do not ship 4K media merely because the source is 4K;
- stop rendering 3D when offscreen;
- no scroll handler that performs layout reads and writes every event without batching.

These are budgets to engineer against, not guarantees. Measure the actual build.

## Hard rules

| Never | Instead |
|---|---|
| Generate assets before the journey and source-of-truth are clear | Plan first, spend second |
| Pretend a scrub video is live 3D | Name the technique honestly |
| Upload client assets to a third party silently | Get approval first |
| Invent dimensions, prices, stats, performance figures, or technical layers | Use verified source data only |
| Text baked into generated media | Real markup |
| Same device repeatedly with different copy | Change interaction or cut the act |
| Full-page dark overlay to rescue unreadable copy | Local scrim where the copy sits |
| Decorative “scroll to explore” instruction as a default | Let the first interaction teach itself |
| `transition: all` | Transition explicit properties |
| Animate layout-heavy properties when transform/opacity works | Prefer compositor-friendly motion |
| Ship without reduced-motion behavior | Provide a meaningful static/low-motion path |
| Ship real-time 3D without fallback | Static/video fallback |
| Change a locked product/building geometry for aesthetics | Reject the asset |
| Claim browser automation proves real-phone behavior | State the gap |

## Final report

Keep the report concise and evidence-based:

- chosen grammar and why;
- signature move;
- journey and engineered peak;
- media route: scrub / WebGL / hybrid;
- providers used and whether external upload occurred;
- fingerprint result;
- performance measurements available;
- desktop/mobile/reduced-motion verification;
- technical truth checks;
- remaining unverified items;
- local or deployed URL if one exists.

Append the accepted build's fingerprint row only after the plan/build is no longer being actively redesigned.
