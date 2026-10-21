---
summary: Structures constructor rejects per-structure temperature quantities accepted by its native storage
issue: uibcdf/molsysmt#395
status: resolved
opened: 2026-10-21
closed: 2026-10-21
severity: medium
verification: reproduced
area: [argdigest, structure]
guard: tests/native/test_structure_observables.py
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

## Accepted implementation — 2026-10-21

The maintainer authorizes the constructor/append correction for temperature,
potential_energy and kinetic_energy after the proposed review. All three
existing digesters restrict their default setting context to scalars. An explicit
`structure_series=True` decorator-owned context is now supplied only by native
Structures construction and append; no user keyword or global caller wildcard
is introduced. ArgDigest already supports these semantic parameters at the
declared 0.13.0 floor (source inspected), including inherited methods.

A shared private helper validates explicit units through PyUnitWizard, checks
real numeric rank before unit scaling, normalizes a scalar to shape (1,), and
standardizes the result. Numeric validation before scaling is necessary because
unit conversion can turn Boolean magnitudes into floating-point values. Bare
values, Boolean/complex data, incompatible dimensions and rank > 1 are refused.
None stays absent and an empty series represents zero structures. No scalar
broadcasting or physical value imputation is introduced.

The existing native axis validator now requires the three stored observables
to be one-dimensional before comparing series lengths. It remains the owner of
cross-field alignment and validates candidates before append commits them,
including trusted calls from native append_structures. Unit-bearing input is
converted to native K/kJ/mol storage; get follows the active output policy.
The scalar setting and Boolean query contracts remain unchanged.

## Resolution and evidence — 2026-10-21

The first 31 public failure guards all fail on the original implementation.
The expanded focused set passes 64 cases, including three scalar-setting
regressions, H5MSM/StructuresDict round trips under nondefault units, ordered
repeated structure selection, inherited methods and malformed stored-series
refusal. Existing structured YAML does not store these three observables;
its format is not expanded by this correction.

**Contract/parity tested:** the affected native, argument-digestion, generic
get/info, StructuresDict/YAML and conversion-truth selection passes 1,276 cases
with twelve workers and pytest-receptor. The 64-case focused selection is a
subset, not an additional distinct total. Ten constructor/append doctest
examples pass. Three new Toolbox/Cookbook/course examples execute in kernels
using the existing development interpreter; the actual native API page and new
Foundations/guide/course sections render with zero Sphinx diagnostics.

All fourteen fast gates, full Ruff check/format verification and the public API
signature guard pass. No public signature, dependency, numerical algorithm or
storage format changes. These are source checks, not a new installed-pair or
release qualification. No tag, release or promotion is authorized by this work.

The primary guard uses the public constructor, append and queries with literal
expected values, including 300000 mK -> 300 K and 1 kcal/mol -> 4.184 kJ/mol.
It requires ordered/repeated structure selections, scalar length-one semantics,
empty/absent series, unit-aware H5MSM 0.5 and StructuresDict round trips under
nondefault output units, inherited methods, and rejection without mutation for
invalid units/ranks/axis lengths. The shared native alignment check also rejects
malformed observables supplied through a public property before appending from
that source. Additional digester tests retain scalar setting and Boolean query
contracts. No coordinate-derived temperature/energy calculation is introduced.

Provenance: existing Linux/Python 3.14.7 development environment. ArgDigest's
semantic-parameter facility was source-inspected at 0.13.0; no separate installed
minimum-provider qualification is claimed.
