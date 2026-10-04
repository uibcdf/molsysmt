# Preserving nonproduction development experiments

This normative maintenance rule is established by uibcdf/molsysmt#317. Release
tags follow the adopted [MolSysSuite guide](../MOLSYSSUITE_GUIDE.md); a
development experiment does not receive a tag pretending to be a release.

## Archive contract

Before retiring a development branch whose evidence must survive, preserve its
Git objects in an incremental Git bundle under
[`devtools/data/development_archives/`](../devtools/data/development_archives/).
Store a JSON manifest beside it with schema version, bundle filename, SHA-256,
exact source commit, required main-history prerequisite, purpose and owning
issue. An existing annotated marker must retain its original tag object and
ref **inside the bundle**, without adding it to the live tag namespace.

The prerequisite commit must remain an ancestor of `main`. The bundle retains
the experiment's source and annotation; it is neither a production merge nor
a release artifact. A manifest or commit hash alone is insufficient evidence
because unreachable Git objects can be garbage-collected. Preserve dated
integration receipts unchanged and record the replacement separately.

Run the restoration check before publishing the archive:

```bash
python devtools/scripts/validate_development_archives.py
```

The check verifies the payload checksum, original annotated ref, target commit,
prerequisite and readable experiment objects. It restores into temporary bare
Git storage using the current repository only for prerequisite history. Every
experiment-specific object must exist in the restored local pack, so source
objects cannot hide an incomplete archive. It modifies no source refs.

## Rust C1 spike

The [manifest](../devtools/data/development_archives/rust_c1_spike_20261002.json)
is the authoritative identity and checksum record. Its bundle preserves the
unmerged experiment previously identified by
`archive/rust-c1-spike-20261002`, including the exact annotation. This replacement
fulfils the archival promise in uibcdf/molsysmt#252; the original dated merge
receipt remains historical evidence.

To inspect the source, use an isolated clone with main history. Run these
commands **inside that clone**, supplying the archive path from a current main
checkout:

```bash
git bundle verify /path/to/main/devtools/data/development_archives/rust_c1_spike_20261002.bundle
git fetch /path/to/main/devtools/data/development_archives/rust_c1_spike_20261002.bundle refs/tags/archive/rust-c1-spike-20261002:refs/tags/archive/rust-c1-spike-20261002
git show archive/rust-c1-spike-20261002
git show archive/rust-c1-spike-20261002:devguide/pending_proposals/rust_packaging_backend_design.md
```

Do not push the restored development marker back to the component repository.
The spike demonstrates a historical packaging approach and is explicitly not
the production Rust backend.

## Published references

Published historical release tags are immutable under MolSysSuite policy.
This procedure does not authorize their deletion or rewriting. Correcting a
mistaken development marker introduced after policy adoption requires
maintainer review of its exact ref, proof that it has no GitHub Release, and a
published, verified replacement archive before retiring the marker. No gate
waiver, fake release version or expansion of the historical allowlist is used.

The regression guard
`devtools/tests/test_development_archives.py::test_rust_spike_archive_replaces_nonrelease_tag`
requires both successful restoration and absence of the rejected live tag.
The hosted MolSysSuite conformance job checks published refs; archive tests
alone do not certify that remote state.
