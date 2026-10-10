---
summary: Complete legacy bridge and native-probe temporary-resource lifecycles.
issue: uibcdf/molsysmt#374
status: open
opened: 2026-10-10
closed:
verification: inspected
area: [form, performance]
guard:
normative:
blocked_by: []
supersedes: []
---

# Legacy temporary-resource lifecycle exceptions

**Reported:** 2026-10-10, owner review in uibcdf/molsysmt#371.
**Status:** Post-1.0 maintenance, with an explicit bounded interim procedure.

## What

Complete failure/lifetime cleanup in legacy optional file bridges, generated
file-returning outputs before successful return, and the standalone temporal
native-library benchmark. Successful returned files are caller results and must
remain available. This adds no molecular capability or scientific method.

## How

Source inspection of `70d1400b9514904fbf9b1a5ca126ddf4591e63dc` identifies:

- `molsysmt/form/openmm_Simulation/to_pdbfixer_PDBFixer.py`: intermediate PDB
  removal occurs only after both conversions complete.
- `molsysmt/build/get_missing_bonds.py`, optional pytraj branch: its intermediate
  PDB is not retired after eager topology conversion.
- File-returning writers/downloads using generated paths: define failure custody
  before the path is returned, preserving successful result ownership and caller
  destinations. Inspect partial-write/download behavior before changing it.
- `devtools/scripts/benchmark_interactions_temporal.py::rust_query`: temporary
  directory and loaded-library lifetime rely on the returned resource tuple and
  finalization, without a surrounding explicit preparation/query failure scope.

Prefer existing managed contexts and owner-local lifecycle operations. Respect
actual eager reader and loaded-library lifetimes; do not invent a generic
cleanup abstraction or delete returned results.

## Why

These independently owned operations need their remaining lifecycle debt visible.
The reproduced current memmap/LEaP defects are repaired under uibcdf/molsysmt#372
and uibcdf/molsysmt#373. This follow-up concerns legacy optional/research routes
outside the selected pre-1.0 qualification scope; source inspection is not a
scientific regression or executed platform-leak claim. Shared policy ownership
remains uibcdf/molsyssuite#104.

## Bounded implementation exception

- **Owners:** dprada/LMMV.
- **Review:** 2026-10-24, or before the next affected invocation.
- **Reason:** provider/reader/native lifetimes and failure output semantics need
  independent guards; the standalone probe is research tooling, not the runtime.
- **Interim:** select an exclusive process scratch root through TMPDIR before
  interpreter startup. Retain it through error inspection; retire it after
  children, readers and loaded libraries end. Use explicit output filenames
  when file-creation failure must be recoverable.
- **Removal condition:** execute success, preparation/conversion/start/query failure,
  caller-custody and visible-retirement-error guards for the actual owning routes.
  Loaded DLL lifetime requires relevant platform evidence before a Windows claim.

## What is measured and what is assumed

The listed source was inspected. No optional engine, native compilation or
all-platform failure reproduction executes for this follow-up. No historical
resource deletion or complete-compliance claim is made.

## What was refuted

Successful files located under a temporary root are not automatically disposable.
Managed Python finalization is not the same evidence as explicit success/failure
retirement of a still-loaded native library. Linux unlink behavior is insufficient
for Windows lifetime guarantees.

## Scope and acceptance criteria

Close only after the explicit owners establish the listed lifetimes and outcome
semantics without changing scientific criteria or deleting caller results. Preserve
public validation, form/unit behavior and dependency direction. No heavyweight
universal matrix, blanket disk cleanup or release rebuilding is required merely
to register this debt. See [the owner contract](../temporary_resource_operations.md).
