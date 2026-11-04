---
summary: Source archive validation mistakes addon directories for unreviewed files.
issue: uibcdf/molsysmt#537
status: resolved
opened: 2026-11-03
closed: 2026-11-03
severity: medium
verification: reproduced
area: [packaging, tests]
guard: devtools/tests/test_validate_rust_sdist.py
normative:
blocked_by: []
supersedes: []
---

# Source archive directory entries lose their type

**Reported:** MolSysViewer's supported-report contribution under #421 and PR #538.
**Status:** resolved in the native validator, independently received from
PR #538. The supported/attribute addon contributions retain their separate
integration and exact-candidate qualification requirements.

## What and how

`devtools/scripts/validate_rust_sdist.py` converts every TarInfo entry to a
PurePosixPath before passing names to the exact Viewer-addon file inventory.
Directory type is lost, and path normalization also removes a trailing slash.
Ordinary addon directories are therefore reported as retired/unreviewed files.

On main 639ec85d831482c06ed871509b8dc0a6a6f7f01c, the existing minimal source
archive fixture passes unchanged. Adding only four ordinary TarInfo directory
entries makes it fail, both with and without trailing slashes. The sole error
lists `molsysviewer_molsysmt` and its `_private`, `_private/argument` and
`_private/function` directories. No extra file, cache or retired module is added.
The compact receipt is retained in ignored
`.pytest_cache/stabilization-review-next/537-reproduction.json`.

The reporter also built an actual 59,026,468-byte development archive on
4e1a06ee1; its reported SHA-256 is
`58e05d28c440f48dde845993b5744f9d4f5182b426f4f5e08df5c83af68a6a5a`.
That actual-archive acceptance is contribution evidence, not a new local build
or independently repeated installed qualification in this review.

## Why

The source-distribution gate rejects a normal producer artifact. Relaxing the
exact addon inventory or accepting only selected suffixes would hide real
unreviewed payloads rather than repair file/directory classification.

## Correction and receiving

PR #538 commit 3c13ba1a5c248de11622ff015b24551f72c59846 preserves TarInfo
objects, retains all entries for structural/cache checks and uses the
non-directory inventory for required-source, addon-file and Rust-source checks.
Four contribution regressions cover directory entries with both spellings,
continued rejection of unreviewed files and directories that cannot substitute
for required files. The core correction is separate from that PR's supported
report wrappers, although one test names its new required `_supported.py` file.

The production validator is byte-identical to that PR revision. Its four
regression cases are received alongside #551's cache rejection guard; the
required-addon-file case names existing `tools.py` rather than the not-yet-
admitted `_supported.py`. No supported-report namespace is required to exercise
the file/directory contract, and no package allowlist is widened.

An actual source distribution built locally from main e1facf624 plus the new
guards has 59,061,773 bytes and SHA-256
`c0a0ab9c3975f3249963f5598cc52e7a91ff7f527b9b68a0556a86ded5e9e557`.
The original validator rejects only its four ordinary addon directory entries;
the corrected validator accepts those exact unchanged bytes. This does not
qualify a wheel build, source round trip or installed release closure.

The four new guards fail before the repair (four failures, six passes). Final
packaging/runtime/workflow receiving passes 98 cases without failures or skips,
using published Pytest Receptor 1.2.1 and two workers on Linux/Python 3.14.7.
One existing Setuptools-Rust `py_limited_api` deprecation remains. Ruff lint and
format checks, developer-guide lifecycle checks and all 14 fast gates pass.
The [receiving receipt](../../../devtools/data/sdist_directory_native_receiving_537_20261103.json)
records versions, input hashes, negative controls and exact scope.

The original PR performance failures and old combined installed-workflow failure
remain historical. #539 and #551 have independent native repairs. Neither this
source-validator fix nor the old passing full matrix qualifies the refreshed
combined addon candidate: its applicable gates still need to execute.

## Scope and exclusions

This is the source archive validator, not #533's installed extension/export
boundary. No native algorithm, public API, format version, package floor, tag
or artifact publication changes. Argument, units, engine and attribution
providers are not applicable to this developer-only file inventory correction.
