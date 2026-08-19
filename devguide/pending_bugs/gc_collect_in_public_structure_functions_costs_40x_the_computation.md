---
summary: gc.collect() in public structure functions costs 40x the computation.
issue: uibcdf/molsysmt#183
status: open
opened: 2026-08-19
closed:
severity: high
verification: measured
area: [structure, performance]
guard:
normative:
blocked_by: []
supersedes: []
---

# Bug: an unconditional `gc.collect()` dominates the public analysis path

**Reported:** 2026-08-19, during an external audit that profiled `structure.get_center`
after finding it two orders of magnitude slower than the Rust kernel it calls.
**Status:** open. Measured on `b9a2098e4`; the call sites have been present since the
memory-hygiene pass and are not gated by size, mode, or configuration.

## What

Every public function in `molsysmt/structure/` and three in `molsysmt/pbc/` ends with an
unconditional full garbage collection. It costs 40 to 58 times the computation it
follows:

```bash
$ python devtools/scripts/gc_collect_cost.py
function                  as shipped   gc disabled   ratio
get_center                  191.8 ms        4.3 ms     44x
get_radius_of_gyration      192.7 ms        4.8 ms     40x
get_principal_axes          166.3 ms        2.9 ms     58x
get_contacts                336.3 ms        7.8 ms     43x
```

The system is 181L: 1441 atoms, one structure. The Rust kernel inside `get_center` runs
in 8 ms; the collection that follows it runs in 190.

A profile attributes the time unambiguously:

```
     ncalls  tottime  cumtime  filename:lineno(function)
        5    0.000    0.982   molsysmt/structure/get_center.py:55(get_center)
        5    0.943    0.943   {built-in method gc.collect}
        5    0.008    0.008   {built-in method molsysmt._rust.get_center}
```

## How

37 call sites across 22 modules, all on the return path:

```bash
$ grep -rn 'gc.collect' molsysmt --include='*.py' | wc -l
37
$ grep -rln 'gc.collect' molsysmt --include='*.py' | wc -l
22
```

`molsysmt/structure/get_center.py:231` is representative — the collection is outside every
branch, after the result is already built:

```python
                del coordinates, length_unit, groups_of_atoms, weights_arr

        center = puw.standardize(center)

        gc.collect()

        return center
```

`molsysmt/structure/get_distances.py:693` places the same call four lines under a comment
explaining that standardisation is skipped *"to save time"*.

The cost is not in MolSysMT's objects. `gc.collect()` walks the entire process heap, so
the price is set by everything the session holds — other libraries, notebook history, a
loaded trajectory — and MolSysMT pays it once per public call regardless. This is why the
ratio is worse for the cheapest functions: the numerator is a constant the caller cannot
influence, and `get_principal_axes`, the fastest kernel measured, has the worst ratio.

## Why

**The performance argument in the public presentation does not survive it.** `README.md`
offers precompiled kernels with "no just-in-time compilation and no warm-up cost on the
first call". Both halves are true and neither reaches the user: the public path costs 40x
the kernel it exists to expose.

**The project's own competitor baseline already recorded the symptom.**
`benchmarks/baselines/competitor_matrix_session.json`, 2026-05-22, MolSysMT 0.18.0:

| benchmark | median |
|---|---:|
| `competitor_center_mdtraj` | 0.0016 s |
| `competitor_center_molsysmt_jit` | 0.0082 s |
| `competitor_center_molsysmt_public` | 0.2803 s |
| `competitor_rmsd_mdtraj` | 0.0003 s |
| `competitor_rmsd_molsysmt_jit` | 0.0079 s |
| `competitor_rmsd_molsysmt_public` | 0.2845 s |

The gap between the `_jit` and `_public` rows is a near-constant 0.27 s in both, which is
the signature of a fixed per-call cost rather than of digestion or unit handling scaling
with the work. The measurement existed for three months and was read as public-API
overhead in general; it is one call.

**The blast radius is per-call.** Anything that loops — a per-structure analysis, a
`Iterator` walk, a docs notebook, a course module — multiplies 190 ms by its iteration
count. A 1000-structure per-frame loop spends three minutes collecting garbage.

## What is measured and what is assumed

Measured: the four ratios above, the profile attribution, the 37 call sites, the 22
modules, and the historical baseline medians quoted from the committed JSON.

Assumed — *estimate*: that removing the calls recovers substantially all of the gap
between the `_jit` and `_public` baseline rows. The measurement above shows 4.3 ms
remaining for `get_center` against a 8 ms kernel figure taken from a different profile,
so the residual public overhead is small, but the two were not measured in one session on
one system and the claim is not yet established.

Not measured: whether any call site was added to solve a real memory-pressure incident.
The chunked heavy path in `ChunkedExecutor` is a plausible origin and is the one place
where a bounded collection could be justified.

## What was refuted

*The overhead is argument digestion.* Refuted by the profile: ArgDigest and SMonitor
wrappers together account for under 15 ms of the 984 ms in five calls, and `gc.collect`
accounts for 943.

*The overhead is unit handling.* Refuted the same way; `puw.standardize` does not appear
in the hot path at any significant cost.

*It only matters for small systems.* The absolute cost is constant, so it matters most
for small systems — but a 5000-structure trajectory measured 251 ms as shipped against
62 ms with collection disabled, so it does not disappear at scale either.

## Scope and exclusions

Covers the 37 unconditional call sites in `molsysmt/structure/` and `molsysmt/pbc/`.

Excludes the `del` statements next to them: dropping a local reference is free and
harmless, and removing both at once would confuse what the fix demonstrated. Excludes
memory behaviour of the chunked heavy path, which may genuinely need a bounded collection
and should be argued on its own evidence rather than kept by default. Excludes the
benchmark gate's ability to detect this class of regression, which is
`benchmark_regression_gate_reliability.md`.

## Acceptance criteria

1. No unconditional `gc.collect()` remains on a public return path; any surviving call is
   inside a documented memory-pressure branch with the condition stated in the code.
2. A benchmark asserts a per-call budget for a small-system `get_center` that the current
   code fails and the corrected code passes. This is the `guard`.
3. The scientific-truth suite passes unchanged: this is a performance fix and must move
   no number.
4. `benchmarks/baselines/competitor_matrix_session.json` is regenerated, so the recorded
   `_public` rows stop carrying a cost that has been removed.

## Dependencies and risks

The risk is memory, not correctness. If any call site was load-bearing under chunked
execution, removing it raises peak RSS on large trajectories; the heavy suite and the
`peak_rss_mb` fields the benchmark harness already records are the check.

## Provenance

Measured 2026-08-19 on Linux 7.0.0-28-generic x86_64, 20-core Intel Xeon E5-2630 v4,
Python 3.13.14, MolSysMT `0.21.0+325.g7cedab74a` at repository commit `b9a2098e4`,
NumPy 2.4.6. Median of 15 calls after one warm-up, per function. Historical rows are
quoted from the committed 2026-05-22 session on MolSysMT 0.18.0 and were not re-run.
