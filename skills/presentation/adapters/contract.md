# Adapter contract

Every adapter must accept the same validated Slide Specification and immutable brand package. It may translate platform mechanics, but it may not change business meaning or geometry rules.

## Required operations

1. `preflight(execution_package) -> report`
2. `validate(deck_ir, brand_package) -> validation_result`
3. `render(deck_ir, brand_package) -> pptx, optional_pdf, render_manifest`
4. `render_preview(pptx) -> ordered_slide_images`
5. `collect_qa(slide_images) -> qa_ledger`
6. `release(outputs, run_record, approval) -> artifact_references`

## Required guarantees

- No raw geometry is accepted from model output.
- Layout IDs resolve only through the pinned renderer/brand registry.
- Live tool calls are recorded; replay mode uses stored responses.
- Rendered outputs and inputs are hashed.
- Validation failures are structured and cannot be converted to warnings by the agent.
- External release requires human approval while the package is in pilot.
