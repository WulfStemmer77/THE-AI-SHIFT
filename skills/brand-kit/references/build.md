# Build mode

Input is a completed `brand-source.json`. Use `scripts/brandkit.py build`; do not hand-author generated files when the script can produce them deterministically.

## Separation of concerns

- `REFERENCE.md` preserves rationale, rejected alternatives, and source context.
- `BRAND.md` contains the short binding rules used in daily production.
- `brand.tokens.json` is the machine contract.
- `brand.css` is a derived artifact; never edit it independently.
- `AGENTS.md` tells project-local agents how to resolve conflicts and apply the package.
- `examples/reference.html` demonstrates the tokens and core components with clearly marked sample content.

## Build rules

- Preserve every approved number, color, measure, font, percentage, and prohibition.
- Remove repetition and rationale from `BRAND.md`, not from `REFERENCE.md`.
- Convert prose to tables/contracts where this increases testability.
- Use only approved tokens in derived assets.
- Do not create a logo, wordmark, or mark without approved source assets or explicit construction rules.
- Build to a new directory or require an explicit force flag; never silently overwrite a brand package.

## Validation

Run `python scripts/brandkit.py validate <brand-directory>`. A `PASS` proves structural and deterministic invariants, not subjective quality. Human visual review remains required before certification.
