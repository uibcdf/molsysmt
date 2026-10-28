---
summary: append_structures partially publishes structures before validating named analyses and state links.
issue: uibcdf/molsysmt#520
status: open
opened: 2026-10-28
closed:
severity: high
verification: reproduced
area: [api, structure]
guard:
normative:
blocked_by: []
supersedes: []
---

# append_structures leaves a partial structure/state/analysis publication

**Reported:** 2026-10-28, expert addon composition receiving under
uibcdf/molsysviewer#264 / uibcdf/molsysmt#421.
**Status:** open; reproduced independently of Viewer. No scientific fix belongs
in the addon.

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

Record — devguide/pending_bugs/append_structures_named_analyses_partial_state.md


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
