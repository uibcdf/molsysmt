---
summary: Installed Rust validation rejects get_vectors missing from the reviewed export manifest.
issue: uibcdf/molsysmt#533
status: active
opened: 2026-11-03
closed:
severity: high
verification: reproduced
area: [packaging, tests]
guard:
normative:
blocked_by: []
supersedes: []
---

# The installed extension and reviewed export inventory disagree

**Reported:** MolSysViewer installed-source receiving under uibcdf/molsysviewer#269.
**Status:** source correction and focused guards implemented; noneditable
installed validation remains pending.

## What

The real Rust module exports 102 public names, including the accepted
`get_vectors` kernel. The reviewed manifest lists 101 and omits that name.
The installed validator correctly rejects the disagreement; it must not filter
the actual module or accept a subset of its exports.

## How

`rust/src/vectors.rs` implements and registers the vector kernel, which is used
by the existing public geometry tool. The manifest under `devtools/data/` was
not updated with that admitted implementation. Its old unit test checked only
the manifest's size and a small subset, so it could not detect the real drift.

The new actual-module guard fails on the original manifest with exactly the
unexpected `get_vectors` export: **one failure / 20 passes**, exit 1, in the
wheel-validator module. Source registration is unchanged by the correction.

## Why

MolSysViewer's installed-source receiving fails before its scientific tests.
Restoring the reviewed provider inventory is an installability correction, not
a new geometry feature or a relaxation of the installed boundary.

## Implementation and acceptance

The reviewed manifest now includes `get_vectors`. A private validator helper
performs the same exact-set comparison as before and is called by the real
installed validator. Tests compare the actual extension to the manifest and
independently remove a known export or add an unreviewed one; both must fail.
The reviewed count and explicit required kernel assertion are updated to 102.

The validator/vector selection passes **55 tests**, exit 0, with two disclosed
existing warnings. An earlier command targeted a nonexistent vector-test folder;
its usage error is retained and does not qualify any tests. The corrected node
is `tests/structure/test_get_vectors.py`.

Before closure, retain real noneditable installed-wheel validation, its file/hash,
actual prefix and extension identity. An editable runtime comparison is a unit
regression, not an installed qualification. Do not change the shared development
installation or claim a release/platform matrix from one local prefix.

## Scope and exclusions

No Rust implementation, scientific definition, public method, runtime dependency
floor, release artifact or consumer workaround changes. The installed guard's
editable/path restrictions and exact export equality remain in force.
Provider #535's alias bootstrap and #534's dependency metadata remain separate.

## Provenance

2026-11-03, existing Linux x86_64 Python 3.14.7 development environment. The
compiled module is reused for focused guards. Local raw/receptor evidence stays
in the ignored `.pytest_cache/stabilization-520-533/` directory. Original
consumer installed failures remain identified by #533; they are not relabeled
as passing source results.
