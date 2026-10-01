---
summary: RDKit conversion loses bracket-declared hydrogen counts
issue: uibcdf/molsysmt#272
status: resolved
opened: 2026-10-01
closed: 2026-10-01
severity: high
verification: reproduced
area: [form, convert, attribute, tests]
guard: tests/form/rdkit_Mol/test_declared_hydrogen_round_trip.py::test_bracket_hydrogen_counts_survive_native_and_h5msm_round_trip
normative:
blocked_by: []
supersedes: []
---

# RDKit conversion loses bracket-declared hydrogen counts

**Reported:** 2026-10-01, while reproducing ProLIF cation-pi resonance matching.
**Status:** Resolved with native, dictionary and H5MSM round-trip guards.

## What

`RDKit -> MolSys -> RDKit` drops RDKit atom-level explicit hydrogen annotations,
which are not separate hydrogen atoms. Guanidinium loses its charged nitrogen's
`[NH2+]` count, changing NX3 resonance recognition from three atoms to one. A pyrrole
`[nH]` can no longer sanitize correctly. Atom count alone does not reveal this loss.

```python
from rdkit import Chem
import molsysmt as msm
source = Chem.MolFromSmiles('NC(=[NH2+])N')
native = msm.convert(source, to_form='molsysmt.MolSys')
restored = msm.convert(native, to_form='rdkit.Mol')
print(Chem.MolToSmiles(source), Chem.MolToSmiles(restored))
# Before fix: NC(N)=[NH2+]  [N+]=C(N)N
```

## How

The RDKit adapter stores `GetNumImplicitHs()` and `GetNoImplicit()`, but not
`GetNumExplicitHs()`. The reverse adapter never calls `SetNumExplicitHs()`.
Add nullable UInt8 `n_explicit_hydrogens` in ChemicalStates, the attribute/get/set
routes, conversion-loss reporting and typed H5MSM tables. Capture/restore the exact
count without adding atom indices or conflating it with real bonded hydrogen atoms.
Update graph delivery through NetworkX using the existing registered field routes.

## Why

This changes molecular chemistry and attributed interaction detection after conversion
or persistence. It blocks faithful form-agnostic ProLIF output (uibcdf/molsysmt#270).
Declared hydrogen annotations belong in ChemicalStates, not an interaction-local cache.

## What is measured and what is assumed

Reproduced on local Python 3.13/RDKit: source guanidinium's charged atom reports
explicit hydrogen count 2 and total degree 3; before fix the restored count was 0,
its total degree 1, and ProLIF's cation SMARTS returned one rather than three atoms.
No atomic coordinates or atom-order change is required for the fix.

## What was refuted

Changing `n_implicit_hydrogens` to include bracket hydrogens would conflate two existing
chemical concepts. Adding real H atoms would change the source atom axis. Relaxing
ProLIF's NX3 pattern would change the original method. A feature-local workaround
would leave the general converter and H5MSM wrong.

## Scope and acceptance criteria

Preserve annotations for guanidinium, pyrrole and ammonium through native/dictionary/
H5MSM and back to RDKit. Preserve implicit counts and unchanged atom membership.
Real explicit H atoms remain normal indexed atoms and have no bracket count at their
parent after RDKit AddHs. Missing legacy counts remain unknown in native storage;
this addition does not reconstruct missing historical chemistry.

## Dependencies and risks

H5MSM 0.5's chemical layer adds an optional registered column with its nullable wire
encoding. Current readers accept older files without it; older implementations that
reject unknown columns cannot read a new file containing it. This is recorded within
the still-experimental pre-1.0 schema rather than hidden in interaction metadata.

## Resolution — 2026-10-01

Implemented `n_explicit_hydrogens` capture, typed storage, public get/set and
RDKit restoration. Guanidinium retains its three original resonance matches;
pyrrole and ammonium preserve canonical SMILES, implicit/declared counts and
atom axes. Real AddHs atoms remain indexed atoms with zero parent bracket counts.
The focused checkpoint including both interaction detectors, chemical conversion
and persistence passed 322 tests; the named guard supplies three molecular cases.
No missing historical hydrogen assignments are reconstructed.
