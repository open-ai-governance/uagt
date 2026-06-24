# UAGC Gap View

> Mappings where coverage is incomplete (`partial`) or absent (`none`). These are the analytically valuable outputs (FR3).

| Master Control | Framework | Ref | Relationship | Confidence | Rationale |
| --- | --- | --- | --- | --- | --- |
| **MC-SE-02** Security, cybersecurity and resilience | ISO/IEC 42001 | `—` | none | high | ISO/IEC 42001 defers information-security controls to ISO/IEC 27001; Annex A contains no dedicated AI cybersecurity control, so there is no clean equivalent. |
| **MC-TR-02** Disclosure of AI-generated and synthetic content | ISO/IEC 42001 | `—` | none | high | ISO/IEC 42001 is a management-system standard and contains no control specific to labelling AI-generated or synthetic content; this obligation has no clean equivalent. |
| **MC-TR-02** Disclosure of AI-generated and synthetic content | NIST AI RMF | `—` | none | high | The NIST AI RMF addresses transparency as an outcome but does not prescribe synthetic-content disclosure or marking; no direct subcategory corresponds. |
| **MC-AC-01** AI policy and governance framework | EU AI Act | `Art.17` | partial | medium | Art.17 requires a QMS including a compliance strategy and written policies; broader than, but encompassing, an AI policy for high-risk providers. |
| **MC-AC-02** Roles, responsibilities and accountability | EU AI Act | `Art.16` | partial | medium | Art.16 allocates accountability to providers (Art.26 to deployers); these are statutory obligations rather than an internal responsibility model, hence partial. |
| **MC-AC-03** AI system inventory and registration | ISO/IEC 42001 | `A.4.2` | partial | low | A.4.2 documents AI resources but is not a system-of-record inventory; coverage is partial. |
| **MC-AC-03** AI system inventory and registration | EU AI Act | `Art.49` | partial | medium | Art.49 requires registration of high-risk systems in the EU database (Art.71); an external register for in-scope systems, narrower than an internal inventory. |
| **MC-DG-01** Data acquisition and provenance | NIST AI RMF | `MAP-2.3` | partial | low | NIST documents data and input characteristics across MAP, but provenance is not a discrete subcategory; coverage is partial. |
| **MC-DG-02** Data preparation, representativeness and bias examination | NIST AI RMF | `MEASURE-2.11` | partial | medium | MEASURE 2.11 evaluates fairness and bias at the measurement stage; data-side representativeness is only partially captured here. |
| **MC-DG-03** Training data governance and quality | NIST AI RMF | `MAP-2.3` | partial | medium | Covers documentation of data; quality thresholds implied, not prescribed. |
| **MC-DG-04** Privacy and personal data protection | ISO/IEC 42001 | `A.4.3` | partial | low | ISO/IEC 42001 manages data resources but defers privacy-specific controls to ISO/IEC 27701 and external regimes; coverage is partial. |
| **MC-DG-04** Privacy and personal data protection | EU AI Act | `Art.10` | partial | medium | Art.10(5) conditions special-category data processing; broader privacy obligations sit in the GDPR outside the AI Act, hence partial. |
| **MC-HO-01** Human oversight of AI systems | ISO/IEC 42001 | `A.9.2` | partial | medium | Annex A.9 addresses responsible use and accountable deployment but does not prescribe per-decision human intervention controls, so coverage is partial. |
| **MC-HO-01** Human oversight of AI systems | NIST AI RMF | `GOVERN-3.2` | partial | medium | GOVERN-3.2 requires policies for human-AI configurations and oversight roles; it sets the governance expectation but not the operational intervention capability. |
| **MC-HO-02** Operator competence and human-AI configuration | ISO/IEC 42001 | `A.9.4` | partial | medium | A.9.4 (with A.9.2 responsible use) constrains use to intended purpose; operator competence is implied rather than prescribed. |
| **MC-LC-01** Responsible design and development | NIST AI RMF | `MAP-1.1` | partial | medium | MAP 1.1 documents purpose, context, and requirements that drive design; NIST spreads lifecycle activity across functions. |
| **MC-LC-01** Responsible design and development | EU AI Act | `Art.16` | partial | low | Art.16 obliges providers to ensure systems are designed to meet Section-2 requirements; there is no single lifecycle article, hence partial. |
| **MC-LC-02** Verification, validation and testing (TEVV) | EU AI Act | `Art.15` | partial | medium | Art.15 implies testing of accuracy/robustness; formal conformity testing sits in Art.43, so coverage of a general TEVV control is partial. |
| **MC-LC-04** Record-keeping and event logging | NIST AI RMF | `MANAGE-4.1` | partial | medium | NIST captures logging within monitoring (MANAGE 4.1 / MEASURE 2.4) rather than as a discrete record-keeping control. |
| **MC-RM-01** AI risk assessment and treatment | NIST AI RMF | `MANAGE-1.1` | partial | medium | MANAGE covers treatment and MAP covers identification; the assessment activity is distributed across functions rather than a single prescribed process, so the correspondence to one consolidated control is partial. |
| **MC-RM-03** Risk tolerance and acceptance criteria | ISO/IEC 42001 | `6.1` | partial | medium | Clause 6.1 frames risk criteria and treatment, but ISO does not separately codify a risk-tolerance statement. |
| **MC-RM-03** Risk tolerance and acceptance criteria | EU AI Act | `Art.9` | partial | medium | Art.9 requires judging acceptable residual risk within the risk-management system; partial to a standalone tolerance control. |
| **MC-SE-01** Accuracy and robustness | ISO/IEC 42001 | `A.6.2.4` | partial | medium | A.6.2.4 covers verification and validation; accuracy/robustness performance levels are not a discrete Annex A control. |
| **MC-TR-03** Technical documentation | NIST AI RMF | `MAP-2.3` | partial | low | NIST treats documentation as cross-cutting and has no single technical-documentation subcategory; coverage is partial. |
