---
summary: Setuptools build minimum does not establish support for declared license metadata.
issue: uibcdf/molsysmt#541
status: resolved
opened: 2026-11-03
closed: 2026-11-03
severity: medium
verification: reproduced
area: [packaging, deps]
guard: devtools/tests/test_license_build_contract.py
normative:
blocked_by: []
supersedes: []
---

# Qualifying the backend minimum for existing license metadata

**Reported:** DockingMT's packaging review in uibcdf/molsysmt#541, coordinated
through uibcdf/molsyssuite#162.
**Status:** resolved; explicit backend floors are aligned and actual native minimum/current-backend artifacts retain their metadata and notices.

## What and how

Current `pyproject.toml` permits setuptools>=68.0 while declaring a string
SPDX license and license-files. Static source inspection confirms those fields.
The reporter points to Setuptools's PEP 639 support boundary; an exact compatible
patch minimum still needs primary-documentation review and build qualification.
No old-backend failure has been reproduced in this intake, and successful builds
with a newer backend do not certify the declared minimum.

## Why

The declared build contract should cover its actual metadata syntax. This is a
build dependency question, separate from #524's runtime floors. It matters
before the next public source/wheel publication; there is no evidence here that
an existing public artifact is broken or omits its license.

## Proposed work and acceptance

Choose and justify a supported Setuptools minimum, align applicable build inputs
and test actual wheel/sdist metadata plus license inclusion in that minimum
context. Preserve runtime Python support and scientific code. Do not downgrade
the shared development environment to investigate an old backend. Retain exact
context, artifact names/digests and exclusions in the final receiving record.
No license change, release, package replacement or sibling pin update is implied.

## Reviewed source and decision — 2026-11-03

Review basis: 55f18aefd284c422fbf93634c2076fc4de322f92. The source already
declares MIT and `license-files = ["LICENSE"]`; both the project notice and
`molsysmt/interactions/cation_pi/PROLIF_LICENSE.txt` are preserved byte for byte.
The exact hashes are in the [receiving receipt](../../../devtools/data/license_backend_receiving_541_20261103.json).

