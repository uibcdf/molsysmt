---
summary: Assign partial charges with an explicit named model
issue: uibcdf/molsysmt#221
status: resolved
opened: 2026-09-22
closed: 2026-10-04
verification: measured
area: [build, attribute]
guard: tests/physchem/test_get_partial_charges.py
normative: devguide/partial_charge_assignment.md
blocked_by: []
supersedes: []
---

# Assign partial charges with an explicit named model

**Reported:** 2026-09-22, from the MolSysMT–DockingMT preparation review.
**Status:** Resolved. Bounded calculation, native attachment and public
contracts are implemented and verified.

## What

Provide form-agnostic named charge calculation through
`physchem.get_partial_charges` and detached full-system attachment through
`build.assign_partial_charges`. Require an explicit method and preserve source
chemistry, atom ordering, IDs and coordinates. Implement two distinct routes:
Gasteiger-Marsili for compatible indexed-H organic graphs, and matched force-field
template charges for compatible explicitly parameterizable inventories.

## How

Normalize at public digested boundaries and delegate scientific work to optional,
lazy RDKit/OpenMM. Existing chemical graph/readiness, state resolution, converters
and force-field resolver remain general tools. Private charge orchestration and
binding bookkeeping introduce no competing chemical store.

Gasteiger-Marsili uses RDKit twelve-iteration equalization with strict parameter
failures, complete covalent orders and closed-shell H/C/N/O/F/P/S/Cl/Br/I chemistry.
Provider sanitation may perceive missing aromaticity on a detached graph, but known
conflicts fail. Virtual H and unmapped hydrogen charges are rejected. Force-field
assignment names its model, matches existing templates and rejects extra particles
or virtual sites instead of repairing the input. AMBER14 protein fixtures are
separate evidence from ligand Gasteiger fixtures.

Validate finite full coverage and a total-charge difference no greater than
1e-6 elementary charge. Use complete formal charges or a caller declaration;
never assume zero, use preexisting charges as a result, or renormalize. Output
selection happens only after full-graph calculation. Explicit structure selections
are validated against the actual source axis, including RDKit conformers.

Detached `molsysmt.partial_charge_assignment@1` reports contain method/parameters,
state, atom scopes, evidence, units, totals, scientific references and original
producer versions. Ackredit is optional; references and science survive its failure.
Native one-state attachment stores canonical elementary-charge values and their
bound report in experimental MolecularMechanics. Copy/pickle preserve provenance;
extraction retains parent charges and original indices without claiming fragment
recalculation. Chemistry/value binding failures remain stale after projection.
Strict joins reject incompatible named provenance; intersection joins clear it
with an explicit diagnostic. Manual charge replacement clears named attribution.

The PDBQT writer validates the binding and emits a JSON REMARK summary of the
producer, source coverage and total before three-decimal rounding. It does not
restore that report on native reading, infer typing or redistribute H charges.

## Why

Previously stored mechanical values and provider-specific converted properties
did not establish a general named assignment operation. Docking preparation and
other workflows need inspectable chemistry, coverage and producer provenance.
Ligand success alone cannot establish receptor coverage. The conventional villin
protein fixture supplies a distinct tested route instead of zero-filled values.

## What is measured and what is assumed

**Measured:** The manual-setting module passed 12 tests in 4.19 s; native
assignment/export tests passed 13 tests in 8.63 s. Commands:

```bash
env PYTHONPATH=/tmp/molsysmt-readiness-argdigest-013 python -m pytest --receptor=llm tests/basic/test_set_partial_charge.py
env PYTHONPATH=/tmp/molsysmt-readiness-argdigest-013 python -m pytest --receptor=llm tests/build/test_assign_partial_charges.py
```

Tests distinguish full-graph calculation from selection, known versus declared
totals, unsupported chemistry, provider failures, original versions, units,
source immutability, stale binding/projection, incompatible joins and H5MSM 0.5
mechanical exclusion. A numeric H5MSM query forbids coordinate dataset reads;
a rich spatial selection checks the original coordinates.

**Inspected and reproduced:** RDKit control values from the clean reference
checkout at `cbfb37abddcd5b5feeac97d53530ae6be83cac0d`,
`Code/GraphMol/PartialCharges/Wrap/test_data/halgren_out.txt`, supply independent
implementation controls for methanol, methanethiol, acetonitrile and acetamide.
OpenMM's installed ff14SB parameter file supplies alanine controls. Bundled villin
contains 596 atoms and assigned total +2 e; exported values meet the PDBQT
three-decimal rounding bound. These are implementation/coverage controls, not an
electrostatic accuracy benchmark or validation of mock AutoDock labels.

