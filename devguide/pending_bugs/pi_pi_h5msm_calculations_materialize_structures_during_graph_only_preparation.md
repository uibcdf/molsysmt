---
summary: Pi-pi H5MSM calculations materialize structures during graph-only preparation.
issue: uibcdf/molsysmt#542
status: partial
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
**Status:** corrected and locally received; hosted receiving of the corrected
combined candidate remains pending before integration and issue closure.

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

## Caller audit — 2026-11-03

The seven occurrence detectors using a separate `coordinate_source` are pi-pi,
cation-pi, attributed hydrogen bonds, halogen bonds, hydrophobic contacts, metal
coordination and water bridges (including two-water paths). Their numeric/all
routes need chemistry only during candidate preparation; their existing geometry
executors own coordinate delivery. Rich-selection routes retain structural context.
The correction makes that choice explicit at each detector boundary rather than
changing the shared default and breaking spatial chemical queries.

Three other graph-only preparations need the same explicit boundary: SMARTS
matching with numeric/all selections, the local directional-site support plan,
and known-source PDBQT pose reconstruction. The latter uses coordinates from the
pose input, not the source trajectory. Hydrogen projection already converts its
source to a native MolSys before requesting the context and uses its own source
geometry; its existing route is retained. Ring/aromatic recognition, atom
correspondence and hydrogen-site recognition already declare their structural
needs. Other graph-only descriptor, charge, typing and connectivity tools already
pass `with_structures=False`.

Existing streaming tests are strengthened to reject independent structural reads
as well as whole-system and named-analysis loads. A chunk-count assertion alone
would not detect an eager read occurring before the iterator. The original pi-pi
sentinel remains unchanged.

## Local receiving — 2026-11-03

- The unchanged four pi-pi sentinels failed before the correction. New numeric
  SMARTS and directional-plan sentinels also failed at the independent structural
  reader. The valid H5MSM known-source PDBQT sentinel reproduced that same read;
  earlier attempts with unsupported mechanical payloads or invalid fixture setup
  are not counted as reproductions.
- Detector-stage receiving: **3,045 passed**, no failures or skips, 387.07 seconds,
  two workers. Selection: `tests/interactions`, `tests/chemical_states`,
  `tests/physchem`, the structure-index type guards and bound Viewer hydrogen-site
  tools. This includes all 256 site-scope controls from #509. This checkpoint began
  before the three additional graph-only corrections and expanded cation-pi cases;
  it is not represented as one uniformly frozen final-source execution.
- Final-context receiving: **457 passed**, no failures or skips, 65.11 seconds,
  two workers. Selection: complete SMARTS/reference-selection, cation-pi,
  directional-site, PDBQT and hydrogen-projection modules, plus the new graph-only
  H5MSM module. This reruns consumers of the final three context corrections.
- The twelve focused cases (including both cation-pi profiles, both heavy modes,
  and explicit missing-inventory rejection) pass. They overlap the runs above;
  counts must not be added as unique coverage.
- Eight public function doctests pass. This check also exposed a stale pi-pi
  example assigning aromaticity to bare Topology after chemical-domain separation;
  the example now assigns it to MolSys, whose ChemicalStates owns that metadata.
- Full-tree Ruff lint/format and public docstring validation pass; the hosted
  smoke command guard passes. The new graph-only and PDBQT sentinels are explicit
  native smoke arguments.
- All fourteen fast readiness gates pass after the report/index update; these
  do not replace the required full source and installed-package matrices.

The shared development environment uses Linux/Python 3.14.7, NumPy 2.4.6 and
Pandas 2.3.3; the bound receiving path uses Viewer source
ca7ebea60d530a7a0c65cb4d0ccea7b4288f3352 and the existing compiled backend.
No environment, backend or scientific profile was replaced. Broad-run warnings
include legacy H5MSM reads, Pandas future behavior, deliberately small numerical
RAM budgets, unavailable GPU controls and off-axis structural drops. Final-context
warnings include six MDAnalysis mass notices and one NumPy binary-size notice.
These warnings are retained, not reclassified as failures or proof of measured
memory savings. Local source tests do not qualify installed packages or platforms.

The obsolete candidate's Rust and full matrices were cancelled. Its failed smoke
remains failed. New exact-source smoke/full/native
receiving is required on the refreshed integration branch before merging the
metadata contributions. No tag, release or registry publication follows from this
local result.

## Frozen combined candidate receiving — 2026-11-03

Main correction dbdbc9bfeb8a3963e533250f3a566861bcb2c34a is included in the
published combined candidate a24b14f3d241893e51703588f9db07a3a70cf11d on
`dev/review-tools-537-540`, retaining both reviewed PR ancestries. On this frozen
commit, **2,687 passed**, no failures or skips, 379.60 seconds, two workers. The
selection includes the complete 2,662-case bound addon, the original four pi-pi
sentinels, the expanded cation-pi controls, new graph-only/PDBQT controls, archive
validation and the hosted-command guard. All fourteen fast gates, full-tree Ruff
and public docstring validation also pass. The original receipt remains unchanged;
the new [corrected receiving receipt](../../devtools/data/molsysviewer_tools_corrected_receiving_20261103.json)
records this distinct checkpoint, scope, warnings and hosted run identities.

All nine new hosted workflows were queued at the last observation. They target
the exact candidate above and the controlled Viewer source used locally. The
metadata PRs and #537 remain unmerged/open pending their required executed gates;
#542 remains partial pending corrected hosted receiving. No current local result
is substituted for those remote checks or an installed-package qualification.

## Provenance

Linux/Python 3.14 hosted smoke on the two exact sources above, with the controlled
Viewer source ca7ebea60d530a7a0c65cb4d0ccea7b4288f3352 selected by the workflows.
The regression assertion is native and does not depend on displaying a scene.
Raw failed-step logs are retained in ignored stabilization caches for #509 and
#537/#540. The report does not infer a dependency cause from version differences.
