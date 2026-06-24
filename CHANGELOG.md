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
- Draft Master Control Set: **23 controls across all 7 domains** (accountability,
  risk-management, data-governance, transparency, human-oversight, security, lifecycle),
  69 mappings total (45 full, 21 partial, 3 none). Framework identifiers verified against
  the published structure of ISO/IEC 42001 Annex A, NIST AI RMF 1.0 (72 subcategories),
  and the EU AI Act.
- Documented gaps (`relationship: none`): EU AI Act Art.50 synthetic-content disclosure
  and Art.15 cybersecurity have no clean ISO/IEC 42001 equivalent (ISO defers security to
  ISO/IEC 27001).

### Note
- Mappings authored in this draft carry `reviewer: "draft"`. They are grounded in the
  frameworks' published structure but are **pending human review** against the methodology
  paper before being signed off (`reviewer: "vinod"`) for a v1.0 release.

### Tracking
- **EU AI Act — Digital Omnibus on AI:** provisional political agreement reached
  7 May 2026; formal adoption expected ~June–July 2026. The source manifest currently
  reflects Regulation (EU) 2024/1689 as enacted. Official Journal publication of the
  Omnibus will trigger a MAJOR version bump and re-review of affected mappings.
