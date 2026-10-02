---
summary: SMARTS matching mutates read-only arrays with Pandas 3.
issue: uibcdf/molsysmt#289
status: resolved
opened: 2026-10-02
closed: 2026-10-02
severity: high
verification: reproduced
area: [selection, deps]
guard: tests/topology/get_substructure_matches/test_get_substructure_matches.py::test_read_only_bond_arrays_preserve_source_chemistry
normative:
blocked_by: []
supersedes: []
---

# SMARTS matching mutates read-only arrays with Pandas 3

## What

The public native-system SMARTS path raises `ValueError: assignment destination
is read-only` with Pandas 3.0.6. MolSysViewer reported this in its cation–pi
installed-artifact qualification, uibcdf/molsysviewer#140.

```python
import molsysmt as msm
from rdkit import Chem
molsys = msm.convert(Chem.MolFromSmiles('c1ccccc1.[NH4+]'), to_form='molsysmt.MolSys')
msm.topology.get_substructure_matches(molsys, '[a;r6]1:[a;r6]:[a;r6]:[a;r6]:[a;r6]:[a;r6]:1')
```

## How

`get_substructure_matches` fills missing numeric bond orders and substitutes
aromatic order 1.5 in a Pandas-owned NumPy array. Pandas 3 copy-on-write may make
that extraction read-only. Inspection found the same mutation in
`physchem.get_charge_centers`. Both need explicitly owned writable work arrays.

## Why

The failure blocks chemistry-dependent public interaction detectors. Mutating
the source chemistry to fix it would also violate the matching contract.

## What is measured and what is assumed

The reproduction above failed locally on unmodified main 18536a793 with Pandas
3.0.6 in an isolated environment. Pandas 2.3.3 does not always expose this error.
Regression tests therefore also simulate read-only extractions, preserving
writable extractions when `copy=True` is explicitly requested.

## What was refuted

Coordinates and MolSysViewer are unnecessary to reproduce the error. No global
copy-on-write setting or source chemistry mutation is required.

## Scope and exclusions

Correct numerical extraction in SMARTS matching and charge-center recognition.
This is not an installed-wheel or full Pandas 3 compatibility certification.

## Acceptance criteria

Aromatic and fractional-order native chemistry matches correctly with read-only
input arrays; source atom and bond DataFrames remain identical. Both Pandas 2
and Pandas 3 execute the focused tests.

## Provenance

2026-10-02, Linux x86_64, Python 3.13.14, NumPy 2.4.6. The shared environment
uses Pandas 2.3.3; an isolated temporary environment uses Pandas 3.0.6 and the
same remaining scientific dependencies. Commands and final counts are recorded
in the resolution below when verification completes.

## Resolution

Both numeric bond-order work arrays now request `copy=True`. SMARTS conversion
uses independent chemical-state records and a topology inventory view that
omits ownership links without invoking pickle compatibility restoration. A
naive shallow `copy.copy(Topology)` was refuted: its restoration normalized the
original state's optional columns. Selection also uses independent chemistry.

The guard matches benzene/ammonium plus ordinary bonds with read-only arrays,
including fractional-order input, and asserts exact preservation of the source
atom and bond DataFrames. The related charge-center test recognizes a
carboxylate from fractional orders while preserving its bond table.

Paired Pandas 2.3.3 and Pandas 3.0.6 tests use the same source path and scientific
dependencies. No global copy-on-write setting or client workaround is required.

## Verification checkpoint — 2026-10-02

The default local suite passed **11,744 tests**, with 11 known environment skips,
in 341.85 seconds. The focused interaction/chemistry/doctest suite passed 723
tests; Pandas 3.0.6 focused qualification passed 161 tests. Developer-tool tests
and result doctests passed 260 tests. Ruff, docstrings, API signatures and the
14 fast release gates passed. This is local source evidence, not an installed
artifact or cross-platform release certification.

The [dated evidence artifact](../../../devtools/data/interactions_reported_bugs_20261002.json)
records commands, source hashes, measurements and exclusions.
