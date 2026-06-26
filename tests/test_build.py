# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vinod Dhiman and UAGT contributors
"""Tests for the UAGT build pipeline: validation guarantees (NFR2), reproducibility
(NFR3), three-way coverage (FR1), relationship typing (FR3), and OSCAL output.

These lock the contracts that community PRs must not break.
"""
import json

import build_oscal
import build_tables as bt
import pytest

MANIFEST = bt.load_yaml(bt.MANIFEST_PATH)
CONTROLS = bt.load_controls()
ALLOWED_VERSIONS = {fw["id"]: fw["version"] for fw in MANIFEST["frameworks"]}


# --- The shipped data must be clean ----------------------------------------

def test_canonical_data_has_no_validation_problems():
    problems = bt.validate(CONTROLS, MANIFEST)
    assert problems == [], "\n".join(problems)


def test_controls_exist():
    assert len(CONTROLS) >= 1


def test_fr1_every_control_covers_the_three_anchor_frameworks():
    for c in CONTROLS:
        fws = {m["framework"] for m in c["mappings"]}
        missing = set(bt.REQUIRED_FRAMEWORKS) - fws
        assert not missing, f"{c['id']} missing {missing}"


def test_optional_frameworks_are_not_required_everywhere():
    # ISO/IEC 27001 is an attached framework: in the display order, not in the required set.
    assert "ISO-IEC-27001" in bt.FRAMEWORK_ORDER
    assert "ISO-IEC-27001" not in bt.REQUIRED_FRAMEWORKS
    # and at least one control actually uses it (the attachment is real, not just declared)
    assert any(m["framework"] == "ISO-IEC-27001" for c in CONTROLS for m in c["mappings"])


def test_versions_match_pinned_manifest():
    for c in CONTROLS:
        for m in c["mappings"]:
            assert m["version"] == ALLOWED_VERSIONS[m["framework"]], \
                f"{c['id']} {m['framework']} version {m['version']}"


def test_ids_unique_and_match_domain_enum():
    seen = set()
    for c in CONTROLS:
        assert c["id"] not in seen, f"duplicate {c['id']}"
        seen.add(c["id"])
        assert c["domain"] in bt.DOMAIN_LABELS, f"{c['id']} unknown domain {c['domain']}"


def test_relationship_none_has_null_ref_others_have_ref():
    for c in CONTROLS:
        for m in c["mappings"]:
            if m["relationship"] == "none":
                assert m.get("ref") in (None, ""), f"{c['id']} none mapping has a ref"
            else:
                assert m.get("ref"), f"{c['id']} {m['framework']} non-none mapping missing ref"


def test_every_mapping_has_principle_and_evidence():
    for c in CONTROLS:
        assert c.get("principle"), f"{c['id']} missing principle"
        assert c.get("evidence"), f"{c['id']} missing evidence"


# --- The validator must reject bad data ------------------------------------

def _bad(**overrides):
    base = {
        "_path": "data/controls/MC-D1-99.yaml",
        "id": "MC-D1-99",
        "title": "Synthetic bad control",
        "domain": "d1-accountability-governance",
        "objective": "A long enough objective string for the schema.",
        "principle": "Test principle",
        "evidence": ["test evidence"],
        "mappings": [
            {"framework": fw, "version": ALLOWED_VERSIONS[fw], "ref": "X.1", "label": "x",
             "relationship": "full", "confidence": "high",
             "rationale": "rationale long enough", "reviewer": "tester"}
            for fw in bt.REQUIRED_FRAMEWORKS
        ],
    }
    base.update(overrides)
    return base


def test_validator_flags_unknown_domain():
    problems = bt.validate([_bad(domain="not-a-domain")], MANIFEST)
    assert any("domain" in p for p in problems)


def test_validator_flags_version_mismatch():
    bad = _bad()
    bad["mappings"][0]["version"] = "1999"
    problems = bt.validate([bad], MANIFEST)
    assert any("version" in p for p in problems)


def test_validator_flags_missing_framework_fr1():
    bad = _bad()
    bad["mappings"] = bad["mappings"][:2]  # drop EU-AI-ACT
    problems = bt.validate([bad], MANIFEST)
    assert any("FR1" in p for p in problems)


def test_validator_flags_filename_id_mismatch():
    bad = _bad(id="MC-D2-99")  # path still says MC-D1-99
    problems = bt.validate([bad], MANIFEST)
    assert any("filename" in p for p in problems)


# --- Reproducibility (NFR3) ------------------------------------------------

def test_build_json_is_deterministic():
    a = json.dumps(bt.build_json(CONTROLS, MANIFEST), sort_keys=True)
    b = json.dumps(bt.build_json(bt.load_controls(), MANIFEST), sort_keys=True)
    assert a == b


def test_oscal_uuids_are_deterministic():
    assert build_oscal.det_uuid("catalog") == build_oscal.det_uuid("catalog")
    one = json.dumps(build_oscal.build_catalog(CONTROLS, MANIFEST), sort_keys=True)
    two = json.dumps(build_oscal.build_catalog(CONTROLS, MANIFEST), sort_keys=True)
    assert one == two


# --- OSCAL structure -------------------------------------------------------

def test_coverage_report_renders_all_frameworks():
    md = bt.render_coverage_md(CONTROLS, MANIFEST)
    assert "## Coverage by framework" in md
    assert "## Coverage by domain × framework" in md
    for fw in bt.FRAMEWORK_ORDER:
        assert bt.FRAMEWORK_LABELS[fw] in md


def test_oscal_catalog_shape():
    cat = build_oscal.build_catalog(CONTROLS, MANIFEST)["catalog"]
    assert cat["metadata"]["oscal-version"] == build_oscal.OSCAL_VERSION
    n_controls = sum(len(g["controls"]) for g in cat["groups"])
    assert n_controls == len(CONTROLS)
    ids = {ctrl["id"] for g in cat["groups"] for ctrl in g["controls"]}
    assert ids == {c["id"].lower() for c in CONTROLS}
