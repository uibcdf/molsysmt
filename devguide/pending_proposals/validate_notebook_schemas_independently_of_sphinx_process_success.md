---
summary: Validate notebook schemas independently of Sphinx process success.
issue: uibcdf/molsysmt#700
status: active
opened: 2026-11-10
closed:
verification: reproduced
area: [docs, tests]
guard:
normative:
blocked_by: []
supersedes: []
---

# Notebook schema validation needs an independent result

## What / How / Why

During #421 receiving, Sphinx exits zero while reporting invalid notebook JSON:
a new cell id is not permitted by a course notebook's declared nbformat 4.4.
The same source-error mechanism recurs in the combined 4183c2909 build. The
specific source is corrected, but exit status alone did not establish valid
notebook input. The individual receipt's earlier HTML acceptance is corrected
by the combined receiving record, retaining both actual zero exits and failures.

An independent strict, read-only schema check on the corrected source validates
all seven changed notebooks. The corrected HTML build has no notebook errors;
ten rendered pages and 81 unchanged executed code cells/outputs are inspected.
This is manual source-specific receiving, not an implemented global gate.

## Proposed outcome

Add a maintained validation route that checks real notebook schemas before
accepting documentation builds, including a build that exits zero after
reporting invalid input. Use the installed provider's supported API and declare
any developer dependency contract needed by the owning gate. Do not alter
runtime dependencies merely to validate development documentation.

Reject a malformed v4.4 cell id, invalid outputs and other schema violations;
accept valid v4.4 and v4.5 sources. Validate the declared version. Never repair,
upgrade, reserialize or add ids to source merely to obtain acceptance. Compare
inputs before and after validation. Inventory pre-existing debt explicitly.
The guard must require the protected property, not just search logs for ERROR
or accept syntactically shaped but semantically empty output.

## Scope and acceptance

A small valid/invalid fixture pair must prove that invalid input fails even
when a fake or real Sphinx process exits zero. Include actual provider validation
and unchanged source bytes. Then receive the route in the documentation gate.
The current corrected notebooks can be qualified through the recorded strict
manual check; this automation proposal adds no release waiver or original plan
weight. It is a bounded follow-up, not a reason to reopen the corrected cell.

## Implementation and receiving — 2026-11-10

The existing schema assertion is reused through one maintained developer CLI.
Fast release preflight, local Makefile build targets and the documentation
publication workflow call it before construction/publication. Read-only checks
reject schema failures, unknown declared versions, missing/empty inventories,
unexpected provider mutation or failure, and changed source bytes. Diagnostics
name schema locations without dumping cells or embedded outputs. No scientific
or public runtime dependency changes; docs/dev requirements and documentation/
test environments explicitly declare nbformat >=5.1.3.

Receiving must include every stored source, valid 4.4/4.5 controls, invalid
cell IDs/outputs, unique IDs, source preservation, and an actual Makefile build
whose controlled Sphinx process always succeeds. The invalid input must stop
before that process runs. A SHA-256-verified official nbformat 5.1.3 wheel probes
the declared API floor without modifying the shared environment. No closure or
additional formal plan credit is claimed until receiving and public delivery.
