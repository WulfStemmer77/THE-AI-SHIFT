# Third-party notices and port notes

This Codex-native skill is a derivative adaptation of `scroll-craft` by Nate Herk:
https://github.com/nateherkai/scroll-craft

Upstream source reviewed: commit `e95798551874854cef6dd3996ec7de1364a82bbd`
(plugin version 0.2.0).

The upstream project is MIT licensed. The upstream copyright and permission
notice are retained verbatim in `LICENSE.upstream-scrollcraft`.

The THE-AI-SHIFT port changes the orchestration and governance layer substantially:
- removes Claude Code plugin packaging and Claude-specific invocation;
- replaces tool-name assumptions with Codex-compatible workflow guidance;
- makes media generation provider-neutral;
- adds Krea as an optional adapter without embedding credentials;
- adds an explicit external-upload/privacy gate;
- adds a source-of-truth / geometry-lock workflow for technical products;
- adds a decision gate between pre-rendered scroll scrub, real WebGL 3D, and hybrid;
- replaces the bash-only video encoder with a cross-platform Node wrapper;
- supports integration into existing React/Next/Vite/Astro projects instead of
  assuming one standalone HTML page;
- adds package-level manifests, schemas, evals, and release gates consistent with
  THE-AI-SHIFT skill governance.

Runtime concepts and portions of the engine are derived from upstream and remain
subject to the MIT notice above. New orchestration, governance, schemas, adapters,
and templates are part of the THE-AI-SHIFT port.
