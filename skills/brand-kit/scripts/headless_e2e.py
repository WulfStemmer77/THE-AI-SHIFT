#!/usr/bin/env python3
"""Run the complete Brand Kit build, validation, demo, and image path headlessly."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str]) -> dict:
    result = subprocess.run(command, check=False, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed ({result.returncode}): {' '.join(command)}\n{result.stdout}\n{result.stderr}")
    return json.loads(result.stdout)


def tree_hashes(root: Path) -> dict[str, str]:
    return {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*")) if path.is_file()
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workdir", type=Path, help="Keep results in this directory instead of a temporary directory.")
    args = parser.parse_args()
    temporary = None
    if args.workdir:
        workdir = args.workdir.resolve()
        if workdir.exists() and any(workdir.iterdir()):
            raise SystemExit(f"Work directory must be empty: {workdir}")
        workdir.mkdir(parents=True, exist_ok=True)
    else:
        temporary = tempfile.TemporaryDirectory(prefix="ai-shift-brand-kit-")
        workdir = Path(temporary.name)

    python = sys.executable
    source = ROOT / "evals" / "fixtures" / "brand-source.valid.json"
    first, second = workdir / "brand-a", workdir / "brand-b"
    preflight = run([python, str(ROOT / "scripts" / "brandkit.py"), "preflight"])
    build_a = run([python, str(ROOT / "scripts" / "brandkit.py"), "build", str(source), str(first)])
    build_b = run([python, str(ROOT / "scripts" / "brandkit.py"), "build", str(source), str(second)])
    validation = run([python, str(ROOT / "scripts" / "brandkit.py"), "validate", str(first)])
    demo = run([python, str(ROOT / "scripts" / "brandkit.py"), "publish-demo", str(first), str(workdir / "published.html")])
    krea_request = run([python, str(ROOT / "scripts" / "validate_media_request.py"), str(ROOT / "evals" / "fixtures" / "krea-media-request.valid.json")])
    hashes_a, hashes_b = tree_hashes(first), tree_hashes(second)
    if hashes_a != hashes_b:
        raise RuntimeError("Deterministic build check failed: output trees differ.")

    raw = workdir / "raw.png"
    Image.new("RGB", (1600, 1000), (22, 27, 34)).save(raw)
    labelled = run([
        python, str(ROOT / "scripts" / "ai_label.py"), str(raw),
        "-o", str(workdir / "labelled.jpg"), "--width", "1120", "--aspect", "16:9",
    ])
    with Image.open(workdir / "labelled.jpg") as result_image:
        if result_image.size != (1120, 630):
            raise RuntimeError(f"Unexpected labelled image size: {result_image.size}")

    forbidden = ("affiliate link", "referral link", "commercial endorsement")
    leaks = []
    for path in list(first.rglob("*")) + [workdir / "published.html"]:
        if path.is_file() and path.suffix.lower() in {".md", ".json", ".css", ".html"}:
            lower = path.read_text(encoding="utf-8").lower()
            if any(term in lower for term in forbidden):
                leaks.append(str(path))
    if leaks:
        raise RuntimeError(f"Upstream identity leaked into generated output: {leaks}")

    report = {
        "status": "PASS",
        "workdir": str(workdir) if args.workdir else "temporary-cleaned",
        "preflight": preflight,
        "build": build_a["status"],
        "second_build": build_b["status"],
        "deterministic_file_count": len(hashes_a),
        "validation": validation["status"],
        "publish_demo": demo["status"],
        "image_path": labelled["status"],
        "krea_request_contract": krea_request["status"],
        "identity_leak_check": "PASS",
    }
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    if temporary:
        temporary.cleanup()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
