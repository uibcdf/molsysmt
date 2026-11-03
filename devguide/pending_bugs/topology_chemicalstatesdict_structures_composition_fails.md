---
summary: Topology with ChemicalStatesDict and Structures bypasses native domain composition.
issue: uibcdf/molsysmt#532
status: open
opened: 2026-11-03
closed:
severity: medium
verification: reproduced
area: [native, convert, form]
guard:
normative:
blocked_by: []
supersedes: []
---

# Explicit inventory plus dictionary chemistry cannot compose a MolSys

**Reported:** while building independent #531 regression inputs.
**Status:** reproduced; no composition repair is included in #531.

## What

The native three-domain composition route accepts ChemicalStates but falls
through to generic attribute setters when its chemical provider is a
ChemicalStatesDict. The documented equivalent typed-domain combination fails.

```python
import numpy as np
import molsysmt as msm
from molsysmt.native import MolSys

source = MolSys(n_atoms=1)
source.structures.append(
    coordinates=msm.pyunitwizard.quantity(np.zeros((1, 1, 3)), 'nm'))
payload = msm.convert(source.chemical_states,
                      to_form='molsysmt.ChemicalStatesDict')
msm.convert([source.topology, payload, source.structures],
            to_form='molsysmt.MolSys')
```

Observed: InternalAlgorithmError and diagnostics about missing setters for
state/chemical fields on stable Topology or Structures.

## How

The explicit dictionary chemical provider is not received by the native triple
composition route. Its fallback tries to flatten chemical collection attributes
through generic setters. The public convert Notes and maintained migration
guide admit dictionary chemical providers alongside independent domains.

## Why

Consumers should not need an extra manual chemical decoding step merely because
stable inventory is also present. Preserve independent domain ownership rather
than adding state/component setters to Topology.

## What is measured and what is assumed

Reproduced on source 00abb958fb93649131d5ce5fe5e12e90cf4900e9 and rechecked
while correcting unrelated #531. The same one-atom source yields:

- Native Topology/ChemicalStates/Structures triple: succeeds with topology.
- ChemicalStatesDict/Structures pair: succeeds without topology.
- Topology/ChemicalStatesDict/Structures triple: InternalAlgorithmError.

## What was refuted

The source axes match and native composition succeeds. No chemical perception,
trajectory file, viewer, aromaticity or geometry calculation is required. The
#269 two-domain dictionary pair remains repaired; this is a different input
combination after the #255 native-model cutover.

## Scope and exclusions

Receive the explicit dictionary provider through the existing ChemicalStates
decoder and composition owner, preserving selection, source nonmutation,
reference state, units and honest structure/state associations. Do not restore
chemical facades in Topology, silently overwrite domains or infer correspondence
from equal counts. No implementation or release qualification is claimed here.

## Acceptance criteria

Public native/dictionary parity with an explicit Topology, both supported input
orders, valid selected axes, mismatched-domain refusal and source nonmutation.
Keep the already-supported native triple and topology-free pair as controls.

## Workaround

Explicitly convert the dictionary to ChemicalStates before composing the triple.

## Provenance

2026-11-03, Linux x86_64, existing Python 3.14.7 / Pandas 2.3.3 development
environment. Small synthetic molecular domains; no extra environment or build.
