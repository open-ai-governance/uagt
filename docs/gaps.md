# UAGC Gap View

> Mappings where coverage is incomplete (`partial`) or absent (`none`). These are the analytically valuable outputs (FR3).

| Master Control | Framework | Ref | Relationship | Confidence | Rationale |
| --- | --- | --- | --- | --- | --- |
| **MC-D4-04** Disclosure of AI-generated and synthetic content | ISO/IEC 42001 | `—` | none | high | ISO/IEC 42001 contains no control specific to labelling AI-generated or synthetic content; no clean equivalent. |
| **MC-D4-04** Disclosure of AI-generated and synthetic content | NIST AI RMF | `—` | none | high | The NIST AI RMF does not prescribe synthetic-content disclosure or marking. |
| **MC-D6-03** Security, cybersecurity and resilience | ISO/IEC 42001 | `—` | none | high | ISO/IEC 42001 defers information-security controls to ISO/IEC 27001; no dedicated AI cybersecurity control in Annex A. |
| **MC-D1-01** AI policy and governance framework | EU AI Act | `Art.17` | partial | medium | Art.17 requires a QMS including a compliance strategy and written policies; broader than a single AI policy. |
| **MC-D1-02** Roles, responsibilities and accountability | EU AI Act | `Art.16` | partial | medium | Art.16 with Art.26 allocates accountability by role; statutory obligations rather than an internal RACI. |
| **MC-D1-03** AI system inventory and registration | ISO/IEC 42001 | `A.4.2` | partial | low | A.4.2 documents AI resources but is not a system-of-record inventory; coverage is partial. |
| **MC-D1-03** AI system inventory and registration | EU AI Act | `Art.49` | partial | medium | Art.49 requires registration of high-risk systems in the EU database (Art.71); an external register, narrower than an internal inventory. |
| **MC-D2-01** AI risk assessment and treatment | NIST AI RMF | `MANAGE-1.1` | partial | medium | Risk activity is distributed across MAP/MEASURE/MANAGE rather than one consolidated process. |
| **MC-D2-03** Risk tolerance and acceptance criteria | ISO/IEC 42001 | `6.1` | partial | medium | Clause 6.1 frames risk criteria; ISO does not separately codify a risk-tolerance statement. |
| **MC-D2-03** Risk tolerance and acceptance criteria | EU AI Act | `Art.9` | partial | medium | Art.9 requires judging acceptable residual risk; partial to a standalone tolerance control. |
| **MC-D3-01** Data acquisition and provenance | NIST AI RMF | `MAP-2.3` | partial | low | NIST documents data across MAP; provenance is not a discrete subcategory. |
| **MC-D3-02** Data quality and preparation | NIST AI RMF | `MAP-2.3` | partial | medium | Covers documentation of data; quality thresholds implied, not prescribed. |
| **MC-D3-03** Data representativeness and bias examination | ISO/IEC 42001 | `A.7.4` | partial | medium | ISO addresses data quality; representativeness/bias is examined via quality, not a dedicated control. |
| **MC-D3-04** Privacy and personal data protection | ISO/IEC 42001 | `A.4.3` | partial | low | ISO manages data resources but defers privacy-specific controls to ISO/IEC 27701 and external regimes. |
| **MC-D3-04** Privacy and personal data protection | EU AI Act | `Art.10` | partial | medium | Art.10(5) conditions special-category processing; broader privacy duties sit in the GDPR. |
| **MC-D4-02** Technical documentation | NIST AI RMF | `MAP-2.3` | partial | low | NIST treats documentation as cross-cutting; no single technical-documentation subcategory. |
| **MC-D4-03** Record-keeping and event logging | NIST AI RMF | `MANAGE-4.1` | partial | medium | NIST captures logging within monitoring rather than as a discrete record-keeping control. |
| **MC-D5-01** Human oversight of AI systems | ISO/IEC 42001 | `A.9.2` | partial | medium | Annex A.9 addresses responsible use but not per-decision human intervention controls. |
| **MC-D5-01** Human oversight of AI systems | NIST AI RMF | `GOVERN-3.2` | partial | medium | GOVERN 3.2 sets the oversight expectation, not the operational intervention capability. |
| **MC-D5-02** Operator competence and human-AI configuration | ISO/IEC 42001 | `A.9.4` | partial | medium | A.9.4 with A.9.2 constrains use to intended purpose; operator competence is implied. |
| **MC-D6-01** Accuracy and reliability | ISO/IEC 42001 | `A.6.2.4` | partial | medium | A.6.2.4 covers verification and validation; accuracy levels are not a discrete Annex A control. |
| **MC-D6-02** Robustness and safety | ISO/IEC 42001 | `A.6.2.6` | partial | medium | A.6.2.6 supports detecting degradation; robustness is not a discrete Annex A control. |
| **MC-D6-04** Verification, validation and testing (TEVV) | EU AI Act | `Art.15` | partial | medium | Art.15 implies testing of accuracy/robustness; formal conformity testing sits in Art.43. |
| **MC-D6-05** Responsible design and development | NIST AI RMF | `MAP-1.1` | partial | medium | MAP 1.1 documents purpose, context, and requirements driving design. |
| **MC-D6-05** Responsible design and development | EU AI Act | `Art.16` | partial | low | Art.16 obliges providers to design systems to meet requirements; there is no single lifecycle article. |
| **MC-D7-03** Performance evaluation and continual improvement | NIST AI RMF | `MANAGE-2.3` | partial | medium | MANAGE 2.x sustains value and responds to emergent risks; improvement is distributed across functions. |
| **MC-D7-03** Performance evaluation and continual improvement | EU AI Act | `Art.72` | partial | medium | Art.72's monitoring feeds improvement; there is no standalone continual-improvement article. |
| **MC-D8-02** Customer and downstream responsibilities | EU AI Act | `Art.26` | partial | medium | Art.26 places downstream duties on deployers; partial to a provider-side handoff control. |
| **MC-D8-03** General-purpose AI (GPAI) model governance | ISO/IEC 42001 | `A.4.4` | partial | low | ISO addresses GPAI/foundation models only through general controls (tooling and third- party), not a dedicated provision. |
| **MC-D8-03** General-purpose AI (GPAI) model governance | NIST AI RMF | `MAP-4.1` | partial | medium | The NIST Generative AI Profile (AI 600-1) and MAP 4.1 address generative and value- chain model risks; the base RMF lacks GPAI specifics. |
