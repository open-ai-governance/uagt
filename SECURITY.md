# Security Policy

UAGT is open governance **data** (CC BY 4.0) plus small build **tooling** (Apache-2.0). It
runs no service and handles no user data, so the realistic security surface is the Python
build/validation scripts and the GitHub Actions workflows.

## Reporting a vulnerability

Please report suspected vulnerabilities **privately**, not in a public issue:

- Use GitHub's **"Report a vulnerability"** (Security → Advisories) on this repository, or
- Open a minimal private channel with the maintainer via the repository's contact options.

Include the affected file/workflow, a description, and a reproduction if possible. We aim to
acknowledge within a few days and to credit reporters (with permission) in the release notes.

## Scope

In scope: the scripts under `scripts/`, the workflows under `.github/workflows/`, and the
JSON Schema. Out of scope: the correctness of individual control mappings (use a
[mapping-correction issue](.github/ISSUE_TEMPLATE/mapping-correction.yml) for those) and the
content of the referenced source standards.

## Supported versions

Only the latest tagged release and `main` are supported. Fixes ship in the next release.
