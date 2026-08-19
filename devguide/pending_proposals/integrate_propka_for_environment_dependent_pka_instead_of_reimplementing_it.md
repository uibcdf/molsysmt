---
summary: Integrate PROPKA for environment-dependent pKa instead of reimplementing it.
issue: uibcdf/molsysmt#177
status: open
opened: 2026-08-19
closed:
verification: measured
area: [build, deps]
guard:
normative:
blocked_by: []
supersedes: []
---

# Depend on PROPKA rather than rebuild it

**Reported:** 2026-08-19, from the question of whether deferring PROPKA-style pKa to
post-1.0 was the best available answer while closing
[`uibcdf/molsysmt#176`](https://github.com/uibcdf/molsysmt/issues/176).
**Status:** open, post-1.0 by decision. Feasibility measured; the design is not settled.

## What

Take PROPKA as a soft dependency and read per-residue pKa from it, instead of writing a
PROPKA-like calculation ourselves. The standing note estimates 2-3 weeks plus validation
for our own implementation. That comparison was never checked against the alternative.

## How

`propka.run.single(filename, optargs=(), stream=None, write_pka=False)` returns a
`MolecularContainer` in memory and accepts a stream, so nothing touches disk. Each
`Group` under `container.conformations[...]` carries:

| attribute | content |
|---|---|
| `pka_value` | the computed pKa |
| `type` | `'COO'`, `'HIS'`, `'CYS'`, `'N+'`, `'C-'` |
| `residue_type` | ASP, GLU, ... |
| `atom.res_num`, `atom.chain_id` | identification |

`get_expected_hydrogens` is already called per group and already receives `pH`, so an
optional per-residue `pka` argument fits its shape without restructuring it.

Whether this surfaces as a new `engine`, an argument, or a public `get_pka` is an API
decision and is deliberately left open here.

## Why

Measured, not assumed:

| | |
|---|---|
| version | 3.5.1 |
| licence | LGPL-2.1 — compatible with our MIT as a dependency, since it is imported rather than vendored |
| runtime dependencies | none |
| conda-forge | **noarch** build, `python >=3.9` |
| platforms | linux-64, osx-64, osx-arm64, win-64 |
| repository | active, last push 2026-07-31, not archived |

PyPI declares Python 3.8-3.12 and its most recent release is January 2024, which reads
as excluding 3.13. It does not: the conda-forge package is noarch and pure Python with
`python >=3.9`, and the repository was touched three weeks before this was written. The
PyPI metadata is stale, not a constraint. This is worth stating because it is what would
otherwise stop the idea at the first check.

Integration also removes the expensive half of validation. There is no need to
demonstrate that our numbers reproduce PROPKA's when they are PROPKA's; what remains is
showing we feed and read it correctly.

## What is measured and what is assumed

Measured: every row of the table above, and the `run.single` and `Group` surfaces, read
from the project's source at `master`.

Not evaluated, and this is where the work is:

- **Mapping PROPKA's `(chain_id, res_num)` back to `group_index`.** We write the
  structure, so we control the identifiers — but `to_string_pdb_text` collapses an
  unnamed chain to `"A"` (`chain_id = "A" if pd.isna(raw_chain_id)`), which is ambiguous
  once there is more than one. Insertion codes and residue-number collisions across
  chains are unexamined.
- **Absence semantics.** PROPKA reports only ionizable groups. A residue that does not
  appear has no pKa rather than an unknown one, and that has to be interpreted, not
  filled in.
- **Ligands.** PROPKA 3.1+ claims protein-ligand support; not assessed.

## What was refuted

**That a native converter to PROPKA's own objects would be better than passing text.**
The idea is sound — PROPKA does have an internal `Atom` / `ConformationContainer` /
`MolecularContainer` representation — but `input.py` exposes no public way to build it
from pre-made objects. `read_molecule_file(filename, mol_container, stream=None)` and
`read_pdb` / `read_mmcif` all take a path or a stream. A converter would therefore rest
on private internals and break on any upstream refactor.

**The honest form of that idea is mmCIF, not native objects.** PROPKA reads `.cif` and
`.mmcif`, which removes the PDB column limits, the four-character atom-name field and
the single-character chain id — that is, most of the mapping risk above. MolSysMT cannot
yet write CIF from `MolSys`, so that route depends on
[`uibcdf/molsysmt#135`](https://github.com/uibcdf/molsysmt/issues/135).

**That integrating is "an order of magnitude" cheaper than reimplementing.** Claimed in
conversation and withdrawn. The direction holds and the validation saving is real, but
the figure was invented; the mapping question above has to be looked at before any
estimate means anything.

## Scope and exclusions

Post-1.0 by decision. Not a 1.0 blocker: the fixed-threshold model is documented as an
approximation in `structure_preparation_pipeline.md` and, since
[`uibcdf/molsysmt#176`](https://github.com/uibcdf/molsysmt/issues/176), in the public
docstring of `add_missing_hydrogens`.

Excluded: replacing the threshold table. This proposal adds a source of pKa; which
source wins, and whether the table stays as the no-dependency default, is a separate
decision.

## Dependencies and risks

The mmCIF route needs `uibcdf/molsysmt#135`. The PDB route needs the chain-id question
resolved and works today otherwise.

Adding a soft dependency for a scientific result raises a question the threshold table
does not: two MolSysMT installations would protonate differently depending on whether
PROPKA is present. Whichever way that is resolved, it must be visible to the caller
rather than silent.

## Provenance

PyPI JSON API, conda-forge Anaconda API, and the GitHub repository `jensengroup/propka`
at `master`, all consulted 2026-08-19.
