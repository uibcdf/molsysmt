---
summary: Fixed-state hydrogen addition rejects valid aromatic-only bond tables
issue: uibcdf/molsysmt#318
status: resolved
opened: 2026-10-04
closed: 2026-10-04
severity: medium
verification: reproduced
area: [build]
guard: tests/build/add_missing_hydrogens/test_fixed_state.py::test_observed_benzene_template_aromatic_only_bonds_gain_six_hydrogens
normative:
blocked_by: []
supersedes: []
---

# Fixed-state hydrogen addition rejects valid aromatic-only bond tables

**Reported:** 2026-10-04 while independently checking uibcdf/dockingmt#41.
**Status:** Resolved. Aromatic-only bond tables are accepted without invented integer orders; observed BNZ and strict failure controls pass.

## What

The observed 181L BNZ accepts the public explicit heavy-only benzene template,
then `build.add_missing_hydrogens(mode='fixed_chemical_state', pH=None,
engine='RDKit')` rejects it with `MSM-ERR-STRUCT-003`: every covalent bond requires
explicit supported order and aromaticity. All six source bonds already declare
`is_aromatic=True` and `fractional_bond_order=1.5`. Their table has no integer
`bond_order` column, as permitted by the native chemical-state contract.

## How

The private fixed-H preflight first requires both column names unconditionally,
then applies a correct per-row predicate accepting a supported integer order or
explicit aromaticity. The column requirement rejects a valid all-aromatic table
before that predicate can execute. Existing mixed aromatic/aliphatic tables can
contain the integer column with missing entries on aromatic rows and do pass.

## Why

This blocks a chemically prepared ligand in DockingMT's public workflow. It also
rejects ordinary aromatic-only RDKit/native representations. Failure is explicit
and source-preserving; it does not silently generate incorrect chemistry.

## What is measured and what is assumed

**Reproduced on published main b5d94746a:** public conversion of the bundled
181L PDB, extraction of BNZ, template conversion from `smiles:c1ccccc1`, an
explicit identity atom map and `stored_counts` template application produce
six aromatic bonds and six fractional orders of 1.5. Fixed-state H addition then
fails. The expected neutral C6H6 inventory follows the explicitly chosen benzene
state, not an inferred state of the protein or a biological acceptance claim.

## What was refuted

The earlier consumer diagnostic was interpreted as missing bond aromaticity.
The prepared bond table proves that those flags are present. A new aromaticity
perception/attachment API is not needed for this particular rejection. The
provider should accept the declared representation, without inventing alternating
integer orders, changing the chemical state or normalizing the consumer input.

## Scope and exclusions

Correct only the fixed-state preflight for aromatic-only bond tables. Preserve
explicit atom/bond aromaticity, complete covalent connectivity, formal charges,
closed-shell H inventory, stereo, local pose and optional-engine requirements.
Nonaromatic bonds still require a declared supported integer order. Missing
aromatic flags, incomplete graphs and conflicting engine reinterpretation still
fail. Polymer preparation, aromatic/Kekule normalization, chemical-provenance
attachment, export charge projection and full consumer acceptance remain separate.

## Acceptance criteria

- Original observed BNZ plus the declared template gains exactly six indexed H,
  preserving all six source atom identities and coordinate values without mutation.
- Source bond flags/fractional orders remain explicit; no guessed integer Kekule
  assignments are written to the old aromatic bonds.
- H parent maps and independently plausible C-H lengths are correct; the expanded
  chemical state and pose persist through public H5MSM 0.5 conversion.
- Missing nonaromatic order or bond aromaticity still fails without mutation.
- Public docstring, User Guide and relevant course describe the accepted bond
  representation accurately; focused provider regressions pass.

## Provenance

Linux source checkout, Python 3.13.14, RDKit 2025.09.5, NumPy 2.4.6 and pandas
2.3.3, 2026-10-04. Released ArgDigest 0.13.0 at
`9880fa7b990fd0987ff0de715b665eb9e11c11b2` supplies the controlled development
boundary. This uses the temporary interpreter exception uibcdf/molsysmt#237;
it does not certify the supported release matrix or consumer's final workflow.

## Resolution — 2026-10-04

**Implemented and contract-tested:** the preflight requires explicit known bond
aromaticity, then validates each bond against an existing supported integer order
or its declared aromatic flag. An absent integer-order column remains unknown,
not a fabricated single bond. No perception or store is introduced; conversion,
template assignment, hydrogen inventory, local attachment and units use the
existing general tools and native ChemicalStates.

The guard first failed at the exact original preflight. It now applies the
public heavy-only benzene template to the bundled observed BNZ, checks six
appended H with one parent per carbon, exact old coordinates/IDs, unchanged
input, broad independent 1.0–1.15 angstrom C-H intervals and H5MSM 0.5
persistence. Old aromatic bonds retain flags and fractional orders, with unknown
integer orders. Their identity is checked by endpoint indices rather than row
positions because native expanded bonds follow canonical ordering. Two negative
controls still reject missing nonaromatic order and missing aromaticity without
mutation. B-factor/occupancy drops are explicit under intersection policy.

The controlled command passes **116 tests in 37.81 s**, including the public
doctest and existing fixed-state, aromaticity, template and EST controls:

```bash
python -m pytest --receptor=llm \
  tests/build/add_missing_hydrogens/test_fixed_state.py \
  tests/physchem/test_get_aromaticity.py \
  tests/physchem/test_chemical_template.py \
  tests/physchem/test_chemical_template_est.py --doctest-modules \
  molsysmt/build/add_missing_hydrogens.py
```

The released ArgDigest source override described above supplies PYTHONPATH.
Five warnings comprise two existing H5MSM reader downcasting warnings and three
explicit attribute-drop warnings. The three new cases separately pass in 4.83 s.
Ruff and format over the repository, all 238 public docstrings and the maintained
course validator pass (156 notebooks). Foundations, Toolbox, Cookbook and Module
12 describe the accepted representation. Sphinx HTML completes with existing
course-header/directive/navigation warnings; no new target was added. The legacy
`docs/content/course/devtools/validate_course.py` still rejects its obsolete
section template (0/156); it is not the maintained validator or release gate.

**Local consumer composition checked:** a read-only probe using public
`dockingmt.prepare_ligand()` on this live provider succeeds for the original
mapped BNZ with explicit fixed-state H and Gasteiger–Marsili options. It reports
12 expanded atoms, six added H, six retained prepared aromatic carbon types A,
unchanged old coordinates and a consistent consumer charge audit. This is a
local source observation; the consumer's former expected-failure guard and
published source pin still need its owner's update. No consumer repository was
edited, no Vina score was computed, and provisional typing/export/receptor
readiness remain separate acceptance conditions under uibcdf/dockingmt#41,
#223 and #298.
