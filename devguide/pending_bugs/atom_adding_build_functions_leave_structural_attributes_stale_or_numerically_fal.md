---
summary: Atom-adding build functions leave structural attributes stale or numerically false.
issue: uibcdf/molsysmt#175
status: open
opened: 2026-08-19
closed:
severity: high
verification: measured
area: [build, attribute, scientific-integrity]
guard:
normative:
blocked_by: []
supersedes: []
---

# Atom-adding build functions maintain only `coordinates`

**Reported:** 2026-08-19, from an audit of the README's code examples. The flagship
example names `1l2y.pdb` and does not run; following the failure led here.
**Status:** open. Measured on all three functions and both insertion routes. Nothing
modified.

## What

The three `molsysmt.build` functions that add atoms grow `coordinates` and leave every
other atom-aligned attribute on the old atom axis. Separately, and worse, they leave the
system-level observables untouched.

```python
import molsysmt as msm
molsys = msm.extract(
    msm.convert(msm.systems['T4 lysozyme L99A']['181l.h5msm'], to_form='molsysmt.MolSys'),
    structure_indices=[0])
molsys = msm.build.add_missing_hydrogens(molsys, pH=7.4, engine='MolSysMT')
# n_atoms 1441 -> 2752, coordinates 2752, b_factor 1441
```

The system is inconsistent from that point on, but nothing says so. It surfaces later
and elsewhere:

```
StructuralInconsistencyError: Atom axis for 'coordinates' has size 305 while
'b_factor' has size 304.
```

raised by `solvate`, which did not cause it.

## How

`molsysmt/build/_native_placers.py` has two atom-insertion routes:

- `append_atoms_to_molsys` (line 146) — used by all three functions;
- `rebuild_molsys_with_new_groups` (line 505) — used additionally by
  `add_missing_terminal_cappings` when it adds whole ACE/NME groups.

The file contains **exactly two** assignments to a structural attribute, lines 255 and
745, and both are `coordinates`. Neither route touches `velocities`, `b_factor`,
`occupancy`, `temperature`, `potential_energy` or `kinetic_energy`.

`molsysmt/native/structures.py` already declares what has to be maintained:

```python
_ATOM_ALIGNED_ATTRIBUTES = ('coordinates', 'velocities', 'b_factor', 'occupancy')
```

and, immediately below, `_SYSTEM_LEVEL_OBSERVABLES` with the comment *"These describe
the system as a whole rather than one atom or one structure. Adding atoms changes the
system they describe, so they cannot survive the operation."*

`Structures.add` (lines ~886-925) honours both: it concatenates every atom-aligned name
along `axis=1`, drops one-sided attributes to `None` while recording them in
`one_sided`, raises under `attribute_policy='strict'`, warns on what it discarded, and
clears the system-level observables when atoms were added. It also handles
`alternate_location` separately, through `_merge_alternate_locations` with an
`atom_offset`.

The placers use none of it. The defect is not a missing decision; it is a second,
poorer implementation of a path that already exists.

## Why

**The energies are the serious half.** `temperature`, `potential_energy` and
`kinetic_energy` have shape `(n_structures,)` and no atom axis, so `_payload_dimensions`
has nothing to compare and cannot catch them. A system that has just gained 1311
hydrogens still reports 123.4 kJ/mol of kinetic energy, and nothing downstream will
contradict it. It serialises to `file:h5msm` and propagates into any analysis built on
it.

The atom-aligned arrays are less severe precisely because they eventually raise. The
energies never do.

**The diagnosis is misdirected.** The invariant breaks in `build` and the exception is
raised in `solvate`, so the report lands on the wrong function.

**The advertised workflow is affected.** `build → solvate → openmm.Simulation` is what
the README presents as the reason to use MolSysMT.

## What is measured and what is assumed

Measured. Each row is one function against a system that actually exercises it, one
structure extracted, `engine='MolSysMT'`:

| function | system | n_atoms | `coordinates` | `b_factor` |
|---|---|---|---|---|
| `add_missing_heavy_atoms` | 1BRS | 5151 → 5229 | 5229 | **5151** |
| `add_missing_terminal_cappings` | 181L | 1441 → 1442 | 1442 | **1441** |
| `add_missing_hydrogens` | 181L | 1441 → 2752 | 2752 | **1441** |

`occupancy` and `velocities` are `None` in those systems, so they are not exercised
there. Injected on 1L2Y they fail together:

```
add_missing_hydrogens: n_atoms 304 -> 305
    coordinates   304 -> 305   maintained
    velocities    304 -> 304   stale
    b_factor      304 -> 304   stale
    occupancy     304 -> 304   stale
```

The system-level observables, same system and operation, against the native path for
contrast:

| attribute | after `add_missing_hydrogens` | after `msm.add()` |
|---|---|---|
| `velocities` | 304 for 305 atoms | 314 for 314 atoms |
| `kinetic_energy` | **123.4 kJ/mol, unchanged** | `None`, with a warning |
| `potential_energy` | **−567.8 kJ/mol, unchanged** | `None`, with a warning |
| `temperature` | **300 K, unchanged** | `None`, with a warning |

`msm.add` emits: *"Structural attributes were discarded during concatenation:
temperature, potential_energy, kinetic_energy."*

