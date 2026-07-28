# Final Numba-to-Rust Oracle Artifact

**Date:** 2026-07-28

**MolSysMT commit:** `6485a0c08a36ec335c4b37554249dcc1e03352be`

**Status:** Segment B complete; B4 and B5 exit gates passed

## Purpose

This is the dated final CPU Numba-to-Rust migration artifact required before
the production Rust packaging and Rust-only cut. It supersedes, without
rewriting, the red campaign recorded in
[Rust-Forced Release Campaign Checkpoint](release_1_0_rust_campaign_checkpoint.md).

The campaign answers three distinct questions:

1. can the Rust extension be rebuilt from an identified clean MolSysMT commit;
2. does the bounded two-backend oracle and independent scientific evidence
   pass;
3. does the complete MolSysMT application suite pass with Rust forced.

All three answers are yes.

## Exact Source and Binary Identity

The source was reconstructed from Git rather than copied from the dirty
working tree:

```bash
git archive --format=tar \
  --output=/tmp/molsysmt-b4-6485a0c08.tar \
  6485a0c08a36ec335c4b37554249dcc1e03352be
```

Source archive SHA-256:

```text
6bcaf5dc923e4780fec338151495a84e80b884451d4d0942b129606e43aaecc4
```

The migration crate was built from that archive:

```bash
python -m maturin build --release \
  --manifest-path \
  /tmp/molsysmt-b4-6485a0c08/experiments/rust_kernels/Cargo.toml \
  --out /tmp/molsysmt-b4-wheelhouse-6485a0c08
```

Produced wheel:

```text
msm_rust_kernels-0.1.0-cp311-abi3-manylinux_2_39_x86_64.whl
```

Wheel SHA-256:

```text
14a2c0a42ae51ca95150d8360a105370c61dc5a5ed208f89c1f8ed19d368c5b2
```

Installed extension SHA-256:

```text
df71dc855373cb5cebd53f6fd63439b57cf93890eaa2039162f58493421f9e34
```

The campaign used a temporary `--system-site-packages` virtual environment.
Python resolved `molsysmt` from the clean source archive and
`msm_rust_kernels` from the wheel installed inside that environment.

The `manylinux_2_39` tag is same-host campaign evidence only. It is not
production portability evidence and does not satisfy Segment C.

## Environment

| Component | Value |
| --- | --- |
| Python | 3.13.12 |
| platform | Linux 6.17.0-35 x86_64, glibc 2.39 |
| NumPy | 2.3.5 |
| Numba | 0.64.0 |
| llvmlite | 0.46.0 |
| pytest | 9.0.2 |
| pytest-xdist | 3.8.0 |
| rustc | 1.97.1 |
| cargo | 1.97.1 |
| Ruff | 0.15.5 |

Normal pytest remained the result authority. Pytest-receptor rendered its
result and showed no disagreement. PR-PILOT-013 was independently verified on
the MolSysMT deselection reproducer before this campaign:

```text
PASS exit=0 | 39 passed, 40 deselected
```

## Bounded Two-Backend Oracle

The final bounded oracle surface was run explicitly:

```bash
python -m pytest --receptor=llm \
  --molsysmt-kernel=rust tests/rust
```

Result:

```text
PASS exit=0 | 264 passed, 3 skipped | 19.04s
```

These tests exercise the frozen Numba implementation directly against the
Rust routes. The three skips are the documented cases where the upstream
Numba result is not minimum-image correct; Rust property and independent
scientific tests preserve the accepted corrected behavior.

No complete Numba application-suite run was performed. The testing contract
restricts Numba to this bounded oracle because the release runtime is Rust and
a second full application run would add substantial cost without stronger
migration evidence.

## Combined Migration and Scientific Gate

The forced-backend harness, Rust oracle, complete scientific-truth suite,
peptide-builder regressions, and H5MSM reporter regressions passed together:

```text
PASS exit=0 | 501 passed, 3 skipped | 80.64s
```

This gate includes external, curated, property, and invariant evidence that
does not depend only on agreement with Numba.

## Complete Forced-Rust Application Suite

Command:

```bash
python -m pytest --receptor=llm -n 12 --dist loadfile \
  --molsysmt-kernel=rust
```

Result:

```text
PASS exit=0
9774 effective tests
9769 passed
5 skipped
213 warnings in 50 groups
456.89 seconds
```

The five skips are:

- three deliberate upstream minimum-image exclusions;
- one RDKit-dependent SMILES ambiguity expectation;
- one unavailable-CuPy test.

There were zero failures and zero errors. The 213 warnings were fully listed
by pytest-receptor; none represented an unsuccessful test outcome.

## Closure Decision

Segment B is complete because:

1. every inventoried CPU Numba callable has a Rust or absorbed-helper
   disposition;
2. every CPU consumer has a Rust route;
3. deliberate divergences and tolerances are recorded and independently
   justified;
4. the bounded final two-backend oracle passes;
5. independent scientific evidence passes;
6. the complete application suite passes with Rust forced;
7. source, binary, environment, commands, results, and the exact commit are
   preserved here.

This artifact authorizes Segment C to integrate the accepted private
`molsysmt._rust` packaging design. It does not authorize deleting Numba until
Segments C and D complete their installed-artifact, direct-routing, CUDA, and
zero-Numba gates.
