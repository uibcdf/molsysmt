---
summary: An unparameterised residue surfaces as a bare KeyError naming only the residue code.
issue: uibcdf/molsysmt#179
status: open
opened: 2026-08-19
closed:
severity: low
verification: reproduced
area: [build, diagnostics]
guard:
normative:
blocked_by: []
supersedes: []
---

# A missing residue template escapes as a raw dictionary lookup

**Reported:** 2026-08-19, while auditing the README examples for
[`uibcdf/molsysmt#176`](https://github.com/uibcdf/molsysmt/issues/176).
**Status:** open. Reproduced; the raising line was not located.

## What

A residue with no entry in the template database aborts the build with a bare
`KeyError` carrying only the three-letter code.

```python
import molsysmt as msm
mol = msm.convert(msm.systems['T4 lysozyme L99A']['181l.pdb'], to_form='molsysmt.MolSys')
mol = msm.remove(mol, selection='molecule_type in ["water","ion"]')
mol = msm.build.add_missing_heavy_atoms(mol, engine='MolSysMT')
```

```
KeyError: 'HED'
```

`HED` is beta-mercaptoethanol, a crystallisation additive present in 181L.

## How

Not located. The message carries no traceback context worth quoting and the code is
reached through the template lookup in the native placer path. `verification:
reproduced` rather than `inspected` records that honestly.

## Why

Every other failure in this area arrives through the smonitor catalog with a caller, a
hint and a docs link. This one escapes as a raw dictionary lookup, so it reads as an
internal defect rather than as a decision the caller has to make about their system.

The remedy — remove the ligand, or parameterise it — is not discoverable from the
message. Neither is the residue's index, nor which function failed.

It cost real time during the #176 audit: a bare `KeyError` gives nothing to search for,
and the first hypothesis was that the build functions were broken rather than that the
system contained something they do not know.

Severity is `low` because it fails loudly and stops. It is a diagnostics defect, not a
correctness one.

## Scope and exclusions

Covers `engine='MolSysMT'` in the build functions that consult the residue template
database. Any structure carrying a ligand, additive or non-standard residue — which is
most crystal structures.

Excluded: adding templates for ligands. This is about the message, not the coverage.

## Acceptance criteria

- The failure names the residue, its index, the function, and what the caller can do.
- It arrives through the catalog, like the neighbouring failures.
- A guard asserting the message rather than only the exception type.

## Provenance

Linux 7.0.0-28-generic, Python 3.13.14, MolSysMT at `d77786517`, 2026-08-19. System
`T4 lysozyme L99A` (`181l.pdb`) from `molsysmt.systems`.
