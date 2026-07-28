# MolSysMT 1.0 Rust-Only Cut Artifact

**Date:** 2026-07-28
**Status:** complete

## Decision

MolSysMT 1.0 has one supported numerical-kernel implementation: the private
Rust extension distributed as `molsysmt._rust`.

The bounded Numba coexistence period ended only after the exact final oracle
campaign was preserved in `release_1_0_final_numba_oracle_artifact.md`.
Historical oracle manifests remain evidence; they are not active runtime or
CI inputs.

## Removed surfaces

- CPU backend selection and the private dual-dispatch fallback;
- 108 CPU JIT callables and their compilation/cache infrastructure;
- 52 CUDA JIT callables and 13 CUDA-coupled modules;
- the experimental Taichi kernel modules that did not form a complete backend;
- Numba from Python, Conda, development, test, documentation, and build
  dependencies;
- `warmup_numba`, JIT diagnostics, signature construction, and the temporary
  `--molsysmt-kernel` pytest option;
- two-backend parity tests whose migration purpose is complete.

## Preserved surfaces

- `molsysmt.core` and `molsysmt.lib` remain low-level compatibility facades for
  MolSysSuite consumers, now backed by Rust;
- the independent MIC/neighbour/SASA scientific battery remains active;
- final oracle and documented-divergence JSON artifacts remain available for
  historical audit;
- public GPU-related arguments remain accepted but cannot select an
  unsupported backend.

## GPU boundary

MolSysMT 1.0 does not advertise GPU acceleration. Automatic requests use Rust
CPU. An explicit `use_gpu=True` request emits `GpuNotAvailableWarning` and
falls back to the same CPU path.

GPU redesign is post-1.0 work. It must be based on the Rust architecture and
define operation coverage, device support, precision, transfers, residency,
errors, fallback, installed artifacts, and scientific validation before being
advertised.

## Executable zero gate

The maintained command is:

```bash
python devtools/scripts/audit_numba_surface.py --require-zero
```

It fails if runtime imports, CPU/CUDA JIT sites, runtime controls,
dependencies, tests, or direct consumers reintroduce Numba or llvmlite.
Historical documentation and frozen evidence are intentionally allowed.

## Native parallel-control follow-up

The subsequent Rayon-control vertical closed the independent API gap. Session
defaults and per-function `parallel`/`num_threads` overrides now resolve to
reusable, size-specific Rayon pools. The implementation preserves sequential
inner loops for LLVM auto-vectorization and has explicit serial, multi-pool,
nested-override, numerical-parity, and release-build scaling evidence.

## Validation

- zero-Numba executable gate: pass;
- focused compatibility, diagnostics, low-level math, neighbour, and
  independent MIC/SASA battery: 122 passed;
- broad `lib`, PBC, structure, physchem, Rust, GPU-fallback, diagnostics, and
  audit surface: 450 passed;
- one network-dependent `5XJH` neighbour test was excluded after independently
  failing only because the environment could not resolve the download host.

Normal pytest outcomes remained authoritative; pytest-receptor reported the
same exit codes and counts.
