# Interview mode

The interview produces `brand-source.json`, not final artwork. Ask in compact rounds, include a reasoned recommendation for consequential choices, and do not repeat answered questions.

## Decision order

1. **Core:** offering, audiences, market category, promise, differentiation, evidence.
2. **Personality:** 3–6 traits and explicit anti-traits.
3. **Architecture:** master brand, sub-brands, product brands, personal name usage.
4. **References:** 2–3 positive references and at least one near-but-wrong counterexample; identify what to borrow, not what to copy.
5. **Color:** surface strategy, primary neutrals, one or two meaningful accents, usage percentages, contrast requirements, light/dark modes.
6. **Typography:** display, body, optional mono/data roles; licensing and fallbacks.
7. **Composition:** grid, whitespace, symmetry, radii, borders, shadows, gradients, glass, motion.
8. **Components and signature:** recurring components and one recognisable device where justified.
9. **Voice:** language, form of address, tone, good/bad paired example, banned words and claims.
10. **Formats:** actual output types, dimensions, print requirements, responsive breakpoints.
11. **Imagery:** photography/illustration/generated assets, allowed and forbidden motifs, people/rights constraints, treatment and disclosure policy.
12. **Governance:** brand owner, approval gate, versioning, allowed deviations, regional variants.

## Push back on weak inputs

- “Modern and professional” is not discriminating. Ask for an extreme and a counterexample.
- “All colors” defeats the system. Ask for surface percentages and semantic roles.
- An empty banned list is rarely credible. Ask what the brand must never sound or look like.
- A visual reference without a named property invites imitation. Ask what exact trait is relevant.

## Completion gate

Validate the source against `schema/brand-source.schema.json`. Unknowns remain explicit in `open_decisions`; do not convert them into plausible defaults. Build may proceed only when all fields marked required by the schema are resolved.