Also measured, on the b_factor question below — real `b_factor` distributions in the
shipped systems, one structure each:

| system | n | min | zeros |
|---|---|---|---|
| 181L (crystal) | 1441 | 0.09 | 0 |
| 1TCD (crystal) | 3983 | 0.05 | 0 |
| 1ATP (crystal) | 3070 | 0.01 | 0 |
| 1L2Y (NMR) | 304 | 0.00 | 304 (100%) |

Assumed: nothing load-bearing. Whether `rebuild_molsys_with_new_groups` can delegate to
the native path without restructuring is **not** established — it rebuilds whole groups
and may not fit directly.

## What was refuted

**That the cause was `alternate_location`.** It is not, and it is the one attribute
structurally immune to this. It is stored as a sparse mapping keyed by atom index, one
per structure — `structures.py:75`, *"the series is stored per structure but its content
is keyed by atom index"* — so appending atoms leaves existing keys valid. It is
deliberately outside `_ATOM_ALIGNED_ATTRIBUTES`. The cause is adding atoms, nothing else.

**That `b_factor` for new atoms should be inherited from the parent heavy atom.**
Proposed during this audit on the claim that PDBFixer and OpenMM do so. They do not:
`openmm/app/pdbfile.py:395` hardcodes `1.00  0.00` into the ATOM format string and
carries no B-factor at all. Inheriting fabricates a measurement and makes the array
unable to distinguish measured from constructed, which is what a B-factor exists to say.

**That `NaN` should mark "not measured".** Refuted by the format. wwPDB v3.3 gives
`tempFactor` as `Real(6.2)` in columns 61-66 and states: *"If there are neither isotropic
B values from the depositor, nor anisotropic temperature factors in ANISOU, then the
default value of 0.0 is used for the temperature factor."* Our writer formats with
`f"{float(b):>6.2f}"` (`to_string_pdb_text.py:320`), so a NaN emits `   nan`, which is
not a `Real(6.2)` — the same class of non-conformance as
[`uibcdf/molsysmt#174`](https://github.com/uibcdf/molsysmt/issues/174).

Worth recording because it would have gone unnoticed: NaN survives the round trip
through our PDB writer and reader, through `file:h5msm`, and is accepted by OpenMM,
MDTraj and Biopython — the last even with `PERMISSIVE=0`. Nothing would have failed
loudly. We would simply have been emitting invalid PDB.

**That 0.0 is indistinguishable from a real measurement.** The argument that killed the
0.0 option, and it is false in the data. The three crystal structures never contain a
zero; 1L2Y, an NMR structure with no depositor B-factors, is 100% zeros. The convention
the format specifies is already present in the shipped systems.

**That a value has to be chosen at all.** The whole question dissolves once the native
path is used: one-sided attributes go to `None`, and the wwPDB default of `0.0` is the
*writer's* concern, which `to_string_pdb_text.py:275-284` already handles correctly with
`0.0 if item.structures.b_factor is None`. The two layers already agreed.

## Scope and exclusions

Covers the `engine='MolSysMT'` paths of the three functions and both insertion routes in
`_native_placers.py`.

Not covered:

- Non-native engines. `engine='PDBFixer'` and `engine='OpenMM'` route elsewhere and were
  not measured.
- `alternate_location`, immune for the reason given above.
- `formal_charge` and `partial_charge`, which are topological rather than structural and
  were `None` in every system measured.
- The two README errata found alongside this: block 1 omits
  `add_missing_terminal_cappings` and fails on the very file it names; block 3 writes
  `box_shape='truncated_octahedral'` where the accepted spelling is
  `'truncated octahedral'`. Separate work, no issue filed yet.
- Whether any release gate should execute the README examples. None does today.

## Acceptance criteria

- All three functions, on both routes, leave every name in `_ATOM_ALIGNED_ATTRIBUTES`
  either correctly sized for the new atom count or `None`.
- `_SYSTEM_LEVEL_OBSERVABLES` are cleared whenever atoms are added, as `Structures.add`
  already does.
- The discard is reported the way the native path reports it, rather than silently.
- `attribute_policy` is reachable, so a caller can demand failure instead of loss.
- A guard test that adds atoms with all six attributes populated and asserts the
  post-conditions, for each of the three functions. It must cover the energies, which no
  dimension check can catch.
- The README flow `convert → add_missing_* → solvate → openmm.Simulation` runs on a
  shipped system.

## Dependencies and risks

Clearing `b_factor` on a build step is a visible behaviour change for anyone colouring
by B-factor after adding hydrogens. It is the correct behaviour and matches `msm.add`,
but it should be in the release notes rather than discovered.

The `strict` policy raising where code currently succeeds silently is the same trade
`Structures.add` already made.

## Provenance

Linux 7.0.0-28-generic, Python 3.13.14, NumPy 2.4.6, pandas 2.3.3,
PyUnitWizard 0.22.0, MolSysMT `0.21.0+325.g7cedab74a` at `a9aa5f883`, 2026-08-19.
Systems from `molsysmt.systems`; wwPDB v3.3 ATOM record consulted at
<https://www.wwpdb.org/documentation/file-format-content/format33/sect9.html>.
