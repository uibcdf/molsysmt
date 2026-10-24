---
summary: H5MSM copy without a destination attempts to overwrite its source.
issue: uibcdf/molsysmt#450
status: resolved
opened: 2026-10-24
closed: 2026-10-24
severity: medium
verification: reproduced
area: [basic, form]
guard: tests/basic/test_file_copy.py
normative: devguide/session_file_copies.md
blocked_by: []
supersedes: []
---

# H5MSM copy without a destination attempts to overwrite its source

**Reported:** 2026-10-24 while executing the PCA lessons for uibcdf/molsysmt#448
and uibcdf/molsysmt#449. The maintainer authorizes correction of this separate bug.
**Initial status:** active; source-copy contract and adapter validation.

## What

`msm.copy(path)` for a valid H5MSM 0.5 raises `shutil.SameFileError`. A synthetic
three-atom MolSys written to H5MSM reproduces the failure. A source SHA-256 before
and after the exception is identical. Explicit distinct destinations work and
retain the exact file bytes. `align_principal_axes` on a disk-backed composite
reaches the same missing-destination path through its internal `copy()`.

## How

`form/file_h5msm/copy.py` replaces a missing output filename with the input,
then invokes `shutil.copy`. Several raw-file adapters repeat this implementation.
Other recent adapters (FASTA, PIR, SMI, SDF) already require an explicit destination.
The generic copy dispatcher does not preflight file destinations or reject one
filename for a composite source; low-level filesystem/type errors leak out.

## Why

A copy must be independent. Returning the source path would create an alias;
creating an implicit temporary file would need a lifetime/cleanup contract and
could duplicate a large on-disk dataset without a user-chosen destination.
Loading a file as MolSys silently would change form and RAM cost. File copying
must remain a byte-preserving operation, including legacy format versions,
compression, chemical states, interactions and uninterpreted stored data.

## Accepted contract — 2026-10-24

The maintainer chooses automatic process-session temporaries in the platform's
system-temporary directory. Without a destination, file copying retains the
source form and returns an independent ordinary path string. With a destination,
it creates a persistent caller-owned file. The explicit-destination-only option
was considered but would require callers of `copy()` inside general operations
to invent filenames or change forms and RAM costs. It was never published.

The private session filesystem owner reserves paths securely, retains ownership
independently of path reference counts, and attempts cleanup at normal interpreter
exit. Only registered automatic files are removed, never caller-provided paths;
an explicit persistent file inside the workspace also survives. The directory
is removed only when empty. Failed automatic copies retire their own reservation.
Forked children reset inherited ownership and locks without deleting parent files.
Concurrent allocations receive distinct paths. Abrupt termination and locked
files may leave leftovers. The temporary directory is selected by Python's platform
rules rather than a hardcoded `/tmp`; existing TMPDIR/TEMP/TMP choices apply.

Raw copies keep file bytes, format version, compression, units and stored domains.
Automatic reservations retain private writable permissions even for read-only
sources. Explicit copies retain the existing mode-copy/overwrite behavior. Source
aliases (including symlinks/hard links) and directory destinations reject before
writing. SDF/PDBQT keep their envelope/profile checks inside the same ownership
context. Composite inputs without a destination copy their members individually;
a single explicit filename for a composite is rejected. Resident protocols are
unchanged. Copying does not add missing write capabilities to file adapters.
Live file handlers retain their separate resource contracts.

## Acceptance and initial guards

Guard public and direct adapter routes, byte equality and independent file
identity, original-file preservation, temporary lifetime through garbage
collection, normal-exit cleanup and persistent-file survival. Check source aliases,
directory arguments, rollback on copy/validation failure, parallel reservations,
fork ownership and unchanged native copying. Prove H5MSM 0.4/0.5 copies retain
stored domains without conversion or migration. The broader coordinate-transform
API is not redesigned by this correction.

The initial session suite passes **52 tests in 8.00 seconds** on Linux/Python 3.14,
using pytest-receptor and 12 workers. It includes actual interpreter-exit and fork
subprocesses. The earlier explicit-only draft's regression results are not used
as final qualification. Final regression/documentation/hosted evidence is added
at closure. No release or installed-package qualification is implied.


## Final source qualification — 2026-10-24

The native/filesystem regression passes **421 tests** with pytest-receptor and
12 workers on Linux/Python 3.14. It includes all new copy/ownership guards,
existing native-copy boundaries, H5MSM extraction and SDF/PDBQT contracts. All
filesystem primitives, symlinks and fork scenarios in this local scope execute;
there are no skips. Windows-specific locked-file deletion is not claimed as
qualified by the Linux subprocess tests. The portable implementation uses Python's
filesystem APIs and host-platform PathLike normalization; it no longer assumes
that an output path is a PosixPath.

The 33 warnings remain visible: 24 legacy H5MSM reads, six MDAnalysis mass-guesser
pending-deprecation warnings, two existing structure-attribute-drop warnings and
one optional-provider NumPy ABI warning. None becomes a test success by omission.

The public copy doctest and automatic/persistent/native-edit Cookbook example
pass. The Toolbox copy notebook and Common Core module 10 pass fresh Jupyter
execution. Ruff lint/format, dependency checks and the fourteen fast gates pass.
The HTML documentation builds with existing warnings tracked by uibcdf/molsysmt#144.
The normative contract lives in [session file copies](../../session_file_copies.md);
the final publication commit and exact-source hosted checks are recorded when the
issue closes. No tag, release or installed-artifact qualification is implied.

Reproduce the bounded regression with:

```bash
python -m pytest tests/basic/test_copy.py tests/basic/test_file_copy.py tests/basic/test_file_copy_lifecycle.py tests/form/test_raw_file_copy.py tests/form/file_h5msm/test_extract.py tests/form/file_sdf/test_native_contract.py tests/form/file_pdbqt/test_native_contract.py tests/native/test_molsys_copy.py tests/native/test_structure_copy.py tests/native/test_remaining_copy.py tests/native/test_copy_boundaries.py --receptor=llm -n 12
```
