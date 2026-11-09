---
summary: Unsigned H5MSM axis maps wrap out-of-range indices to unknown
issue: uibcdf/molsysmt#661
status: resolved
opened: 2026-11-08
closed: 2026-11-08
severity: medium
verification: reproduced
area: [form, data]
guard: tests/form/file_h5msm/test_association_uint64_overflow.py
normative:
blocked_by: []
supersedes: []
---

# Unsigned axis-map overflow becomes an unknown index

## What

The public H5MSM 0.5 layer writer accepts a uint64 atom map containing
18446744073709551615. The shared normalizer casts to signed int64 before
checking bounds: that value wraps to -1 and becomes the supported unknown
marker. An invalid source index must be refused before creating a file.
This is a synthetic invalid-input finding, not a demonstrated corrupted valid
client artifact. The same normalization primitive serves structure/state maps.

## How

`tests/form/file_h5msm/test_association_uint64_overflow.py` supplies an atom
map `[18446744073709551615, 0]` with dtype uint64 to
`msm.h5msm.write_layers`. Two native atom domains each contain two atoms.
The writer accepts and the refusal assertion fails. The negative selection
has one failure and three passes: the other out-of-range boundary (2**63),
a valid unsigned permutation and a signed unknown map behave as expected.
Its source base is `08a225009`, with in-progress #256 changes; the original
cast-before-bounds mechanism is unchanged at that observation point.

The initial command and full source manifests are retained in the private
`mechanics-256-unsigned-negative` receipt/log/JUnit set. It runs under one
CPU and 2 GiB and has no resource interruption.

## Why

Unsigned NumPy indices are accepted integer inputs. Narrowing before validation
must not reinterpret an out-of-range value as meaningful missing data. Correcting
the shared primitive protects the current public writer and the #256 development
format without changing the declared index/unknown semantics.

## Resolution plan and acceptance

- Reject unsigned values above signed-int64 capacity before casting.
- Preserve valid unsigned indices, signed -1 unknown values and endpoint bounds.
- Exercise public file writing and all shared axis kinds, with unchanged inputs
  and no output file after refusal.
- Retain the original failure and run affected 0.5/association regressions.
- Keep first-stable-format/publication gates separate from this correction.

## Implemented correction — 2026-11-08

The shared normalizer checks unsigned signed-64-bit representability before
casting. Twelve public writer guards cover invalid 2**63/2**64-1 values, valid
unsigned permutations and signed unknown maps across atom, structure and
structure-state axes. They check unchanged input and refusal before output.
The integrated 1,229-case selection passes without omissions. Final clean-source
qualification, verified source delivery and issue closeout remain pending.

## Resolution and clean-source qualification — 2026-11-08

Fixed in `b184e9d181513f50580aa8243f13d9f8941acdd7`. The 12 public guards
and the whole affected selection pass: **1,229 cases without omissions**,
**14/14 fast gates**, and fresh HTML with six unchanged baseline warnings.
The [composition receipt](../../devtools/data/mechanics_composition_receiving_256_20261108.json)
retains the original failing atom-map control, all attempts, source/input hashes
and resource observations. Final tests peak at 1,067,900,928 bytes; all final
profiles preserve over 12 GB decimal host availability without resource stops.

The guard fails when a uint64 maximum narrows to the meaningful -1 marker; valid
unsigned permutations and signed unknown maps verify that the intended contract
survives the correction. All three public axis kinds are exercised. No new public
format or valid-client-data-loss claim follows. Public source delivery and issue
closure are separately recorded after qualification.
