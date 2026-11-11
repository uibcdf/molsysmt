---
summary: Selective interaction queries reject supported modular H5MSM roots
issue: uibcdf/molsysmt#709
status: resolved
opened: 2026-11-11
closed: 2026-11-11
severity: medium
verification: reproduced
area: [form, data]
guard: tests/interactions/test_hdf5_query.py
normative:
blocked_by: []
supersedes: []
---

# Selective interaction queries reject supported modular H5MSM roots

## What

The private selective interaction reader rejects a named analysis written by
current default public H5MSM writers with `ValueError: Expected an H5MSM 0.5 file.`
The complete source session on `01c6266f6` reproduces 25 failures at that check.
Run `python -m pytest --receptor=llm tests/interactions/test_bounded_hdf5_writer.py`.

## How

`HDF5InteractionsReader.__init__` in `interactions/_hdf5_query.py` hard-codes
root 0.5 before validating the named collection and interaction payload. The
current default is 1.0; all three implemented modular roots share the relevant
versioned interaction codec. The reusable root validator already lives in
`_private/h5msm_storage/modular.py`.

## Why

Bounded-writer, original-software and execution-provenance receiving cannot
query the files they just wrote. This is a consumer compatibility omission,
not evidence of incorrect detector geometry or corrupted scientific results.

## What is measured and what is assumed

The full suite has 49 failures, 33,748 passes and 16 skips across 33,813 cases.
Only the 25 root-check failures are attributed to this issue. Other causes keep
separate ownership under #710 and #334/#256. The input and native hashes remain
unchanged during the session. No installed or platform claim follows.

## What was refuted

Pinning all current-writer tests to 0.5 would hide the incompatibility. Accepting
arbitrary future root versions or bypassing collection/payload validation would
weaken the existing reader. Loading a complete MolSys is unnecessary for one
independent analysis and would violate the selective-read intent.

## Scope and acceptance

Reuse explicit central root validation for implemented 0.5, 0.6 and 1.0 roots.
Retain named collection and codec checks, occurrence identity, coverage, maps,
units and bounded reads. Guard default/explicit supported roots, unknown/malformed
roots and unrelated-layer nonmaterialization. This remains a private reader;
no new public file-backed API or format-stability decision is introduced.

## Provenance

2026-11-11, local Linux/Python 3.14.7; MolSysMT `01c6266f6`, native ABI3 SHA-256
`4ffb82e4250a1862fff17dbe7725fb8f0770d613ffef2648370389a66983d345`,
PyUnitWizard 0.29.2, ArgDigest 0.15.0, DepDigest 0.15.1, SMonitor 0.21.0 and
Pytest Receptor 1.2.1. Three workers, 6-GiB cap, no own swap; minimum host
available memory about 8.96 GiB. Full-session receipt belongs to #334.

## Resolution — 2026-11-11

Implementation: `245c8730b`.

The private reader now delegates supported root/type/metadata validation to the
central modular H5MSM validator, preserving collection/payload validation and
close-on-error. The new cases compare selected nonconsecutive structures and
atom filters against resident results for default 1.0 and explicit 0.5/0.6/1.0.
A dataset-read guard rejects unrelated coordinate/mechanics materialization;
unknown or malformed roots reject and the actual HDF5 handle is closed.

The relevant 449-case receiving passes with no omissions, including the 25
originally failing root-check cases. The primary guard protects both accepted
and rejected roots and scientific result parity, rather than merely matching
one version string. No public file-backed API, scientific detector change or
format-freeze decision follows.

The [polishing receipt](../../../devtools/data/pre_1_0_polishing_receiving_334_20261111.json)
retains original failures, the first focused eight-failure attempt, input/native
identities, resource limits and documentation receiving. The original complete
suite remains failed until a new full corrected-source session succeeds. This
bounded closeout is not installed, graphical, platform or candidate acceptance.
