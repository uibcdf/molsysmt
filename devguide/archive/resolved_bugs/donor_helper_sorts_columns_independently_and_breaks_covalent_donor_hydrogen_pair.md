---
summary: Donor helper sorts columns independently and breaks covalent donor-hydrogen pairs
issue: uibcdf/molsysmt#258
status: resolved
opened: 2026-09-29
closed: 2026-09-29
severity: high
verification: reproduced
area: [api, structure, scientific-integrity]
guard: tests/interactions/hbonds/test_donor_pair_integrity.py::test_donor_hydrogen_pairs_keep_declared_covalent_membership
normative:
blocked_by: []
supersedes: []
---

# Donor sorting breaks covalent hydrogen membership

**Reported:** 2026-09-29, while checking participant integrity for the Buch
result adapter under `uibcdf/molsysmt#250` and `uibcdf/molsysmt#252`.
**Status:** Resolved. The helper sorts intact covalent-pair rows.

## What

`interactions.hbonds.get_donor_atoms` can return a hydrogen paired with a heavy
atom to which it is not covalently bonded. With donor-H bonds `(0, 3)` and
`(2, 1)`, it returns `(0, 1)` and `(2, 3)`. Both hydrogen-bond detectors then
consume the incorrect donor-H assignment. The legacy `molsysmt.hbonds` path
uses the same implementation.

```python
import molsysmt as msm

builder = msm.MolSysBuilder()
for name, kind in [("N1", "N"), ("H2", "H"), ("N2", "N"), ("H1", "H")]:
    builder.add_atom(atom_name=name, atom_type=kind)
builder.add_group([0, 1, 2, 3], group_name="ALA")
builder.add_bond(0, 3)
builder.add_bond(2, 1)
molsys = builder.build()
print(msm.topology.get_covalent_paths(molsys, [[0, 2], 'atom_type=="H"']))
print(msm.interactions.hbonds.get_donor_atoms(molsys))
```

The covalent paths are `[[0, 3], [2, 1]]`; the old donor result is
`[[0, 1], [2, 3]]`.

## How

The donor helper calls `np.sort(output, axis=0)` after retrieving covalent
paths. This sorts the donor and hydrogen columns independently rather than
sorting intact rows. Hydrogen membership is therefore lost whenever the
hydrogen-index order differs from the donor-index order. A lexicographic row
permutation can provide deterministic ordering while retaining each bond.

## Why

The result is consumed by both Buch and Luzard-Chandler detectors. The wrong
hydrogen can change Buch's H-A distance and Luzard-Chandler's H-D-A angle, and
can give an interaction relation that contradicts the system's chemistry.
This is a scientific-integrity defect rather than an output-order preference.
It becomes particularly relevant when atoms are extracted or reordered and
when a viewer interprets explicit donor/hydrogen/acceptor roles.

## What is measured and what is assumed

- **Reproduced:** The four-atom example above preserves the declared bonds in
  `get_covalent_paths` and loses them only in `get_donor_atoms`.
- **Inspected:** Both detectors read `donors[:, 0]` and `donors[:, 1]` as
  corresponding covalent partners.
- **Assumed:** No frequency estimate is made for affected user systems. Atom
  inventories that place hydrogens in increasing donor order can conceal the
  defect.

## What was refuted

The topology and covalent-path helper retain the correct bond identities.
The mismatch appears after sorting, so changing inclusion/exclusion chemistry
or rebuilding bonds does not address its cause. Sorting each column cannot
be treated as harmless presentation ordering.

## Scope and exclusions

This report covers deterministic ordering of intact donor-H pairs and the
resulting participant integrity in the two existing detectors. It does not
change chemical eligibility rules, geometric thresholds, chemical-state
selection policy, periodic geometry, or the optional result schema.

## Acceptance criteria

1. A guard with interleaved atom indices returns exactly the declared donor-H
   pairs in deterministic donor/hydrogen order.
2. Both detectors emit triples containing the hydrogen covalently attached to
   the donor in a synthetic geometry with an eligible acceptor.
3. The Buch sparse result responds to a hydrogen query using that true partner.
4. Existing bundled-system detector regressions remain valid or are corrected
   only when a previously incorrect partner is independently demonstrated.

## Provenance

Reproduced on 2026-09-29 on host `nauta`, Python 3.13.14, NumPy 2.4.6,
starting from `b582c321c` with the Buch adapter under development. The
reproduction uses only native `MolSysBuilder`, explicit covalent bonds, and
the public donor helper; it requires no downloaded molecular data.

## Resolution — 2026-09-29

`get_donor_atoms` now orders rows with
`output[np.lexsort((output[:, 1], output[:, 0]))]`. It never sorts the two
columns independently. The inclusion/exclusion rules and the covalent-path
construction remain the authority for the pairs; sorting changes only row
order.

All four interleaved-index tests failed before the correction and passed
afterward. The named guard compares the reported pairs with the explicitly
declared `(0, 3)` and `(2, 1)` bonds; restoring independent column sorting
makes that assertion fail. Additional checks cover triples from both
detectors and Buch sparse queries for the true hydrogen. The complete
interaction and legacy hydrogen-bond battery passed 65 tests, including the
existing HP35 and Barnase/Barstar regressions. Two updated public-function
doctests also passed.
