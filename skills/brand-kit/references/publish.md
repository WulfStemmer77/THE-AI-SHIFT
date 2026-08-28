# Publish mode

Load and validate the brand package before producing anything. `BRAND.md` and `brand.tokens.json` override general aesthetic defaults; accessibility, factual accuracy, safety, and law remain hard constraints.

## Output routing

- **Web:** semantic HTML, responsive layouts, keyboard access, visible focus, contrast, alt text, and source-backed claims.
- **PDF/documents:** use the appropriate document/PDF workflow; preserve vector text and inspect every rendered page.
- **Presentations:** use the governed presentation skill and translate brand tokens into a certified presentation brand package.
- **Images:** use an approved available provider, then inspect anatomy, text, numbers, logos, people, rights, crop, and disclosure requirements.

## Claim integrity

Never invent prices, dates, metrics, addresses, testimonials, certifications, customers, or legal claims. Use conspicuous placeholders or source-backed values. Generated imagery must not imply an event, facility, product state, endorsement, or person that does not exist.

## Image generation

Start from the imagery contract in `brand.tokens.json`. Prompts must state composition, aspect ratio, subject placement, lighting, intended crop, allowed motifs, and explicit exclusions. Provider selection is an adapter decision, not part of the brand.

When Krea is selected, use the dedicated [Krea media adapter](providers/krea.md). Validate the request contract before invoking Krea, discover the current model/tool schema live, and preserve Krea job IDs and execution metadata in the provenance record.

## Visible disclosure helper

Use `scripts/ai_label.py` only after determining that a label is required or voluntarily desired. It provides a visible text label and optional metadata writing; it does not establish legal compliance by itself and does not replace provider-side machine-readable marking.

## Final QA

- validate package version and output profile
- inspect every final page/screen/image at target size
- verify tokens, banned terms, contrast, crop, and placeholders
- verify claims and asset provenance
- record deviations and named human approval
