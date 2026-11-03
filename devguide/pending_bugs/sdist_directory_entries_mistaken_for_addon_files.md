---
summary: Source archive validation mistakes addon directories for unreviewed files.
issue: uibcdf/molsysmt#537
status: active
opened: 2026-11-03
closed:
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
**Status:** independently reproduced on main; proposed correction reviewed in
PR #538, with integration and final receiving pending.

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

## Proposed correction and receiving

PR #538 commit 3c13ba1a5c248de11622ff015b24551f72c59846 preserves TarInfo
objects, retains all entries for structural/cache checks and uses the
non-directory inventory for required-source, addon-file and Rust-source checks.
Four contribution regressions cover directory entries with both spellings,
continued rejection of unreviewed files and directories that cannot substitute
for required files. The core correction is separate from that PR's supported
report wrappers, although one test names its new required `_supported.py` file.

Receive the patch against current main, preserving every existing guard and the
exact tools inventory. Re-run its positive/negative archive controls and the
unchanged real archive. PR #538's remaining full checks and failed performance
audit (#539) remain visible; neither an inspected patch nor an earlier source
smoke certifies the integrated current tree. No merge or main runtime change is
made by this review.

## Scope and exclusions

This is the source archive validator, not #533's installed extension/export
boundary. No native algorithm, format version, package floor, tag or artifact
publication is introduced. Closure requires the integrated correction, a live
pytest guard and its source-distribution receiving evidence.

## Combined candidate receiving — 2026-11-03

The isolated integration candidate based on main 402bdc6e4 retains both PRs and
all newer native/CI guards. Source merge 0bdb4f55ec031597ea44ac07bceb20800ad35863
builds actual archive `molsysmt-0.23.0+389.g0bdb4f55e.tar.gz`: 59,029,845 bytes,
SHA-256 `70522f0d1203c4a7bc5b649e4d30c1fcaedeace3e63f524d00e0ca7308b892bb`.
The corrected validator accepts it. The old classifier from main 402bdc6e4,
using the same candidate file inventory, rejects this identical archive solely
for its four ordinary addon directories. No producer output or allowlist is
weakened to obtain acceptance. Temporary comparison code is removed automatically;
the archive and raw receiving logs remain in the ignored integration cache.

Combined receiving passes 3,362 cases without skips/failures, including the
complete 2,662-case addon invocation and live distribution/inventory guards;
538 documentation controls and 14 fast gates also pass. Native alias collisions
retain their strict error, and the six attribute cold-process tests separately
pass while enforcing the actual parent's Viewer source path. The
[combined receipt](../../devtools/data/molsysviewer_tools_combined_receiving_20261103.json)
retains hashes, warnings, backend reuse and scope limits.

The patch is still on `dev/review-tools-537-540`, not main. Keep #537 open until
the combined candidate's applicable hosted source/native-distribution checks
complete and its correction is integrated. The original PR failure is historical;
#539's independent source-route correction is already on main. This source-archive
receipt is not a wheel install, installed-pair or release qualification.
