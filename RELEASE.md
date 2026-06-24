# Release & go-live checklist

This is the runbook for taking UAGC public and cutting a citable release. Steps marked
**[you]** require human decisions or account access and cannot be automated here.

## One-time setup (before the first public release)

1. **[you] Decide the public home.** Create the neutral GitHub org (e.g.
   `open-ai-governance`) and transfer the repo into it (Settings → Transfer ownership).
   GitHub redirects old URLs and preserves history, issues, and stars. Update
   `repository-code`/`url` in `CITATION.cff` and `.zenodo.json` references afterward.
2. **[you] Make the repo public.** Required for Zenodo archiving, the dependency graph,
   the Traffic API value at scale, and the "no login wall" principle (NFR6).
3. **[you] Connect Zenodo.** Log in to <https://zenodo.org> with GitHub, then flip the
   repo switch ON in Zenodo → GitHub settings. Zenodo reads `.zenodo.json` and mints a
   DOI automatically the next time a GitHub Release is published. It also issues a
   **concept DOI** that always resolves to the latest version (FR8).
4. **[you] Add the metrics PAT (optional but recommended).** The Traffic API needs push
   access, which the default Actions token lacks. Create a fine-grained/classic PAT with
   `repo` scope and add it as the `METRICS_TOKEN` repository secret so
   `collect-metrics` captures traffic, not just stars/forks.
5. **[you] Enable GitHub Pages (optional).** To host `site/index.html`, either publish
   the `site/` output via a Pages workflow or point Pages at a built branch.

## Cutting a release (repeatable)

1. Ensure `main` is green: `python scripts/build_tables.py --check`.
2. Update `CHANGELOG.md` — move `[Unreleased]` items under the new version with the date.
3. Bump `version` in `CITATION.cff` (and it will flow into the Zenodo deposit).
4. Tag and push:
   ```bash
   git tag v1.0.0 -m "UAGC v1.0.0"
   git push origin v1.0.0
   ```
5. The `release` workflow validates, rebuilds all outputs, bundles `uagc-v1.0.0.zip`
   plus the JSON/CSV/XLSX exports, and publishes the GitHub Release.
6. If Zenodo is connected, the DOI is minted within a few minutes. **[you]** copy the
   release DOI and the concept DOI into `CITATION.cff` (and the README badge), then
   commit — this closes the reciprocal paper↔repo citation loop (FR8).

## Definition of done for v1.0 (design appendix C)

- [ ] Every Master Control mapped to all three frameworks (or explicitly flagged `none`)
- [ ] Schema-validated; all outputs build from one command
- [ ] Methodology reviewed against the paper (reviewers reflect real sign-off)
- [ ] Site live (Pages or other host)
- [ ] DOI minted; `CITATION.cff` updated
- [ ] Metrics pipeline running (first snapshot captured)
- [ ] Methodology preprint posted and cross-linked with the repo DOI
