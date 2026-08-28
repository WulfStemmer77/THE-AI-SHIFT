#!/usr/bin/env python3
"""Validate a governed Krea media request without calling Krea or spending credits."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


HASH = re.compile(r"^[0-9a-f]{64}$")
ASPECT = re.compile(r"^[1-9][0-9]*:[1-9][0-9]*$")
OPERATIONS = {"generate-image", "generate-video", "enhance", "upscale", "run-workflow"}
SECRET_KEYS = {"token", "api_token", "api_key", "authorization", "password", "secret"}


@dataclass(frozen=True)
class Finding:
    code: str
    path: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {"code": self.code, "path": self.path, "message": self.message}


def obj(value: Any, path: str, findings: list[Finding]) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    findings.append(Finding("E_TYPE_OBJECT", path, "Expected an object."))
    return {}


def unknown(value: dict[str, Any], allowed: set[str], path: str, findings: list[Finding]) -> None:
    for key in sorted(set(value) - allowed):
        findings.append(Finding("E_UNKNOWN_FIELD", f"{path}.{key}", "Field is not allowed."))


def text(value: Any, path: str, findings: list[Finding], minimum: int = 1) -> str:
    if not isinstance(value, str) or len(value.strip()) < minimum:
        findings.append(Finding("E_TEXT_REQUIRED", path, f"Expected at least {minimum} characters."))
        return ""
    return value.strip()


def scan_secrets(value: Any, path: str, findings: list[Finding]) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if key.lower() in SECRET_KEYS:
                findings.append(Finding("E_SECRET_FIELD", f"{path}.{key}", "Secrets must not be stored in media requests."))
            scan_secrets(item, f"{path}.{key}", findings)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            scan_secrets(item, f"{path}[{index}]", findings)
    elif isinstance(value, str) and ("bearer " in value.lower() or value.startswith("krea_")):
        findings.append(Finding("E_SECRET_VALUE", path, "Value resembles a credential."))


def validate(request: Any) -> list[Finding]:
    findings: list[Finding] = []
    root = obj(request, "$", findings)
    scan_secrets(root, "$", findings)
    unknown(root, {"schema_version", "provider", "connection", "operation", "brand", "request", "governance"}, "$", findings)
    if root.get("schema_version") != "1.0.0":
        findings.append(Finding("E_SCHEMA_VERSION", "$.schema_version", "Expected 1.0.0."))
    if root.get("provider") != "krea":
        findings.append(Finding("E_PROVIDER", "$.provider", "Provider must be krea."))
    if root.get("connection") not in {"mcp-oauth", "api-token"}:
        findings.append(Finding("E_CONNECTION", "$.connection", "Expected mcp-oauth or api-token."))
    operation = root.get("operation")
    if operation not in OPERATIONS:
        findings.append(Finding("E_OPERATION", "$.operation", "Unsupported Krea operation."))

    brand = obj(root.get("brand"), "$.brand", findings)
    unknown(brand, {"id", "version", "package_hash"}, "$.brand", findings)
    text(brand.get("id"), "$.brand.id", findings)
    text(brand.get("version"), "$.brand.version", findings)
    package_hash = brand.get("package_hash")
    if not isinstance(package_hash, str) or not HASH.fullmatch(package_hash):
        findings.append(Finding("E_PACKAGE_HASH", "$.brand.package_hash", "Expected a lowercase SHA-256 hash."))

    media = obj(root.get("request"), "$.request", findings)
    unknown(media, {"model_or_workflow_id", "trained_style_id", "live_schema_checked_at", "prompt", "exclusions", "aspect_ratio", "input_assets"}, "$.request", findings)
    text(media.get("model_or_workflow_id"), "$.request.model_or_workflow_id", findings)
    if media.get("trained_style_id") is not None:
        text(media.get("trained_style_id"), "$.request.trained_style_id", findings)
    checked_at = text(media.get("live_schema_checked_at"), "$.request.live_schema_checked_at", findings)
    if checked_at:
        try:
            datetime.fromisoformat(checked_at.replace("Z", "+00:00"))
        except ValueError:
            findings.append(Finding("E_SCHEMA_TIMESTAMP", "$.request.live_schema_checked_at", "Expected an ISO 8601 timestamp."))
    text(media.get("prompt"), "$.request.prompt", findings, 20)
    exclusions = media.get("exclusions")
    if not isinstance(exclusions, list) or not exclusions or any(not isinstance(item, str) or not item.strip() for item in exclusions):
        findings.append(Finding("E_EXCLUSIONS", "$.request.exclusions", "Expected at least one non-empty exclusion."))
    elif len(exclusions) != len(set(exclusions)):
        findings.append(Finding("E_EXCLUSIONS_DUPLICATE", "$.request.exclusions", "Exclusions must be unique."))
    ratio = media.get("aspect_ratio")
    if not isinstance(ratio, str) or not ASPECT.fullmatch(ratio):
        findings.append(Finding("E_ASPECT", "$.request.aspect_ratio", "Expected a ratio such as 16:9."))
    assets = media.get("input_assets")
    if not isinstance(assets, list):
        findings.append(Finding("E_ASSETS", "$.request.input_assets", "Expected an array."))
        assets = []
    for index, item in enumerate(assets):
        asset = obj(item, f"$.request.input_assets[{index}]", findings)
        unknown(asset, {"id", "hash", "rights_confirmed"}, f"$.request.input_assets[{index}]", findings)
        text(asset.get("id"), f"$.request.input_assets[{index}].id", findings)
        if not isinstance(asset.get("hash"), str) or not HASH.fullmatch(asset["hash"]):
            findings.append(Finding("E_ASSET_HASH", f"$.request.input_assets[{index}].hash", "Expected a lowercase SHA-256 hash."))
        if asset.get("rights_confirmed") is not True:
            findings.append(Finding("E_ASSET_RIGHTS", f"$.request.input_assets[{index}].rights_confirmed", "Input rights must be confirmed."))
    if operation in {"enhance", "upscale"} and not assets:
        findings.append(Finding("E_INPUT_ASSET_REQUIRED", "$.request.input_assets", "This operation requires an input asset."))

    governance = obj(root.get("governance"), "$.governance", findings)
    unknown(governance, {"workspace_reference", "credit_spend_authorized", "max_attempts", "human_review_required"}, "$.governance", findings)
    text(governance.get("workspace_reference"), "$.governance.workspace_reference", findings)
    if governance.get("credit_spend_authorized") is not True:
        findings.append(Finding("E_CREDIT_AUTHORIZATION", "$.governance.credit_spend_authorized", "Credit spending must be explicitly authorized."))
    attempts = governance.get("max_attempts")
    if not isinstance(attempts, int) or isinstance(attempts, bool) or not 1 <= attempts <= 6:
        findings.append(Finding("E_MAX_ATTEMPTS", "$.governance.max_attempts", "Expected an integer from 1 to 6."))
    if governance.get("human_review_required") is not True:
        findings.append(Finding("E_HUMAN_REVIEW", "$.governance.human_review_required", "Human review must remain enabled."))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("request", type=Path)
    args = parser.parse_args()
    try:
        payload = json.loads(args.request.read_text(encoding="utf-8"))
        findings = validate(payload)
        result = {"status": "PASS" if not findings else "FAIL", "findings": [item.as_dict() for item in findings]}
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0 if not findings else 1
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "FAIL", "findings": [{"code": "E_INPUT", "path": "$", "message": str(exc)}]}, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
