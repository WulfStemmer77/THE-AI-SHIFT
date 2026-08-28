---
name: brand-kit
description: Discover, build, validate, or apply a reusable brand system when a user needs consistent visual identity, design tokens, voice rules, reference surfaces, or governed branded output. Use for new or existing brands; do not invent unresolved brand decisions or silently install external tools.
metadata:
  version: 1.1.0
  status: pilot
---

# AI-SHIFT Brand Kit

Turn explicit brand decisions into a portable, versioned package that people and execution agents can use consistently. Separate discovery from deterministic generation: the model conducts the interview and structures decisions; scripts validate and build the working files.

## Select one mode

- **Setup** — inspect the environment and choose available providers. Read [references/setup.md](references/setup.md).
- **Interview** — elicit positioning, visual, verbal, format, and governance decisions. Read [references/interview.md](references/interview.md).
- **Build** — turn a completed `brand-source.json` into a working package. Read [references/build.md](references/build.md).
- **Publish** — apply a validated package to web, documents, presentations, or images. Read [references/publish.md](references/publish.md); for AI-content disclosure also read [references/compliance.md](references/compliance.md).
- **Krea media** — when Krea is selected for image, video, enhancement, upscaling, trained styles, or workflows, also read [references/providers/krea.md](references/providers/krea.md).

If the request spans several modes, run them in that order and stop at any unresolved hard gate.

## Non-negotiable rules

- Do not guess colors, fonts, positioning, forbidden language, logo geometry, or compliance decisions. Record unresolved items and ask for them.
- Do not install global packages, authenticate external services, spend credits, publish externally, or mutate another repository without explicit authorization at that point.
- Do not bind the package to one model, image provider, editor, or agent runtime.
- Use tokens instead of raw visual values in generated artifacts.
- Keep brand rules concise and executable; preserve rationale separately as reference material.
- Treat the generated `AGENTS.md` as project-local operating instructions. Platform adapters may derive other instruction files, but `BRAND.md` and `brand.tokens.json` remain authoritative.
- Never claim validation passed unless the deterministic validator and the relevant visual/human gates passed.

## Deterministic commands

From this skill directory:

```bash
python scripts/brandkit.py preflight
python scripts/brandkit.py build path/to/brand-source.json path/to/Brand
python scripts/brandkit.py validate path/to/Brand
python scripts/brandkit.py publish-demo path/to/Brand path/to/preview.html
python scripts/validate_media_request.py path/to/krea-media-request.json
```

For optional visible AI-content disclosure:

```bash
python scripts/ai_label.py input.png -o output.jpg --label "AI-generated" --width 1120 --aspect 16:9
```

The label helper is not a legal-compliance guarantee. Scope the obligation using the current official rules and the actual use case.

## Required package output

- `BRAND.md` — concise authoritative rules
- `REFERENCE.md` — interview rationale and extended context
- `brand.tokens.json` — machine-readable design/voice/format contract
- `brand.css` — executable CSS variables derived from tokens
- `AGENTS.md` — local agent operating rules
- `validation.json` — structured result with package hashes
- `examples/reference.html` — deterministic reference surface

Logo or wordmark files are included only when approved source assets or explicit construction rules exist. Never fabricate them merely to make the folder look complete.

## Release gates

1. Source contract complete.
2. Build deterministic and repeatable.
3. Package validator returns `PASS`.
4. Reference surface inspected at target sizes.
5. Any claims/assets traceable.
6. Human brand owner approves the version before external use.

After the configured retry limit, stop rather than weakening a hard rule.
