---
summary: Legacy donor digester tests retain obsolete selector and list expectations
issue: uibcdf/molsysmt#552
status: resolved
opened: 2026-11-04
closed: 2026-11-04
severity: medium
verification: reproduced
area: [tests, argdigest]
guard: tests/_private/argdigest/test_hbond_ion_digesters.py
normative:
blocked_by: []
supersedes: []
---

# Legacy donor guards contradict the accepted role contract

**Reported:** exact candidate 4ea80278f7dc1cd2009a9440fcc5786627430950,
source matrix 41755216514. **Status:** reproduced in all eight JUnit reports
and locally; the retained tests and public rejection controls are corrected.

## What

The two generic private-digester tests still require donor selector strings to
pass through, and expect Python lists for numeric tuples/ranges. Both conflict
with the accepted #511 contract: explicit integer donor anchors or intact
(n, 2) donor-H rows, normalized to int64 arrays. Selectors use the detector's
separate selection arguments. Acceptor digestion has its own legacy contract;
this repair does not broaden or restrict it.

## How

Each Linux/macOS arm64 x Python 3.11--3.14 cell has the same two failures:
`test_hbond_acceptor_and_donor_digesters` and
`test_acceptors_and_donors_accept_selection_like_inputs`. The first string
assertion raises the intended ArgumentError before the stale list expectations
are reached. Python 3.14 Linux has 25,104 passes and 102 skips; macOS cells
have 25,103 passes and 103 skips. All cells retain 40 deselected peptide-parity
cases. These distinct outcomes must not be relabelled as passing suites.

The local original selection reproduces two failures and 117 passes, with no
skips, in 26.11 seconds. It includes the public precomputed-donor guards.

## Why

Full-source integration is blocked by obsolete tests despite the numerical
public contract passing its own guards. Re-enabling selector strings in the
normalizer would contradict the explicit contract and merely move failure into
covalent-role resolution. Weakening errors, removing tests, marking xfail or
changing a geometry threshold would not repair the coverage mismatch.

## Accepted contract and correction

The existing #511 archive is read specifically to verify its accepted numeric
input contract, migration scope and earlier receiving selection; it remains
immutable. Both public classic-detector docstrings and the existing public
covalent/role tests independently support the same contract.

The generic tests are retained and assert integer array shape/dtype/values and
intact pair ordering. They require ArgumentError for donor selectors while
retaining acceptor selector controls. Literal selector strings extend the public
invalid-role matrix for both detectors and both donor sides by eight cases.
Production code, chemical membership, coordinates, units and detector thresholds
are unchanged. The two generic modules now join the precomputed-donor module
in the same native hosted smoke invocation, so that coverage is no longer left
only to the full matrix.

## Receiving evidence

The focused selection passes 127 cases without failures, skips or warnings,
27.38 seconds. Wider receiving of every private digester, hydrogen-bond tests,
bound classic detectors and bound site tools passes 1,141 cases without
omissions, 118.09 seconds. Its 15 warnings comprise eleven legacy H5MSM reads
and four deliberate memory-budget controls; these are not new memory failures.
A negative control executes the pre-511 normalizer in an isolated namespace:
it accepts selectors and list outputs, so it violates the retained strict
assertions. No historical source is restored in the worktree. Eight hosted-command/receptor
controls, Ruff lint/format, developer-guide checks and all 14 fast gates pass.

The [receiving receipt](../../../devtools/data/legacy_donor_guard_receiving_552_20261104.json)
records original JUnit hashes/counts, local red/green evidence, unchanged
production inputs, and exact successful native-wheel jobs/artifacts for r2.
The latter are artifact-container digests from GitHub, not registry package
coordinates or the SHA-256 of each contained wheel.

## Scope and acceptance

Focused red/green controls and the wider selection are received. Original
workflow outcomes and the frozen r2 candidate remain unchanged. A separately
identified candidate must execute applicable hosted gates before PR #538/#540
integration. This local test repair does not waive source-matrix or release/
platform qualification. No runtime API, scientific algorithm, unit, provider
boundary, dependency floor, tag or package-publication change is introduced.

## Provenance

Linux x86_64, shared Python 3.14.7, two workers, published Pytest Receptor 1.2.1.
GH Run Receptor 1.4.0 reports the original matrix failure and native-wheel
success; native logs and all eight original JUnit artifacts verify the failure
identity. Raw evidence is under `.pytest_cache/stabilization-537-540/r2-ci/`.
