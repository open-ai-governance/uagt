# UAGC — Unified AI Governance Crosswalk

An open, machine-readable, citable, and continuously versioned crosswalk across
**ISO/IEC 42001:2023**, the **NIST AI Risk Management Framework 1.0**, and the
**EU AI Act (Regulation (EU) 2024/1689, as amended)**.

Organizations adopting AI rarely get to pick a single governance regime — they are
pulled toward all three at once. UAGC publishes the reconciliation between them as a
single normalized control set, so practitioners stop re-deriving the same mapping and
the field gets a shared, maintained reference point.

> **Status:** v0.1 scaffolding. Sample data only — not yet a complete or authoritative
> crosswalk. Not compliance certification, not legal advice, not a substitute for the
> source standards.

## What makes this different

Existing comparisons are point-in-time blog tables or gated commercial tools. UAGC is,
all at once: **openly licensed**, **anchored on a transparent normalized control layer**,
**schema-validated and machine-readable**, **citable via DOI**, **version-controlled
against a pinned source manifest**, and **neutrally governed** for community contribution.

## Methodology

UAGC is the open implementation of the **Unified AI Governance Taxonomy (UAGT)** from the
paper *Bridging AI Risk Frameworks: Reconciling ISO/IEC 42001, the NIST AI Risk Management
Framework, and the EU AI Act into a Unified Governance Taxonomy* (Vinod Kumar). The
taxonomy's **5 analytical layers** and **8 regulation-stable governance domains (D1–D8)**,
bound by a **traceability spine**, are the structure this repository encodes. See
[`docs/methodology.md`](docs/methodology.md).

## How it works

The spine is the **Master Control Set (MCS)** — a normalized catalog of governance
controls organised into the eight UAGT domains, each expressed once and mapped *outward* to
the three source frameworks. Every control carries the traceability spine: an upward
`principle`, sideways framework `mappings`, and forward `evidence` artefacts. New frameworks
(ISO 27001, SOC 2, …) can attach later without disturbing existing mappings.

Each mapping records the **nature** of correspondence — `full` / `partial` / `superset`
/ `subset` / `none` — plus a rationale, confidence, and reviewer. The `none` flags are
deliberate: they are how genuine **gaps** surface (e.g. an EU AI Act obligation with no
clean ISO/NIST equivalent — see [`docs/gaps.md`](docs/gaps.md)). Per the methodology,
unification is *structural, not legal*, and the three risk verdicts are preserved, not
averaged.

```
data/controls/*.yaml   ──►  scripts/build_tables.py  ──►  docs/  (Markdown crosswalk + gaps)
data/source-manifest.yaml                                  build/ (JSON, CSV, XLSX)
schema/control.schema.json  (validation gate)
```

Everything derives from the canonical YAML — there are no hand-edited downstream tables
(NFR1). The build is the single source of truth.

## Quick start

```bash
pip install -r requirements.txt

# Validate the canonical data (this is the CI gate):
python scripts/build_tables.py --check

# Build tables/exports (docs/ + build/):
python scripts/build_tables.py

# Build the searchable static site (site/index.html — open it in any browser):
python scripts/build_site.py
```

## Repository layout

```
data/controls/         one YAML per Master Control (canonical source)
data/source-manifest.yaml  pinned versions of each framework
schema/control.schema.json JSON Schema for validation
scripts/build_tables.py    YAML -> Markdown / CSV / XLSX / JSON
scripts/build_site.py      YAML -> searchable static site (site/index.html)
scripts/collect_metrics.py organic adoption metrics -> /evidence/ (run on a schedule)
docs/                  rendered crosswalk + methodology (committed)
site/                  built static site (regenerated; not committed)
evidence/              timestamped metric snapshots + dashboard (committed)
```

## Licensing

- **Data + docs:** [CC BY 4.0](LICENSE-DATA) — attribution is a license condition.
- **Tooling (scripts):** [Apache-2.0](LICENSE).
- **Source standards are never reproduced.** UAGC references clause/article identifiers
  and short labels only; the standards themselves remain the copyright of ISO, NIST, and
  the EU and must be obtained from their issuers.

## Contributing

Corrections and additions are welcome via pull request — see
[CONTRIBUTING.md](CONTRIBUTING.md). Every mapping change needs a rationale and a reviewer,
and CI must pass (schema valid, references resolve, build clean) before merge.

## Citing

See [CITATION.cff](CITATION.cff). Each release will carry a persistent DOI (via Zenodo),
plus a concept DOI for the project as a whole.
