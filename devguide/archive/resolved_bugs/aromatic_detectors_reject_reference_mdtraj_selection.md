---
summary: Aromatic detectors reject MDTraj string selections for reference chemistry.
issue: uibcdf/molsysmt#516
status: resolved
opened: 2026-10-28
closed: 2026-11-03
severity: medium
verification: reproduced
area: [interactions, selection, molsysviewer]
guard: tests/interactions/test_aromatic_reference_selections.py
normative:
blocked_by: []
supersedes: []
---

# Reference-state external selectors in aromatic detectors

## What

pi_pi.get_pi_pi_interactions and cation_pi.get_cation_pi_interactions reject
MDTraj atom-selection strings with the public chemical_state='reference'
default. Equivalent explicit atom indices return one expected observation on
the same source. No Viewer call is required to reproduce the failure.

## How

Source bb808a8b14f15805477f177c5dbfe1b3ea49aff6, routine Python 3.14 environment.
The native proof uses RDKit-declared benzene/benzene and benzene/ammonium
chemistry with analytical coordinates and explicit nm quantities. Two parallel
rings have centroids 0.35 nm apart; the cation is 0.35 nm above the ring.
The custom pi-pi call supplies all four documented cutoffs. Both numeric
selections return one observation; equivalent `index 0 1 ...` strings with
syntax='MDTraj' raise ArgumentError for syntax in basic.select.

```python
import numpy as np
from rdkit import Chem
import molsysmt as msm
angles = np.arange(6)*np.pi/3
ring = np.column_stack((.14*np.cos(angles), .14*np.sin(angles), np.zeros(6)))
for family, name, smiles, xyz, options in [
    ('pi_pi', 'get_pi_pi_interactions', 'c1ccccc1.c1ccccc1',
     np.vstack((ring, ring+[0,0,.35])),
     dict(distance_threshold='.6 nm', angle_threshold='30 degrees',
          offset_threshold='.2 nm', planarity_threshold='.02 nm')),
    ('cation_pi', 'get_cation_pi_interactions', 'c1ccccc1.[NH4+]',
     np.vstack((ring, [0,0,.35])), {}),
]:
    molsys = msm.convert(Chem.MolFromSmiles(smiles))
    molsys.structures.append(coordinates=msm.pyunitwizard.quantity(xyz[None], 'nm'))
    calculate = getattr(getattr(msm.interactions, family), name)
    indices = list(range(len(xyz)))
    print(family, calculate(molsys, selection=indices, pbc=False, **options).n_interactions)
    calculate(molsys, selection='index '+' '.join(map(str, indices)),
              syntax='MDTraj', pbc=False, **options)
```

Execute each family independently. The scalar records and native traceback are
retained with the consumer source receipt. Reproduction imported the live owner
checkout; both detector file hashes match the recorded published basis and the
isolated validation snapshot. New facade code is unnecessary for this proof.

## Why

Both callers set selection_state=state_index for a string selection, losing
the public reference sentinel. basic.select deliberately rejects external
syntax for a nonreference chemical-state argument. Existing reusable chemical
selection already distinguishes reference requests from genuinely different
states; the native detector should preserve its intended contract. Related
previous selector work is uibcdf/molsysmt#482, not a reason to translate inputs
inside a consumer.

## What is measured and what is assumed

Numeric selection succeeds; equivalent MDTraj selection fails for both
prepared sources under reference chemistry. The inspected state forwarding
explains the observed guard. Broader profile, second-selection and nonreference
semantics need the native owner's test matrix; this report does not promise
that every external state/syntax combination should be supported.

## What was refuted

This is not missing aromatic/formal-charge evidence, a partial participant,
a missing custom cutoff, a Viewer selection translation or a geometric
threshold-boundary ambiguity. The same native source and numeric atom set
produce the expected positive result.

## Scope and exclusions

