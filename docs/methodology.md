# UAGT methodology

**UAGT — the Unified AI Governance Taxonomy** — is set out in:

> Vinod Dhiman, *Bridging AI Risk Frameworks: Reconciling ISO/IEC 42001, the NIST AI Risk
> Management Framework, and the EU AI Act into a Unified Governance Taxonomy.*

The paper is the cited methodology; **this repository is its open, machine-readable
implementation** — the maintained, versioned crosswalk that operationalises the taxonomy,
realising the paper's own "future work" item of expressing the atomic-obligation crosswalk
in a machine-readable, version-controlled schema.

## Five analytical layers

The taxonomy is a comparative lens with five layers. Each is a dimension along which all
three instruments can be compared — a layer is *not* equated with a single framework.

| Layer | ISO/IEC 42001 | NIST AI RMF | EU AI Act |
| --- | --- | --- | --- |
| Normative purpose | Responsible AI management | Trustworthy AI characteristics | Health, safety, fundamental rights; internal market |
| Governance subject | The organisation's AIMS | The AI system in socio-technical context | AI systems by risk; provider/deployer roles |
| Risk logic | Org risk + AI impact assessment (PDCA) | Dynamic, contextual, socio-technical risk | Ex ante legal risk tiers tied to intended purpose |
| Control architecture | Annex A: 38 controls / 9 objectives | Govern–Map–Measure–Manage | Prohibitions; high-risk reqs (Arts 9–15); Art 50; conformity |
| Evidence & assurance | Certification, SoA, audit trail | Risk registers, metrics, evaluations | Technical docs, logs, conformity declarations, FRIA |

## Eight regulation-stable governance domains

Where layers describe the architecture, **domains are the operative content** — the
substantive control surface the instruments share. They are chosen to stay intact as
specific deadlines, annexes, and profiles change. Each Master Control belongs to exactly
one domain (encoded in its id, `MC-D<n>-<NN>`).

| Domain | Principal expression |
| --- | --- |
| **D1** Accountability & organisational governance | EU Art 17 / QMS · NIST Govern · ISO Clauses 4–5, Annex A governance |
| **D2** Risk & impact assessment | EU Art 9 · NIST Map & Measure · ISO Clause 6.1, ISO/IEC 42005 |
| **D3** Data governance & quality | EU Art 10 · NIST Map/Measure (data) · ISO Annex A data-for-AI |
| **D4** Transparency, documentation & records | EU Arts 11–13, 50 · NIST accountable-and-transparent · ISO documented info / SoA |
| **D5** Human oversight & autonomy | EU Art 14 · NIST human-AI configuration / Govern · ISO Annex A oversight |
| **D6** Robustness, accuracy & security | EU Art 15 · NIST safe / secure-and-resilient / valid-and-reliable · ISO Annex A lifecycle & security |
| **D7** Lifecycle monitoring & post-market surveillance | EU Arts 72–73 · NIST Manage · ISO Clauses 9–10 |
| **D8** Value-chain, third-party & GPAI governance | EU GPAI (Arts 53–55) & value chain (Art 25) · NIST Govern 6 / GenAI Profile · ISO Annex A third-party |

## The traceability spine

Every Master Control carries explicit links in both directions, so a domain's controls
connect upward to a principle and outward to evidence:

- **Upward (`principle`)** — the normative principle the control descends from
  (normative-purpose layer).
- **Sideways (`mappings`)** — typed back-links into each source framework
  (control-architecture layer), with relationship, rationale, confidence, and reviewer.
- **Forward (`evidence`)** — the assurance artefacts that demonstrate the control
  (evidence-&-assurance layer).

Read downward the spine gives design guidance; read upward it gives an audit trail.

## Design principles (and where unification stops)

1. **Layer separation** — a change in one layer (e.g. a deferred AI Act deadline) does not
   force a redesign of the others.
2. **Traceability** — every control is decomposed into traceable units, not a flat table.
3. **Risk-verdict preservation** — the three instruments constitute risk differently
   (ex ante legal tiers vs. contextual measured risk vs. organisational risk). A control
   crosswalk does **not** average these verdicts. A system can be legally high-risk under
   the EU AI Act even where a contextual NIST measurement returns modest residual risk;
   both verdicts must be recorded against the system, not collapsed.
4. **Regulation stability** — the eight domains hold steady while the control-architecture
   and evidence layers are re-mapped as standards move (tracked via the source manifest and
   changelog).

**Unification is structural, not legal.** This crosswalk helps reuse effort and evidence;
it does **not** convert ISO/IEC 42001 certification or NIST alignment into EU AI Act
conformity. Only the Article 40 harmonised standards, once adopted, confer that presumption.
The `none` and `partial` relationships in the data are where these non-equivalences surface.
