# Optional Krea media adapter

Krea is an optional media-production route, not a runtime dependency.

## Rules

1. Prefer an already connected Krea MCP/OAuth session when available.
2. Never embed account credentials, tokens, project IDs, or user-specific paths in the skill.
3. Before the first upload of private/client media to Krea, obtain explicit user authorization.
4. Record every generated/transformed asset in `assets/manifest.json`.
5. For technical products, pass the geometry-lock reference assets and reject any result that mutates locked geometry.
6. Krea output is media input to the website. It does not replace SOURCE_OF_TRUTH validation.

## Typical operations

- generate-image
- image-to-image / controlled variation
- generate-video / image-to-video
- enhance / upscale
- workflow execution

Use the capabilities actually exposed by the connected Krea integration. Do not invent endpoints or credentials.
