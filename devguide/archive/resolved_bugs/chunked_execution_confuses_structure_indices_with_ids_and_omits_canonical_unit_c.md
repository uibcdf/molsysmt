---
summary: Chunked execution confuses structure indices with IDs and omits canonical unit conversion
issue: uibcdf/molsysmt#263
status: resolved
opened: 2026-09-30
closed: 2026-09-30
severity: high
verification: reproduced
area: [structure, units, performance]
guard: tests/heavy/test_chunk_identity.py
normative:
blocked_by: []
supersedes: []
---

# Chunk identity and quantity integrity at reducer boundaries

**Reported:** 2026-09-30, while preparing the ionic detector's shared trajectory execution.
**Status:** Resolved; regression guards and maintained contract updated.

## What

The executor delivered `structure_id` labels under `structure_indices`, and stripped
quantity units without explicitly converting to its documented nm/ps convention.
For a coordinate quantity of 10 angstrom it delivered the bare value 10 instead
of 1 nm. Source labels such as `external-104` became reducer structure indices.
Eager metadata also reported the full source count when only a subset was requested.

```bash
python -m pytest --receptor=llm tests/heavy/test_chunk_identity.py --disable-warnings
```

Before correction, the initial five tests failed: canonical conversion, both
nonconsecutive traversal modes, and both empty-selection modes. The additional
failure cases were introduced after that reproduction.

## How

`ChunkedExecutor._build_chunk` used `puw.get_value` without a target unit and
populated `structure_indices` from `structure_id`. Heavy traversal now derives
indices from the requested source traversal; IDs are a separate optional field.
Both eager and heavy paths distinguish requested and total source cardinality.
Short, excess, misaligned, noninteger, or incorrectly indexed deliveries fail
before result finalization. Empty traversal does not open a trajectory.
Read-only chunk views do not freeze the source arrays.

The public center, RMSD, and distance consumers now explicitly wrap reducer values
with nm. RMSD's reference is also explicitly converted to nm. This is necessary
when changing the boundary to genuinely canonical values; merely correcting the
executor would otherwise introduce an error in nondefault-unit sessions.

## Why

Index provenance is required by sparse interaction results and client queries.
Numerical reduction over incompatible units can produce scientifically incorrect
results despite valid shapes. The shared executor serves public structure analyses,
so this issue is not limited to the future ionic integration.

## What is measured and what is assumed

**Reproduced:** Five failures before correction using the initial test module above.

**Contract-tested:** Source traversal `[4, 1, 4, 0, 3]`, two-frame chunks with a
final partial chunk, unrelated string IDs, empty traversal, and fail-fast delivery.
Canonical quantity checks use angstrom coordinates/boxes and ns times.

**Parity-tested:** Public centers, RMSD, and distances under a nondefault
angstrom/ns session compare heavy and eager values after explicit conversion to nm.
The existing legacy-file structure parity tests remain applicable.

No peak RAM, detector speedup, or whole-pipeline streaming benchmark is claimed.

## What was refuted

- IDs cannot be recovered as positional indices: they can be arbitrary strings.
- Stripping units is not canonical conversion, even if default-session tests pass.
- Correcting the executor alone is insufficient when its consumers mislabel output
  values or supply a reference in session units.
- Iterating a file by blocks does not prove every public preflight call avoids
  materialization, or that the accumulated result is bounded in RAM.

## Scope and exclusions

This defect concerns the shared reducer boundary and its existing numerical
consumers. The same implementation checkpoint adds native projection and a
H5MSM 0.5 structural iterator as prerequisites of `uibcdf/molsysmt#261`:

- native MolSys iteration reads its existing Structures domain;
- the coordinate getter selects before copying;
- executor H5MSM 0.5 dimensions come from metadata;
- the file iterator projects coordinates, box, time, and structure IDs, validates
  stored series metadata, preserves selected atom/frame order, and owns its handle;
- legacy H5MSM 0.4 iteration retains its existing route.

These prerequisites are separately exercised by
`tests/heavy/test_native_modular_sources.py`. The source-copy test observes the
actual copy argument shape; native iteration tests forbid full Structures extraction.
File tests forbid full-domain materialization and reject corrupted schema, shape,
and unit metadata. The projected iterator does not read chemistry or validate
cross-domain associations. It does not yet support other structural attributes.

The ionic detector remains eager. Its sparse accumulator, chemistry preparation,
output budgets, end-to-end streaming, real-system evaluation, and benchmarks remain
under #261. The shared chunk-size heuristic is not a complete RAM bound, and some
public H5MSM 0.5 preflight routes still materialize domains.

## Acceptance criteria

1. Source indices and IDs are unambiguous and independent.
2. Canonical nm/ps conversion holds independently of session policy.
3. Read-only chunks preserve caller ownership and requested traversal order.
4. Empty and invalid traversals have explicit finalization behavior.
5. Existing structure analyses retain heavy/eager quantity parity.
6. Maintained scalability documentation explains the contract and limits.

## Provenance

2026-09-30; Linux 7.0.0-28-generic, x86_64, glibc 2.39; Python 3.13.14;
NumPy 2.4.6; h5py 3.16.0. Base checkout `372f9a4a5` with the local correction.
Tests require the repository's local pytest socket permission.

## Resolution

The guard module checks actual canonical numeric values and source indices,
including unrelated string IDs, repeated/nonconsecutive selections, final partial
blocks, empty sources, and incorrect deliveries. It fails if IDs are substituted
for indices, target units are omitted, or a partial traversal is finalized.
Public-consumer unit parity and projected native/file reads have separate tests.
The maintained boundary and limits are documented in `devguide/SCALABILITY.md`.

Verification commands on the final correction:

```bash
python -m pytest --receptor=llm tests/heavy tests/form/file_h5msm/test_structures_v05_probe.py tests/form/molsysmt_Structures/test_get_structural_attributes_comprehensive.py tests/interactions/ionic tests/structure/test_group_minimum_contacts.py tests/pbc/test_whole_participants.py --disable-warnings
python -m pytest --receptor=llm tests/heavy/test_native_modular_sources.py --disable-warnings
python -m pytest --receptor=llm --doctest-modules molsysmt/structure/get_center.py molsysmt/structure/get_rmsd.py molsysmt/structure/get_distances.py --disable-warnings
python docs/execute_notebooks.py -q -f -n 1 docs/content/user/cookbook/big_data_trajectories.ipynb
```

The combined regression command passed 245 tests in 11.99 s. After adding two
file-handle lifecycle tests, the source module passed 15 tests in 3.63 s; those
two were not part of the 245-test invocation. The doctest command passed its
one collected example in 3.95 s. The cookbook executed successfully (9.2 s,
including kernel startup), using native blocks without retaining them all.
Toolbox and Four Paths updates are narrative-only; their previous code cells
were preserved and were not re-executed in this checkpoint.

Ruff, dependency validation, both API stability guards, developer-guide validation,
course structure validation, and the scientific evidence registry structure check
passed. The latter validates declarations and does not execute scientific tests.
No full-suite or ionic end-to-end benchmark claim is made.
