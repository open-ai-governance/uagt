# Mapping review log

A record of deliberate reviews of the relationship calls (the crosswalk's most
analytically valuable and most drift-prone output). Each mapping also carries a per-mapping
`confidence` (`high`/`medium`/`low`) in the canonical data — the in-band drift signal.

## 2026-06-26 — `partial` relationship audit

**Scope:** all 72 `partial` mappings, with priority on the 27 anchor-framework partials
(ISO/IEC 42001, NIST AI RMF, EU AI Act) — the analytically critical calls.

**Method:** (1) each of the 27 anchor partials individually re-assessed against the source
framework, asking whether it is actually `full` (reference substantially covers the control)
or `none` (no genuine equivalent); (2) a rationale-language scan across all 72 for phrases
implying a mis-type ("comprehensively/directly/fully" → `full`; "no equivalent/has no" →
`none`).

**Result:** no mis-types. All 72 partials confirmed correctly typed. The most `none`-leaning
cases are NIST AI RMF on data provenance (`MC-D3-01`) and on technical documentation
(`MC-D4-02`): both retain a weak-but-real overlap (NIST documents data/system characteristics
cross-cuttingly), so they stay `partial` with `confidence: low` rather than `none`. The most
`full`-leaning case is NIST on GPAI (`MC-D8-03`), where the Generative AI Profile is
substantial but does not cover systemic-risk obligations; it stays `partial`.

**Standing rule:** re-run this audit whenever mappings change or a source standard moves
(e.g. the Digital Omnibus — see [omnibus-tracking.md](omnibus-tracking.md)).
