---
summary: Composite ChemicalStates and Structures inputs cannot convert to MolSys
issue: uibcdf/molsysmt#269
status: open
opened: 2026-10-01
closed:
severity: medium
verification: reproduced
area: [convert, form]
guard:
normative:
blocked_by: []
supersedes: []
---

# Composite chemical and structural domains cannot convert to MolSys

**Reported:** 2026-10-01, during the final pi-pi form-parity review.
**Status:** Reproduced conversion limitation; domain composition needs a shared repair.

## What

Converting aligned `ChemicalStates` and `Structures` together fails with
`InternalAlgorithmError`. The same failure occurs with `ChemicalStatesDict`.
These domains already work together inside a topology-free native MolSys or
H5MSM 0.5. A list of `Topology` and `Structures` also works.

```python
import numpy as np
import molsysmt as msm

molsys = msm.MolSys(n_atoms=1)
molsys.structures.append(
    coordinates=msm.pyunitwizard.quantity(np.zeros((1, 1, 3)), 'nm'))
msm.convert([molsys.chemical_states, molsys.structures],
            to_form='molsysmt.MolSys')
# InternalAlgorithmError: The conversion needs to include new set functions.
```

## How

`basic.convert._convert_multiple_to_one` resolves a composite through a base
form with a direct target converter, followed by attribute setters. Neither
ChemicalStates nor Structures advertises a direct MolSys route. The chemical
form exposes collection metadata, rather than the complete chemistry as flat
topology attributes. The generic fallback cannot assemble the native domains.

Ring recognition's shared `topology._rings.ring_context` also reaches that
conversion failure when asked to use this composite. The defect is owned by
conversion/domain assembly, rather than pi-pi's scientific criteria. Repairing
only the detector would duplicate composition policy and leave other consumers
with the same failure.

## Why

Users should be able to supply separately stored, explicitly aligned chemical
and structural domains to general molecular tools. This is especially relevant
to independent ChemicalStates and topology-free systems. Failure occurs before
scientific evaluation; no incorrect interactions are returned.

The supported workaround is to load the domains together from H5MSM 0.5 into
a MolSys before calculation. Matching counts alone must not invent an axis
correspondence or a structure-to-state assignment.

## What is measured and what is assumed

**Reproduced:** Native and dictionary chemical domains fail in the minimal
conversion above on source commit 18cc43021 with the pi-pi worktree additions.
Topology/Structures composition gives the same two pi-pi observations as the
corresponding native analytical three-frame fixture.

**Inspected:** Missing direct conversion routes and the generic fallback explain
the failure. No runtime or memory benchmark is claimed for a future repair.

## What was refuted

The detector's candidate search and plane fitting do not cause the failure:
conversion alone reproduces it with one atom and no ring. Presence of a separate
topology is unnecessary for the equivalent loaded partial MolSys calculation.

## Scope and exclusions

Repair general composition for chemical and structural domains, with explicit
atom-axis validation, reference-state preservation, selection/remapping and
source immutability. Preserve missing topology and unknown chemical-state
association. Arbitrary conflicting domain lists and automatic association of
independent files require explicit policy; they must not be silently inferred.

## Acceptance criteria

- Public conversion succeeds for native and dictionary chemical domains with
  compatible Structures, in either input order, without inventing topology.
- Atom and nonconsecutive structure selections preserve values, units, source
  order and chemical reference state; conflicting axes fail clearly.
- Multiple chemical states do not acquire an invented per-structure assignment.
- Shared ring/aromatic and pi-pi tools consume the repaired composite route.
- A mechanically addressable public conversion regression test protects the
  failure, and the conversion tutorial documents the supported composition.

## Provenance

2026-10-01; Linux, Python 3.13, local MolSysSuite development environment.
No network data or optional scientific dependency is needed for reproduction.
