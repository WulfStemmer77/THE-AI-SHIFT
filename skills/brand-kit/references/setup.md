# Setup mode

Setup is a read-only preflight unless the user separately authorizes installation or authentication.

## Inspect

Run:

```bash
python scripts/brandkit.py preflight
```

Report core and optional capabilities separately:

- Python 3.10+ — deterministic build and validation
- Pillow — optional image labelling/transformation
- Git — versioning
- Chromium/Chrome/Edge — optional HTML-to-PDF route
- ExifTool — optional metadata writing
- approved image-generation connector/CLI — optional and provider-specific

Missing optional tooling must not block interview, build, validation, or HTML publishing.

## Provider selection

Use the provider already approved and available in the current environment. Possible routes include built-in image generation, an authorized MCP connector, or an approved CLI/API. Do not install or authenticate a provider merely because this skill mentions it.

Record the selected execution profile in the run manifest. Provider choice must not alter the brand contract.

## External dependencies

Do not auto-install auxiliary writing, SEO, accessibility, interview, or image skills. Use an already available applicable skill when present. If a missing capability materially blocks the requested output, ask before installing anything.
