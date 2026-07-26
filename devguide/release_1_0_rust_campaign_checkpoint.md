# Rust-Forced Release Campaign Checkpoint

**Date:** 2026-07-26

**MolSysMT commit:** `48127120499469c28501df2100f44e5a18de683e`

**Status:** B4 evidence collected; B4 not closed because the exact-commit suite
is not green

## Purpose

This checkpoint tests the intended Rust runtime without validating the complete
Numba application runtime that will be deleted before 1.0. It answers three
separate questions:

1. does a Rust wheel built from the exact MolSysMT commit load and execute;
2. does the bounded Numba-to-Rust oracle surface and independent scientific
   evidence pass;
3. does the complete application suite pass with Rust forced.

The answer to the first two is yes. The third is no because the clean committed
snapshot exposes pre-existing, backend-independent WIP failures. The identical
failing node IDs were rerun with Numba to classify that result; a second full
Numba suite was deliberately not run.

## Exact Source and Binary Identity

The source was reconstructed without the dirty working tree:

```bash
git archive --format=tar \
  --output=/tmp/molsysmt-b4-481271204.tar \
  48127120499469c28501df2100f44e5a18de683e
```

Source archive SHA-256:

```text
dd8f54824f2b264e2986683412136844ab28990b50a86df71c37379d723be0f6
```

The Rust wheel was compiled from the crate inside that archive:

```bash
python -m maturin build --release \
  --manifest-path \
  /tmp/molsysmt-b4-481271204/experiments/rust_kernels/Cargo.toml \
  --out /tmp/molsysmt-b4-wheelhouse
```

Produced wheel:

```text
msm_rust_kernels-0.1.0-cp311-abi3-manylinux_2_39_x86_64.whl
```

Wheel SHA-256:

```text
96910b18798b9ab55a3372e78407716286ef1ef079cceac0491b03665c8a43ba
```

Installed extension SHA-256:

```text
df71dc855373cb5cebd53f6fd63439b57cf93890eaa2039162f58493421f9e34
```

The campaign used a temporary `--system-site-packages` virtual environment. The
Python import resolved to the clean source snapshot and the Rust import resolved
to the exact wheel installed inside that virtual environment.

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
| maturin | 1.14.1 |
| cargo | 1.97.1 |
| rustc | 1.97.1 |

Normal pytest remained the result authority. `pytest-receptor` only rendered
the pytest result.

## Results

### Forced-Rust smoke

```text
PASS: 15 passed
```

The smoke included topology, PBC, RMSD, component, and xdist backend-forcing
checks.

### Bounded final oracle surface

```bash
python -m pytest --receptor=llm \
  --molsysmt-kernel=rust tests/rust
```

Result:

```text
PASS: 264 passed, 3 skipped
```

The three skips are the deliberate direct-parity exclusions for the incorrect
Numba triclinic minimum-image result. The Rust property tests for the corrected
behavior pass.

### Independent scientific evidence

The selected PBC, structure, topology, external MDAnalysis/MDTraj, and curated
pentalanine evidence passed:

```text
PASS: 82 passed
```

### Complete forced-Rust suite

```bash
python -m pytest --receptor=llm -n 12 --dist loadfile \
  --molsysmt-kernel=rust
```

Result:

```text
FAIL exit=1
9744 collected
9361 passed
36 failed
342 errors
5 skipped
167 warnings in 47 groups
11 root causes
418.90 seconds
```

The dominant root cause accounts for all 342 setup errors:
`pyunitwizard.NotImplementedFormError` for a Python `list` while collecting
generated `string:pdb_text` topological-attribute cases.

The remaining root causes cover committed-snapshot debt in:

- SMILES-to-amino-acid conversion used by peptide building;
- list-based PyUnitWizard conversion in build helpers;
- missing `structure_index` delivery from `MolSys`;
- the network-dependent `2LAO` conversion doctest;
- structure metadata extraction;
- ambiguous multi-state H5MSM attribute access;
- NGLView attribute expectations and hydrogen-bond rendering.

None of the reported frames terminate in a Rust kernel or the Rust dispatcher.

### Bounded Numba diagnosis

Only the 378 unsuccessful Rust node IDs were rerun:

```bash
python -m pytest --receptor=llm -n 12 --dist loadfile \
  --last-failed --molsysmt-kernel=numba
```

Result:

```text
FAIL exit=1
36 failed
342 errors
11 root causes
74.06 seconds
```

Every node ID that failed under forced Rust also failed under forced Numba.
The counts and root-cause groups are identical. This demonstrates that the
current red suite is not a Rust migration regression. It does not turn a red
release snapshot into a green one.

## Conclusions

1. The CPU Rust implementation is substantially more mature than the release
   packaging state: its mapped oracle and scientific evidence are green.
2. No missing CPU Rust kernel or Rust-specific regression was demonstrated.
3. A complete second Numba application-suite run would add cost without useful
   evidence. The bounded failing-node rerun already separated backend behavior
   from snapshot debt.
4. B4 cannot close until the active WIP required by the current tests is landed
   in reviewable commits and the exact-commit forced-Rust suite is green.
5. B5 cannot create the final oracle artifact from this checkpoint; this record
   must be superseded, not rewritten, by the later green campaign.

## Packaging Finding Promoted to Segment C

The local build produced a `manylinux_2_39_x86_64` wheel. The older packaging
note claimed a `manylinux_2_34` result, and the intended release needs a
deliberately selected portable manylinux baseline rather than the host glibc
version. This does not affect the same-host B4 scientific result, but it is an
explicit C3 portability item and must be solved by the production wheel build
container.

## Required Next Step

Land and audit the current uncommitted production/test WIP without absorbing
unrelated proposals. Then reconstruct a new exact commit, rebuild its Rust
wheel, and rerun:

1. the forced-Rust smoke;
2. the bounded oracle and scientific evidence;
3. the complete forced-Rust suite.

Only the final step needs repeating at full-suite cost. Numba remains limited
to the bounded oracle or to failing-node diagnosis if a new backend attribution
question appears.
