# UAGT — Unified AI Governance Taxonomy

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20823079.svg)](https://doi.org/10.5281/zenodo.20823079)

An open, machine-readable, citable, and continuously versioned crosswalk anchored on
**ISO/IEC 42001:2023**, the **NIST AI Risk Management Framework 1.0**, and the
**EU AI Act (Regulation (EU) 2024/1689, as amended)**, with optional cross-mappings to
**ISO/IEC 27001**, **SOC 2 (Trust Services Criteria)**, **COBIT 2019**, and
**ISO/IEC 27701** — seven frameworks in all.

Organizations adopting AI rarely get to pick a single governance regime — they are
pulled toward all three at once. UAGT publishes the reconciliation between them as a
single normalized control set, so practitioners stop re-deriving the same mapping and
the field gets a shared, maintained reference point.

> **Status:** v1.0.0 — first public release. A reviewed three-way crosswalk implementing
> the UAGT taxonomy across 8 governance domains. Not compliance certification, not legal
> advice, and not a substitute for the source standards; references identifiers only.

## What makes this different

Existing comparisons are point-in-time blog tables or gated commercial tools. UAGT is,
all at once: **openly licensed**, **anchored on a transparent normalized control layer**,
**schema-validated and machine-readable**, **citable via DOI**, **version-controlled
against a pinned source manifest**, and **neutrally governed** for community contribution.

## Methodology

This repository is the open, machine-readable implementation of the **Unified AI
Governance Taxonomy (UAGT)** set out in the paper *Bridging AI Risk Frameworks: Reconciling
ISO/IEC 42001, the NIST AI Risk Management Framework, and the EU AI Act into a Unified
Governance Taxonomy* (Vinod Dhiman). The taxonomy's **5 analytical layers** and
**8 regulation-stable governance domains (D1–D8)**, bound by a **traceability spine**, are
the structure this repository encodes. See
[`docs/methodology.md`](docs/methodology.md).

## How it works

The spine is the **Master Control Set (MCS)** — a normalized catalog of governance
controls organised into the eight UAGT domains, each expressed once and mapped *outward* to
the source frameworks. Every control carries the traceability spine: an upward `principle`,
sideways framework `mappings`, and forward `evidence` artefacts.

The three anchor frameworks (ISO/IEC 42001, NIST AI RMF, EU AI Act) are **required** on
every control (FR1). Four further frameworks attach *optionally* to the Master Control Set
without disturbing the anchor mappings, each across all 28 controls:

- **ISO/IEC 27001:2022**, **SOC 2 (Trust Services Criteria)**, and **COBIT 2019** — strong on
  governance, lifecycle, security, monitoring, and vendor management; `none` on AI-specific
  concerns (bias, transparency, human oversight, GPAI). All three independently fill the
  security gap where ISO/IEC 42001 defers out (`MC-D6-03`: 42001 `none` → `superset` in each).
- **ISO/IEC 27701** — privacy-only; `superset` on the privacy control and `none` almost
  everywhere else.

Their coverage shape (see [`docs/coverage.md`](docs/coverage.md): anchors 61–68% strong vs.
the others 4–32%) is itself the analytical point — a security/governance/privacy framework
is not an AI-governance framework. The same mechanism extends to further frameworks.

Each mapping records the **nature** of correspondence — `full` / `partial` / `superset`
/ `subset` / `none` — plus a rationale, confidence, and reviewer. The `none` flags are
deliberate: they are how genuine **gaps** surface (e.g. an EU AI Act obligation with no
clean ISO/NIST equivalent — see [`docs/gaps.md`](docs/gaps.md)). The
[`docs/coverage.md`](docs/coverage.md) report answers the recurring question directly — *how
much does each framework cover, and where are the gaps?* — with per-framework and per-domain
coverage and a hard-gap list. Per the methodology, unification is *structural, not legal*,
and the three risk verdicts are preserved, not averaged.

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

# Build the OSCAL 1.1.2 catalog (build/oscal/uagt-catalog.json) for GRC tooling:
python scripts/build_oscal.py
```

## Repository layout

```
data/controls/         one YAML per Master Control (canonical source)
data/source-manifest.yaml  pinned versions of each framework
schema/control.schema.json JSON Schema for validation
scripts/build_tables.py    YAML -> Markdown / CSV / XLSX / JSON
scripts/build_site.py      YAML -> searchable static site (site/index.html)
scripts/build_oscal.py     YAML -> OSCAL 1.1.2 catalog (build/oscal/uagt-catalog.json)
scripts/collect_metrics.py organic adoption metrics -> /evidence/ (run on a schedule)
tests/                 pytest contract tests (validation, reproducibility, OSCAL)
docs/                  rendered crosswalk + methodology (committed)
site/                  built static site (regenerated; not committed)
evidence/              timestamped metric snapshots + dashboard (committed)
```

## Licensing

- **Data + docs:** [CC BY 4.0](LICENSE-DATA) — attribution is a license condition.
- **Tooling (scripts):** [Apache-2.0](LICENSE).
- **Source standards are never reproduced.** UAGT references clause/article identifiers
  and short labels only; the standards themselves remain the copyright of ISO, NIST, and
  the EU and must be obtained from their issuers.

## Contributing

Corrections and additions are welcome via pull request — see
[CONTRIBUTING.md](CONTRIBUTING.md). Every mapping change needs a rationale and a reviewer,
and CI must pass (schema valid, references resolve, build clean) before merge.

## Citing

Cite via the **concept DOI [10.5281/zenodo.20823079](https://doi.org/10.5281/zenodo.20823079)**,
which always resolves to the latest version (v1.0.0 is
[10.5281/zenodo.20823080](https://doi.org/10.5281/zenodo.20823080)). Machine-readable
metadata is in [CITATION.cff](CITATION.cff). The crosswalk implements the UAGT taxonomy
from the methodology paper — see [docs/methodology.md](docs/methodology.md) — making the
paper and repo a reciprocal, traceable pair.
