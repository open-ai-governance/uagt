# Contributing to UAGT

Thank you for helping improve the Unified AI Governance Taxonomy. Corrections,
additional mappings, and new Master Controls are all welcome.

## Ground rules

1. **Never paste source-standard text.** Reference clause / Annex control / Article
   identifiers and short labels only. The standards remain the copyright of ISO, NIST,
   and the EU. PRs that reproduce standard text will be declined.
2. **Every mapping needs a rationale and a reviewer.** A mapping without a defensible,
   reviewable justification is not mergeable.
3. **One file per Master Control**, named exactly `<id>.yaml` (e.g. `MC-D3-03.yaml`),
   under `data/controls/`.
4. **The build is the source of truth.** Never hand-edit anything in `docs/` or
   `build/` — regenerate with `python scripts/build_tables.py`.

## Data model (what a control looks like)

See [`schema/control.schema.json`](schema/control.schema.json) for the authoritative
rules and any existing file in `data/controls/` for a worked example. In short:

- `id` — `MC-D<N>-<NN>`, where `<N>` is the domain number 1–8 (e.g. `MC-D2-01`).
- `domain` — one of the eight UAGT domains: `d1-accountability-governance`,
  `d2-risk-impact-assessment`, `d3-data-governance-quality`,
  `d4-transparency-documentation`, `d5-human-oversight`,
  `d6-robustness-accuracy-security`, `d7-lifecycle-monitoring`, `d8-value-chain-gpai`.
- `objective` — what the control achieves, in our own words.
- `mappings` — **all three frameworks** (ISO-IEC-42001, NIST-AI-RMF, EU-AI-ACT) must
  appear (FR1). If there is genuinely no equivalent, set `relationship: none` with a
  rationale — do not omit the framework.
- Optional frameworks (`required: false` in the manifest, e.g. ISO-IEC-27001,
  KR-AI-BASIC-ACT) are added the same way. Adding a new one also means adding its id to
  the framework enum in the schema and to `FRAMEWORK_ORDER` in `scripts/build_tables.py`;
  propose it as an issue first (see [GOVERNANCE.md](GOVERNANCE.md)).

### Relationship types (FR3)

| Value      | Use when… |
| ---------- | --------- |
| `full`     | the reference substantially covers the Master Control |
| `superset` | the reference covers the control **and more** |
| `subset`   | the reference covers **part** of the control |
| `partial`  | meaningful but incomplete overlap |
| `none`     | no clean equivalent exists (a real gap — valuable, not a failure) |

When `relationship: none`, set `ref` and `label` to `null`.

`version` for each framework **must** match the pinned value in
[`data/source-manifest.yaml`](data/source-manifest.yaml). Changing a pinned version is a
maintainer decision tied to a changelog entry (see [GOVERNANCE.md](GOVERNANCE.md)).

## Workflow

```bash
pip install -r requirements-dev.txt
# make your change in data/controls/ or data/source-manifest.yaml
python -m pytest -q                       # contract tests must pass
python scripts/build_tables.py --check    # must pass — this is the CI gate
python scripts/build_tables.py            # regenerate docs/ outputs to include in the PR
```

Open a pull request (the template prompts for the rationale and reviewer). CI re-runs the
tests, `--check`, and a dry-run build of every output; merge is blocked until all are clean
and a maintainer has reviewed the rationale on each changed mapping.

Contributors are credited in releases and in the citation metadata.
