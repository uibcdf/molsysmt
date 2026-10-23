---
summary: Native SDF stereo verification rejects inferred non-CIP atom tags
issue: uibcdf/molsysmt#436
status: resolved
opened: 2026-10-23
closed: 2026-10-23
severity: medium
verification: reproduced
area: [form, convert]
guard: tests/form/file_sdf/test_stereochemistry.py
normative:
blocked_by: []
supersedes: []
---

# Distinguishing declared stereo from inferred non-CIP readback tags

**Reported:** 2026-10-23 by DockingMT through the original 1IEP SDF example.
**Status:** Resolved for the explicit supported profile; consumer receiving remains separate.

## What

The explicit RDKit writer rejects an admitted 1IEP molecular graph even though
its requested atom and bond CIP inventories are absent. The preexisting output
is protected. The native encoder remains a separately selected supported route;
there is no silent fallback or proven chemical corruption.

Input: `tests/form/data/vina_examples/1iep_ligand.sdf`, SHA-256
`051b8742c32adc05c07fb486a4e7c9327f84e131cee33ac4e6a568d07553eb38`.
It is the unmodified Vina example also supplied by the consumer. Reproduce:

```python
native = msm.convert(source, to_form='molsysmt.MolSys',
                     stereo_engine='rdkit', discard_properties=True)
msm.convert(native, to_form=output, ctfile_version='V3000', stereo_engine='rdkit')
```

## How

`write_stereo_sdf` rereads the generated MolBlock without sanitization, assigns
accurate CIP labels and compares canonical isomeric SMILES. The rereader infers
3D tetrahedral tags at atom indices 27, 29, 30, 31, 32, 33, 34 and 36. None
receives a CIP descriptor; the expected constructed molecule has no such tags.
Raw isomeric SMILES therefore differ even though the observed atom-field
mismatch is confined to these inferred tags.

RDKit exposes `RemoveNonExplicit3DChirality` specifically for tags inferred from
3D coordinates rather than explicit wedge/CFG evidence. Its source is in
`Code/GraphMol/Chirality.cpp`, with its Python contract in
`Code/GraphMol/Wrap/MolOps.cpp`. A diagnostic copy using that operation matches
the expected isomeric SMILES for this fixture. This observation alone is not a
safe general fix: declared and genuine CIP stereochemistry must stay protected.

## Why

A receiving client cannot use the explicitly selected writer on an admitted
real input. Determine whether preservation is possible without changing source
graph, H inventory, valence policy, coordinates or declared stereo. Never catch
and retry with a different writer, clear declared labels or disable verification.

## Evidence and proposed qualification

Reproduced locally on Linux/Python 3.14.7 and RDKit 2025.09.5; the consumer also
reports RDKit 2026.03.1. Local execution does not qualify that newer environment.
This input has 69 atoms, 73 bonds and charge +1, and is independently compared
in the existing Vina corpus guards. The source and expected output bytes must
remain unchanged on failures.

Verify stereo inventories explicitly before normalizing only transient readback
information for comparison. Retain the isomeric graph check, including isotope,
H, charge and bond information. Positive cases cover V2000/V3000, original
1IEP, 1S63 and both 5X72 configurations. Negative controls must still detect true
CIP inversion/loss, changed chemical graph or isotope/H inventory, and output
corruption before destination writes. No scientific repair or normalization of
the input chemical state belongs in this fix.

## Resolution — 2026-10-23

The writer verifies accurate atom and bond CIP inventories on the same axes,
then compares the isomeric graph using private verification copies. RDKit's
public RemoveNonExplicit3DChirality removes only nonexplicit 3D marks on those
copies; every accurate-CIP-tagged center is protected/restored for the isomeric
check, even when its tag originated from geometry. Explicit wedge/CFG marks
are untouched. Neither encoded text nor source molecules are normalized or
repaired. The existing graph comparison still catches isotope and H changes.

All four original ligand cases now qualify V2000/V3000 against independent
RDKit graph/CIP reads. 1IEP additionally preserves its atom-31 NoImplicit and
zero virtual-H declarations. Deliberate CIP inversion/removal, isotope and
H-inventory changes fail before replacing the destination. Running the original
helper from 3c43a9554 in a disposable interpreter reproduces the 1IEP refusal in
both formats and preserves the preexisting bytes; the new guards protect that
specific failure without disabling verification.

The executed stereo-encoding branch contributes Hanson 2018 and original
producer software versions through optional Ackredit. A shared private credit
factory is also used by the public CIP tool; its result schema is unchanged.
Real-provider and absence controls pass. The verification normalization is a
MolSysMT preservation check using RDKit's public utility, not a new scientific
stereochemistry-assignment algorithm.

The combined SDF/PDBQT, CIP/template-stereo, correspondence attribution,
Ackredit and conversion-execution selection passes 827 tests in 54.01 seconds
with 12 workers and pytest-receptor. The public doctest passes. Fourteen fast
gates pass, and the affected documentation compiles. Warnings and source hashes
are retained in [the receipt](../../devtools/data/sdf_stereo_verification_20261023.json).
Course module 01 prose is updated; its executable code is unchanged. This is
source qualification on RDKit 2025.09.5, not a rerun of the consumer's 2026.03.1
installation or release admission.