Both aromatic detector callers and their two selection slots are in scope.
Keep whole rings/compound centers, chosen methods/profiles, chemical-state
resolution and native restrictions for genuinely unsupported requests intact.
No selector translation, forced state or scientific algorithm is implemented
in the addon. Consumer ownership: uibcdf/molsysmt#421 / uibcdf/molsysviewer#264.

## Acceptance criteria

Addressable native pytest guards for both detectors, primary/secondary string
selectors, internal/incident/disjoint-between scopes, supported profiles and
custom cutoffs, reference versus nonreference requests, numerical equivalence,
nonconsecutive structures and untouched source/state. Reuse the owning
chemical-state selection tool where appropriate. Receive the native repair
separately; preserve explicit errors for genuinely unsupported requests.

## Dependencies and risks

The scientific owner resolves supported state/syntax combinations. A consumer
workaround would conceal the native defect and create inconsistent selector
semantics across the suite.

## Correction and receiving — 2026-11-03

Both detectors now reuse `chemical_states._chemical_graph.select_chemical_atoms`,
which distinguishes the public reference request (`None`/`reference`) from an
explicit state index or structure-assigned state. Numeric/all selections keep
the detached chemistry view; rich selections retain the original context and
validated structure scope. No selector translation, forced state, new chemistry
or geometry threshold is introduced. H5MSM rich selections still reject forced
streaming and numeric/all routes retain #542's graph-only preparation.

Fourteen focused native cases failed before the change: both reference spellings
across all seven attributed/custom profiles, using both external selection slots.
The expanded native matrix covers all seven profiles, nonzero declared reference
index 1, native/H5MSM/composite forms, internal/incident/between scopes, each/both
selection slots, repeated nonconsecutive structures and evaluated-empty coverage.
It also verifies explicit state 0/1 and structure-assigned rejection for external
syntax while the equivalent numeric queries work. Source tables, state reference,
structure assignments and file bytes remain unchanged.

The 482-case checkpoint passes: the complete expanded selector matrix, both
aromatic detector regression modules and final supplied-donor controls. This
includes #542's unchanged four pi-pi and expanded cation-pi eager-read sentinels.
The bound remaining-interaction tests now require positive reference-selection
parity instead of enshrining the reported native error, retaining explicit-state
rejection. Final addon/documentation receiving remains in progress.

Docstrings, both detector tutorials, the sparse-query recipe and the four
physicochemical course modules explain reference versus explicit-state requests.
Notebook code, outputs and metadata are preserved. Other course interaction
modules were reviewed: their existing default/numeric calls need no change.

## Final receiving — 2026-11-03

The final combined selection passes **2,021 tests**, zero failures or skips,
254.79 seconds, two workers: all interaction tests, both bound detector receiving
modules, bound hydrogen-site tools, covalent-path and reference-SMARTS controls,
structure-index types and the hosted-command guard. It includes 114 final
supplied-donor cases and 238 aromatic-reference cases. Numerical 2 MB budget
controls retain seventeen memory-pressure warnings; legacy H5MSM reads retain
fifteen warnings. These are not process-RSS benchmarks or installed qualification.

Final documentation receiving passes **569 tests/doctests**, zero failures or
skips, 77.24 seconds. Its 531 warnings are 514 Sphinx/MyST deprecations, ten
legacy-H5MSM reads, six headless-display notices and one deliberate structural
attribute-drop control. Full-tree Ruff lint/format, public docstrings and all
fourteen fast readiness gates pass. The new native guard is explicitly selected
by hosted smoke. Earlier checkpoint counts overlap; they must not be added as
unique coverage.

Linux source receiving uses the shared Python 3.14.7, NumPy 2.4.6 and Pandas 2.3.3
environment, the unchanged compiled backend, and Viewer source
ca7ebea60d530a7a0c65cb4d0ccea7b4288f3352. No environment, dependency floor,
scientific threshold, attribution branch, H5MSM schema or publication route
changes. The frozen metadata candidate a24b14f3d is separate and does not contain
these later corrections. Its queued full/Rust gates remain its own evidence.