**Assumed:** Other inventories accepted by providers require their own chemistry
controls. No arbitrary protein, force-field, ligand or metal coverage is claimed.
No joint consumer preparation acceptance or supported-platform release gate has
been performed. The final broad regression passed 459 tests in 87.38 s, with 51 warnings in
ten groups (legacy H5MSM, provider/structural/unit diagnostics and one binary-size
import warning), rather than a warning-free result. Command:

```bash
env PYTHONPATH=/tmp/molsysmt-readiness-argdigest-013 python -m pytest --receptor=llm tests/basic/test_set_partial_charge.py tests/build/test_assign_partial_charges.py tests/physchem/test_get_partial_charges.py tests/interactions/test_scientific_attribution.py tests/native tests/basic/add tests/basic/test_extract.py tests/basic/test_extract_extended.py tests/form/file_pdbqt tests/form/rdkit_Mol --doctest-modules molsysmt/build/assign_partial_charges.py molsysmt/physchem/get_partial_charges.py
```

Ruff, public docstring fidelity, dependency validation and 156-notebook course
structure pass. The HTML build exits successfully with existing documentation
warnings; it is not a warning-free full documentation certification.

## What was refuted

- Zero-filled placeholders and an implicit method would hide missing science.
- Reusing existing RDKit properties could conceal another producer/model.
- Adding virtual hydrogen charge to a heavy atom would silently change atom scope.
- Ligand Gasteiger tests cannot establish a conventional receptor route.
- Total conservation cannot establish physical charge accuracy.
- A projected subset is not an independently parameterized chemical fragment.
- Source frame indices cannot be accepted without a validated structure axis.
- H5MSM 0.5 is not a charge/provenance round trip: mechanical persistence is
  explicitly deferred to 0.6 under uibcdf/molsysmt#256.

## Scope and exclusions

The durable contract is [partial_charge_assignment.md](../../partial_charge_assignment.md).
Numeric detached H5MSM calculation reads chemistry without coordinates. Rich
spatial selection may load coordinates; attachment copies the complete system
and can materialize a large trajectory. This is not an out-of-core assignment API.
Current mechanical attachment requires one state. Formal chemistry, AutoDock
labels, full force-field parameterization, protomer selection, geometry optimization,
nonpolar-H merging and active docking torsions remain independent concerns.
Existing analyses preserve their snapshots; callers explicitly invalidate analyses
that depend on changed mechanical values.

## Acceptance criteria

- Named methods deliver atom-aligned unitful charges and original provenance on
  supported inputs; source chemistry and coordinates are unchanged.
- Missing prerequisites, nonfinite/partial coverage, total mismatches and unsupported
  chemistry fail explicitly, without mutation or silent substitution.
- A separate conventional protein route records matched templates, named model and
  full source coverage visible in PDBQT; unsupported templates fail clearly.

The guards and user-facing contracts establish these bounded criteria. Wider
chemical quality and consumer-profile validation remain separate tracked work.

## Dependencies and risks

Related work: uibcdf/molsysmt#214, uibcdf/molsysmt#222, uibcdf/molsysmt#223,
uibcdf/molsysmt#224 and uibcdf/molsysmt#311.
Consumer profile and acceptance: uibcdf/dockingmt#5 and uibcdf/dockingmt#33.
Existing fixed-state H/template tools: uibcdf/molsysmt#298 and uibcdf/molsysmt#300.
Public docstrings/doctests, Foundations, Toolbox, Cookbook and Common Core module 12
are updated. No new dependency floor is introduced.

## Provenance

Local Linux x86_64, Python 3.13.14, NumPy 2.4.6, pandas 2.3.3,
RDKit 2025.09.5 and OpenMM 8.5.2, verified on 2026-10-04.
ArgDigest 0.13.0 released source at
`/tmp/molsysmt-readiness-argdigest-013` is pinned to
`9880fa7b990fd0987ff0de715b665eb9e11c11b2`; the bounded environment deviation
is uibcdf/molsysmt#237. Local editable optional attribution has a dirty producer
version; it is not a clean release certification. No full Linux matrix or consumer
acceptance is inferred from the focused scientific regression.
