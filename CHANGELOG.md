# Changelog

All notable changes to the UAGC crosswalk are recorded here. The changelog narrates
*why* a mapping moved — especially as source standards shift — which is the living-document
value static comparison tables cannot match.

The format is based on [Keep a Changelog](https://keepachangelog.com/), and the dataset
uses semantic versioning (see [GOVERNANCE.md](GOVERNANCE.md)): MAJOR for material source-
standard changes, MINOR for added controls/mappings, PATCH for corrections.

## [Unreleased]

### Added
- Initial repository scaffolding: JSON Schema, source manifest, build pipeline
  (`scripts/build_tables.py`), governance/contribution/license files, and CI.
- Master Control Set reconciled to the **UAGT taxonomy** from the methodology paper:
  re-architected into the paper's **8 regulation-stable governance domains (D1–D8)** with
  controls re-keyed `MC-D<n>-<NN>`. Now **28 controls, 84 mappings** (54 full, 27 partial,
  3 none), including the previously-missing **D8 value-chain / third-party / GPAI** domain.
  Framework identifiers verified against ISO/IEC 42001 Annex A, NIST AI RMF 1.0
  (72 subcategories), and the EU AI Act; D2 references ISO/IEC 42005 and D8 the NIST
  Generative AI Profile.
- **Traceability spine** added to the schema and every control: an upward `principle`
  (normative-purpose link) and forward `evidence` artefacts (assurance link), alongside the
  sideways framework `mappings` — implementing the paper's central design principle.
- `docs/methodology.md` documents the 5 analytical layers, 8 domains, the spine, and the
  "structural not legal / preserve all three risk verdicts" boundary conditions, and links
  the repo to the paper (reciprocal citation).
- Documented gaps (`relationship: none`): EU AI Act Art.50 synthetic-content disclosure
  and Art.15 cybersecurity have no clean ISO/IEC 42001 equivalent (ISO defers security to
  ISO/IEC 27001).
- Searchable static site (`scripts/build_site.py` → `site/index.html`): a single
  self-contained HTML file (no CDN, no login) with full-text search and filtering by
  domain, framework, relationship, and a gaps-only toggle. XLSX export enabled.
- Metrics pipeline (`scripts/collect_metrics.py` + `.github/workflows/metrics.yml`):
  captures organic, third-party-sourced, UTC-timestamped GitHub signals (stars, forks,
  watchers, 14-day traffic, release downloads) into append-only `evidence/` snapshots +
  `metrics.csv` + `dashboard.html`. Scheduled biweekly (1st & 15th) for the rolling
  traffic window. Zenodo/PyPI channels stubbed for launch. Verified live against the API.
- Release tooling: `.zenodo.json` (DOI metadata), `.github/workflows/release.yml`
  (tag → rebuild + bundle + GitHub Release, which triggers Zenodo DOI minting once
  connected), and `RELEASE.md` go-live checklist for the gated public-launch steps.

### Note
- All mappings are signed off with `reviewer: "Vinod Dhiman"`.

### Tracking
- **EU AI Act — Digital Omnibus on AI:** provisional political agreement reached
  7 May 2026; formal adoption expected ~June–July 2026. The source manifest currently
  reflects Regulation (EU) 2024/1689 as enacted. Official Journal publication of the
  Omnibus will trigger a MAJOR version bump and re-review of affected mappings.
