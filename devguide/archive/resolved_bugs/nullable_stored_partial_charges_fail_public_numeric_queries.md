---
summary: Nullable stored partial charges fail public numeric queries
issue: uibcdf/molsysmt#662
status: resolved
opened: 2026-11-08
closed: 2026-11-08
severity: medium
verification: reproduced
area: [form, attribute]
guard: tests/form/molsysmt_MolecularMechanics/test_nullable_charge_queries.py
normative:
blocked_by: []
supersedes: []
---

# Nullable stored charges fail numeric queries

**Reported:** 2026-11-08, by the first bounded #256 storage benchmark.
**Status:** Resolved in qualified source `990474db0`; direct fix `3830a1aeb`.

## What

`msm.get(mechanics, element='atom', partial_charge=True)` raises
`TypeError: float() argument must be a string or a real number, not 'NAType'`
for a column such as `pd.array([0.25, pd.NA, -0.25], dtype='Float64')`.
Selecting only indices `[2, 0, 2]` also fails. Public native MolecularMechanics,
MolSys and H5MSM 0.6 queries use the same failing getter.

## How

The native adapter first obtains an object-backed array and applies
`np.asarray(..., dtype=np.float64)` to the entire column. Pandas NA is not
accepted by that conversion. Selection occurs afterward. The correction uses
the stored Series' explicit numeric conversion with `na_value=np.nan`, after
positional selection, and requests an independent output array.

## Why

H5MSM preserves admitted nullable columns, but its public query route cannot
consume these values. The issue affects stored partial-charge retrieval, not
charge calculation, storage fidelity or the validity of a scientific assignment.

## What is measured and what is assumed

The first new benchmark pilot passes ten guards and fails its campaign at the
charge query; writing, full read, mechanical-layer read and scalar query are
already reached. An independent unchanged-getter run of
`python -m pytest --receptor=llm -n0 tests/form/molsysmt_MolecularMechanics/test_nullable_charge_queries.py`
passes six controls and fails five with the same TypeError. Original attempts
remain separate. No timing outcome is accepted from this failed campaign.

## What was refuted

The persisted dtype and missing markers are retained correctly: the benchmark's
full/layer comparisons pass before the getter fails. This is not a file codec,
ArgDigest or unit-policy defect. Replacing missing charges with zero would invent
scientific values and is not an acceptable correction.

## Scope and exclusions

Preserve detached float64 arrays in elementary-charge magnitudes, order,
repetitions, empty selected arrays and canonical NaN for mixed missing entries.
An absent or entirely missing charge column retains its existing None contract.
Native storage, nullable dtypes and named evidence remain unchanged. No new
charge model, chemical repair or representation change is introduced; NaN is
not an assigned or scientifically usable charge.

## Acceptance criteria

The public guards pass for native and file forms, Float32/Float64 extension
columns and object columns with NA/None/NaN. Queries cannot mutate the source.
The original benchmark completes, and relevant query/preparation/file tests and
documentation gates pass. The source and exact evidence are delivered before
closure; independent client qualification stays outside this local defect.

## Provenance

2026-11-08, shared Linux x86-64 development host, Python 3.14, executable source
`e06a0788d053f985282549b1fc2019998f3d446a` plus the new guards/benchmark only.
Both original process trees use one CPU and a 2 GiB cgroup without swap, monitor
the shared reserve, and end without a resource interruption. Exact dependency,
source and measured resource identities belong in the final receiving record.


## Resolution

Clean `990474db05f09b853cc470d9e9f14e3b37d0af82` passes 1,869 affected
cases without skips/failures/errors, including the eleven new public missing-value
controls, eleven benchmark guards and the getter doctest. Fourteen fast gates
and fresh HTML pass. Four inspected pages and the exact benchmark download agree;
all fourteen course code cells, execution counts and saved outputs are unchanged.
The six existing HTML warnings and 760 pytest warnings in six groups match the
prior baseline; no warning-clean or optional-ABI qualification is claimed.

[Exact receiving evidence](../../../devtools/data/mechanics_storage_and_nullable_receiving_256_662_20261108.json)
retains the first failed benchmark, unchanged-getter failures, an intermediate
test's unsupported convenience-method assumption, corrected selection and final
clean identities. The full test process tree peaks at 1,758,154,752 bytes;
HTML at 1,347,592,192 bytes. Final checks preserve over 13.9 GB decimal host
availability without pressure/OOM/reserve interruption. No Rust, dependency,
scientific model, schema or public signature changes.

The resumed three-case storage study completes independently on clean
`b7269b77e`. Its synthetic reports do not certify scientific charges; measured
performance does not accept DockingMT's reference workflow, installed packages,
platform gates, or stable H5MSM. Those remain #256/#334. Correcting this incidental
defect adds no weight to the original milestone scorecard.
