#!/usr/bin/env python3
"""Deterministic business validator for presentation IR and brand packages."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


CORE_LAYOUTS = {
    "cover_v1",
    "section_v1",
    "statement_v1",
    "content_v1",
    "comparison_v1",
    "metrics_v1",
    "cards_v1",
    "timeline_v1",
    "chart_v1",
    "close_v1",
}


@dataclass(frozen=True)
class Finding:
    code: str
    path: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {"code": self.code, "path": self.path, "message": self.message}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate(deck: Any, brand: Any | None = None) -> list[Finding]:
    findings: list[Finding] = []

    if not isinstance(deck, dict):
        return [Finding("E_ROOT_TYPE", "$", "Deck specification must be a JSON object.")]

    for key in ("schema_version", "run", "deck", "sources", "slides"):
        if key not in deck:
            findings.append(Finding("E_REQUIRED", f"$.{key}", "Required field is missing."))

    if deck.get("schema_version") != "1.0.0":
        findings.append(Finding("E_SCHEMA_VERSION", "$.schema_version", "Expected schema version 1.0.0."))

    run = deck.get("run") if isinstance(deck.get("run"), dict) else {}
    deck_meta = deck.get("deck") if isinstance(deck.get("deck"), dict) else {}
    sources = deck.get("sources") if isinstance(deck.get("sources"), list) else []
    slides = deck.get("slides") if isinstance(deck.get("slides"), list) else []

    source_ids: set[str] = set()
    for index, source in enumerate(sources):
        path = f"$.sources[{index}]"
        if not isinstance(source, dict):
            findings.append(Finding("E_SOURCE_TYPE", path, "Source must be an object."))
            continue
        source_id = source.get("id")
        if not isinstance(source_id, str) or not source_id.startswith("SRC-"):
            findings.append(Finding("E_SOURCE_ID", f"{path}.id", "Source ID must start with SRC-."))
        elif source_id in source_ids:
            findings.append(Finding("E_SOURCE_DUPLICATE", f"{path}.id", "Source ID must be unique."))
        else:
            source_ids.add(source_id)
        for key in ("title", "locator"):
            if not source.get(key):
                findings.append(Finding("E_REQUIRED", f"{path}.{key}", "Required source field is missing."))

    approved_layouts = set(CORE_LAYOUTS)
    if isinstance(brand, dict):
        approved_layouts = set(brand.get("approved_layouts") or [])
        if run.get("brand_id") != brand.get("brand_id"):
            findings.append(Finding("E_BRAND_ID_MISMATCH", "$.run.brand_id", "Run and brand package IDs differ."))
        if run.get("brand_version") != brand.get("brand_version"):
            findings.append(Finding("E_BRAND_VERSION_MISMATCH", "$.run.brand_version", "Run and brand versions differ."))
        if deck_meta.get("format") not in set(brand.get("slide_formats") or []):
            findings.append(Finding("E_FORMAT_NOT_APPROVED", "$.deck.format", "Slide format is not approved by the brand package."))
        if deck_meta.get("release_class") == "external" and brand.get("certification_status") != "certified":
            findings.append(Finding("E_BRAND_NOT_CERTIFIED", "$.deck.release_class", "External release requires a certified brand package."))

    seen_slides: set[str] = set()
    if not slides:
        findings.append(Finding("E_SLIDES_EMPTY", "$.slides", "At least one slide is required."))

    for index, slide in enumerate(slides):
        path = f"$.slides[{index}]"
        if not isinstance(slide, dict):
            findings.append(Finding("E_SLIDE_TYPE", path, "Slide must be an object."))
            continue
        slide_id = slide.get("slide_id")
        if not isinstance(slide_id, str) or not slide_id.startswith("SLIDE-"):
            findings.append(Finding("E_SLIDE_ID", f"{path}.slide_id", "Slide ID must start with SLIDE-."))
        elif slide_id in seen_slides:
            findings.append(Finding("E_SLIDE_DUPLICATE", f"{path}.slide_id", "Slide ID must be unique."))
        else:
            seen_slides.add(slide_id)

        if not slide.get("title"):
            findings.append(Finding("E_TITLE_REQUIRED", f"{path}.title", "Slide title is required."))
        elif len(slide["title"]) > 90:
            findings.append(Finding("E_TITLE_TOO_LONG", f"{path}.title", "Slide title exceeds 90 characters."))

        if slide.get("layout_id") not in approved_layouts:
            findings.append(Finding("E_LAYOUT_NOT_APPROVED", f"{path}.layout_id", "Layout is not approved by the brand package."))

        for claim_index, claim in enumerate(slide.get("claims") or []):
            claim_path = f"{path}.claims[{claim_index}]"
            if not isinstance(claim, dict):
                findings.append(Finding("E_CLAIM_TYPE", claim_path, "Claim must be an object."))
                continue
            referenced = claim.get("source_ids") or []
            if claim.get("kind") == "fact" and not referenced:
                findings.append(Finding("E_FACT_SOURCE_REQUIRED", f"{claim_path}.source_ids", "Factual claims require at least one source."))
            for source_id in referenced:
                if source_id not in source_ids:
                    findings.append(Finding("E_SOURCE_UNKNOWN", f"{claim_path}.source_ids", f"Unknown source ID: {source_id}"))

        for source_id in slide.get("asset_source_ids") or []:
            if source_id not in source_ids:
                findings.append(Finding("E_SOURCE_UNKNOWN", f"{path}.asset_source_ids", f"Unknown source ID: {source_id}"))

    approval = deck.get("approval") if isinstance(deck.get("approval"), dict) else {}
    if deck_meta.get("release_class") == "external" and approval.get("status") != "approved":
        findings.append(Finding("E_HUMAN_APPROVAL_REQUIRED", "$.approval.status", "External release requires human approval."))

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deck", type=Path, help="Path to deck IR JSON")
    parser.add_argument("--brand", type=Path, help="Path to brand package JSON")
    args = parser.parse_args()

    try:
        deck = load_json(args.deck)
        brand = load_json(args.brand) if args.brand else None
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "FAIL", "findings": [{"code": "E_INPUT", "path": "$", "message": str(exc)}]}, indent=2))
        return 2

    findings = validate(deck, brand)
    payload = {"status": "PASS" if not findings else "FAIL", "findings": [item.as_dict() for item in findings]}
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
