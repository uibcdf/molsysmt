---
summary: mmCIF model merging mistakes inequality requests for ignored labels.
issue: uibcdf/molsysmt#595
status: active
opened: 2026-11-05
closed:
severity: high
verification: reproduced
area: [form, convert]
guard: tests/form/string_pdb_id/test_to_mmcif_PdbxContainers_DataContainer.py::test_convert_multimodel_pdb_id_uses_all_nmr_models_offline
normative:
blocked_by: []
supersedes: []
---

# Incorrect mmCIF multi-model compatibility criterion

## What

The bundled 1L2Y BCIF/NMR input converts into a list of 38 separate MolSys
objects rather than one 304-atom, 20-group, 38-structure ensemble. The offline
identifier conversion guard fails on both the full hosted PR run and the
combined owner receiving tree.

## How

The DataContainer converter compares actual identity-bearing fields, but also
passes atom_id=False and component_name=False with comments claiming these
labels are ignored. In basic.compare, False requests inequality. It therefore
rejects identical component names, even though all requested atom names/types,
group identities/membership and component/molecule indices/names agree.
Native comparison semantics are correct; this consumer call is wrong.

The correction omits those non-identity labels from the explicit comparison.
It retains every positive identity criterion and the separate-system result
when those criteria disagree. The first model supplies stable native labels;
source atom serial labels do not determine positional correspondence.

## Why

An ensemble must not be fragmented because generated labels agree. This is
conversion fidelity, not a display issue or a reason to change public compare
semantics. No implicit atom alignment or merging of genuinely different
inventories is introduced.

## Evidence and acceptance

- Reproduced from bundled 1l2y.bcif.gz with no network and from the existing
  offline public-identifier guard. All 37 comparisons reject only component_name.
- Retain one complete 38-structure result, coordinates and expected native axes.
- Keep genuine identity mismatches separate; preserve native IDs as string labels.
- Run the converter and fidelity controls before integration. Hosted Python 3.14
  failure belongs to job 127683524087 of run 42153312659; other failures retain
  their independent causes and qualification requirements.

## Provenance

Linux / Python 3.14.7; main ed09f64539a5af6c1dbe9bd352c7ef65dcd4a7a6 plus PR
1c88e785b4327350ad586d437a569eff1a2c5c9a in the isolated receiving worktree.

## Receiving correction and result

After correcting the comparison, the existing public guard reached its next
assertion: it still expected absent occupancy. The source explicitly declares
1.0 for every atom/structure; the delivered primary-occupancy contract preserves
that information. The guard now checks the complete (38, 304) array of ones.
No occupancy is manufactured by this fix. The selected conversion run passes
146 cases, including the existing genuine-inventory-mismatch control and full
PDB fidelity. A serial CCD/conversion run passes 72 overlapping cases.
