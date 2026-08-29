# Asset pipeline

## 1. Use real assets first

Existing photography, product renders, CAD, approved technical diagrams, and brand assets are the strongest anchors. Do not regenerate a real product simply because generation is available.

## 2. Provider resolution

The skill is provider-neutral.

Preferred order:
1. existing approved assets;
2. connected provider explicitly requested by the user;
3. another connected media provider, after user approval;
4. an API script configured by the user;
5. placeholders for prototypes.

Do not assume KIE, Krea, OpenAI image generation, or any other vendor is present.

## 3. External-upload gate

Before uploading any local client asset to an external provider:
- identify the provider;
- identify which files will leave the local environment;
- ask for approval once for that batch/workflow;
- record the event in the asset manifest.

## 4. Style consistency

Write one style preamble for the visual family and reuse it verbatim.

For physical/technical subjects, add a geometry-lock block:
- shape/proportions;
- openings;
- roof/facade form;
- product silhouette;
- labels/logos;
- materials that must remain fixed.

Generated media that breaks the lock is rejected, not “fixed in copy.”

## 5. Camera moves for scrub

Scrub-friendly clips use:
- one continuous move;
- one primary direction;
- slow, controlled motion;
- subject remains in frame;
- no cuts;
- no subject entering/leaving unexpectedly;
- no morphing or geometry drift.

## 6. Posters

The poster should be extracted from the actual encoded clip, not separately generated, to avoid a visible first-frame jump.

## 7. Encoding

Dense keyframes improve arbitrary seeking. Use `scripts/encode.mjs` for desktop/mobile outputs. Remove audio from scrub clips.

## 8. Asset manifest

Example:

```json
{
  "assets": [
    {
      "path": "assets/hero.mp4",
      "source": "client-footage",
      "provider": null,
      "external_upload": false,
      "truth_status": "verified",
      "notes": "Encoded for scroll scrub"
    }
  ]
}
```
