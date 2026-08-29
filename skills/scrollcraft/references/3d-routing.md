# 3D Routing: scrub media, WebGL, or hybrid

The term “3D scroll website” covers three different implementations. Pick deliberately.

## Route A — Pre-rendered scrub

A photoreal video or image sequence is mapped to scroll progress.

Best for:
- cinematic architecture/product reveals;
- construction or assembly sequences;
- controlled camera paths;
- strong mobile performance;
- exact art direction and lighting.

Weaknesses:
- visitor cannot freely rotate/inspect;
- every alternative camera path needs another render;
- changing product configuration may require new media.

Treat this as **cinematic scrollytelling**, not real-time 3D.

## Route B — Real WebGL 3D

Three.js, React Three Fiber, Babylon, or the current project's equivalent renders geometry live.

Best for:
- product configurators;
- exploded views with selectable parts;
- live material changes;
- pointer-driven orbit and inspection;
- spatial annotations that must stay attached to geometry;
- data-driven 3D states.

Weaknesses:
- asset optimization is real engineering work;
- mobile GPU/memory limits matter;
- lighting/render quality may be lower than offline CGI;
- accessibility and reduced-motion fallbacks are mandatory.

## Route C — Hybrid

Use a scrub/video for the emotional hero and a smaller real-time 3D scene for technical inspection.

This is often the best route for architecture and premium physical products: cinematic first impression, interactive proof later.

## Decision test

Ask one question:

> Does the visitor need to choose the camera/object state, or only control time?

If only time: scrub.
If camera/object state: WebGL.
If both: hybrid.

## Geometry lock

Before generating or rendering, list geometry that must not change: footprint, roof type, openings, module proportions, joints, materials, product silhouette. Reject any generated frame that violates the lock.
