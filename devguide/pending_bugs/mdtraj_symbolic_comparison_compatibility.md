---
summary: The installed MDTraj parser rejects symbolic non-strict comparisons.
issue: uibcdf/molsysmt#484
status: open
opened: 2026-10-26
closed:
severity: medium
verification: reproduced
area: [selection, dependencies]
guard:
normative:
blocked_by: []
supersedes: []
---

# The installed MDTraj parser rejects symbolic non-strict comparisons.

## What
The installed MDTraj 1.11.1 / PyParsing 3.3.3 pair rejects `index >= 0` and `index <= 0` directly on a valid one-atom MDTraj topology. `ge`/`le` aliases and the other tested comparisons work. MolSysMT exposes the same upstream parsing failure through its external-syntax route. This is a dependency-compatibility record, separate from #482's chemical-state normalization.

## How
```python
import mdtraj as md
molecular_topology = md.Topology()
group = molecular_topology.add_residue('LIG', molecular_topology.add_chain())
molecular_topology.add_atom('C', md.element.carbon, group)
for expression in ['index >= 0', 'index <= 0']:
    molecular_topology.select(expression)  # ValueError from parser
assert molecular_topology.select('index ge 0').tolist() == [0]
assert molecular_topology.select('index le 0').tolist() == [0]
```
The [official MDTraj selection reference](https://mdtraj.readthedocs.io/en/latest/atom_selection.html#operators) lists these symbolic comparisons as supported. A 12-operator native-provider audit reproduces failures only for <= and >= in this environment. No molecular preparation, Viewer or MolSysMT import is necessary to reproduce it.

## Why
External selections are a public MolSysMT capability used by the expert Viewer addon (uibcdf/molsysmt#421; uibcdf/molsysviewer#264). Compatibility and upstream routing belong to the scientific provider; consumers must not silently rewrite selectors.

## Acceptance criteria
Determine the affected provider/dependency range and an upstream or compatible-version resolution; do not infer it from this single environment. Add a native public-selection pytest matrix covering symbolic and alias comparisons with intended populations, using an explicitly complete target hierarchy. Keep underlying diagnostic cause and make any actual compatibility limits visible. No consumer monkeypatch or automatic selector rewrite.

Measured Linux/Python 3.14.7, MDTraj 1.11.1 and PyParsing 3.3.3, existing shared development environment. This is not a clean installed-pair or cross-platform qualification.

## What is measured and what is assumed

The reported behavior was executed in the existing Python 3.14 environment.
No clean-install or full compatibility-range conclusion is inferred.

## Alternatives and refuted paths

The reproduction excludes the molecular viewer. Native authority and the direct
provider remain separate from the compact or consumer presentation. The caller
will not rewrite inputs or reinterpret successful/failed exits to hide the gap.

## Scope and exclusions

This report records the defect and requested provider-owned guard. It does not
change runtime code, dependencies, release tags or publication state.
