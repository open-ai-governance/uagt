#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vinod Dhiman and UAGT contributors
"""Build an OSCAL catalog of the Master Control Set from the canonical YAML source.

Output: build/oscal/uagt-catalog.json — an OSCAL 1.1.2 catalog where each Master Control
is an OSCAL control under its governance-domain group. The three-way crosswalk is encoded
as structured control props (class = framework id) plus links to back-matter resources for
each source framework, so OSCAL-aware GRC tooling can ingest the mapping natively (FR5).

The OSCAL *mapping* model is not part of the stable 1.1.2 schema bundle, so the catalog
(with crosswalk props) is the validated, portable representation we publish in v1.1.

UUIDs are derived deterministically (uuid5) so rebuilds are byte-stable (NFR3).

Usage:
  python scripts/build_oscal.py            # validate data + write catalog
  python scripts/build_oscal.py --check    # validate data only, no write
  python scripts/build_oscal.py --validate-schema PATH   # also validate against an OSCAL schema
"""
from __future__ import annotations

import argparse
import json
import sys
import uuid

import yaml

from build_tables import (
    DOMAIN_LABELS,
    FRAMEWORK_LABELS,
    FRAMEWORK_ORDER,
    MANIFEST_PATH,
    ROOT,
    load_controls,
    load_yaml,
    summarize,
    validate,
)

OSCAL_VERSION = "1.1.2"
NS = "https://uagt.dev/ns/oscal"
OUT_DIR = ROOT / "build" / "oscal"

_UUID_NS = uuid.uuid5(uuid.NAMESPACE_URL, "https://uagt.dev/oscal")


def det_uuid(key: str) -> str:
    return str(uuid.uuid5(_UUID_NS, key))


def release_version() -> str:
    """Single-source the catalog version from CITATION.cff."""
    try:
        cff = yaml.safe_load((ROOT / "CITATION.cff").read_text(encoding="utf-8"))
        return str(cff.get("version", "0.0.0"))
    except Exception:
        return "0.0.0"


def framework_resource_uuid(fw: str) -> str:
    return det_uuid(f"resource:{fw}")


def build_control(ctrl: dict) -> dict:
    cid = ctrl["id"].lower()
    props = [
        {"name": "label", "value": ctrl["id"]},
        {"name": "principle", "ns": NS, "value": ctrl["principle"]},
    ]
    links = []
    map_lines = []
    for m in ctrl.get("mappings", []):
        fw = m["framework"]
        ref = m.get("ref")
        props.append({"name": "mapping-relationship", "ns": NS, "class": fw, "value": m["relationship"]})
        props.append({"name": "mapping-confidence", "ns": NS, "class": fw, "value": m["confidence"]})
        if ref:
            props.append({"name": "mapped-reference", "ns": NS, "class": fw, "value": ref})
            links.append({
                "href": f"#{framework_resource_uuid(fw)}",
                "rel": "reference",
                "text": f"{FRAMEWORK_LABELS[fw]} {ref} — {m['relationship']} ({m['confidence']})",
            })
            map_lines.append(f"- {FRAMEWORK_LABELS[fw]} {ref}: {m['relationship']} ({m['confidence']}) — {' '.join(m.get('rationale','').split())}")
        else:
            map_lines.append(f"- {FRAMEWORK_LABELS[fw]}: none (gap) — {' '.join(m.get('rationale','').split())}")

    parts = [
        {"id": f"{cid}_smt", "name": "statement", "prose": " ".join(ctrl["objective"].split())},
        {"id": f"{cid}_evidence", "name": "guidance",
         "prose": "Evidence artefacts: " + "; ".join(ctrl.get("evidence", []))},
        {"id": f"{cid}_crosswalk", "name": "guidance",
         "prose": "Crosswalk to source frameworks:\n" + "\n".join(map_lines)},
    ]
    return {"id": cid, "title": ctrl["title"], "props": props, "links": links, "parts": parts}


def build_catalog(controls: list[dict], manifest: dict) -> dict:
    by_domain: dict[str, list[dict]] = {}
    for ctrl in controls:
        by_domain.setdefault(ctrl["domain"], []).append(ctrl)

    groups = []
    for domain in sorted(by_domain, key=lambda d: DOMAIN_LABELS.get(d, d)):
        groups.append({
            "id": domain,
            "title": DOMAIN_LABELS.get(domain, domain),
            "controls": [build_control(c) for c in sorted(by_domain[domain], key=lambda c: c["id"])],
        })

    resources = []
    for fw in manifest["frameworks"]:
        resources.append({
            "uuid": framework_resource_uuid(fw["id"]),
            "title": fw["name"],
            "props": [{"name": "version", "value": str(fw["version"])}],
            "rlinks": [{"href": fw["obtain_from"]}],
            "remarks": "Referenced by identifier only; source text is not reproduced.",
        })
    methodology = manifest.get("methodology", {})
    resources.append({
        "uuid": det_uuid("resource:methodology"),
        "title": " ".join(methodology.get("title", "UAGT methodology paper").split()),
        "remarks": f"Cited methodology by {methodology.get('author', 'Vinod Dhiman')} (UAGT).",
    })

    return {
        "catalog": {
            "uuid": det_uuid("catalog"),
            "metadata": {
                "title": "UAGT — Unified AI Governance Taxonomy: Master Control Set",
                "last-modified": f"{manifest['updated']}T00:00:00Z",
                "version": release_version(),
                "oscal-version": OSCAL_VERSION,
                "props": [{"name": "keywords", "value": "AI governance, ISO/IEC 42001, NIST AI RMF, EU AI Act, crosswalk"}],
            },
            "groups": groups,
            "back-matter": {"resources": resources},
        }
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Build the UAGT OSCAL catalog.")
    ap.add_argument("--check", action="store_true", help="validate data only; no output")
    ap.add_argument("--validate-schema", metavar="PATH", help="also validate output against an OSCAL JSON schema")
    args = ap.parse_args()

    manifest = load_yaml(MANIFEST_PATH)
    controls = load_controls()
    problems = validate(controls, manifest)
    if problems:
        print(f"VALIDATION FAILED — {len(problems)} problem(s):", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1
    print(f"validation OK — {summarize(controls)}")
    if args.check:
        return 0

    catalog = build_catalog(controls, manifest)

    if args.validate_schema:
        import jsonschema
        schema = json.loads(open(args.validate_schema, encoding="utf-8").read())

        # OSCAL schema patterns use ECMA \p{...} unicode escapes that Python's re cannot
        # compile; strip "pattern" so structural validation still runs.
        def strip_patterns(node):
            if isinstance(node, dict):
                node.pop("pattern", None)
                for v in node.values():
                    strip_patterns(v)
            elif isinstance(node, list):
                for v in node:
                    strip_patterns(v)
        strip_patterns(schema)

        jsonschema.Draft7Validator(schema).validate(catalog)
        print(f"OSCAL structural validation OK against {args.validate_schema} (regex patterns skipped)")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / "uagt-catalog.json"
    out.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    n_controls = sum(len(g["controls"]) for g in catalog["catalog"]["groups"])
    print(f"wrote build/oscal/uagt-catalog.json ({len(catalog['catalog']['groups'])} groups, {n_controls} controls)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
