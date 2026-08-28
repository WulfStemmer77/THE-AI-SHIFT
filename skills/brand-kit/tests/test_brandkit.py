#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


brandkit = load_module("ai_shift_brandkit", ROOT / "scripts" / "brandkit.py")
ai_label = load_module("ai_shift_ai_label", ROOT / "scripts" / "ai_label.py")
media_request = load_module("ai_shift_media_request", ROOT / "scripts" / "validate_media_request.py")


class BrandKitTests(unittest.TestCase):
    def source(self, name: str = "brand-source.valid.json"):
        return json.loads((ROOT / "evals" / "fixtures" / name).read_text(encoding="utf-8"))

    def test_valid_source_passes(self):
        self.assertEqual([], brandkit.validate_source(self.source()))

    def test_invalid_source_fails_meaningful_rules(self):
        codes = {item.code for item in brandkit.validate_source(self.source("brand-source.invalid.json"))}
        self.assertTrue({"E_OPEN_DECISIONS", "E_FONT_LICENSE", "E_COLOR_HEX", "E_ACCENT_PERCENT"}.issubset(codes))

    def test_rejects_css_injection_in_font_tokens(self):
        source = self.source()
        source["visual"]["typography"]["display"]["family"] = "Safe</style><script>"
        codes = {item.code for item in brandkit.validate_source(source)}
        self.assertIn("E_FONT_TOKEN", codes)

    def test_rejects_unknown_contract_fields(self):
        source = self.source()
        source["visual"]["colors"]["second_accent"] = "#FF00FF"
        codes = {item.code for item in brandkit.validate_source(source)}
        self.assertIn("E_UNKNOWN_FIELD", codes)

    def test_build_is_deterministic_and_valid(self):
        source = ROOT / "evals" / "fixtures" / "brand-source.valid.json"
        with tempfile.TemporaryDirectory() as temp:
            a, b = Path(temp) / "a", Path(temp) / "b"
            self.assertEqual("PASS", brandkit.build(source, a)["status"])
            self.assertEqual("PASS", brandkit.build(source, b)["status"])
            files_a = {str(p.relative_to(a)): p.read_bytes() for p in a.rglob("*") if p.is_file()}
            files_b = {str(p.relative_to(b)): p.read_bytes() for p in b.rglob("*") if p.is_file()}
            self.assertEqual(files_a, files_b)
            self.assertEqual("PASS", brandkit.validate_package(a)["status"])

    def test_build_refuses_nonempty_output(self):
        source = ROOT / "evals" / "fixtures" / "brand-source.valid.json"
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "brand"
            output.mkdir()
            (output / "user-file.txt").write_text("preserve", encoding="utf-8")
            result = brandkit.build(source, output)
            self.assertEqual("FAIL", result["status"])
            self.assertEqual("preserve", (output / "user-file.txt").read_text(encoding="utf-8"))

    def test_visible_image_label_path(self):
        with tempfile.TemporaryDirectory() as temp:
            raw, output = Path(temp) / "raw.png", Path(temp) / "out.jpg"
            Image.new("RGB", (1600, 1000), (20, 24, 30)).save(raw)
            args = ai_label.parser().parse_args([str(raw), "-o", str(output), "--width", "1120", "--aspect", "16:9"])
            result = ai_label.transform(args)
            self.assertEqual("PASS", result["status"])
            with Image.open(output) as im:
                self.assertEqual((1120, 630), im.size)

    def test_krea_media_request_contract_passes(self):
        request = json.loads((ROOT / "evals" / "fixtures" / "krea-media-request.valid.json").read_text(encoding="utf-8"))
        self.assertEqual([], media_request.validate(request))

    def test_krea_request_rejects_secrets_and_unapproved_spend(self):
        request = json.loads((ROOT / "evals" / "fixtures" / "krea-media-request.valid.json").read_text(encoding="utf-8"))
        request["api_token"] = "krea_secret_should_never_be_here"
        request["governance"]["credit_spend_authorized"] = False
        codes = {item.code for item in media_request.validate(request)}
        self.assertTrue({"E_SECRET_FIELD", "E_CREDIT_AUTHORIZATION"}.issubset(codes))


if __name__ == "__main__":
    unittest.main()
