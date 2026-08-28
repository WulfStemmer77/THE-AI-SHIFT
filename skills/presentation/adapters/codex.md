# Codex adapter

Use the available presentation authoring runtime for PPTX creation. Keep the IR and validation independent from the rendering library.

## Execution

- Work in an isolated temporary build directory.
- Resolve the approved brand assets and exact renderer version before authoring.
- Use the platform-supported presentation artifact runtime; do not substitute an unapproved renderer.
- Resolve all coordinates from the selected layout and brand tokens.
- Preserve masters/layouts when a certified reference PPTX supplies them.
- Add source blocks to speaker notes for non-trivial claims and external assets.
- Render every final slide, inspect each at full size, and run overflow/overlap checks.
- Store the IR, manifest, validation ledger, QA ledger, and output hashes with the run.

This adapter is an execution profile, not permission to call external image or data services.
