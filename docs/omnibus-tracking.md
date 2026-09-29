# EU AI Act — Digital Omnibus tracking (applied in v3.0.0)

The **Digital Omnibus on AI** amends Regulation (EU) 2024/1689. It was pre-staged here in
v2.3.0 and is **applied as of v3.0.0**: the crosswalk now reflects 2024/1689 **as amended by
Regulation (EU) 2026/1744**. Details are in
[`data/source-manifest.yaml`](../data/source-manifest.yaml).

## Status

- **Regulation (EU) 2026/1744** of the European Parliament and of the Council of **8 July 2026**,
  published in the Official Journal and **in force 27 July 2026**
  (ELI: <http://data.europa.eu/eli/reg/2026/1744/oj>). It amends Regulations (EU) 2024/1689,
  2018/1139 and 2023/1230.
- History: proposal 19 Nov 2025 → provisional agreement 7 May 2026 → signed 8 Jul 2026.
- Verified on 2026-09-28 against the official text from the EU Publications Office
  (CELEX `32026R1744`), not against secondary summaries.

## Application dates (Art.113, third paragraph, as amended)

| Provision | Applies from |
| --- | --- |
| Penalties, Arts. 102–110 | 27 Jul 2026 |
| Art.50 transparency; GPAI obligations and enforcement | 2 Aug 2026 (unchanged) |
| New Art.5(1)(ba)–(bb) prohibitions + Art.5(1a), (1b) | **2 Dec 2026** |
| Art.50(2) marking, for systems placed on the market before 2 Aug 2026 (Art.111(4)) | **2 Dec 2026** |
| High-risk, Chapter III s.1–3: Art.6(2) / Annex III | **2 Dec 2027** |
| High-risk, Chapter III s.1–3: Art.6(1) / Annex I | **2 Aug 2028** |
| High-risk systems used by public authorities (legacy, Art.111(2)) | 2 Aug 2030 |

UAGT maps **obligations, not dates**, so the dates are recorded in the manifest and changelog.
They do not change relationships.

## Mapping changes applied

| Omnibus change | UAGT effect |
| --- | --- |
| **Art.4 replaced.** The duty is now to *take measures to support* staff AI literacy, and explicitly "does not require … to guarantee any specific level". | `MC-D1-04` Art.4: **full → partial** |
| **Art.4a inserted.** Legal basis for processing special-category data for bias detection and correction: providers of high-risk systems (4a(1)), and other AI systems, models and high-risk deployers (4a(2)), under strict safeguards. | `MC-D3-04` retargeted Art.10 → **Art.4a** (partial). Art.4a **added** to `MC-D3-03` (partial). |
| **Art.10(5) deleted**; its content moved into Art.4a. | `MC-D3-04` no longer cites Art.10 |
| **Art.5(1)(ba)–(bb) inserted.** AI-generated non-consensual intimate material and CSAM are prohibited. Art.5(1a)(a)(ii) requires reasonable, adequate safeguards where such output is a foreseeable, reproducible outcome. | **New** mapping on `MC-D6-05` Responsible design (partial). This is a design-safeguard duty, not the disclosure duty of `MC-D4-04`. |
| **Art.49 / Art.6(3) registration retained.** Only Annex VIII section B points 7 and 9 were deleted. | `MC-D1-03` unchanged |
| **Art.73 serious incidents.** For AI-Office-supervised systems, reports now go to the AI Office (Art.75(1a)). | `MC-D7-02` unchanged (same duty, different recipient) |
| **Art.50 marking:** four-month grace period for legacy generative systems | `MC-D4-04` unchanged (timing only) |

**Article renumbering:** none. The Omnibus inserts provisions (4a, 5(1)(ba)–(bb), 5(1a)–(1b))
and deletes 10(5), and every other `Art.*` reference in `data/controls/` still resolves to the
same obligation.

## Still to watch

- Final Commission **Art.6 high-risk classification guidelines**. A draft was published
  19 May 2026, and the final version was not yet published at the last check.
- OJ citation of **EN 18286:2026** (AI QMS, Art.17) as a harmonised standard. Until it is cited,
  it confers no presumption of conformity. It is recorded as a companion source in the manifest.
- Final Art.73 serious-incident guidance. The obligation effectively applies with the high-risk
  dates.
