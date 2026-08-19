---
summary: An unparameterised residue surfaces as a bare KeyError naming only the residue code.
issue: uibcdf/molsysmt#179
status: resolved
opened: 2026-08-19
closed: 2026-08-19
severity: low
verification: measured
area: [build, diagnostics]
guard: tests/physchem/test_unknown_group_in_table.py
normative:
blocked_by: []
supersedes: []
---

# A missing residue template escapes as a raw dictionary lookup

**Reported:** 2026-08-19, while auditing the README examples for
[`uibcdf/molsysmt#176`](https://github.com/uibcdf/molsysmt/issues/176).
**Status:** resolved. The raising line was located and the attribution in this report corrected.

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

**Not where this report first placed it.** The reproduction above attributes the failure
to `add_missing_heavy_atoms`, because that was the first step of the six-step chain in
which it was originally seen. Run alone, that step succeeds. The failure comes from the
last one:

```
molsysmt/build/solvate.py:653
  -> molsysmt/physchem/get_charge.py:110
     -> molsysmt/physchem/groups/_lookup.py:45
KeyError: 'HED'
```

`solvate` asks for the system charge to compute counter-ions, and the charge table has
no entry for the ligand. Nothing in `build`'s residue-template machinery is involved —
`get_group_db` guards its own lookup and raises a catalog error already. The one
unguarded path was in `physchem`.

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

## Resolution

`group_table_value` now raises `UnknownGroupInTableError`, a catalog error naming the
residue, the table, the function that could not proceed, and the remedy. It takes
`table` and `caller`, passed from all ten call sites across the eight `physchem`
getters.

**The raising itself is unchanged, deliberately.** The module docstring states the
intent — dummy residues resolve to neutral and *"genuine unknown residues still raise so
real gaps are not masked"* — and reading a missing parameter as a neutral value would be
much worse than an unhelpful message. Only the diagnostic changed.

Before:

```
KeyError: 'HED'
```

After:

```
Residue 'HED' has no entry in the charge table, so 'molsysmt.physchem.get_charge'
cannot evaluate it. Ligands, crystallisation additives and non-standard residues are
not parameterised. Remove them from the selection, or supply the value yourself.
Docs: ... | Issues: ...
```

Verified through the path that produced the original report: 181L with its HED ligand,
through `solvate`.

### What was refuted while fixing it

**That inheriting from `KeyError` would mangle the message.** Claimed while
implementing, and false. `KeyError.__str__` does wrap its argument in quotes, but
`CatalogException` defines its own `__str__`, so the outcome depends on base order.
With the catalog base first, the class is both a `KeyError` — which
`tests/physchem/dummy_residues/test_dummy_residue_tolerance.py` relies on — and
readable.

That test is also why the compatibility check that preceded the claim was wrong: it
grepped for `except KeyError` and missed `pytest.raises(KeyError)`. The base order is
load-bearing and easy to lose, so both halves are asserted in the guard rather than left
to a comment.
