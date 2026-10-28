---
summary: Covalent paths lose integer axes and empty path width.
issue: uibcdf/molsysmt#508
status: open
opened: 2026-10-27
closed:
severity: medium
verification: reproduced
area: [topology, interactions, molsysviewer]
guard:
normative:
blocked_by: []
supersedes: []
---

# Covalent paths lose integer axes and empty path width.

**Reported:** 2026-10-27 during expert-addon receiving.
**Status:** open; native correction pending.

## What

`topology.get_covalent_paths()` does not preserve its rectangular empty-result contract. A valid empty position can promote otherwise integer source atom indices to float and cause ArgumentError; disconnected nonempty positions return shape (0,) instead of (0, len(path)). The classic donor helper inherits the failure for custom donor candidates without indexed H.

## How

Reproduced independently without Viewer, native basis 40a8ac2ea4042f807c7897459183b5533126781d, Python 3.14:

```python
import molsysmt as msm
from rdkit import Chem
molsys = msm.convert(Chem.MolFromSmiles("CC=O"))
for path in [[[2], []], [[], [1]], [[0], [2]]]:
    try:
        result = msm.topology.get_covalent_paths(molsys, path=path)
        print(path, result.tolist(), result.shape, result.dtype)
    except Exception as error:
        print(path, type(error).__name__, str(error))

msm.interactions.hbonds.get_donor_atoms(
    molsys, inclusion_rules=("atom_type=='O'",),
    default_inclusion_rules=False, default_exclusion_rules=False,
)
```

Observed: [[2], []] rejects selection 2.0; [[], [1]] rejects 1.0; [[0], [2]] returns int64 array with shape (0,). The custom donor query rejects 2.0. This is a fully converted declared RDKit chemical graph, not missing source chemistry. Concatenating selected indices with an untyped empty selection promotes the union to float; final `np.array(output, dtype=int)` also loses the path-width axis when output is empty. A downstream donor sort needs a two-column result.

## Why

These are ordinary no-match outcomes for scientific graph queries. Please preserve source integer indices and shape (0, len(path)) for valid empty/disconnected paths and receive the outcome through donor-H recognition. Add native pytest cases for empty first/middle/last/all positions, string and equivalent numeric selectors, masks, disconnected graphs, hydrogen-free custom donors, valid nonempty/interleaved pairs, exact dtype/shape and source preservation. Unsupported path specifications should have explicit public validation; do not invent paths or H.

Distinct from #165 (ragged scalar normalization), #258 (donor-pair column ordering), #355 (empty bonded-to selector) and #506/#507 (rule lists/language). Consumer context: uibcdf/molsysmt#421 / uibcdf/molsysviewer#264. The thin expert addon adds no empty-array patch or graph algorithm. Record: devguide/pending_bugs/covalent_paths_lose_integer_axes_and_empty_path_width.md, to land with receiving. Closure needs an addressable native pytest guard.

## What is measured and what is assumed

The standalone native reproducer runs without Viewer. The provider source basis
is 40a8ac2ea; its scientific implementation matches the earlier 667f03b9a basis.
These are contract/shape/form observations, not new scientific methods or a
claim of universal input validity.

## What was refuted

This does not require a GUI callback, a molecular edit or consumer selection
translation. Existing reports named above have different failure mechanisms;
no duplicate was found before filing. The positive expert fixtures use supported
chemistry and valid axes; this excluded native limit stays independently visible.

## Scope and exclusions

The native helper and direct expert consumer are in scope. No wrapper graph
algorithm, index cast, result reshaping or frame policy is introduced here.

## Acceptance criteria

Resolve the public semantics and add mechanically addressable native pytest
coverage for the matrix above. Preserve source chemistry and original source
indices. Receive the owner repair separately in the addon before changing its
documented limitation; a source wrapper is not blanket scientific qualification.

## Dependencies and risks

The native scientific owner chooses and implements the contract. Consumer
compensation would hide disagreement across ordinary source forms and calls.
