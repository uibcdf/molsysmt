# Partial charge calculation and attachment contract

Owner: uibcdf/molsysmt#221. Public interpretation belongs in `physchem`;
detached native reconstruction belongs in `build`. Partial mechanical charges
remain in experimental `MolecularMechanics`, independently of stored formal
charges in `ChemicalStates`.

## Scientific boundary

- Require an explicit method: `gasteiger_marsili` or `forcefield`. Optional
  providers are lazy RDKit and OpenMM, respectively. There is no fallback.
- Calculate and validate the full selected chemical graph before filtering
  output atom indices. Preserve source chemistry, atom ordering and IDs.
- Gasteiger-Marsili uses twelve RDKit iterations and strict parameter failures
  on a complete closed-shell organic graph with indexed H. Reject virtual H,
  unsupported elements/orders, missing required assignments and contradictions.
  Sanitation perceives chemistry only on a detached calculation graph.
- Force-field charges require explicitly named matched templates on the existing
  inventory. Reject unmatched templates, extra particles and virtual sites.
  This operation does not repair protonation, add H or fully parameterize a system.
- Validate finite full coverage and total conservation within 1e-6 elementary
  charge. Use complete formal charges or a declared scalar total; declarations
  must agree with a known formal total. Never infer zero or renormalize.
- Conservation and agreement with implementation controls establish numerical
  behavior, not physical charge accuracy or arbitrary receptor coverage.

## Units, axes and evidence

`get_partial_charges` returns a PyUnitWizard quantity following the active charge
unit policy. Native mechanical values and report numerical totals explicitly use
`elementary_charge`. Bare integer total declarations use that unit; bare float
or boolean totals are rejected. Unitful scalar totals can use any charge unit.
Manual `msm.set(..., partial_charge=...)` accepts finite vectors, converting
quantities to native elementary charge. Bare vector values use elementary charge.

Use atom and structure **indices**, independently of IDs. Validate explicit
frame selections against a known source axis. Structure-associated chemical-state
resolution must be unambiguous. Calculation output selections are sorted and
unique; manual setter values follow the explicit input selection order.

Detached reports use `molsysmt.partial_charge_assignment@1`: method, parameters,
state index/ID, full evaluated atom scope, selected output indices, evidence,
units, total source/tolerance and original producer versions. Retain detached
scientific references even if optional Ackredit reporting fails. Software versions
identify the producer, not whichever package is installed when a result is read.

## Native lifecycle

`assign_partial_charges` returns a complete native copy and requires one chemical
state because the current mechanical store holds one assignment. It replaces
partial charges and binds their report to ordered chemistry/values, without
claiming compatibility of other stored mechanical parameters. Copies and pickle
preserve this report. Automatic interaction coupling currently covers geometry and
ChemicalStates; callers explicitly invalidate/recalculate analyses depending on
changed mechanical values.

Extraction retains parent charge values and source atom mapping, marking a
projection. Preserve original calculation coverage and total separately from the
retained total. Validate the original binding before projection so a stale report
cannot become current by extraction. Joining separately attributed assignments
requires a new joint calculation: strict joins reject; intersection joins keep
numerical values and clear incompatible provenance with an explicit diagnostic.

Manual replacement through the public setter or native charge property clears
named attribution. Raw table edits bypass clearing; the PDBQT writer must reject
a stale bound graph/value/frame association. Graph-based charge assignments do
not become stale from coordinate movement. Binding digests are conservative
consistency checks, not authentication.

## Persistence and scale limits

PDBQT emits `REMARK MOLSYSMT_PARTIAL_CHARGES` with the named model, original
software, source coverage, written count and total before three-decimal rounding.
Retain all indexed H; no merging or redistribution. Reading native PDBQT does not
restore the full report or chemical graph. Types and torsion trees are independent
prepared inputs, not operations hidden in charge assignment or serialization.

MolecularMechanics is excluded from H5MSM 0.5. Mechanical/provenance persistence
is future 0.6 work under uibcdf/molsysmt#256. Do not claim a 0.5 charge round trip.
Numeric detached H5MSM queries read chemistry without coordinates; rich spatial
selections may load coordinates. Native attachment copies the whole system and
can materialize trajectories; it is not a streaming or out-of-core API.

## Regression guards and user surfaces

- `tests/physchem/test_get_partial_charges.py`: named methods, full-graph coverage,
  scientific implementation controls, totals, units, axes and conservative failures.
- `tests/build/test_assign_partial_charges.py`: native immutability, original
  versions, projection/joins, stale bindings, receptor export and H5MSM exclusion.
- `tests/basic/test_set_partial_charge.py`: validated manual assignment independent
  of a scientific calculation backend.
- User Guide: `docs/content/user/tools/physchem/get_partial_charges.md`,
  `docs/content/user/tools/build/assign_partial_charges.md` and
  `docs/content/user/cookbook/assigning_partial_charges.md`.
- Course: Common Core module 12 describes explicit chemical preparation.
