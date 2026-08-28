# Governed workflow

## Execution package

Freeze these inputs before production:

- task ID and run ID
- skill, brand, renderer, schema, and adapter versions
- model identifier and generation parameters where controllable
- source manifest and retrieval/context manifest
- requested output format and slide size
- approval policy and revision limit

Hash the frozen package. A changed source, brand token, template, or context snapshot creates a new run.

## Pipeline

1. **Brief** — resolve audience, decision, purpose, and constraints.
2. **Evidence** — collect source-backed facts, data, assets, unknowns, and assumptions.
3. **Architecture** — define the narrative and assign an approved layout to each slide.
4. **Slide Specification** — emit schema-valid JSON; no raw geometry.
5. **Validation** — apply schema, business, evidence, brand, and policy checks.
6. **Rendering** — code resolves layout tokens and creates PPTX/PDF.
7. **Visual QA** — render all slides; inspect full-size images and deck-level flow.
8. **Human gate** — approve, reject, or request a bounded revision.
9. **Release** — store outputs, hashes, validation ledger, and run manifest.

## Modes

- `live`: retrieve current tool and knowledge results; store responses in the run record.
- `replay`: use frozen stored responses; never silently call live tools.

## Required validators

- **Schema:** required fields, types, enums, unique IDs, and valid references.
- **Business:** audience/purpose fit, approved slide count range when configured, and mandatory sections.
- **Evidence:** every factual claim has a valid source ID; assumptions are labelled.
- **Brand:** certified brand package, allowed layout, logo variant, fonts, colors, and fixed frame.
- **Visual:** no overflow, clipping, accidental overlap, broken crop, or title wrapping.
- **Release:** human approval and output hashes are recorded.

## Retry policy

Validation failures return structured error codes. The agent may revise only the failing semantic fields and may not bypass hard rules. After `max_revision_attempts`, stop and request human resolution.

## Run record

Store at least:

`run_id`, `task_id`, versions, input/context/source hashes, selected layouts, validation results, approval, output hashes, timestamps, and mode.
