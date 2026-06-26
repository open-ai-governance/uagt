#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vinod Dhiman and UAGT contributors
"""Build the searchable static site from the canonical YAML source.

Single self-contained HTML file (data embedded, vanilla JS, no external CDN) so it
works offline, requires no login or build toolchain (NFR6), and is publishable as-is
to any static host. Reuses the data loading + validation from build_tables.py (NFR1).

Usage:
    python scripts/build_site.py            # validate + write site/index.html
    python scripts/build_site.py --check    # validate only, no writes
"""
from __future__ import annotations

import argparse
import json
import sys

from build_tables import (
    BUILD_DIR,  # noqa: F401  (kept for parity / future asset copy)
    DOMAIN_LABELS,
    FRAMEWORK_LABELS,
    FRAMEWORK_ORDER,
    MANIFEST_PATH,
    RELATIONSHIP_ORDER,
    ROOT,
    build_json,
    load_controls,
    load_yaml,
    summarize,
    validate,
)

SITE_DIR = ROOT / "site"

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UAGT — Unified AI Governance Taxonomy</title>
<style>
  :root {{
    --bg: #ffffff; --fg: #1a1d21; --muted: #5b6470; --line: #d7dce2;
    --accent: #1b5e9c; --chip: #eef2f7;
    --full: #1a7f44; --partial: #9a6a00; --none: #b3261e;
    --superset: #5b3fa6; --subset: #36707f;
  }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; font: 16px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
         color: var(--fg); background: var(--bg); }}
  header {{ padding: 1.5rem clamp(1rem, 4vw, 3rem); border-bottom: 1px solid var(--line); }}
  h1 {{ margin: 0 0 .25rem; font-size: 1.5rem; }}
  .sub {{ color: var(--muted); font-size: .95rem; }}
  main {{ padding: 1.25rem clamp(1rem, 4vw, 3rem) 4rem; }}
  .controls {{ display: flex; flex-wrap: wrap; gap: .75rem 1rem; align-items: end; margin-bottom: 1rem; }}
  .field {{ display: flex; flex-direction: column; gap: .25rem; }}
  .field label {{ font-size: .8rem; color: var(--muted); font-weight: 600; }}
  input[type=search], select {{ font: inherit; padding: .45rem .6rem; border: 1px solid var(--line);
         border-radius: 6px; background: #fff; min-width: 11rem; }}
  .checkfield {{ flex-direction: row; align-items: center; gap: .4rem; }}
  .checkfield label {{ color: var(--fg); font-weight: 500; }}
  input:focus-visible, select:focus-visible, button:focus-visible, th button:focus-visible {{
         outline: 3px solid var(--accent); outline-offset: 2px; }}
  .count {{ color: var(--muted); font-size: .9rem; margin: .25rem 0 1rem; }}
  table {{ border-collapse: collapse; width: 100%; font-size: .92rem; }}
  caption {{ text-align: left; color: var(--muted); font-size: .85rem; padding-bottom: .5rem; }}
  th, td {{ text-align: left; padding: .55rem .6rem; border-bottom: 1px solid var(--line); vertical-align: top; }}
  thead th {{ position: sticky; top: 0; background: var(--bg); border-bottom: 2px solid var(--line); white-space: nowrap; }}
  th button {{ font: inherit; font-weight: 700; background: none; border: 0; padding: 0; cursor: pointer; color: var(--fg); }}
  code {{ background: var(--chip); padding: .1rem .35rem; border-radius: 4px; font-size: .85em; }}
  .rel {{ font-weight: 700; text-transform: uppercase; font-size: .72rem; letter-spacing: .03em; }}
  .rel-full {{ color: var(--full); }} .rel-partial {{ color: var(--partial); }}
  .rel-none {{ color: var(--none); }} .rel-superset {{ color: var(--superset); }}
  .rel-subset {{ color: var(--subset); }}
  .rationale {{ color: var(--muted); max-width: 38rem; }}
  .empty {{ padding: 2rem 0; color: var(--muted); }}
  footer {{ padding: 1.5rem clamp(1rem, 4vw, 3rem); border-top: 1px solid var(--line); color: var(--muted); font-size: .85rem; }}
  a {{ color: var(--accent); }}
</style>
</head>
<body>
<header>
  <h1>UAGT — Unified AI Governance Taxonomy</h1>
  <p class="sub" id="baseline"></p>
</header>
<main>
  <div class="controls">
    <div class="field">
      <label for="q">Search</label>
      <input type="search" id="q" placeholder="control, ref, rationale…" autocomplete="off">
    </div>
    <div class="field">
      <label for="domain">Domain</label>
      <select id="domain"><option value="">All domains</option></select>
    </div>
    <div class="field">
      <label for="framework">Framework</label>
      <select id="framework"><option value="">All frameworks</option></select>
    </div>
    <div class="field">
      <label for="relationship">Relationship</label>
      <select id="relationship"><option value="">All relationships</option></select>
    </div>
    <div class="field checkfield">
      <input type="checkbox" id="gaponly">
      <label for="gaponly">Gaps only (partial / none)</label>
    </div>
  </div>
  <p class="count" id="count" aria-live="polite"></p>
  <table>
    <caption>One row per control–framework mapping. Click a column header to sort.</caption>
    <thead>
      <tr>
        <th scope="col"><button data-sort="control_id">Control</button></th>
        <th scope="col"><button data-sort="domain">Domain</button></th>
        <th scope="col"><button data-sort="framework">Framework</button></th>
        <th scope="col"><button data-sort="ref">Ref</button></th>
        <th scope="col"><button data-sort="relationship">Relationship</button></th>
        <th scope="col"><button data-sort="confidence">Conf.</button></th>
        <th scope="col">Rationale</th>
      </tr>
    </thead>
    <tbody id="rows"></tbody>
  </table>
  <p class="empty" id="empty" hidden>No mappings match the current filters.</p>
</main>
<footer>
  Generated from canonical YAML by <code>scripts/build_site.py</code> — do not edit by hand.
  Data &amp; docs licensed CC BY 4.0; references identifiers only, never source text.
  Mappings are not legal advice or certification.
</footer>

<script type="application/json" id="data">{data_json}</script>
<script>
  const DATA = JSON.parse(document.getElementById("data").textContent);
  const FW_LABELS = {fw_labels_json};
  const DOMAIN_LABELS = {domain_labels_json};
  const REL_ORDER = {rel_order_json};
  const REL_RANK = Object.fromEntries(REL_ORDER.map((r, i) => [r, i]));
  const CONF_RANK = {{ high: 0, medium: 1, low: 2 }};

  // Flatten controls -> one row per mapping.
  const ROWS = [];
  for (const c of DATA.controls) {{
    for (const m of c.mappings) {{
      ROWS.push({{
        control_id: c.id, control_title: c.title, domain: c.domain,
        framework: m.framework, ref: m.ref || "", label: m.label || "",
        relationship: m.relationship, confidence: m.confidence,
        rationale: (m.rationale || "").replace(/\\s+/g, " ").trim(),
      }});
    }}
  }}

  document.getElementById("baseline").textContent =
    `Baseline (manifest ${{DATA.manifest_version}}, updated ${{DATA.updated}}): ` +
    DATA.frameworks.map(f => `${{FW_LABELS[f.id] || f.id}} ${{f.version}}`).join(" · ");

  const sel = (id) => document.getElementById(id);
  function fillSelect(el, values, labelFn) {{
    for (const v of values) {{
      const o = document.createElement("option");
      o.value = v; o.textContent = labelFn(v); el.appendChild(o);
    }}
  }}
  fillSelect(sel("domain"), [...new Set(ROWS.map(r => r.domain))].sort(),
             v => DOMAIN_LABELS[v] || v);
  fillSelect(sel("framework"), DATA.frameworks.map(f => f.id), v => FW_LABELS[v] || v);
  fillSelect(sel("relationship"), REL_ORDER, v => v);

  let sortKey = "control_id", sortDir = 1;

  function esc(s) {{ const d = document.createElement("div"); d.textContent = s; return d.innerHTML; }}

  function render() {{
    const q = sel("q").value.trim().toLowerCase();
    const dom = sel("domain").value, fw = sel("framework").value, rel = sel("relationship").value;
    const gaps = sel("gaponly").checked;

    let rows = ROWS.filter(r => {{
      if (dom && r.domain !== dom) return false;
      if (fw && r.framework !== fw) return false;
      if (rel && r.relationship !== rel) return false;
      if (gaps && !(r.relationship === "partial" || r.relationship === "none")) return false;
      if (q) {{
        const hay = `${{r.control_id}} ${{r.control_title}} ${{r.ref}} ${{r.label}} ${{r.rationale}}`.toLowerCase();
        if (!hay.includes(q)) return false;
      }}
      return true;
    }});

    rows.sort((a, b) => {{
      let av, bv;
      if (sortKey === "relationship") {{ av = REL_RANK[a.relationship]; bv = REL_RANK[b.relationship]; }}
      else if (sortKey === "confidence") {{ av = CONF_RANK[a.confidence]; bv = CONF_RANK[b.confidence]; }}
      else {{ av = a[sortKey]; bv = b[sortKey]; }}
      if (av < bv) return -1 * sortDir;
      if (av > bv) return 1 * sortDir;
      return a.control_id < b.control_id ? -1 : 1;
    }});

    const tbody = sel("rows");
    tbody.innerHTML = rows.map(r => `
      <tr>
        <td><strong>${{esc(r.control_id)}}</strong><br>${{esc(r.control_title)}}</td>
        <td>${{esc(DOMAIN_LABELS[r.domain] || r.domain)}}</td>
        <td>${{esc(FW_LABELS[r.framework] || r.framework)}}</td>
        <td>${{r.ref ? `<code>${{esc(r.ref)}}</code>` : "—"}}</td>
        <td><span class="rel rel-${{esc(r.relationship)}}">${{esc(r.relationship)}}</span></td>
        <td>${{esc(r.confidence)}}</td>
        <td class="rationale">${{esc(r.rationale)}}</td>
      </tr>`).join("");

    sel("empty").hidden = rows.length > 0;
    sel("count").textContent =
      `${{rows.length}} of ${{ROWS.length}} mappings` +
      (rows.length !== ROWS.length ? " (filtered)" : "");
  }}

  for (const id of ["q", "domain", "framework", "relationship", "gaponly"]) {{
    sel(id).addEventListener("input", render);
  }}
  document.querySelectorAll("th button[data-sort]").forEach(btn => {{
    btn.addEventListener("click", () => {{
      const k = btn.dataset.sort;
      sortDir = (sortKey === k) ? -sortDir : 1;
      sortKey = k;
      render();
    }});
  }});

  render();
</script>
</body>
</html>
"""


def render_site(controls, manifest) -> str:
    data = build_json(controls, manifest)
    return PAGE.format(
        data_json=json.dumps(data, ensure_ascii=False),
        fw_labels_json=json.dumps(FRAMEWORK_LABELS),
        domain_labels_json=json.dumps(DOMAIN_LABELS),
        rel_order_json=json.dumps(RELATIONSHIP_ORDER),
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="Build the UAGT searchable static site.")
    ap.add_argument("--check", action="store_true", help="validate only; no output written")
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

    SITE_DIR.mkdir(exist_ok=True)
    out = SITE_DIR / "index.html"
    out.write_text(render_site(controls, manifest), encoding="utf-8")
    print(f"wrote site/index.html ({out.stat().st_size // 1024} KB, self-contained)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