The [official migration guide](https://setuptools.pypa.io/en/latest/userguide/license_migration.html#requiring-a-compatible-setuptools)
establishes 77.0.0 as the PEP 639 support boundary. The
[77.0.3 release source](https://raw.githubusercontent.com/pypa/setuptools/v77.0.3/NEWS.rst)
records early fixes around license configuration and diagnostics. We select
`setuptools>=77.0.3`, without an upper bound, and align `pyproject.toml`, both
Conda host recipes and all five environments explicitly provisioning it.
Their no-build-isolation routes cannot rely on a newer backend incidentally
installed elsewhere. Runtime Python/provider floors, native and versioning
plugins, license choices and notices are unchanged. This is the owner-specific
qualification requested by uibcdf/molsyssuite#162, not a new suite-wide floor.

## Reproduced negative control

An unpacked exact Setuptools 76.1.0 wheel, outside the shared prefix and ahead
of it only in the subprocess's PYTHONPATH, imports successfully on Python 3.14.7.
Calling its real `setuptools.build_meta.prepare_metadata_for_build_wheel` on
the original source exits 1: `project.license` must use its old file/text table
syntax, so the string MIT is rejected before native compilation. This version
is admitted by the old >=68.0 declaration. We do not claim to have tested exact
68.0, or to have diagnosed a defect in the SPDX expression or an old public file.

## Actual build receiving

The same isolated source worktree, with only the eight floor edits, produces:

- With an unpacked exact Setuptools **77.0.3**: a real sdist, a native wheel
  rebuilt from that sdist, and a native wheel built directly from the worktree.
- With shared-prefix Setuptools **84.0.0**: a real sdist and a native wheel
  rebuilt from it. All wheel Generator fields confirm the intended backend.

Build commands use `python -m build --no-isolation --outdir <directory>` for
sdist/rebuilt-wheel pairs, and `--wheel --no-isolation` for the direct wheel.
The minimum command prepends only the unpacked 77.0.3 wheel to PYTHONPATH.
Existing Rust dependencies are reused offline through the normal Cargo target
cache, with Rust/Cargo 1.97.1 and two build jobs; the actual native crate is
compiled. The source and host prefix are not installed over or downgraded.
Other tools are setuptools-rust 1.13.0, versioningit 3.3.0, packaging 26.3,
wheel 0.48.0 and build 1.6.1. This qualifies the Setuptools minimum with those
plugins, not every plugin's own minimum.

All five artifacts pass the dedicated license checker: Metadata-Version 2.4,
License-Expression MIT, License-File LICENSE, exact project notice bytes and
the exact bundled ProLIF notice. The minimum rebuilt wheel also passes the
existing native wheel-layout validator. Its extracted package and abi3 extension
load from the asserted artifact paths and calculate a 0.3 nm atom distance. That
smoke reuses shared runtime dependencies; it is not a clean installed-pair test.
Artifact names, sizes, SHA-256 values, backend identities and input/notice hashes
are retained in the receipt. The local `.dirty` development artifacts are not
release candidates and are not uploaded.

The complete sdist inventory validator still reproduces **#537**: four ordinary
addon directories are mistaken for files. This known separate defect is not
reported as passing and is not weakened here. The corrected inventory remains
in the unmerged metadata candidate awaiting its required full/native gates.
No claim of overall source-archive release readiness follows from license checks.

## Durable guards and limits

The new focused pytest module checks a PEP-639-capable explicit source floor and
its equality across the eight inputs. Positive/negative archive fixtures check
actual metadata values and bytes, rejecting wrong/missing declarations or project
and third-party notices. A matching filename alone cannot pass. The routine
smoke includes this module; no general scientific suite or universal gate is added.

The reusable developer checker is documented in
[the dependency audit guide](../../dependency_contract_audit.md#build-backend-license-contract).
No public molecular API, course lesson, runtime floor, package identity, source
pin, policy caller, published file or release route changes. Non-Linux platforms,
Conda packages and the eventual exact installed release matrix retain their own
qualification. The shared development environment remains on Setuptools 84.0.0.

## Resolution and owner disposition — 2026-11-03

**Review completed — corrected.** The published closing commit identifies the
reviewed corrected source; the receipt identifies the separate artifact-producing
55f18aefd worktree plus the exact eight floor edits. The MIT expression, project
notice and bundled third-party notice are unchanged. Both Conda host/no-isolation
routes and the source/build/test/docs tool declarations carry the same floor.

Final packaging receiving passes **62 tests**, no failures or skips, 4.06 seconds,
two workers. This includes the new metadata/notice and floor guards, dependency
auditor, both Conda workflow profiles, native-wheel validator and hosted-command
guard. One existing setuptools-rust limited-API deprecation remains visible. The
floor guard also rejects the original unchanged declarations from 55f18aefd; the
actual 76.1.0 metadata rejection is the independent backend reproduction.

The five qualified local artifacts pass final metadata/notice validation. The
shared prefix still imports Setuptools 84.0.0 and the development extension keeps
its original hash. Real-source artifact identities and limitations remain in
the receipt; no release, public-file rebuild or package promotion occurred.
The separate #537 inventory correction and eventual exact installed/platform
release gates remain pending. The owner disposition links back to
uibcdf/molsyssuite#162; it does not close that central adoption effort.

All fourteen fast readiness gates, full-tree Ruff lint/format, dependency-route
audit, devguide validation and generated indexes pass. The host/dependency
parser also rejects a Setuptools pin placed only in an unrelated recipe section
or environment field. Qualification caches remain local under `.pytest_cache`
for inspection; the committed receipt and addressable guards retain the durable
evidence after ordinary cache cleanup.
