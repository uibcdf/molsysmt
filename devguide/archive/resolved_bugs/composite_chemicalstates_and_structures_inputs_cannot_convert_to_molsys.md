---
summary: Composite ChemicalStates and Structures inputs cannot convert to MolSys
issue: uibcdf/molsysmt#269
status: resolved
opened: 2026-10-01
closed: 2026-10-01
severity: medium
verification: reproduced
area: [convert, form]
guard: tests/basic/convert/mult_to_one/test_convert_chemical_and_structural_domains.py::test_compose_chemical_and_structural_domains_without_inventing_topology
normative: devguide/forms_and_conversions.md
blocked_by: []
supersedes: []
---

# Composite chemical and structural domains cannot convert to MolSys

**Reported:** 2026-10-01, during the final pi-pi form-parity review.
**Status:** Resolved through shared conversion shortcuts and native partial-domain extraction.

## What

Converting aligned `ChemicalStates` and `Structures` together fails with
`InternalAlgorithmError`. The same failure occurs with `ChemicalStatesDict`.
These domains already work together inside a topology-free native MolSys or
H5MSM 0.5. A list of `Topology` and `Structures` also works.

```python
import numpy as np
import molsysmt as msm
from molsysmt.native import MolSys

molsys = MolSys(n_atoms=1)
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

## Resolution — 2026-10-01

**Implemented:** Both exact pairs (native ChemicalStates or ChemicalStatesDict,
with native Structures) register in the existing composite conversion graph.
The private converter reuses `MolSys._from_partial_domains` and `MolSys.extract`,
validating full axes before ordered remapping. Default outputs own independent
domains; explicit full-axis `copy_if_all=False` permits native sharing. Dictionary
chemistry is decoded using its existing converter. Topology remains absent and
all states, reference selection, chemistry evidence and units are preserved.

The shared ring context delegates these composites to public conversion with
full native sharing for read-only recognition. Covalent and aromatic ring tools,
and pi-pi observations, therefore use one composition policy. No detector-local
assembly routine or chemical store is introduced. No per-structure state
association is inferred for multiple states.

**Contract-tested:** Twelve conversion cases cover both input orders and chemical
forms, bonds and assignments, source immutability, ordered atom and repeated
structure selections, nondefault unit policy, incompatible full atom axes,
copy policy, implicit single-state resolution and public H5MSM persistence.
Four additional pi-pi cases compare composite observations with the analytical
native ensemble and check both ring tools. The guard asserts complete chemistry
and topology absence through public conversion; the original generic fallback
cannot satisfy it.

**Validation checkpoint:** 162 tests pass across composite conversion routes,
aromatic/covalent ring recognition, pi-pi analytical and independent molecular
oracles, public MolSys/H5MSM workflows and the converter's doctest. The existing
legacy-format and off-axis-reference warnings remain visible. Both updated
tutorials execute (convert: 58.3 s; aromatic persistence recipe: 9.8 s).
The converter docstring now uses a bundled BCIF example instead of a downloaded
PDB identifier. Foundations, Toolbox, Cookbook and the common native-forms course
module describe the same supported composition and association limits.
The HTML build completes without errors; existing navigation/reference warnings
remain visible. No new dependency, Rust routine or API namespace is introduced.
Two additional doctests for the updated ring-tool notes pass independently.

Reproduction:

```bash
python -m pytest --receptor=llm tests/basic/convert/mult_to_one tests/physchem/test_get_aromatic_rings.py tests/topology/test_get_rings.py tests/interactions/pi_pi tests/scientific_truth/curated/test_pi_pi_interactions.py tests/interactions/test_public_molsys_h5msm_workflow.py --doctest-modules molsysmt/basic/convert.py --disable-warnings
python docs/execute_notebooks.py -q -f docs/content/user/tools/basic/convert.ipynb docs/content/user/cookbook/saving_pi_pi_interactions.ipynb
```

**Scope:** The registered routes require native Structures and one chemical
collection. Arbitrary conflicting provider lists, independently authenticated
identity, a direct ChemicalStates-to-Topology conversion, and streamed composite
coordinate delivery are not established by this repair. Existing H5MSM/native
MolSys projected streaming routes remain available after explicit composition.
