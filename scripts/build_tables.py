#!/usr/bin/env python3
"""Build all UAGT outputs from the canonical YAML source.

Single source of truth (NFR1): every output here derives from data/controls/*.yaml
and data/source-manifest.yaml. Nothing downstream is hand-edited.

Usage:
    python scripts/build_tables.py            # validate + build all outputs
    python scripts/build_tables.py --check    # validate only (CI gate), no writes

Outputs:
    docs/crosswalk.md          full crosswalk table, grouped by domain
    docs/gaps.md               gap-only view (relationship = none / partial)
    docs/coverage.md           coverage report (per-framework, per-domain, hard gaps)
    build/crosswalk.json       whole crosswalk as one machine-readable file
    build/crosswalk.csv        flat export for spreadsheets / auditors
    build/crosswalk.xlsx       same, if openpyxl is installed (optional)
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
CONTROLS_DIR = ROOT / "data" / "controls"
MANIFEST_PATH = ROOT / "data" / "source-manifest.yaml"
SCHEMA_PATH = ROOT / "schema" / "control.schema.json"
DOCS_DIR = ROOT / "docs"
BUILD_DIR = ROOT / "build"

# The three anchor frameworks every Master Control must cover (FR1). Additional frameworks
# (e.g. ISO/IEC 27001) attach optionally to the Master Control Set where an equivalent exists.
REQUIRED_FRAMEWORKS = ["ISO-IEC-42001", "NIST-AI-RMF", "EU-AI-ACT"]
# Display order for frameworks (columns): anchors first, then optional frameworks.
FRAMEWORK_ORDER = REQUIRED_FRAMEWORKS + ["ISO-IEC-27001", "SOC-2"]
FRAMEWORK_LABELS = {
    "ISO-IEC-42001": "ISO/IEC 42001",
    "NIST-AI-RMF": "NIST AI RMF",
    "EU-AI-ACT": "EU AI Act",
    "ISO-IEC-27001": "ISO/IEC 27001",
    "SOC-2": "SOC 2 (TSC)",
}
RELATIONSHIP_ORDER = ["full", "superset", "subset", "partial", "none"]
# The eight UAGT regulation-stable governance domains (paper, Table 4). D-prefixed labels
# sort naturally D1..D8.
DOMAIN_LABELS = {
    "d1-accountability-governance": "D1 — Accountability & organisational governance",
    "d2-risk-impact-assessment": "D2 — Risk & impact assessment",
    "d3-data-governance-quality": "D3 — Data governance & quality",
    "d4-transparency-documentation": "D4 — Transparency, documentation & records",
    "d5-human-oversight": "D5 — Human oversight & autonomy",
    "d6-robustness-accuracy-security": "D6 — Robustness, accuracy & security",
    "d7-lifecycle-monitoring": "D7 — Lifecycle monitoring & post-market surveillance",
    "d8-value-chain-gpai": "D8 — Value-chain, third-party & GPAI governance",
}


class BuildError(Exception):
    """Raised when validation fails. Message is the aggregated problem list."""


def load_yaml(path: Path):
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_controls() -> list[dict]:
    controls = []
    for path in sorted(CONTROLS_DIR.glob("*.yaml")):
        data = load_yaml(path)
        data["_path"] = str(path.relative_to(ROOT))
        controls.append(data)
    return controls


def validate(controls: list[dict], manifest: dict) -> list[str]:
    """Return a list of human-readable problems. Empty list == valid."""
    problems: list[str] = []

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    # Allowed (framework, version) pairs from the pinned manifest.
    allowed_versions = {fw["id"]: fw["version"] for fw in manifest["frameworks"]}

    seen_ids: dict[str, str] = {}
    for ctrl in controls:
        where = ctrl.get("_path", "<unknown>")

        # 1) Schema validation.
        payload = {k: v for k, v in ctrl.items() if not k.startswith("_")}
        for err in sorted(validator.iter_errors(payload), key=lambda e: e.path):
            loc = "/".join(str(p) for p in err.path) or "(root)"
            problems.append(f"{where}: schema: {loc}: {err.message}")

        cid = ctrl.get("id", "?")

        # 2) Filename matches id.
        expected = f"{cid}.yaml"
        if not where.endswith(expected):
            problems.append(f"{where}: filename should be {expected} to match id '{cid}'")

        # 3) Duplicate ids.
        if cid in seen_ids:
            problems.append(f"{where}: duplicate id '{cid}' (also in {seen_ids[cid]})")
        else:
            seen_ids[cid] = where

        # 4) Cross-reference: each mapping's framework+version is pinned in the manifest.
        frameworks_present = set()
        for m in ctrl.get("mappings", []):
            fw = m.get("framework")
            frameworks_present.add(fw)
            if fw in allowed_versions and m.get("version") != allowed_versions[fw]:
                problems.append(
                    f"{where}: {fw} version '{m.get('version')}' "
                    f"!= pinned '{allowed_versions[fw]}' in source-manifest.yaml"
                )

        # 5) FR1: every control covers the three ANCHOR frameworks (none is allowed, absent
        #    is not). Optional frameworks (e.g. ISO/IEC 27001) are not required everywhere.
        missing = [fw for fw in REQUIRED_FRAMEWORKS if fw not in frameworks_present]
        if missing:
            problems.append(
                f"{where}: FR1 three-way coverage missing for: {', '.join(missing)} "
                "(use relationship: none if there is no equivalent)"
            )

    return problems


def _mapping_by_framework(ctrl: dict) -> dict[str, dict]:
    # If a control maps to a framework more than once, keep them all but index the first
    # for the summary column; the full list is preserved in JSON/CSV.
    out: dict[str, list[dict]] = {}
    for m in ctrl.get("mappings", []):
        out.setdefault(m["framework"], []).append(m)
    return out


def _cell(mappings: list[dict] | None) -> str:
    if not mappings:
        return "—"
    parts = []
    for m in mappings:
        ref = m.get("ref") or "—"
        rel = m.get("relationship")
        parts.append(f"`{ref}` ({rel})")
    return "<br>".join(parts)


# ---------------------------------------------------------------------------
# Renderers
# ---------------------------------------------------------------------------

def render_crosswalk_md(controls: list[dict], manifest: dict) -> str:
    lines = ["# UAGT Crosswalk", ""]
    lines.append(
        "> Generated by `scripts/build_tables.py` — do not edit by hand. "
        "Source of truth is `data/controls/*.yaml`."
    )
    lines.append("")
    lines.append(
        f"Source baseline (manifest `{manifest['manifest_version']}`, "
        f"updated {manifest['updated']}): "
        + ", ".join(f"{FRAMEWORK_LABELS[fw['id']]} {fw['version']}" for fw in manifest["frameworks"])
        + "."
    )
    lines.append("")

    by_domain: dict[str, list[dict]] = {}
    for ctrl in controls:
        by_domain.setdefault(ctrl["domain"], []).append(ctrl)

    header = "| Master Control | " + " | ".join(FRAMEWORK_LABELS[f] for f in FRAMEWORK_ORDER) + " |"
    divider = "| --- | " + " | ".join(["---"] * len(FRAMEWORK_ORDER)) + " |"

    for domain in sorted(by_domain, key=lambda d: DOMAIN_LABELS.get(d, d)):
        lines.append(f"## {DOMAIN_LABELS.get(domain, domain)}")
        lines.append("")
        lines.append(header)
        lines.append(divider)
        for ctrl in sorted(by_domain[domain], key=lambda c: c["id"]):
            idx = _mapping_by_framework(ctrl)
            cells = [_cell(idx.get(f)) for f in FRAMEWORK_ORDER]
            name = f"**{ctrl['id']}** {ctrl['title']}"
            lines.append(f"| {name} | " + " | ".join(cells) + " |")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(
        "Relationship legend: **full** · **superset** · **subset** · **partial** · **none** (gap). "
        "See [gaps.md](gaps.md) for the gap-only view and [coverage.md](coverage.md) for the "
        "per-framework / per-domain coverage report."
    )
    lines.append("")
    return "\n".join(lines)


def render_gaps_md(controls: list[dict]) -> str:
    lines = ["# UAGT Gap View", ""]
    lines.append(
        "> Mappings where coverage is incomplete (`partial`) or absent (`none`). "
        "These are the analytically valuable outputs (FR3)."
    )
    lines.append("")
    lines.append("| Master Control | Framework | Ref | Relationship | Confidence | Rationale |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    rows = []
    for ctrl in controls:
        for m in ctrl.get("mappings", []):
            if m["relationship"] in ("partial", "none"):
                rows.append((ctrl, m))
    # none first (hard gaps), then partial; then by control id.
    rows.sort(key=lambda r: (0 if r[1]["relationship"] == "none" else 1, r[0]["id"]))
    for ctrl, m in rows:
        ref = m.get("ref") or "—"
        rationale = " ".join((m.get("rationale") or "").split())
        lines.append(
            f"| **{ctrl['id']}** {ctrl['title']} | {FRAMEWORK_LABELS[m['framework']]} "
            f"| `{ref}` | {m['relationship']} | {m['confidence']} | {rationale} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_coverage_md(controls: list[dict], manifest: dict) -> str:
    """Coverage analysis: the 'how much do I cover, and where are the gaps?' view."""
    from collections import Counter

    n = len(controls)
    fw_rel = {fw: Counter() for fw in FRAMEWORK_ORDER}
    fw_present = {fw: 0 for fw in FRAMEWORK_ORDER}
    for c in controls:
        seen = set()
        for m in c["mappings"]:
            if m["framework"] in fw_rel:
                fw_rel[m["framework"]][m["relationship"]] += 1
                seen.add(m["framework"])
        for fw in seen:
            fw_present[fw] += 1

    out = ["# UAGT Coverage Report", ""]
    out.append("> Generated by `scripts/build_tables.py` — do not edit by hand.")
    out.append("")
    out.append(
        f"How each framework covers the {n} Master Controls. **Strong** = `full` + `superset`; "
        "**gap** = `none`; **not mapped** = no entry for that framework (optional frameworks only)."
    )
    out.append("")
    out.append("## Coverage by framework")
    out.append("")
    out.append("| Framework | full | superset | partial | subset | none | not mapped | strong % |")
    out.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for fw in FRAMEWORK_ORDER:
        c = fw_rel[fw]
        not_mapped = n - fw_present[fw]
        strong = c["full"] + c["superset"]
        anchor = " *(anchor)*" if fw in REQUIRED_FRAMEWORKS else ""
        out.append(
            f"| {FRAMEWORK_LABELS[fw]}{anchor} | {c['full']} | {c['superset']} | {c['partial']} "
            f"| {c['subset']} | {c['none']} | {not_mapped} | {round(100 * strong / n)}% |"
        )
    out.append("")

    by_domain: dict[str, list[dict]] = {}
    for c in controls:
        by_domain.setdefault(c["domain"], []).append(c)
    out.append("## Coverage by domain × framework")
    out.append("")
    out.append("Each cell: **strong-coverage controls / total controls** in that domain (strong = full or superset).")
    out.append("")
    out.append("| Domain | " + " | ".join(FRAMEWORK_LABELS[fw] for fw in FRAMEWORK_ORDER) + " |")
    out.append("| --- | " + " | ".join(["---"] * len(FRAMEWORK_ORDER)) + " |")
    for domain in sorted(by_domain, key=lambda d: DOMAIN_LABELS.get(d, d)):
        dcs = by_domain[domain]
        cells = []
        for fw in FRAMEWORK_ORDER:
            strong = sum(
                1 for c in dcs
                if any(m["framework"] == fw and m["relationship"] in ("full", "superset")
                       for m in c["mappings"])
            )
            cells.append(f"{strong}/{len(dcs)}")
        out.append(f"| {DOMAIN_LABELS.get(domain, domain)} | " + " | ".join(cells) + " |")
    out.append("")

    hard = sorted(
        ((c, m) for c in controls for m in c["mappings"]
         if m["framework"] in REQUIRED_FRAMEWORKS and m["relationship"] == "none"),
        key=lambda x: x[0]["id"],
    )
    out.append("## Hard gaps (an anchor framework has no equivalent)")
    out.append("")
    if hard:
        for c, m in hard:
            out.append(f"- **{c['id']}** {c['title']} — no equivalent in {FRAMEWORK_LABELS[m['framework']]}")
    else:
        out.append("None — every control has at least a partial mapping in all three anchor frameworks.")
    out.append("")
    return "\n".join(out)


def build_json(controls: list[dict], manifest: dict) -> dict:
    return {
        "manifest_version": manifest["manifest_version"],
        "updated": manifest["updated"],
        "frameworks": manifest["frameworks"],
        "controls": [
            {k: v for k, v in ctrl.items() if not k.startswith("_")}
            for ctrl in sorted(controls, key=lambda c: c["id"])
        ],
    }


def build_rows(controls: list[dict]) -> list[dict]:
    rows = []
    for ctrl in sorted(controls, key=lambda c: c["id"]):
        for m in ctrl.get("mappings", []):
            rows.append(
                {
                    "control_id": ctrl["id"],
                    "control_title": ctrl["title"],
                    "domain": ctrl["domain"],
                    "principle": ctrl.get("principle", ""),
                    "evidence": "; ".join(ctrl.get("evidence", [])),
                    "framework": m["framework"],
                    "version": m["version"],
                    "ref": m.get("ref") or "",
                    "label": m.get("label") or "",
                    "relationship": m["relationship"],
                    "confidence": m["confidence"],
                    "rationale": " ".join((m.get("rationale") or "").split()),
                    "reviewer": m["reviewer"],
                }
            )
    return rows


def write_csv(rows: list[dict], path: Path) -> None:
    fields = list(rows[0].keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_xlsx(rows: list[dict], path: Path) -> bool:
    try:
        from openpyxl import Workbook
    except ImportError:
        return False
    wb = Workbook()
    ws = wb.active
    ws.title = "crosswalk"
    if rows:
        ws.append(list(rows[0].keys()))
        for r in rows:
            ws.append(list(r.values()))
    wb.save(path)
    return True


def summarize(controls: list[dict]) -> str:
    counts = {rel: 0 for rel in RELATIONSHIP_ORDER}
    total = 0
    for ctrl in controls:
        for m in ctrl.get("mappings", []):
            counts[m["relationship"]] = counts.get(m["relationship"], 0) + 1
            total += 1
    parts = [f"{counts[r]} {r}" for r in RELATIONSHIP_ORDER if counts.get(r)]
    return f"{len(controls)} controls, {total} mappings ({', '.join(parts)})"


def main() -> int:
    ap = argparse.ArgumentParser(description="Build UAGT outputs from canonical YAML.")
    ap.add_argument("--check", action="store_true", help="validate only; no outputs written")
    args = ap.parse_args()

    manifest = load_yaml(MANIFEST_PATH)
    controls = load_controls()

    if not controls:
        print("error: no controls found under data/controls/", file=sys.stderr)
        return 1

    problems = validate(controls, manifest)
    if problems:
        print(f"VALIDATION FAILED — {len(problems)} problem(s):", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1

    print(f"validation OK — {summarize(controls)}")

    if args.check:
        return 0

    DOCS_DIR.mkdir(exist_ok=True)
    BUILD_DIR.mkdir(exist_ok=True)

    (DOCS_DIR / "crosswalk.md").write_text(render_crosswalk_md(controls, manifest), encoding="utf-8")
    (DOCS_DIR / "gaps.md").write_text(render_gaps_md(controls), encoding="utf-8")
    (DOCS_DIR / "coverage.md").write_text(render_coverage_md(controls, manifest), encoding="utf-8")

    (BUILD_DIR / "crosswalk.json").write_text(
        json.dumps(build_json(controls, manifest), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    rows = build_rows(controls)
    write_csv(rows, BUILD_DIR / "crosswalk.csv")
    xlsx_ok = write_xlsx(rows, BUILD_DIR / "crosswalk.xlsx")

    print("wrote:")
    print("  docs/crosswalk.md")
    print("  docs/gaps.md")
    print("  docs/coverage.md")
    print("  build/crosswalk.json")
    print("  build/crosswalk.csv")
    print("  build/crosswalk.xlsx" if xlsx_ok else "  build/crosswalk.xlsx (skipped: openpyxl not installed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
