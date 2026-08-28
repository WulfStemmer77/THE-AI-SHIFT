#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("presentation_validate", ROOT / "scripts" / "validate.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class ValidatorTests(unittest.TestCase):
    def load(self, relative: str):
        return json.loads((ROOT / relative).read_text(encoding="utf-8"))

    def test_valid_fixture_passes(self):
        deck = self.load("evals/fixtures/valid-deck.json")
        brand = self.load("brands/afa/brand.json")
        self.assertEqual([], MODULE.validate(deck, brand))

    def test_invalid_fixture_fails_hard_rules(self):
        deck = self.load("evals/fixtures/invalid-deck.json")
        brand = self.load("brands/afa/brand.json")
        codes = {finding.code for finding in MODULE.validate(deck, brand)}
        self.assertTrue(
            {"E_LAYOUT_NOT_APPROVED", "E_FACT_SOURCE_REQUIRED", "E_SOURCE_UNKNOWN"}.issubset(codes)
        )

    def test_external_release_requires_certification_and_approval(self):
        deck = self.load("evals/fixtures/valid-deck.json")
        brand = self.load("brands/afa/brand.json")
        deck["deck"]["release_class"] = "external"
        codes = {finding.code for finding in MODULE.validate(deck, brand)}
        self.assertIn("E_BRAND_NOT_CERTIFIED", codes)
        self.assertIn("E_HUMAN_APPROVAL_REQUIRED", codes)


if __name__ == "__main__":
    unittest.main()
