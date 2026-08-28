#!/usr/bin/env python3
"""Deterministic builder and validator for AI-SHIFT brand packages."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


VERSION = "1.0.0"
HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")
ROOT = Path(__file__).resolve().parents[1]
REQUIRED_OUTPUTS = (
    "brand-source.json",
    "BRAND.md",
    "REFERENCE.md",
    "brand.tokens.json",
    "brand.css",
    "AGENTS.md",
    "examples/reference.html",
)


@dataclass(frozen=True)
class Finding:
    code: str
    path: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {"code": self.code, "path": self.path, "message": self.message}


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def pretty_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def require_object(value: Any, path: str, findings: list[Finding]) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    findings.append(Finding("E_TYPE_OBJECT", path, "Expected an object."))
    return {}


def require_text(value: Any, path: str, findings: list[Finding], minimum: int = 1) -> str:
    if not isinstance(value, str) or len(value.strip()) < minimum:
        findings.append(Finding("E_TEXT_REQUIRED", path, f"Expected at least {minimum} characters."))
        return ""
    return value.strip()


def require_list(value: Any, path: str, findings: list[Finding], minimum: int = 1, maximum: int | None = None) -> list[Any]:
    if not isinstance(value, list):
        findings.append(Finding("E_TYPE_ARRAY", path, "Expected an array."))
        return []
    if len(value) < minimum:
        findings.append(Finding("E_ARRAY_TOO_SHORT", path, f"Expected at least {minimum} items."))
    if maximum is not None and len(value) > maximum:
        findings.append(Finding("E_ARRAY_TOO_LONG", path, f"Expected at most {maximum} items."))
    return value


def reject_unknown(value: dict[str, Any], allowed: set[str], path: str, findings: list[Finding]) -> None:
    for key in sorted(set(value) - allowed):
        findings.append(Finding("E_UNKNOWN_FIELD", f"{path}.{key}", "Field is not allowed by the contract."))


def validate_source(source: Any) -> list[Finding]:
    findings: list[Finding] = []
    root = require_object(source, "$", findings)
    reject_unknown(root, {"schema_version", "brand", "positioning", "personality", "architecture", "visual", "voice", "formats", "imagery", "governance", "references", "open_decisions"}, "$", findings)
    if root.get("schema_version") != "1.0.0":
        findings.append(Finding("E_SCHEMA_VERSION", "$.schema_version", "Expected 1.0.0."))

    required = ("brand", "positioning", "personality", "architecture", "visual", "voice", "formats", "imagery", "governance", "open_decisions")
    for key in required:
        if key not in root:
            findings.append(Finding("E_REQUIRED", f"$.{key}", "Required field is missing."))

    brand = require_object(root.get("brand"), "$.brand", findings)
    reject_unknown(brand, {"id", "name", "version", "language"}, "$.brand", findings)
    brand_id = require_text(brand.get("id"), "$.brand.id", findings)
    if brand_id and not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,62}", brand_id):
        findings.append(Finding("E_BRAND_ID", "$.brand.id", "Use 2–63 lowercase letters, digits, or hyphens."))
    for key in ("name", "version", "language"):
        require_text(brand.get(key), f"$.brand.{key}", findings)

    positioning = require_object(root.get("positioning"), "$.positioning", findings)
    reject_unknown(positioning, {"one_liner", "audiences", "category", "promise", "differentiators", "evidence"}, "$.positioning", findings)
    require_text(positioning.get("one_liner"), "$.positioning.one_liner", findings, 20)
    require_list(positioning.get("audiences"), "$.positioning.audiences", findings)
    require_text(positioning.get("category"), "$.positioning.category", findings)
    require_text(positioning.get("promise"), "$.positioning.promise", findings)
    require_list(positioning.get("differentiators"), "$.positioning.differentiators", findings)
    if not isinstance(positioning.get("evidence"), list):
        findings.append(Finding("E_TYPE_ARRAY", "$.positioning.evidence", "Expected an array."))

    personality = require_object(root.get("personality"), "$.personality", findings)
    reject_unknown(personality, {"traits", "anti_traits"}, "$.personality", findings)
    require_list(personality.get("traits"), "$.personality.traits", findings, 3, 6)
    require_list(personality.get("anti_traits"), "$.personality.anti_traits", findings, 2)

    architecture = require_object(root.get("architecture"), "$.architecture", findings)
    reject_unknown(architecture, {"model", "rules"}, "$.architecture", findings)
    if architecture.get("model") not in {"single-brand", "endorsed", "house-of-brands", "hybrid"}:
        findings.append(Finding("E_ARCHITECTURE_MODEL", "$.architecture.model", "Unsupported brand architecture model."))
    require_list(architecture.get("rules"), "$.architecture.rules", findings)

    visual = require_object(root.get("visual"), "$.visual", findings)
    reject_unknown(visual, {"colors", "typography", "layout", "spacing", "forbidden"}, "$.visual", findings)
    colors = require_object(visual.get("colors"), "$.visual.colors", findings)
    reject_unknown(colors, {"background", "surface", "text", "muted", "border", "accent", "accent_ink", "accent_max_percent"}, "$.visual.colors", findings)
    for key in ("background", "surface", "text", "muted", "border", "accent", "accent_ink"):
        value = colors.get(key)
        if not isinstance(value, str) or not HEX.fullmatch(value):
            findings.append(Finding("E_COLOR_HEX", f"$.visual.colors.{key}", "Expected #RRGGBB."))
    percent = colors.get("accent_max_percent")
    if not isinstance(percent, (int, float)) or isinstance(percent, bool) or not 1 <= percent <= 40:
        findings.append(Finding("E_ACCENT_PERCENT", "$.visual.colors.accent_max_percent", "Expected a number from 1 to 40."))

    typography = require_object(visual.get("typography"), "$.visual.typography", findings)
    reject_unknown(typography, {"display", "body", "mono"}, "$.visual.typography", findings)
    for role in ("display", "body", "mono"):
        font = require_object(typography.get(role), f"$.visual.typography.{role}", findings)
        reject_unknown(font, {"family", "fallback", "license_confirmed"}, f"$.visual.typography.{role}", findings)
        family = require_text(font.get("family"), f"$.visual.typography.{role}.family", findings)
        fallback = require_text(font.get("fallback"), f"$.visual.typography.{role}.fallback", findings)
        if any(character in family + fallback for character in ("{", "}", ";", "<", ">", "\\", "\n", "\r")):
            findings.append(Finding("E_FONT_TOKEN", f"$.visual.typography.{role}", "Font values contain unsafe CSS characters."))
        if font.get("license_confirmed") is not True:
            findings.append(Finding("E_FONT_LICENSE", f"$.visual.typography.{role}.license_confirmed", "Font license must be confirmed."))

    layout = require_object(visual.get("layout"), "$.visual.layout", findings)
    reject_unknown(layout, {"content_width_px", "page_padding_px", "radius_px", "composition"}, "$.visual.layout", findings)
    ranges = {"content_width_px": (640, 1920), "page_padding_px": (16, 240), "radius_px": (0, 80)}
    for key, (low, high) in ranges.items():
        value = layout.get(key)
        if not isinstance(value, int) or isinstance(value, bool) or not low <= value <= high:
            findings.append(Finding("E_LAYOUT_RANGE", f"$.visual.layout.{key}", f"Expected integer {low}–{high}."))
    require_text(layout.get("composition"), "$.visual.layout.composition", findings)
    require_list(visual.get("spacing"), "$.visual.spacing", findings, 4, 8)
    require_list(visual.get("forbidden"), "$.visual.forbidden", findings)

    voice = require_object(root.get("voice"), "$.voice", findings)
    reject_unknown(voice, {"address", "tone", "good_example", "bad_example", "banned_terms"}, "$.voice", findings)
    require_text(voice.get("address"), "$.voice.address", findings)
    require_list(voice.get("tone"), "$.voice.tone", findings, 2, 6)
    require_text(voice.get("good_example"), "$.voice.good_example", findings, 10)
    require_text(voice.get("bad_example"), "$.voice.bad_example", findings, 10)
    require_list(voice.get("banned_terms"), "$.voice.banned_terms", findings)

    formats = require_list(root.get("formats"), "$.formats", findings)
    for index, item in enumerate(formats):
        fmt = require_object(item, f"$.formats[{index}]", findings)
        reject_unknown(fmt, {"id", "width", "height", "unit"}, f"$.formats[{index}]", findings)
        require_text(fmt.get("id"), f"$.formats[{index}].id", findings)
        if fmt.get("unit") not in {"px", "mm", "in"}:
            findings.append(Finding("E_FORMAT_UNIT", f"$.formats[{index}].unit", "Expected px, mm, or in."))
        for key in ("width", "height"):
            value = fmt.get(key)
            if not isinstance(value, (int, float)) or isinstance(value, bool) or value <= 0:
                findings.append(Finding("E_FORMAT_SIZE", f"$.formats[{index}].{key}", "Expected a positive number."))

    imagery = require_object(root.get("imagery"), "$.imagery", findings)
    reject_unknown(imagery, {"modes", "allowed", "forbidden", "people_policy", "disclosure_policy"}, "$.imagery", findings)
    modes = require_list(imagery.get("modes"), "$.imagery.modes", findings)
    if any(mode not in {"photography", "illustration", "generated", "none"} for mode in modes):
        findings.append(Finding("E_IMAGERY_MODE", "$.imagery.modes", "Unsupported imagery mode."))
    if not isinstance(imagery.get("allowed"), list):
        findings.append(Finding("E_TYPE_ARRAY", "$.imagery.allowed", "Expected an array."))
    require_list(imagery.get("forbidden"), "$.imagery.forbidden", findings)
    require_text(imagery.get("people_policy"), "$.imagery.people_policy", findings)
    require_text(imagery.get("disclosure_policy"), "$.imagery.disclosure_policy", findings)

    governance = require_object(root.get("governance"), "$.governance", findings)
    reject_unknown(governance, {"owner", "approval_required", "deviation_policy"}, "$.governance", findings)
    require_text(governance.get("owner"), "$.governance.owner", findings)
    if not isinstance(governance.get("approval_required"), bool):
        findings.append(Finding("E_APPROVAL_BOOL", "$.governance.approval_required", "Expected true or false."))
    require_text(governance.get("deviation_policy"), "$.governance.deviation_policy", findings)

    open_decisions = root.get("open_decisions")
    if not isinstance(open_decisions, list):
        findings.append(Finding("E_TYPE_ARRAY", "$.open_decisions", "Expected an array."))
    elif open_decisions:
        findings.append(Finding("E_OPEN_DECISIONS", "$.open_decisions", "Resolve all open decisions before build."))
    return findings


def make_tokens(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "brand": source["brand"],
        "positioning": {key: source["positioning"][key] for key in ("one_liner", "audiences", "promise", "differentiators")},
        "personality": source["personality"],
        "visual": source["visual"],
        "voice": source["voice"],
        "formats": source["formats"],
        "imagery": source["imagery"],
        "governance": source["governance"],
        "build": {
            "generator": "ai-shift-brand-kit",
            "generator_version": VERSION,
            "source_hash": sha256_bytes(canonical_bytes(source)),
        },
    }


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def render_brand_md(source: dict[str, Any]) -> str:
    b, p, pe, v, voice, imagery, gov = (source[key] for key in ("brand", "positioning", "personality", "visual", "voice", "imagery", "governance"))
    colors, type_, layout = v["colors"], v["typography"], v["layout"]
    color_rows = "\n".join(f"| `{key}` | `{value}` |" for key, value in colors.items() if key != "accent_max_percent")
    type_rows = "\n".join(f"| {role} | {font['family']} | {font['fallback']} |" for role, font in type_.items())
    format_rows = "\n".join(f"| {item['id']} | {item['width']} × {item['height']} {item['unit']} |" for item in source["formats"])
    return f"""# {b['name']} Brand System

