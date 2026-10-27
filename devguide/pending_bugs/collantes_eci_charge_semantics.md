---
summary: Review the Collantes ECI electric-charge and aggregation contract.
issue: uibcdf/molsysmt#475
status: open
opened: 2026-10-26
closed:
severity: medium
verification: reproduced
area: [physchem, units]
guard:
normative:
blocked_by: []
supersedes: []
---

# Review the Collantes ECI electric-charge and aggregation contract

## What

The original article identifies ECI as an electronic charge index for side-chain
QSAR. MolSysMT exposes it through get_charge(definition='collantes'), wraps it
using the shared elementary-charge unit and sums group scores for higher axes.
The accessible primary abstract does not establish that physical dimension or
an additive net-charge interpretation. This is a suspected semantic mismatch,
not a proven incorrect numerical entry or established alternative unit.

## How

The original abstract is indexed at [PMID 7629809](https://pubmed.ncbi.nlm.nih.gov/7629809/).
The [publisher record](https://doi.org/10.1021/jm00014a022) identifies the 1995
Collantes/Dunn article. Full definition, formula and table remain to be read.
The report was discovered while reviewing ISA under uibcdf/molsysmt#473.

The public call on pentalanine produces five ALA scores of 0.05 in elementary
charge, whereas the physical_pH7 definition is a separate group reference:

```python
import molsysmt as msm
molsys = msm.convert(
    msm.systems['pentalanine']['traj_pentalanine.h5msm'], structure_indices=[0])
score = msm.physchem.get_charge(
    molsys, selection='group_name=="ALA"', definition='collantes')
assert msm.pyunitwizard.get_value(score, to_unit='e').tolist() == [0.05] * 5
```

Executed on Linux/Python 3.14.7 at source 9d7d81d31. The unit wrapper and
higher-level sums are also directly inspected in get_charge.py and the shared
`units = 'e'` declaration in groups/charge.py. Different values between two
named definitions do not themselves prove that either implementation is wrong.

## Why

A QSAR score must not be interpreted as a force-field charge, assigned formal
charge or independently verified net molecular charge merely because the API
returns a quantity. A source-parity guard cannot establish physical meaning.

## Scope and acceptance

Read the original definition and formula, establish dimension and justified
aggregation, and check the original table. Decide whether a distinct public
ECI descriptor route or a qualified compatibility contract is appropriate.
Then align naming, docs, provenance, units and meaningful guards. Do not alter
physical_pH7 or OpenMM behavior, infer atom charges or guess a replacement unit
from the descriptor's name. Until that review, existing numerical behavior is
preserved and its semantic uncertainty is explicit. No new algorithm, optional
provider, scientific certification or dimensional correction is implemented.

## Scientific-evidence scope correction — 2026-10-26

The prior machine-readable registry classified the whole get_charge API as
validated, including a test described as independently transcribed original
Collantes values. That provenance is unsupported by the current primary-reference
review: the original table, dimension and aggregation have not been read and
verified. Matching the retained legacy numbers is not an independent oracle.

The registry now classifies get_charge as partial. Physical_pH7 Arg/Asp/Ala
reference checks and independently declared OpenMM parameters retain their
bounded evidence; the Collantes node is removed from the scientific inventory.
Its unchanged numeric/wrapper/sum assertions move to
`tests/physchem/test_collantes_legacy_contract.py`, explicitly as compatibility
regression. No values, units, sums, signatures or runtime dependency change.
The maintained scientific-validation contract and generated matrix carry this
boundary. This corrects the evidence claim, not the unresolved physical contract;
#475 remains open, and #473 still needs original ISA units and normalization.

The scoped registry/reference/legacy regression and changed get_charge doctest
selection passes 26 cases on Linux/Python 3.14.7 (two expected legacy-H5MSM
warnings). The numerical assertions were moved intact; no original paper access
is claimed. Commands, hashes and the remaining primary-reference requirement are
recorded in [the evidence-scope receipt](../../devtools/data/collantes_evidence_scope_20261026.json).
