---
summary: RDKit group-free conversions leave the molecule inventory empty
issue: uibcdf/molsysmt#491
status: resolved
opened: 2026-10-26
closed: 2026-10-26
severity: medium
verification: measured
area: [form, native, selection]
guard: tests/native/test_group_free_molecules.py::test_group_free_molecule_inventory_and_atom_membership
normative:
blocked_by: []
supersedes: []
---

# Group-free RDKit graphs lose the general molecule query axis

**Reported:** 2026-10-26 during TPSA/logP public-contract review under
uibcdf/molsysmt#485.
**Status:** resolved; native membership and public queries support group-free inventories.

## What

A group-free RDKit input with two covalent components converts into a native
MolSys with six atoms and two components, but no molecules. Public molecular
queries cannot provide a usable axis: the count is zero and a combined
molecule/atom-index query raises IndexError. Native and direct RDKit query paths
exhibit the same problem. The accepted element inference contract uses
components as the fallback molecule partition when no better declaration exists.

```python
import molsysmt as msm
from rdkit import Chem

molsys = msm.convert(Chem.MolFromSmiles('CCO.COC'), to_form='molsysmt.MolSys')
print(msm.get(molsys, n_atoms=True))       # 6
print(msm.get(molsys, n_components=True))  # 2
print(msm.get(molsys, n_molecules=True))   # 0, expected fallback partition of 2
print(msm.topology.get_covalent_blocks(molsys, output_type='sets'))
# [{0, 1, 2}, {3, 4, 5}]
msm.get(molsys, element='molecule', molecule_index=True, atom_index=True)
# IndexError: arrays used as indices must be of integer (or boolean) type
```

## How

The RDKit topology converter preserves a graph with no group declarations and
calls rebuild_components, rebuild_molecules and rebuild_entities. The first
produces two components; the molecule table remains empty. The native
project_molecule_index_from_topology path relies on group-to-molecule mapping.
This bounded inspection identifies the failing seam, not a complete root-cause
or repair across every inference path.

## Why

General molecule-level descriptor tools cannot assume that group-free SMILES or
RDKit graphs already expose a valid molecule axis. A descriptor-specific component
fallback would duplicate inference and risk conflicting source indices. Fix the
native inventory/inference and form-agnostic public-query route rather than
creating a competing molecule definition inside physchem.

## Acceptance criteria

- Group-free connected/disconnected RDKit and native equivalents provide a
  consistent fallback molecule count and source atom membership.
- Preserve declared valid molecular membership and string IDs; do not invent
  biological group names or overwrite ChemicalStates.
- Whole-molecule, empty, reordered/repeated and string selections retain their
  documented source-index semantics and fail cleanly for invalid indices.
- Read-only queries do not mutate source/native chemistry or provider objects.
- Include charged disconnected components and validate state-specific
  connectivity where molecule metadata and the selected graph can differ.
- A named pytest regression protects the original six-atom/two-component case.

## Scope and exclusions

No RDKit descriptor or new public API is implemented here. The two chemical
components are present; this is not missing covalent connectivity, a coordinate
problem or a reason to infer extra hydrogen atoms. Components and molecules must
not be conflated when an existing declared molecule partition has other meaning.

## Provenance

Source cff1f8fe0acb0728d5b4374ba531a47db33309a1, Linux/Python 3.14.7,
RDKit 2025.9.5. Reproduced locally using RDKit-generated input; no network,
external files, scientific table or user dataset was needed.


## Resolution

Native rebuilding now creates molecule metadata from reference-state components
when no groups exist. Names/types follow component metadata and IDs remain
strings. No groups, chains or competing chemical store are invented. The shared
native atom-to-molecule projection bypasses absent groups and is reused by
public queries. Other active chemical-state components cannot silently change
this reference fallback. Existing declared group-based membership remains intact.

MolSysDict 0.1 conversion exposed the same prerequisite at its builder boundary:
empty group lists caused invented groups or rejected empty molecular membership.
Direct conversion now uses private native finalization that retains declared
absence, validates group-free molecule-record cardinality and preserves metadata.
Builders decoded from group-free records, or initialized from an existing
group-free native molecule inventory, retain that explicit absence when built.
The empty incremental builder's normal defaults do not change. Dictionary
inventory support does not imply preservation of every chemical assignment.

The guard protects six-atom/two-molecule native, RDKit, dictionary and H5MSM
routes, including zero groups, source atom maps and repeated/empty/string
selections. Additional tests protect native rebuild/string IDs, charged
components, independent reference versus active-state components and explicit
molecular declarations. Initial regression: 18 failed, 4 passed before repair.
The affected hierarchy/form block passes 1,354 tests. The broad block passes
5,129 tests plus its one network-dependent test recovered unchanged outside the
DNS-restricted sandbox. Final focused native/builder/TPSA controls pass 121 tests; doctest/schema
checks pass 502 and all fourteen fast gates pass. Source qualification is Linux/
Python 3.14 only; no benchmark, installed pair or release claim is made.

The [receipt](../../../devtools/data/group_free_molecule_inventory_20261026.json)
records exact source hashes, commands, limitations and recovery evidence. Native
class guidance and course bridges explain the fallback without biological groups.
