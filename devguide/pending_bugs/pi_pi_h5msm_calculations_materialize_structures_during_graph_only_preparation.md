---
summary: Pi-pi H5MSM calculations materialize structures during graph-only preparation.
issue: uibcdf/molsysmt#542
status: active
opened: 2026-11-03
closed:
severity: high
verification: reproduced
area: [interactions, performance]
guard: tests/interactions/pi_pi/test_get_pi_pi_interactions.py::test_projected_file_and_native_parity_without_saved_analysis_loading
normative:
blocked_by: []
supersedes: []
---

# Pi-pi preparation bypasses bounded H5MSM geometry delivery

**Reported:** 2026-11-03, inspecting hosted receiving after the #509 correction.
**Status:** reproduced by the same four existing guards on main and the combined
metadata candidate; correction pending before integration.

## What

The shared chemical context now retains structural data when `with_structures`
is true. Pi-pi detection calls `ring_context` with that default, even on its
index/all H5MSM route, which supplies geometry separately through bounded blocks.
Its chemical preparation consequently calls `read_independent_structures`.
That eager read violates the detector's established memory contract.

## How

The existing guard reproduces the failure without Viewer:

```bash
python -m pytest --receptor=llm \
  tests/interactions/pi_pi/test_get_pi_pi_interactions.py::test_projected_file_and_native_parity_without_saved_analysis_loading
```

All four topology-present/absent and heavy-mode off/force combinations fail in
main [41711081692](https://github.com/uibcdf/molsysmt/actions/runs/41711081692)
on 402bdc6e4b852453da4e3a95dcae867ddd5fa686, and in candidate
[41714614542](https://github.com/uibcdf/molsysmt/actions/runs/41714614542)
on dd2c958c6bf5c8d6d83d88e95d623eb613be3cfa. The assertion explicitly forbids
materializing saved structural series or named analyses. Both native invocations
report 4 failed, 4,797 passed and 16 optional skips, exit 1; the later addon tier
does not execute after this native failure. Compact GH Run Receptor inspection
exposes only the nonzero step exit, so native failed-step logs supply these
specific tests and traceback facts.

Inspection traces the call from `get_pi_pi_interactions` to `ring_context`,
`chemical_graph_context` and the newly optional structural read in
`_read_calculation_chemistry`. The change landed with #509. Its native hydrogen
site behavior is covered, but its shared-context effect on the bounded pi-pi
consumer was absent from that local 1,279-case selection. Existing hosted guards
therefore reveal a real collateral regression, not an unexplained CI-only issue.

## Why and scope

Large H5MSM requests can acquire unnecessary coordinate memory before their
intended block iteration. No new peak-RSS measurement or OOM is claimed. The
regression affects main as well as the candidate, so the metadata PRs are not
its cause. Fix the producer/context request without weakening the memory guard
or removing structural context needed by genuine spatial chemical selections.

Review other shared-context consumers, including cation-pi. Preserve original
structure-axis validation, None/empty semantics, selected-state chemistry,
requested-row spatial site recognition and original source indices from #509.
No new detector, threshold, dependency floor or H5MSM version is required.

## Acceptance

- The original four sentinel cases pass while still forbidding eager structure
  and saved-analysis reads, in both heavy modes and topology cases.
- Audit and test the other callers of the shared context, retaining bounded
  geometry delivery where the detector already owns a separate coordinate source.
- All #509 site/scope guards and relevant pi-pi/cation-pi/native/addon controls pass.
- Qualify a corrected main and refreshed combined candidate; failed/superseded
  runs remain failures and missing hosted tiers remain unexecuted.

## Provenance

Linux/Python 3.14 hosted smoke on the two exact sources above, with the controlled
Viewer source ca7ebea60d530a7a0c65cb4d0ccea7b4288f3352 selected by the workflows.
The regression assertion is native and does not depend on displaying a scene.
Raw failed-step logs are retained in ignored stabilization caches for #509 and
#537/#540. The report does not infer a dependency cause from version differences.
