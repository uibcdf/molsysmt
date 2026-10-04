---
summary: Retain a declared prohibition of implicit H after RDKit sanitation of aromatic NH.
issue: uibcdf/molsysmt#320
status: resolved
opened: 2026-10-04
closed: 2026-10-04
severity: high
verification: measured
area: [form, convert]
guard: tests/form/molsysmt_MolSys/test_to_rdkit_Mol.py::test_declared_no_implicit_hydrogen_policy_survives_aromatic_nh_sanitization
normative:
blocked_by: []
supersedes: []
---

# RDKit sanitation loses a declared implicit-hydrogen prohibition on aromatic NH

**Reported:** 2026-10-04, while preparing the observed 1QKU peptide under
uibcdf/molsysmt#298 for uibcdf/pharmacophoremt#22.
**Status:** Resolved with a guarded native-to-RDKit conversion fix.

## What

Public conversion of explicitly prepared HID, HIE and TRP references produced
aromatic NH atoms with RDKit GetNoImplicit()==False despite the native declaration
allows_implicit_hydrogens=False. The strict fixed-state H operation then correctly
rejected those molecules, including HIS550 in the bounded receptor fragment.

```python
import molsysmt as msm
molsys = msm.physchem.get_peptide_chemical_template(
    ['HIE'], 'ammonium', 'carboxylate')['template']
rdmol = msm.convert(molsys, to_form='rdkit.Mol')
assert all(atom.GetNoImplicit() for atom in rdmol.GetAtoms())
```

The assertion failed before the fix. It now holds while the original explicit H
counts and zero implicit H counts remain unchanged.

## How

The converter set the permission before Chem.SanitizeMol(). RDKit's aromatic NH
Kekule conversion clears explicit H and calls setNoImplicit(false); subsequent
sanitation recovers the count but not the caller's prohibition. The primary source
is Code/GraphMol/Kekulize.cpp around line 787, inspected at RDKit commit
cbfb37abddcd5b5feeac97d53530ae6be83cac0d.

After sanitation, the converter restores each explicitly prohibited permission
only if the resulting implicit H count is zero. Otherwise it raises the existing
conversion diagnostic rather than erasing inferred H. Charges, aromaticity,
stored H counts and fixed-state preflight remain intact.

## Why

Prepared aromatic NH groups occur in amino-acid residues and ligands. Losing a
stored chemical constraint in the general converter blocks consumers whose
fixed-state contract requires exactly the declared chemistry. This is a converter
fault, not evidence that HIE/TRP need a different protonation state.

## What is measured and what is assumed

Before the fix, all three HID/HIE/TRP cases failed (3 failed, 8 deselected).
The converter tests and declared-state roundtrip controls then passed (15 passed).
The completed affected chemistry gate passed 234 tests, including peptide factory,
template application/completion, aromatic normalization, the real receptor
fragment, fixed-state H and native/RDKit metadata contracts, plus two public
function doctests. Its seven warnings comprise three pandas FutureWarnings,
one legacy H5MSM warning and three deliberate structural-attribute loss warnings.

```bash
env PYTHONPATH=/tmp/molsysmt-readiness-argdigest-013 python -m pytest --receptor=llm \
  tests/physchem/test_normalize_aromatic_bond_orders.py \
  tests/physchem/test_chemical_template_receptor.py \
  tests/physchem/test_chemical_template.py \
  tests/physchem/test_chemical_template_connectivity.py \
  tests/physchem/test_get_peptide_chemical_template.py \
  tests/form/molsysmt_MolSys/test_to_rdkit_Mol.py \
  tests/build/add_missing_hydrogens/test_fixed_state.py \
  tests/form/rdkit_Mol/test_chemical_metadata.py tests/form/rdkit_Mol/test_contract.py \
  --doctest-modules molsysmt/physchem/normalize_aromatic_bond_orders.py \
  molsysmt/physchem/get_peptide_chemical_template.py
```

The temporary PYTHONPATH selected released ArgDigest 0.13.0 without modifying the
sibling editable checkout. Normal supported environments need no such override.
The run took 61.38 s; this is a validation duration, not a performance benchmark.

## What was refuted

HIE/TRP did not require guessed H counts or a relaxed chemical preflight. Their
original count survived sanitation. Restoring the independent permission at the
converter boundary permits the existing strict checks to work.

## Scope and exclusions

This retains explicit prohibitions in the returned converted molecule. A later
external RDKit sanitation can reinterpret that molecule again. Unknown or allowed
permissions are not changed; forbidden inferred H still fail. This does not add
hydrogens, choose protonation, certify aromaticity or validate receptor biology.

## Resolution

The guard constructs independent HID/HIE/TRP references through the public API
and checks GetNoImplicit(), original explicit H counts and zero implicit H after
public conversion. Removing the post-sanitation restoration makes it fail.
Converter notes and the preparation/H tutorials describe this boundary.

## Provenance

2026-10-04, Linux workstation, Python 3.13.14, RDKit 2025.09.5, ArgDigest 0.13.0,
NumPy 2.4.6, pandas 2.3.3. Routine interpreter migration remains tracked in
uibcdf/molsysmt#237; this is not Python 3.14 release qualification.
