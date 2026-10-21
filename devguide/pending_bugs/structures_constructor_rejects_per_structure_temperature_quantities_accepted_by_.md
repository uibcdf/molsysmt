---
summary: Structures constructor rejects per-structure temperature quantities accepted by its native storage
issue: uibcdf/molsysmt#395
status: open
opened: 2026-10-21
closed:
severity: medium
verification: reproduced
area: [argdigest, structure]
guard:
normative:
blocked_by: []
supersedes: []
---

# Structures constructor rejects per-structure temperature quantities accepted by its native storage

## What

The validated native Structures constructor rejects a temperature quantity of
shape `(n_structures,)`, even though its public temperature property, molecular
queries and StructuresDict conversion support that series.

## How

```python
import numpy as np
import molsysmt as msm
from molsysmt.native import Structures

Structures(coordinates=msm.pyunitwizard.quantity(np.zeros((2, 2, 3)), "nm"),
           temperature=msm.pyunitwizard.quantity([300.0, 301.0], "K"))
```

**Reproduced:** this raises ArgumentError in
`molsysmt/_private/argdigest/argument/temperature.py`. The shared temperature
digester accepts scalar values only, without distinguishing a simulation
setting from a structural observable. Constructing the same Structures without
temperature and then assigning the quantity to its public `temperature`
property succeeds; conversion/query returns the two values.

Discovered by the real-payload StructuresDict documentation guard under #393.
The guard uses the existing property route to test storage/serialization; it
neither bypasses digestion nor claims the constructor accepts a series.

## Why

A supported native structural observable cannot be supplied through the normal
validated constructor, encouraging users to bypass validation. The scalar
simulation-setting contract should remain distinct from a structure series.

## Intended resolution and acceptance criteria

Study caller-scoped array admission for native structure-series boundaries,
including shape, physical dimensions and structure-axis alignment. Preserve
scalar temperature semantics for simulation settings. Check related energy
observable digesters before claiming they have the same or a different defect.
Add public constructor/append/query tests with compatible units, invalid shapes
and wrong dimensions. This report does not broaden any boundary yet.