Version `{b['version']}` · Language `{b['language']}` · Owner `{gov['owner']}`

## Brand in one sentence

{p['one_liner']}

**Promise:** {p['promise']}

**Personality:** {', '.join(pe['traits'])}. Never: {', '.join(pe['anti_traits'])}.

## Audiences

{bullet_list(p['audiences'])}

## Differentiators

{bullet_list(p['differentiators'])}

## Color tokens

| Token | Value |
| --- | --- |
{color_rows}

Accent remains at or below **{colors['accent_max_percent']}%** of the visible surface.

## Typography

| Role | Family | Fallback |
| --- | --- | --- |
{type_rows}

## Composition and spacing

- Composition: {layout['composition']}
- Content width: {layout['content_width_px']} px
- Page padding: {layout['page_padding_px']} px
- Radius: {layout['radius_px']} px
- Spacing scale: {', '.join(str(x) for x in v['spacing'])} px

## Visual prohibitions

{bullet_list(v['forbidden'])}

## Voice

- Address: {voice['address']}
- Tone: {', '.join(voice['tone'])}
- Good: “{voice['good_example']}”
- Bad: “{voice['bad_example']}”
- Banned terms: {', '.join(voice['banned_terms'])}

## Formats

| ID | Size |
| --- | --- |
{format_rows}

