---
summary: append_structures partially publishes structures before validating named analyses and state links.
issue: uibcdf/molsysmt#520
status: resolved
opened: 2026-10-28
closed: 2026-11-03
severity: high
verification: reproduced
area: [api, structure]
guard: tests/basic/append_structures/test_domain_atomicity.py
normative:
blocked_by: []
supersedes: []
---

# append_structures leaves a partial structure/state/analysis publication

**Reported:** 2026-10-28, expert addon composition receiving under
uibcdf/molsysviewer#264 / uibcdf/molsysmt#421.
**Status:** existing transactional correction has qualified combined public regressions.
The original failure was reproduced
independently of Viewer. No scientific fix belongs in the addon.

## What

What — `basic.append_structures` partially extends a native target before failing when it has named interactions and explicit structure-to-chemical-state associations.

How — Reproduced without Viewer on `ac30d5ba4f392016f9bd15eda660886ef044b93b`, Python 3.14 (`molsyssuite@uibcdf_3.14`):

```python
import numpy as np
import molsysmt as msm
from molsysmt.native import MolSys, Structures

target = MolSys(n_atoms=3)
target.structures = Structures(
    coordinates=msm.pyunitwizard.quantity(np.zeros((3, 3, 3)), 'nm'))
msm.set(target, structure_chemical_state_index=[0, 0, 0])
incoming = target.copy()
target.interactions = {'saved': msm.Interactions.from_records(
    [], n_atoms=3, n_structures=3,
    evaluated_structure_indices=[0, 2], method='append-regression')}
msm.append_structures(target, incoming)
```

Raises `ValueError: Interaction analysis 'saved' has atom/structure domains (3, 3), expected (3, 6).` The coordinate/structure axis has already grown to six; reading `target.interactions` also raises. The same target without explicit state associations completes, narrowing the trigger.

`MolSys.append_structures` appends the structural payload, then calls `_set_structure_chemical_state_indices` before extending named analyses. Its invalidation context validates the old analysis against the already-grown structure axis. This is a scientific-owner problem; the addon does not reorder these internal steps or clear analyses to conceal it.

Why — Named analyses are normal input to the expert addon under uibcdf/molsysviewer#264 / uibcdf/molsysmt#421. A failed native in-place call leaves an inconsistent system; Viewer must quarantine it as an uncertain partial write. Independent mode must preserve the caller's source even on rejection.

Acceptance — Add pytest regression coverage for implicit and explicit single-state associations, compatible/unknown multi-state associations, empty and populated named observations, native versus coordinate-only sources, in_place True/False and rejection paths. A successful append must extend analysis axes/maps, preserve old observations/evaluated coverage and leave new structures unevaluated. Rejected operations must not leave a partially published structure/state/analysis combination. Do not silently drop analyses or weaken scientific assertions.

Record — devguide/archive/resolved_bugs/append_structures_named_analyses_partial_state.md


## What is measured and what is assumed

The public minimal reproduction uses only MolSysMT and NumPy on isolated
ac30d5ba4f392016f9bd15eda660886ef044b93b. It raises after the structure count
becomes six while the named analysis remains defined on three structures.
A pentalanine-based live-view receiving case exposed the same failure; the
Viewer host is unnecessary for reproduction. The counterpart without explicit
state links completes. Multi-state, persisted and nonempty-observation variants
need owner qualification and are not claimed as reproduced here.

## How

`MolSys.append_structures` publishes `Structures.append` and then enters
`_set_structure_chemical_state_indices` before `_extend_interaction_structures`.
The setter's `_invalidating_interaction_frames` reads `self.interactions`, whose
validator observes mismatched current and stored structure domains. This is
an ordering/publication problem, not a frame query or native-selector issue.

## What was refuted

No rendering, GUI, source interaction merge or optional scientific engine is
needed. Incoming interactions are empty. Coordinates and structure/state counts
match before the call. The initial implicit-state counterpart succeeds, so
empty named analyses alone are insufficient to trigger the failure.

## Scope and exclusions

Receive the native append/state/analysis publication contract and rejection
atomicity. Do not add an analysis-merge policy, invent observations, recalculate
interactions or repair the scientific operation in a Viewer adapter. The host
must keep a potentially partial write uncertain until explicit recovery.

## Current-source reassessment (2026-11-03)

