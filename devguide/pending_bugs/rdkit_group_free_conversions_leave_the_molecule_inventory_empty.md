---
summary: RDKit group-free conversions leave the molecule inventory empty
issue: uibcdf/molsysmt#491
status: open
opened: 2026-10-26
closed:
severity: medium
verification: reproduced
area: [form, native, selection]
guard:
normative:
blocked_by: []
supersedes: []
---

# Group-free RDKit graphs lose the general molecule query axis

**Reported:** 2026-10-26 during TPSA/logP public-contract review under
uibcdf/molsysmt#485.
**Status:** reproduced; no runtime fix included in the descriptor study.

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
