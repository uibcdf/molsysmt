---
summary: Installed Rust validation rejects get_vectors missing from the reviewed export manifest.
issue: uibcdf/molsysmt#533
status: resolved
opened: 2026-11-03
closed: 2026-11-03
severity: high
verification: reproduced
area: [packaging, tests]
guard: devtools/tests/test_validate_rust_wheel.py
normative:
blocked_by: []
supersedes: []
---

# The installed extension and reviewed export inventory disagree

**Reported:** MolSysViewer installed-source receiving under uibcdf/molsysviewer#269.
**Status:** source correction, focused guards, local noneditable installed
validation and hosted native-source qualification completed.

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

The real noneditable installed-wheel validation, its file/hash, actual prefix
and extension identity are retained below. An editable runtime comparison is a
unit regression, not an installed qualification. The shared development
installation is unchanged; one local prefix does not establish a release or
platform matrix.

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

## Noneditable installed validation (2026-11-03)

Source correction **2797c5425f5735568422325928520ae591c3676a** produced diagnostic
wheel `molsysmt-0.23.0+374.g2797c5425.dirty-cp311-abi3-linux_x86_64.whl`
(61,908,543 bytes), SHA-256
`2a28b2ac39b633431c709cd8be9c52512f050696b8aa41164c400da335b4b5ac`.
All **3,053 tracked Python files** in that wheel match their committed Git blobs;
the only generated Python file is versioningit's `_version.py`. The dirty suffix
is retained honestly; this is an unpublished diagnostic artifact, not a candidate
release identity.

The wheel passes the unchanged static wheel validator and is installed with
`--no-deps --no-index --ignore-installed` into a temporary actual Python prefix
with inherited development dependencies. The main editable development install
is not replaced. From outside the checkout, the ordinary
`validate_installed_rust_extension.py` command succeeds: **102 exact exports**,
minimum-image check **2.5**, no editable direct URL, and the extension physically
inside that prefix. Its binary SHA-256 is
`27c807631306c0c4b97e4beb3f97aacae1071d67df0616116a40cb74dc8aa951`.
The parent environment supplies NumPy 2.4.6; Python is 3.14.7.

The literal installed CLI was used after correcting two local harness commands:
an initial relative script path was invalid from the external working directory,
and Python `-I` removed the script's sibling-module import directory. Neither
changes the validator contract or indicates a packaging defect. Receipts retain
the actual installed distribution, direct URL, prefix, hashes and successful
command. This qualifies the local Linux installed-extension boundary only,
not a clean dependency closure, the Viewer installed matrix or another platform.

## Hosted native-source qualification — 2026-11-03

Source **d8ea626a0ab6dbd976d0e04ad9299019e4ae0a42** retains correction
2797c5425f5735568422325928520ae591c3676a and passes the native test step in
[CI smoke run 41687790382](https://github.com/uibcdf/molsysmt/actions/runs/41687790382),
job 126098035944. The bounded tier includes the actual-extension equality guard
and both missing/unexpected export controls: **4,184 passed / 16 skipped**, exit 0,
419.08 s, 590 warnings. The skips are 14 unavailable Ackredit checks and one
each for unavailable unyt and astropy. The bound-Viewer tier separately passes
**2,449 cases / four Ackredit skips**, exit 0, 353.23 s, 1,539 warnings. Both
tiers use Linux/Python 3.14 with Pandas 3.1.0 and the exact Viewer source
ca7ebea60d530a7a0c65cb4d0ccea7b4288f3352. All six applicable workflows succeed;
GH Run Receptor's final watch agrees with native GitHub state and exits 0.
These optional omissions are not counted as executed scientific evidence.
Its editable source environment is
distinct from the real installed-prefix validation above. No consumer installed
matrix is dispatched or claimed by this provider repair.
