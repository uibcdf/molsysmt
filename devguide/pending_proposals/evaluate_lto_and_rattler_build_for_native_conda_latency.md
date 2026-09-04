---
summary: Evaluate LTO and Rattler Build for native Conda latency
issue: uibcdf/molsysmt#205
status: active
opened: 2026-09-04
closed:
verification: measured
area: [build, performance, ci]
guard:
normative:
blocked_by: []
supersedes: []
---

# Evaluate LTO and Rattler Build for native Conda latency

**Reported:** 2026-09-04, after the first production ABI3 staging publication.
**Status:** Active. The baseline is decomposed, the first LTO sweep and local Rattler
prototype are complete, and corrected macOS Intel and five-platform Rattler runs are in
progress.

## What

Measure whether Thin LTO or disabled LTO can shorten native extension builds without a
meaningful kernel-performance regression, then measure whether Rattler Build can replace
`conda-build` while preserving the five-platform CEP 20 ABI3 package contract. Neither
experiment changes production until artifact metadata, installed execution, scientific
performance, and release-gate behavior pass.

## How

Use Cargo's `CARGO_PROFILE_RELEASE_LTO` override to build the same source with `true`,
`thin`, `false`, and `off` where useful. Compare cold build time, extension and package
size, exported native surface, Python 3.11--3.13 execution, and representative kernel
benchmarks. The committed `lto = true` remains the control.

Prototype a Rattler Build recipe separately from `devtools/conda-build/meta.yaml` and
teach the experimental workflow, not the production publisher, to invoke it. Compare
the exact extracted metadata and installed runtime contract with the accepted
`conda-build` artifact before considering action or recipe migration.

## Why

Production staging run `33849332945` took 19:56 on `macos-15-intel`, versus 4:34 on
Linux x86-64, 4:12 on Linux ARM64, 8:05 on macOS ARM64, and 10:49 on Windows. The
Intel job determines the wall time of every five-platform publication.

## What is measured and what is assumed

**Measured:** the macOS Intel job spent 17:48 in the composite build/publish step. The
inner `conda build` reported 17:05 total: 6:57.8 building and installing the wheel,
approximately 3:25 packaging 5,528 files, and approximately 6:42 rendering, solving,
and provisioning build environments. Upload took 10 seconds.

**Measured:** the comparable wheel-build phase took 1:17.3 on Linux x86-64, 3:06.3 on
macOS ARM64, and 3:28.7 on Windows. The macOS Intel build used 8:36.9 user CPU time
over 6:57.8 wall time, only about 1.23 user CPU cores on average despite the runner's
four CPUs.

```bash
gh api repos/uibcdf/molsysmt/actions/jobs/100948330713
gh run view 33849332945 --repo uibcdf/molsysmt --job 100948330713 --log
```

**Inspected:** `rust/Cargo.toml` sets `lto = true`, which Cargo defines as fat LTO over
the dependency graph. Cargo documents `thin` as substantially faster while retaining
similar runtime gains, but that upstream characterization is not a MolSysMT result.

**Inspected:** Boa is archived and explicitly superseded by Rattler Build. The action's
existing `mambabuild` switch therefore is not a durable migration target.

**Estimate:** LTO changes can affect at most the 6:58 wheel-build phase. A large further
reduction requires attacking Conda's remaining render, environment, and packaging cost.

## Experimental evidence

The first four macOS Intel runs used the same commit and were dispatched together. All
four artifacts passed the extracted CEP 20 metadata check and loaded the installed Rust
extension under Python 3.11, 3.12, and 3.13. The observed wheel-build durations were:

| Cargo release LTO | Wheel build | Difference from `true` |
| --- | ---: | ---: |
| `true` (fat LTO control) | 6:37.7 | -- |
| `thin` | 4:29.4 | -32.3% |
| `false` (local thin LTO) | 6:12.1 | -6.4% |
| `off` | 7:08.9 | +7.8% |

All packages were 53 MiB at the workflow's rounded resolution. These are single cold
samples on separate hosted runners, so they establish a strong Thin-LTO candidate but
not a final runtime or variance conclusion. Runs `33855381273`, `33855381257`,
`33855381300`, and `33855381334` failed only after the three installed-extension checks:
the supposedly Rust-only benchmark imported the public `molsysmt` package and therefore
required `smonitor`. Commit `100d686e8` added an explicit isolated-installed-extension
mode, verified against a no-dependencies install. Corrected runs `33863114690`,
`33863117348`, `33863120356`, and `33863123319` repeat the measurements and retain the
runtime JSON and package.

Rattler Build 0.72.2 rendered and solved the v1 recipe locally as exactly one
`linux-64` `pyabi3` variant. A cold local build with fat LTO and four compression threads
completed in approximately 2:03, emitted a 54.82 MiB package containing 2,945 files,
and passed the existing artifact validator. The exact package then loaded and executed
the 99-export Rust contract under isolated Python 3.11, 3.12, and 3.13 environments.
Unlike the accepted `conda-build` package, which contained 5,528 files, the Rattler
package did not include generated bytecode. This local timing is not comparable to a
GitHub macOS runner; five-platform run `33863426589` is the controlled portability and
latency trial. The local worktree lacked the ephemeral release tag, so its wheel
distribution metadata retained a development version while the Conda package metadata
used `0.22.0a0`; the workflow creates the tag before building and must be inspected for
exact agreement.

## What was refuted

- The 19:56 is not a slow upload: publication itself took 10 seconds.
- The build is not keeping four CPU cores busy throughout; fat LTO and serial packaging
  leave substantial parallel capacity unused.
- Merely enabling the action's Boa-based `mambabuild` flag is not an acceptable durable
  solution because Boa has been archived since 2024.
- Disabling LTO is not automatically faster: the first `off` sample was slower than fat
  LTO. The candidate justified by current evidence is Thin LTO, not blanket removal.

## Scope and exclusions

This study covers cold native Conda builds, package correctness, and representative
Rust-kernel runtime performance. It does not remove macOS Intel support, purchase larger
runners, weaken the 5 x 3 staging gate, reuse an unverified wheel from another workflow,
or alter the already published MolSysMT 0.22.0 build-2 artifacts.

## Acceptance criteria

- Cold LTO variants are compared on the same source and runner class.
- Each candidate passes the installed ABI3 extension contract on Python 3.11--3.13.
- Representative scientific kernels show no material regression under the chosen LTO.
- The Rattler prototype emits one native artifact with the accepted CEP 20 metadata.
- The Rattler artifact installs and executes with Conda-compatible clients on all five
  native platforms before production migration is considered.
- Measured gains and rejected alternatives are recorded, and production changes have
  regression guards.

## Dependencies and risks

Changing LTO can alter hot-kernel performance even when correctness is unchanged.
Rattler Build uses a different recipe format and package implementation, so a green
build alone cannot establish compatibility with Conda, Anaconda upload, prefix
relocation, or Windows paths.

## Provenance

GitHub-hosted `macos-15-intel`, `macos-15`, `ubuntu-24.04`, and `windows-2025` runners;
MolSysMT candidate `e5820d4794f8ce31a1f64e345c5edf9073ade975`; Rust 1.97.1;
`conda-build` 26.7.1; Rattler Build 0.72.2 documentation; Cargo profile documentation;
2026-09-04.
