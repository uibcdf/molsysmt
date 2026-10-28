---
summary: Aromatic detectors reject MDTraj string selections for reference chemistry.
issue: uibcdf/molsysmt#516
status: open
opened: 2026-10-28
closed:
severity: medium
verification: reproduced
area: [interactions, selection, molsysviewer]
guard:
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