## Imagery

- Modes: {', '.join(imagery['modes'])}
- Allowed: {', '.join(imagery['allowed']) or 'None'}
- Forbidden: {', '.join(imagery['forbidden'])}
- People: {imagery['people_policy']}
- Disclosure: {imagery['disclosure_policy']}

## Governance

- External approval required: {'yes' if gov['approval_required'] else 'no'}
- Deviations: {gov['deviation_policy']}

## Release checklist

- [ ] Package validator passes.
- [ ] Only defined tokens are used.
- [ ] Visual and verbal prohibitions pass.
- [ ] Claims and assets are traceable.
- [ ] Target sizes have been visually inspected.
- [ ] Brand owner approval is recorded where required.
"""


def render_reference_md(source: dict[str, Any]) -> str:
    return "# Brand discovery reference\n\nThis file preserves the approved discovery input and rationale. `BRAND.md` is authoritative for daily production.\n\n```json\n" + pretty_json(source).rstrip() + "\n```\n"


def font_stack(font: dict[str, Any]) -> str:
    return f"'{font['family']}', {font['fallback']}"


def render_css(source: dict[str, Any]) -> str:
    colors = source["visual"]["colors"]
    type_ = source["visual"]["typography"]
    layout = source["visual"]["layout"]
    spacing = source["visual"]["spacing"]
    template = (ROOT / "assets" / "brand.css.template").read_text(encoding="utf-8")
    replacements = {
        "<BACKGROUND>": colors["background"], "<SURFACE>": colors["surface"],
        "<TEXT>": colors["text"], "<MUTED>": colors["muted"],
        "<BORDER>": colors["border"], "<ACCENT>": colors["accent"],
        "<ACCENT_INK>": colors["accent_ink"], "<DISPLAY_STACK>": font_stack(type_["display"]),
        "<BODY_STACK>": font_stack(type_["body"]), "<MONO_STACK>": font_stack(type_["mono"]),
        "<CONTENT_WIDTH>": str(layout["content_width_px"]), "<PAGE_PADDING>": str(layout["page_padding_px"]),
        "<RADIUS>": str(layout["radius_px"]), "<SPACE_1>": str(spacing[0]),
        "<SPACE_2>": str(spacing[1]), "<SPACE_3>": str(spacing[2]), "<SPACE_4>": str(spacing[3]),
    }
    for old, new in replacements.items():
        template = template.replace(old, new)
    return template


def render_agents(source: dict[str, Any]) -> str:
    template = (ROOT / "assets" / "AGENTS.md.template").read_text(encoding="utf-8")
    return template.replace("<BRAND_NAME>", source["brand"]["name"])


def render_reference_html(source: dict[str, Any], css: str) -> str:
    b, p, v, voice = source["brand"], source["positioning"], source["visual"], source["voice"]
    forbidden = "".join(f"<li>{escape_html(item)}</li>" for item in v["forbidden"])
    return f"""<!doctype html>
