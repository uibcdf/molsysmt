---
summary: H5MSM subset extraction without an output path overwrites its source
issue: uibcdf/molsysmt#235
status: open
opened: 2026-09-22
closed:
severity: high
verification: reproduced
area: [form, extract, data]
guard:
normative:
blocked_by: []
supersedes: []
---

# H5MSM subset extraction without an output path overwrites its source

**Reported:** 2026-09-22, while investigating the local 181L fixture incident
tracked in uibcdf/molsysmt#216.
**Status:** Open. The current public extraction path can replace a caller's
source file without an output filename.

## What

`msm.extract()` on a `file:h5msm` subset silently writes the result to the
input path when `output_filename` is omitted. On a temporary copy of the
bundled 181L fixture, the following call reduced 1,441 atoms to zero and left
one empty coordinate frame:

```python
msm.extract(temporary_181l_h5msm, selection='atom_index<0')
```

The returned path was the input path. A separate temporary copy subjected to
`selection='atom_index==0'` was likewise replaced, with one atom remaining.

## How

`molsysmt/form/file_h5msm/extract.py` defaults `output_filename` to `item`.
For H5MSM 0.4 subset extraction, it materializes the selected native `MolSys`,
closes the input handler, and calls `to_file_h5msm()` with that same path.
`molsysmt/native/h5msm_file_handler.py` opens the path with
`h5py.File(filename, 'w')`, replacing the previous bytes before writing the
selected system. The same path existed in commit `284038cfc`, which predates
the 181L incident.

## Why

The public extraction operation describes a new molecular system. A caller
can therefore lose a bundled fixture or an arbitrary source H5MSM through an
ordinary subset selection. An empty result remains a syntactically valid H5MSM
file, so a later reader may not distinguish it from an intentionally empty
system. The demo-asset validator catches the bundled 181L case, but does not
protect arbitrary user files.

## What is measured and what is assumed

**Measured:** On Python 3.13.14 and h5py 3.16.0, a temporary copy of the
1,441-atom 181L fixture became a 42,128-byte H5MSM with zero atoms, zero
bonds and coordinates of shape `(1, 0, 3)`. Every one of its 51 HDF5 objects
matched the preserved empty incident file in path, shape, data and attributes
other than creation and modification times. A one-atom selection also
overwrote its temporary source file. The copy was prepared from the intact
tracked 181L asset; the repository fixture was not used as an output path.

**Assumed:** The exact command that caused the historical 181L rewrite is
unknown. Direct serialization of an empty native `MolSys` yields the same
HDF5 contents, so the artifact cannot identify which API call produced it.

## What was refuted

**Only empty selections can damage the source:** false. A one-atom subset
also replaced its input file in the reproduction.

**The file must be malformed to reveal the overwrite:** false. The empty
result is a valid H5MSM file that the form reader opens successfully.

## Scope and exclusions

Constrain `file:h5msm` subset extraction when no distinct output path is
provided. Review any explicit same-path output semantics in that adapter.
The restored local fixture and the inability to attribute its historical
caller remain documented under uibcdf/molsysmt#216.

## Acceptance criteria

1. Empty and nonempty subset extraction without an explicit output filename
   preserves the input file's bytes.
2. Any supported explicit in-place operation has a clear request and safe
   write behavior; unsupported same-path output fails before opening the file
   in write mode.
3. An addressable pytest guard exercises the public `msm.extract()` path on a
   temporary H5MSM copy and checks source preservation and output semantics.

## Dependencies and risks

Changing the default destination may affect callers that relied on implicit
replacement. Check those callers and document the chosen output contract.
The demo-asset validator is a useful release gate but cannot protect every
user-owned file from this API behavior.

## Provenance

Reproduced 2026-09-22 on host nauta with Python 3.13.14 and h5py 3.16.0,
using the intact `181l.h5msm` from `origin/main` as the read-only source for
temporary copies. The code path was also inspected at commit `284038cfc`.
