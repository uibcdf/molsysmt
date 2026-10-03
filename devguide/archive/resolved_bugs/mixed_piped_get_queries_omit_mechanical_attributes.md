---
summary: Mixed piped get queries omit mechanical attributes
issue: uibcdf/molsysmt#301
status: resolved
opened: 2026-10-03
closed: 2026-10-03
severity: medium
verification: reproduced
area: [basic, attribute]
guard: tests/basic/get/test_mixed_mechanical_pipes.py
normative:
blocked_by: []
supersedes: []
---

# Mixed piped get queries omit mechanical attributes

**Reported:** 2026-10-03, while validating prepared PDBQT retrieval for DockingMT.
**Status:** Resolved; mixed-query regression verification passed.

## What

A combined query for chemical elements, mechanical labels/charges and
coordinates raises `KeyError: 'atom_ff_type'` instead of returning every
requested attribute. Individual mechanical queries work.

```python
msm.get(source, element='atom', atom_type=True, atom_ff_type=True,
        partial_charge=True, coordinates=True, output_type='dictionary')
```

The independent PDBQT fixture in
`tests/form/file_pdbqt/test_native_contract.py` reproduces the failure before
the fix. The general native test models a source with supported reduced
Topology and Structures pipes; the defect does not depend on a parser.

## How

`basic.get._piped_molecular_system` groups only topological and structural
attributes. The outer get loop then expects every requested key in the
merged result. Mechanical attributes are never put into a group, so their
keys are absent. A shared MolSys pipe does not repair that omission because
its group also lists only the two classified categories.

The fix retains reduced-domain grouping and appends a query on the original
source for every requested attribute not covered by those groups. That
remaining query follows ordinary direct-getter/derivation rules. It avoids
converting mechanical assignments to a domain that cannot store them.

## Why

Clients need one coherent atom-aligned query for coordinates, elements,
charges and model labels. The failure blocks that ordinary workflow despite
the form exposing every individual attribute. Severity is medium: explicit
separate queries provide a workaround, and no scientific values are fabricated.
Related form delivery is tracked in uibcdf/molsysmt#214.

## What is measured and what is assumed

**Reproduced:** the Vina basic-docking ligand source and independent synthetic
PDBQT fixtures raise the missing-key error before the correction. Native
reduced-pipe tests cover the same failure without external packages.
**Assumed:** no speed improvement is claimed; the change restores missing
queries rather than changing geometric or chemical algorithms.

## What was refuted

Adding more PDBQT converters or declaring different charge capabilities would
not repair the missing query group. Forcing a full native conversion would
also conflict with explicit authorization to discard format-specific trees.
The general get dispatcher must preserve every requested domain.

## Scope and exclusions

Mixed query result completeness, mechanical values and shared source atom
selection order. Public signatures, unit handling, chemistry perception,
format preparation and unsupported getter behavior are unchanged.
A pipe that points back to the same source form is not a valid test of this
contract: it recursively reconverts the source. Tests instead use supported
reduced native pipes and a PDBQT-to-MolSys shared pipe.

## Acceptance criteria

- All requested keys are present in mixed query results.
- Labels, charges and coordinates agree on the requested atom-index order,
  including nonconsecutive reordered indices.
- Reduced and shared native pipes retain mechanical fields.
- Source assignments are unchanged.
- Existing get, form recognition and conversion-report regressions pass.

## Provenance

Linux, Python 3.13, local MolSysMT main development checkout, 2026-10-03.
The fixtures are independent literal data; MDAnalysis is used only for a
separate optional format parity check, not to implement or reproduce the fix.

## Resolution — 2026-10-03

The dispatcher preserves requested attributes not covered by topology/structure
pipes and queries them on the original source. Two native regression cases
check complete and reordered nonconsecutive selections. PDBQT integration tests
check reduced and shared MolSys routes using independent charges/types/coordinates.
The guard checks concrete values and atom order, not only dictionary keys.

The combined mixed-query/PDBQT/existing-pipe/native-get/form-recognition/report
selection passed 292 tests in 37.21 seconds. Ruff and maintained course-structure
validation passed. No public signature, unit policy or scientific calculation
was changed. The updated prepared-PDBQT recipe and Molecular Attributes course
explain the combined query contract.
