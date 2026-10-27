---
summary: Expose context-preserving atomic and hierarchical molecular descriptor contributions
issue: uibcdf/molsysmt#497
status: resolved
opened: 2026-10-27
closed: 2026-10-27
verification: measured
area: [physchem, api, selection, units]
guard: tests/physchem/test_descriptor_contributions.py::test_selected_elements_sum_complete_context_contributions
normative:
blocked_by: []
supersedes: []
---

# Context-preserving descriptor contributions

**Requested:** 2026-10-27; the maintainer requested the usual physchem element
and selection pattern for the newly implemented molecular descriptors.
**Status:** Implemented and locally qualified; APIs remain experimental and
scientific evidence partial.

## What

Extend `physchem.get_tpsa` and `physchem.get_lipophilicity` with atom, group,
component, chain, entity and system output. Keep molecule defaults and existing
scientific methods. These additional outputs represent atomic contributions or
their sums in complete molecular context, not recalculated cut fragments.

## How

Reuse the general `get` hierarchy/selection contract to resolve requested rows
and their complete source parent molecules. The existing shared descriptor
boundary checks full parent chemistry/H inventory, connectivity, aromaticity,
state and covalent boundaries. Evaluate only needed unique parent molecules.
Use compiled RDKit `_CalcTPSAContribs` and `_CalcCrippenContribs`; no copied
coefficient implementation, new dependency or speculative Rust kernel is added.
Atomic output uses a NumPy singleton-column view and vectorized projection,
avoiding an allocation of one Python/NumPy object per output atom.

Crippen's atomic kernel does not materialize nonindexed H. Add only declared
hydrogens on a detached graph, retain source atom order, and fold newly
materialized H contributions onto their retained attachment atom with a weighted
count. Indexed source H atoms keep their own values. TPSA's H contributions are
zero, but hydrogen context determines polar atom types. This projection is an
explicit MolSysMT attribution convention; it is not a new scientific model.

Numeric indices refer to the requested element and preserve order/repetitions.
String selection identifies complete elements at grouped levels. `system`
interprets selection on atoms and returns a scalar contribution sum, including
zero for an empty selection; other empty outputs retain shape `(0,)`. A repeated
selected atom repeats its contribution. Summing contributions from different
molecules is not a physical mixture logP. TPSA quantities continue to follow
PyUnitWizard policy; Wildman–Crippen outputs remain dimensionless.

Reports retain original method/software attribution and complete evaluated
`molecule_indices`, `atom_indices` and `atom_offsets`. New `element`,
`element_indices`, `element_atom_indices`, `element_atom_offsets` and `output_kind`
identify output rows separately. Molecular context rows, net charges and charged
atom maps can therefore have a different length from selected contribution rows.
Keep that distinction when exporting. Existing molecular schema markers are
retained; additional report keys describe the newly supported output levels.

The prerequisite public membership defect discovered here is independently
tracked and repaired under uibcdf/molsysmt#498, in the native form adapter rather
than through a descriptor workaround.

## Why

`get_mass` already demonstrates element-based assignment and aggregation in
physchem. Reference-scale readers such as `get_hydrophobicity` have narrower
scientific applicability; their restrictions must not be generalized blindly.
The two graph models admit contribution outputs, provided chemical context and
H attribution are preserved. This gives clients useful atom/group maps without
silently changing the requested species or inventing source indices.

## Evidence and acceptance

- Independent primary atomic controls: methane C1/H1 values and nonindexed-H
  folding; ethanol's original OH TPSA contribution with repeated atom selection.
  Wider charged/aromatic/S/P/isotope controls are provider parity and contracts,
  not experimental partition/permeability accuracy.
- Test all supported output levels, source-form parity, repeated/empty/spatial
  context selections, scalar shape, units, complete-context admission, report
  maps and detached sources. Verify one provider call per needed parent.
- Preserve existing molecular tests, optional Ackredit behavior and producer
  references. Complete docstring/doctest, executed Tools examples, Foundations,
  paired-descriptor Cookbook and all four course paths.
- Retain exact local qualification commands, counts, warnings, environment and
  hashes in a dated receipt before closeout.

## Refuted alternatives and exclusions

Computing the selected induced graph would change H counts/atom typing and is
not equivalent. Inventing source indices for virtual H breaks correspondence.
Rejecting all charged atoms or neutralizing their parent changes the scientific
state. No fragment preparation, physical mixture model, logD/pKa calculation,
new descriptor persistence codec or installed/release qualification is included.
The API and scientific evidence retain their experimental/partial classifications.

## Provenance

Original model references: Ertl, Rohde and Selzer (2000),
[doi:10.1021/jm000942e](https://doi.org/10.1021/jm000942e); Wildman and Crippen
(1999), [doi:10.1021/ci990307l](https://doi.org/10.1021/ci990307l).
RDKit's [maintainer explanation](https://github.com/rdkit/rdkit/discussions/5352)
and [official examples](https://www.rdkit.org/docs/GettingStartedInPython.html#visualization-of-descriptors)
document the atomic provider routes. The local reference checkout inspected is
`cbfb37abddcd5b5feeac97d53530ae6be83cac0d`, specifically the descriptor C++ wrappers,
MolSurf and Crippen implementations. Executed provider version remains separately
recorded. Prior source/atomic-table checks are in the
[source receipt](../../../devtools/data/tpsa_logp_contract_review_20261026.json).

## Qualification closeout — 2026-10-27

The expanded scope passes 3,185 tests; final targeted qualification passes
1,464 native query/form tests and 218 descriptor/primary-control tests. The
556-case documentation/receiving scope includes two doctests, notebook schema
checks and all seven valid bound TPSA output levels with preserved scene state.
Legacy atom/group rejection controls were replaced by positive forwarding
checks and unsupported bond rejection, preserving test intent after the extension.
All 14 fast gates, scoped Ruff, docstring and signature checks pass.

Both tool notebooks were executed on the final implementation (8.2 and 8.5
seconds); the Cookbook exports were executed and asserted. All five edited
course notebooks retain their original code and saved outputs. HTML exits zero
with existing header/orphan diagnostics outside the new contribution examples.
No warning-debt reduction, whole-suite, benchmark, installed-pair, cross-platform
or release qualification is claimed. Exact commands, chronology, warnings,
environment, hashes and scientific limits are in the
[qualification receipt](../../../devtools/data/descriptor_contributions_20261027.json).