Source **2e5c8b64b7a2e4aa270c09b6311691cd88800ac2** uses
`MolSys._append_structure_payload`, which prepares a candidate structural domain,
state association and extended named analyses before publishing them together.
The helper first appeared in 7b983af32ac4efcc3adb7c4c0617a38957ecc41e during
the chemical-domain separation; this identifies its introduction, not complete
qualification of this issue.

Eight preliminary public `msm.append_structures` probes pass in the existing
Python 3.14.7 development environment. They combine explicit single-state or
two-state associations, native MolSys or coordinate-only Structures sources,
and both `in_place` values. Each target has a populated named pair analysis on
three structures, with evaluated coverage `[0, 2]`. All outputs have six
structures, preserve the original observation/coverage, and leave the three new
structures unevaluated. Native sources retain their state associations;
coordinate-only sources use the single state implicitly or retain unknown
associations for multiple states. Independent mode leaves the target unchanged.

These are local receiving probes, not a durable pytest guard or a consumer/full
matrix certificate. Their bounded receipt remains in the ignored
`.pytest_cache/domain-composition-532/next-520-preliminary-probes.json` while
the acceptance audit continues. A query's projected coverage is read through
`to_dict()`; lightweight views share the base stored arrays. Unknown native
associations use nullable integer values, not an assumed Python sentinel.

Existing tests cover native state-association append, named-analysis append and
Structures rejection separately. Before closing, combine those contracts in
public regressions: implicit/explicit single state, compatible/unknown multiple
states, empty/populated analyses, both source kinds, both copy modes, and rejection
atomicity. In particular, check conflicting chemistry, structural/atom alignment,
strict one-sided attributes and unsupported incoming named analyses without
partially changing target structures, associations, observations or source maps.
Change the runtime only if those controls expose a remaining defect; do not
rewrite the current transactional helper merely because the original report
describes an older implementation.

## Combined acceptance regression (2026-11-03)

`tests/basic/append_structures/test_domain_atomicity.py` adds 45 focused cases:
32 successful combinations of implicit/explicit single-state and known/unknown
multi-state links, coordinate-only/native sources, empty/populated analyses and
both copy modes; two nonconsecutive source selections; eight rejection cases;
two simulated late allocation failures; and a public H5MSM round trip.

Successful appends preserve prior occurrences, handles, source identity/maps and
coverage, extend the structure domain, and leave incoming structures unevaluated.
Rejected operations preserve the original structural owner, coordinates, boxes,
times, velocities, chemical assignments, links and named analysis handles/payloads.
The late-failure control raises during preparation of the second analysis, after
the structural candidate and first analysis are prepared. Both in-place modes
leave the published target and source unchanged.

The combined new and existing append/state/analysis selection passes **68 tests**,
zero failures/omissions, exit 0, 10.01 s, with one existing legacy-format warning.
The initial harness compared a query's full structure-domain size with the old
three-structure size; that assertion was corrected to the explicitly extended
six-structure domain. The initial harness failure is not a new product defect.
No runtime change was needed: the transactional implementation introduced during
#255 already repairs the original publication order. The broader native,
composition, append, H5MSM and tooling selection passes **2,818 cases**, with zero
omissions/failures, exit 0, 169.68 s and 719 disclosed warnings. All 14 fast gates
pass.

## Hosted native-source qualification — 2026-11-03

Source **d8ea626a0ab6dbd976d0e04ad9299019e4ae0a42** passes the native test step in
[CI smoke run 41687790382](https://github.com/uibcdf/molsysmt/actions/runs/41687790382),
job 126098035944. Its bounded tier includes all 45 combined acceptance cases.
The native tier completes with **4,184 passes / 16 optional skips**, exit 0,
and the bound-Viewer tier with **2,449 passes / four optional skips**, exit 0.
The source run uses Linux/Python 3.14, Pandas 3.1.0 and Viewer
ca7ebea60d530a7a0c65cb4d0ccea7b4288f3352. Ackredit accounts for 14 native and
four addon omissions; unyt and astropy account for one native omission each.
The tiers retain 590 and 1,539 warnings, respectively. None of the 45 new
combined append cases is skipped. GitHub concludes success and GH Run Receptor's
final watch exits 0; all six applicable workflows succeed on that source.
This receives the existing transactional runtime together with the new durable
regressions; it is not a new runtime implementation, fresh full platform matrix
or installed Viewer-pair qualification. Consumer adoption remains separately owned.
