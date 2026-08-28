# Brand package preflight and certification

## Required inputs

- approved brand book and owner
- master PPTX or equivalent fixed-frame specification
- logo files with light/dark variants and clearance rules
- licensed font files or approved fallbacks
- primary, secondary, neutral, and semantic color tokens
- approved gradients with exact values and direction
- slide size, safe margins, title zone, footer, and page-number geometry
- approved layouts and density limits
- representative approved decks and Golden Slides
- image style and provider policy
- claim/source and legal/compliance requirements

Image provider policy may name approved routes such as Krea, Flora, or Higgsfield and the permitted MCP/CLI/API path. A provider name alone does not grant authorization to call it.

## Certification states

- `draft`: incomplete package; internal watermarked output only.
- `candidate`: assets and tokens complete; validation/evals pending.
- `certified`: Golden Slides pass, visual QA passes, and brand owner approves.
- `deprecated`: blocked for new runs but retained for replay.

## Certification procedure

1. Validate the brand JSON against `schema/brand.schema.json`.
2. Confirm every referenced asset exists and hash it.
3. Render the Golden Slide set using the production renderer.
4. Compare fixed-frame geometry and tokens deterministically; inspect rendered images visually.
5. Run all eval cases and record results.
6. Obtain named human approval and publish an immutable brand version.

Do not label output pixel-perfect or certified when this sequence is incomplete.

## AFA package status

The AFA package must preserve its concise chapter system, section label, title, short explanatory sentence, metric blocks, product/platform cards, restrained close, and the established themes of precision, premium user experience, co-creation, global expertise/local support, and “Connect. Collaborate. Create.”

As of package version `0.1.0`, exact AFA master geometry, approved logo assets, font files, gradient tokens, and Golden Slides are not present in this repository. Therefore AFA remains `draft` until those assets are installed and certified.
