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
**Status:** Active. The baseline is decomposed; controlled LTO and builder experiments
are pending.

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

## What was refuted

- The 19:56 is not a slow upload: publication itself took 10 seconds.
- The build is not keeping four CPU cores busy throughout; fat LTO and serial packaging
  leave substantial parallel capacity unused.
- Merely enabling the action's Boa-based `mambabuild` flag is not an acceptable durable
  solution because Boa has been archived since 2024.

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
