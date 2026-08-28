# Layout system contract

The renderer owns exact geometry. The Slide Specification selects only an approved `layout_id` and supplies semantic slots.

## Core layout IDs

| Layout ID | Use | Required content |
| --- | --- | --- |
| `cover_v1` | Minimal opening | title, optional subtitle |
| `section_v1` | Chapter transition | section label, title |
| `statement_v1` | One decisive message | title, statement |
| `content_v1` | Explanation with one visual | title, summary, body or visual brief |
| `comparison_v1` | Two comparable states/options | title, exactly two columns |
| `metrics_v1` | KPI or evidence overview | title, 2–4 metrics |
| `cards_v1` | Products, capabilities, or pillars | title, 2–4 cards |
| `timeline_v1` | Ordered phases or milestones | title, 3–6 steps |
| `chart_v1` | Quantitative relationship | title, chart spec, source IDs |
| `close_v1` | Restrained CTA/contact close | title, CTA, optional contact |

Brand packages may disable core layouts or add namespaced layouts such as `afa.product_platform_v1`. Unregistered layout IDs fail validation.

## Fixed-frame invariants

The brand package must define:

- slide size (`16:9` or `A4-landscape`)
- background and cover variants
- safe content margins
- title and section-label zones
- logo light/dark variants, position, size, and clearance
- footer and page-number zones
- typography and color tokens
- grid, spacing scale, and supported density

The model must not override these values per slide.

## Density rules

- Cover slides remain minimal.
- Titles are single-line unless the registered layout explicitly permits two lines.
- A slide has one communication job.
- Shorten content or select another approved layout before reducing type.
- Repeated UI-like card grids are not a default visual language; use them only when the content is genuinely categorical.

## Visual rules

Use a diagram only when relationships are materially clearer than prose or a table. Quantitative charts must use supplied data and preserve truthful axes. Image briefs must state aspect ratio, composition, subject placement, and crop needs. Externally sourced assets require source IDs.
