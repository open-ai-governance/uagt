# EU AI Act — Digital Omnibus tracking (pre-staged)

The **Digital Omnibus on AI** amends Regulation (EU) 2024/1689. This file pre-stages the
update so that when it lands in the Official Journal (expected **~June–July 2026**) the
MAJOR version bump and changelog entry fire cleanly. The crosswalk currently reflects
2024/1689 **as enacted**; the Omnibus is tracked here and in
[`data/source-manifest.yaml`](../data/source-manifest.yaml) until publication.

## Status

- Provisional political agreement: **7 May 2026**; endorsed by Member State representatives
  13 May 2026. **Not yet in the Official Journal** as of the current manifest date.

## What changes (substance is stable; timing and a few articles move)

| Change | Effect | Affected UAGT references |
| --- | --- | --- |
| High-risk obligations (Annex III) deferred | Apply from **2 Dec 2027** | Application date of Art.9–15, 16, 17, 26, 27, 43, 49, 72, 73 — obligations unchanged |
| High-risk (Annex I, product-embedded) deferred | Apply from **2 Aug 2028** | same obligation set; later date |
| National regulatory sandboxes | Pushed to **2 Aug 2027** | (no control maps to sandboxes) |
| New Art.5 prohibitions: AI-generated NCII and CSAM | From **2 Dec 2026** | Candidate **new** mapping for `MC-D4-04` (or a new control) |
| Art.50 transparency / watermarking grace periods adjusted | Timing change | `MC-D4-04` (Art.50) — update rationale wording, not the relationship |
| Live for **2 Aug 2026**: Art.50 transparency, GPAI penalty powers, market surveillance | unchanged | `MC-D4-04` (Art.50), `MC-D8-03` (Art.53/55) |

**Key point:** the obligations the crosswalk maps are *stable in kind*; the Omnibus mostly
shifts **application dates**. Because UAGT maps obligations (not dates), most mappings do not
change — the **changelog narrates the shift**, which is the living-document value. Watch for
two real content effects: (1) the new Art.5 NCII/CSAM prohibition (consider mapping it), and
(2) Art.50 watermarking wording.

**Article renumbering:** the Omnibus is an *amending* regulation (it amends/inserts, it does
not republish the Act), so wholesale renumbering is **not expected**. On publication, still
verify every `Art.*` ref in `data/controls/` still resolves to the same obligation.

## Release checklist (run when the Omnibus is published in the OJ)

1. **Source manifest** — update `EU-AI-ACT`: set `version` note to
   `"2024/1689 as amended by Regulation (EU) 2026/____ (Digital Omnibus)"`, and flip the
   `amendments` entry `status`/`tracked` to published with the OJ citation and date.
2. **Verify refs resolve** — confirm no article renumbering broke any `Art.*` reference
   (`python scripts/build_reverse_coverage.py` lists every EU article used).
3. **Content review** — add an Art.5 (NCII/CSAM) mapping to `MC-D4-04` if in scope; refresh
   the Art.50 rationale for the watermarking timing.
4. **MAJOR version bump** — per [GOVERNANCE.md](../GOVERNANCE.md) semver, a material
   source-standard change is MAJOR. Bump `CITATION.cff` and tag.
5. **Changelog** — promote the pre-drafted stub below.
6. **Re-archive** — ensure Zenodo (under the org owner) mints the new version DOI.

## Pre-drafted changelog stub

```
## [X.0.0] - 2026-__-__

### Changed
- **EU AI Act updated for the Digital Omnibus** (Regulation (EU) 2026/____, OJ __ ___ 2026).
  Source manifest now reflects 2024/1689 as amended. High-risk application dates shifted
  (Annex III → 2 Dec 2027, Annex I → 2 Aug 2028); Art.50 watermarking wording refreshed.
- New Art.5 prohibition (AI-generated NCII / CSAM, from 2 Dec 2026) reflected in MC-D4-04.
  Article references re-verified post-amendment (no renumbering of mapped articles).
```
