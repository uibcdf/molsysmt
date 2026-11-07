---
summary: Scientific certificate release eligibility ignores untracked Python inputs.
issue: uibcdf/molsysmt#636
status: partial
opened: 2026-11-07
closed:
severity: high
verification: reproduced
area: [validation, release, provenance]
guard: devtools/tests/test_execute_scientific_evidence.py
normative: devguide/scientific_validation.md
blocked_by: []
supersedes: []
---

# Scientific execution source correspondence

## What

The execution runner can mark a passing certificate release-eligible with
`--require-clean` despite pytest loading Python input outside its named commit.
The tracked-source classifier ignores every untracked path, rather than
distinguishing workflow artifacts from executable or scientific source.

## How

The runner in `3f66f5931` checks Git with `--untracked-files=no`. A real isolated
Git control commits one passing test, adds an untracked `conftest.py` whose
session-start hook writes a marker and calls `execute_nodes(require_clean=True)`.
The hook demonstrably runs and the test passes. The returned certificate and
require-clean verdict still pass with `tracked_source_dirty=false` and
`release_eligible=true`; ordinary Git status shows the new Python input.
The complete control receipt is retained privately with native pytest exit zero,
the generated certificate, Git status and marker assertion. It is a negative
control of the tool, not MolSysMT scientific or candidate qualification.

## Why

The named commit must not be treated as containing an actually loaded, untracked
helper. The existing allowance for untracked workflow artifacts is legitimate
and must be preserved. Resolved #196 added real oracle execution; this separate
report concerns correspondence of that execution to its named scientific source.

## Acceptance criteria

- Detect and report untracked executable/configuration/reference inputs in the
  declared scientific source scope before claiming release eligibility.
- Preserve explicitly allowed workflow outputs and ignored build artifacts;
  do not satisfy the check by rejecting every artifact or calling all untracked
  files harmless. Native artifact/provider identity retain their separate gates.
- Add a real-Git negative guard with a demonstrably loaded untracked hook and
  positive clean/artifact controls. Retain failure/skip/uncollectable rejection.
- Keep the certificate's source evidence and maintained contract explicit.
- Retain the original successful-but-ineligible-source counterexample. No current
  candidate, tag or publication is authorized by either this control or its fix.

## Current development disposition

The actual #602/#633 development run executes 107 registered molecular oracle
cases across 68 nodes, with zero errors/failures/skips. It explicitly reports
tracked modifications and `release_eligible=false`. This honest development
certificate does not use the gap to claim a clean candidate. Repair #636 before
final exact-candidate source eligibility in phase six of the robustness plan.

## Corrected source boundary and original guard — 2026-11-07

The maintained real-Git guard reproduces nine failures and twelve passes before
correction. The nine failures are six untracked code/config/reference cases,
two actually loaded hooks (including a self-deleting hook), and a real commit
change during otherwise passing execution. No Git cleanliness response is mocked.

The runner now captures complete NUL-delimited Git status before and after the
actual pytest run. Nonignored untracked paths default to scientific source;
only four exact reserved workflow output paths are separated as artifacts.
Ignored builds/caches remain outside this check. Both snapshots must be clean
and name the same known commit for release eligibility. Legacy final-state fields
are preserved; additive snapshots and source-correspondence fields expose why
a developer certificate is ineligible. Failure/skip/collection rejection remains.

The maintained scientific guide defines the artifact paths and limits. They are
reserved outputs, not a way to hide scientific references; matching basenames
inside source directories are rejected. This repository check does not
authenticate ignored binaries or external providers; their gates remain separate.
Receiving and delivery follow; no candidate or publication is selected.

## Guard receiving — 2026-11-07

All **23 runner controls pass**, including original failure/skip/uncollectable
and non-Git refusal, actual loaded and self-deleting hooks, six untracked
source/config/reference paths, clean and reserved/ignored artifact positives,
a real changed commit, tracked source restored during execution and honest
ineligible developer execution. The original 21-case baseline has nine failures
and twelve passes; its native exit one is retained. New controls use independent
temporary Git repositories and execute real pytest nodes, not molecular oracles
or fabricated Git status. Whole-tree Ruff lint/format and developer-guide
validation pass. Next receive the actual registered molecular nodes on the
committed clean development checkpoint before source delivery and closure.
