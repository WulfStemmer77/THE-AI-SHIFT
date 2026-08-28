---
name: presentation
description: Create, revise, validate, or certify governed business presentations when repeatable structure, brand compliance, traceable claims, fixed layouts, or deterministic PPTX/PDF output matters. Use for centrally managed enterprise presentation production; do not use for casual one-off slides where governance is unnecessary.
metadata:
  version: 0.1.0
  status: pilot
---

# Governed Presentation Production

Produce presentations through a typed intermediate representation (IR). The model decides meaning, narrative, evidence, and one approved layout ID. Code owns coordinates, typography, spacing, logos, footers, page numbers, and export.

## Non-negotiable boundary

Never let generative output set raw `x`, `y`, `width`, `height`, font, logo, footer, or page-number geometry. Never claim pixel-perfect brand compliance unless the selected brand package is certified and the rendered deck passes validation and visual QA.

## Workflow

1. Establish topic, audience, purpose, output format, brand package, and evidence requirements. Ask only when a missing item materially changes the result.
2. Run the brand preflight in [references/brand-certification.md](references/brand-certification.md). Stop certification when required assets or tokens are missing; a clearly labelled draft may still be produced.
3. Read [references/workflow.md](references/workflow.md) and create a `deck.schema.json`-conformant Slide Specification. Use only approved layout IDs from [references/layout-system.md](references/layout-system.md).
4. Validate before rendering:

   ```bash
   python scripts/validate.py path/to/deck.json --brand path/to/brand.json
   ```

5. Render through an approved adapter. Read only the relevant adapter guide in `adapters/`.
6. Render every slide to images, inspect each slide at full size, and fix overflow, unintended overlap, wrapping, weak hierarchy, inconsistent elements, and bad crops.
7. Run validation again against the final IR and brand package. Release only when schema, business, brand, source, visual, and human gates pass.

## Semantic decisions allowed to the model

- narrative arc and slide sequence
- slide purpose and approved `layout_id`
- claim selection, synthesis, and concise audience-facing copy
- chart type or visual brief when evidence supports it
- what remains unknown and what needs human approval

## Deterministic decisions reserved for code

- slide size and all geometry
- master/layout selection and fixed frame
- typography tokens and minimum sizes
- logo variant, position, and clearance
- margins, spacing, footer, and page numbering
- chart scales derived from supplied data
- overflow, schema, source, and policy enforcement

## Evidence and release rules

- Every non-trivial factual claim must reference a source ID or be marked as an assumption/unknown.
- Audience-facing slide copy must not expose planning notes or internal reasoning.
- Prefer shortening copy or changing layouts over shrinking type.
- Human approval is mandatory for externally distributed decks while this package is `pilot`.
- Keep skills, brand package, renderer, schema, context, and model versions in the run manifest.
- Record validation results and output hashes for every released run.

## Resources

- Build and gate logic: [references/workflow.md](references/workflow.md)
- Layout contract: [references/layout-system.md](references/layout-system.md)
- Brand onboarding and certification: [references/brand-certification.md](references/brand-certification.md)
- Cross-platform contract: [adapters/contract.md](adapters/contract.md)
- Codex execution: [adapters/codex.md](adapters/codex.md)
- Microsoft execution: [adapters/copilot-studio.md](adapters/copilot-studio.md)
- IR schema: [schema/deck.schema.json](schema/deck.schema.json)
- Brand schema: [schema/brand.schema.json](schema/brand.schema.json)
- Eval contract: [evals/eval-manifest.json](evals/eval-manifest.json)

## Release stop conditions

Return `FAIL` instead of improvising when the IR is invalid, a required source is missing, the requested layout is not approved, the brand package is uncertified for a certified release, or visual QA identifies unresolved defects. Retry only within the configured limit; then require human intervention.