<html lang="{escape_html(b['language'])}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape_html(b['name'])} reference</title><style>{css}
.page{{max-width:var(--brand-content-width);margin:auto;padding:var(--brand-page-padding)}}
.label{{font-family:var(--brand-font-mono);color:var(--brand-accent);text-transform:uppercase;letter-spacing:.12em}}
.hero{{padding:var(--brand-space-4) 0;border-bottom:1px solid var(--brand-border)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:var(--brand-space-3);padding:var(--brand-space-4) 0}}
.sample{{background:var(--brand-surface);border:1px solid var(--brand-border);border-radius:var(--brand-radius);padding:var(--brand-space-3)}}
.muted{{color:var(--brand-muted)}}
</style></head>
<body><main class="page"><section class="hero"><p class="label">Reference surface · sample content</p>
<h1>{escape_html(b['name'])}</h1><p>{escape_html(p['one_liner'])}</p></section>
<section class="grid"><article class="sample"><h2>Promise</h2><p>{escape_html(p['promise'])}</p></article>
<article class="sample"><h2>Voice</h2><p>{escape_html(voice['good_example'])}</p></article>
<article class="sample"><h2>Never</h2><ul>{forbidden}</ul></article></section>
<p class="muted">This reference uses sample content and must not be treated as a factual publication.</p></main></body></html>"""


def escape_html(value: str) -> str:
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build(source_path: Path, output: Path, force: bool = False) -> dict[str, Any]:
    source = load_json(source_path)
    findings = validate_source(source)
    if findings:
        return {"status": "FAIL", "findings": [item.as_dict() for item in findings]}
    if output.exists() and any(output.iterdir()) and not force:
        return {"status": "FAIL", "findings": [Finding("E_OUTPUT_NOT_EMPTY", str(output), "Output directory is not empty; use --force to replace generated files.").as_dict()]}
    output.mkdir(parents=True, exist_ok=True)
    (output / "examples").mkdir(exist_ok=True)
    tokens = make_tokens(source)
    css = render_css(source)
    files = {
        "brand-source.json": pretty_json(source),
        "BRAND.md": render_brand_md(source),
        "REFERENCE.md": render_reference_md(source),
        "brand.tokens.json": pretty_json(tokens),
        "brand.css": css,
        "AGENTS.md": render_agents(source),
        "examples/reference.html": render_reference_html(source, css),
    }
    for relative, content in files.items():
        path = output / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
    return validate_package(output, write_result=True)


def validate_package(output: Path, write_result: bool = False) -> dict[str, Any]:
    findings: list[Finding] = []
    for relative in REQUIRED_OUTPUTS:
        if not (output / relative).is_file():
            findings.append(Finding("E_OUTPUT_MISSING", relative, "Required generated file is missing."))
    tokens: dict[str, Any] = {}
    source: dict[str, Any] = {}
    if (output / "brand-source.json").is_file():
        try:
            source = load_json(output / "brand-source.json")
            findings.extend(validate_source(source))
        except (OSError, json.JSONDecodeError) as exc:
            findings.append(Finding("E_SOURCE_JSON", "brand-source.json", str(exc)))
    if (output / "brand.tokens.json").is_file():
        try:
            tokens = load_json(output / "brand.tokens.json")
        except (OSError, json.JSONDecodeError) as exc:
            findings.append(Finding("E_TOKENS_JSON", "brand.tokens.json", str(exc)))
    if tokens:
        if tokens.get("schema_version") != "1.0.0":
            findings.append(Finding("E_PACKAGE_SCHEMA", "brand.tokens.json", "Expected schema version 1.0.0."))
        build_meta = tokens.get("build") if isinstance(tokens.get("build"), dict) else {}
        if build_meta.get("generator") != "ai-shift-brand-kit" or build_meta.get("generator_version") != VERSION:
            findings.append(Finding("E_GENERATOR", "brand.tokens.json", "Unexpected generator identity or version."))
        if source and build_meta.get("source_hash") != sha256_bytes(canonical_bytes(source)):
            findings.append(Finding("E_SOURCE_HASH", "brand.tokens.json", "Source hash does not match brand-source.json."))
    if source and tokens and make_tokens(source) != tokens:
        findings.append(Finding("E_DERIVATION", "brand.tokens.json", "Token package is not the deterministic derivation of source."))
    hashes = {}
    for relative in REQUIRED_OUTPUTS:
        path = output / relative
        if path.is_file():
            hashes[relative] = sha256_bytes(path.read_bytes())
    payload = {"status": "PASS" if not findings else "FAIL", "generator_version": VERSION, "findings": [item.as_dict() for item in findings], "hashes": hashes}
    if write_result:
        (output / "validation.json").write_text(pretty_json(payload), encoding="utf-8", newline="\n")
    return payload


def publish_demo(brand_dir: Path, output: Path, force: bool = False) -> dict[str, Any]:
    validation = validate_package(brand_dir)
    if validation["status"] != "PASS":
        return validation
    if output.exists() and not force:
        return {"status": "FAIL", "findings": [Finding("E_OUTPUT_EXISTS", str(output), "Output exists; use --force to replace it.").as_dict()]}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text((brand_dir / "examples" / "reference.html").read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
    return {"status": "PASS", "output": str(output), "sha256": sha256_bytes(output.read_bytes()), "findings": []}


def preflight() -> dict[str, Any]:
    try:
        import PIL  # type: ignore
        pillow = getattr(PIL, "__version__", "available")
    except ImportError:
        pillow = None
    return {
        "status": "PASS",
        "python": sys.version.split()[0],
        "capabilities": {
            "brand_build": True,
            "brand_validate": True,
            "image_transform": pillow is not None,
            "pillow_version": pillow,
            "git": shutil.which("git") is not None,
            "browser_pdf": next((name for name in ("google-chrome", "chromium", "chromium-browser", "msedge") if shutil.which(name)), None),
            "metadata_writer": shutil.which("exiftool") is not None,
        },
    }


def emit(payload: dict[str, Any]) -> int:
    print(pretty_json(payload), end="")
    return 0 if payload.get("status") == "PASS" else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("preflight")
    build_p = sub.add_parser("build")
    build_p.add_argument("source", type=Path)
    build_p.add_argument("output", type=Path)
    build_p.add_argument("--force", action="store_true")
    validate_p = sub.add_parser("validate")
    validate_p.add_argument("brand_dir", type=Path)
    demo_p = sub.add_parser("publish-demo")
    demo_p.add_argument("brand_dir", type=Path)
    demo_p.add_argument("output", type=Path)
    demo_p.add_argument("--force", action="store_true")
    args = parser.parse_args()
    try:
        if args.command == "preflight":
            return emit(preflight())
        if args.command == "build":
            return emit(build(args.source, args.output, args.force))
        if args.command == "validate":
            return emit(validate_package(args.brand_dir, write_result=True))
        return emit(publish_demo(args.brand_dir, args.output, args.force))
    except (OSError, json.JSONDecodeError) as exc:
        return emit({"status": "FAIL", "findings": [Finding("E_INPUT", "$", str(exc)).as_dict()]})


if __name__ == "__main__":
    raise SystemExit(main())
