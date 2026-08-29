# Verification

A scroll page has many states. A single screenshot proves almost nothing.

## Automated pass

When Playwright is available, sample the page across scroll positions at desktop, mobile, and reduced-motion viewports.

Look for:
- console/page errors;
- failed media requests;
- video that never advances;
- dead scroll spans;
- cues that never become fully readable;
- horizontal overflow;
- unexpected layout shifts;
- final CTA/statement disappearing before page end.

## Visual pass

Read the contact sheet in order.

Ask:
- Does every frame feel like the same brand/project?
- Is there an actual emotional/argument curve?
- Is the engineered peak visibly stronger?
- Are there awkward half-states between beautiful endpoints?
- Is copy placed over predictable visual quiet areas?

## Technical truth pass

If `SOURCE_OF_TRUTH.md` exists, compare all visible technical/product details against it:
- geometry;
- labels;
- dimensions;
- materials;
- assembly order;
- claims.

## Accessibility
- semantic reading order;
- keyboard focus;
- visible focus state;
- meaningful alt text where appropriate;
- no essential information available only through pointer hover;
- reduced-motion retains content and conversion path.

## Real device gap

Headless desktop browsers do not reproduce every iOS/Android video decoder, autoplay, low-power, memory, touch, or overscroll behavior. If no physical phone was tested, say so in `VALIDATION.md`.
