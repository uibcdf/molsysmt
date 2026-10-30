# Chemical-domain separation benchmarks — 2026-10-30

**Role:** dated measurement report for [MolSysMT #255](https://github.com/uibcdf/molsysmt/issues/255).
**Evidence:** Benchmarked local Linux source paths, not installed artifacts or release qualification.

The complete machine-readable input, source/backend hashes, versions, seven timing
samples, ranges and process high-water memory are in
[`chemical_domain_separation_benchmarks_20261030.json`](../devtools/data/chemical_domain_separation_benchmarks_20261030.json).
The maintained runner is
[`benchmark_chemical_domain_separation.py`](../devtools/scripts/benchmark_chemical_domain_separation.py).

## Method and scope

Baseline: source commit `451b914cab8b596c01d84432a4f41b4a3e28f3cf` in a source-only
archive. Target: the uncommitted #255 worktree based on
`63012f9a60abceb5cab15c6d8e9e44d362f7b89a`, identified by its recorded Python-content
hash. Both use exactly the same ABI3 backend bytes and shared Python 3.14 environment.
No environment or compiled backend was built for this comparison.

The host has an Intel Xeon E5-2630 v4 at 2.20 GHz, 20 logical CPUs and Linux x86-64.
BLAS/OpenMP/Rayon thread controls were set to one. Each source/scenario ran in an
independent process, sequentially, with one warm-up and seven timed repetitions.
Validation runs were stopped during timing. Ordinary host activity remains a
source of noise; there is no claim about another machine, platform or package.

Synthetic inventory cases use 10,000/100,000 atoms, one/ten chemical states and
approximately one stored bond per atom. Ten-state cases have reused or alternating
connected partitions. Stable inventory has no groups; IDs are string labels.
The structural-isolation fixture has 1,000 atoms and 1,000 structures in nm, with
one/ten states. A separate zero-atom fixture has 30 groups and three chains.
The H5MSM fixture adds a named sparse analysis with explicit evaluated coverage.

Topology extraction selects every second atom. Structural extraction requests two
nonconsecutive structures. The private H5 codec read selects two atoms and two
nonconsecutive structures. Every operation checks its result; chemical edits require
unchanged coordinate storage and unchanged unselected-state chemical values.

## Measured results

Times are **median (minimum–maximum), in milliseconds**. This table is a selected
view of the complete artifact, including slower observations.

| Scenario and operation | Baseline ms | Target ms |
| --- | ---: | ---: |
| inventory; 100,000 atoms; 10 states; `stable_counts` | 0.329 (0.317–0.484) | 0.382 (0.312–0.437) |
| inventory; 100,000 atoms; 10 states; `topology_copy` | 44.751 (43.507–46.969) | 5.221 (4.799–5.547) |
| inventory; 100,000 atoms; 10 states; `topology_extract` | 884.997 (863.200–934.880) | 50.463 (47.777–66.711) |
| inventory; 100,000 atoms; 10 states; `molsys_copy` | 40.890 (38.745–45.225) | 45.448 (43.587–47.512) |
| structural; 1,000 atoms; 10 states; `chemical_edit_with_coordinates` | 5.197 (4.809–5.404) | 3.799 (3.529–7.582) |
| structural; 1,000 atoms; 10 states; `molsys_extract_two_structures` | 197.238 (195.022–208.865) | 205.083 (202.866–220.918) |
| group_only; 0 atoms; 1 states; `group_only_counts` | 0.358 (0.342–0.432) | 0.404 (0.336–0.498) |
| h5msm; 1,000 atoms; 10 states; `h5_topology_layer` | 50.026 (46.639–54.994) | 43.763 (42.651–46.182) |
| h5msm; 1,000 atoms; 10 states; `h5_nonconsecutive_block_private_codec` | 3.607 (3.441–4.004) | 3.930 (3.507–5.586) |

The principal improvement is bounded inventory work: pure Topology no longer
copies or remaps chemical states. With 100,000 atoms and ten states, copying the
inventory takes about 5 ms rather than 45 ms, and extracting half of its atoms
about 50 ms rather than 885 ms. The returned Topology intentionally has no
chemical payload under the accepted new contract. This is not a faster chemical
algorithm operating on identical output domains.

Full MolSys copies preserve all states and are **not claimed faster**. In the
initial cases their medians were about 1–15% higher. Target-first repetitions
changed the 10,000-atom comparison's direction and showed overlapping ranges
at 100,000 atoms. Diagnostic profiles showed the expected single chemistry clone
per full copy, with no duplicate chemistry clone introduced by separation.
This bounded variability does not support a universal full-copy speed claim.
Likewise, the small group-only query and private H5 block timings do not establish
a speed improvement. No numerical timing threshold is a correctness gate.

Peak RSS includes imports, fixture construction and every operation in a scenario;
it is not allocation attributable to one call. The 100,000-atom/ten-state reused
case peaks at about 344.8 MiB baseline and 323.3 MiB target. Structural cases peak
about 3 MiB higher in the target. Both implementations retain coordinate storage
identity through the measured chemical edit; the refactor preserves that existing
isolation rather than introducing it.

## Reproducing the comparison

Run from the repository root with the qualified shared environment. Supply an
archive/check-out of the recorded baseline and the same compatible ABI3 binary;
`--source-root` must contain its own `molsysmt` directory. The runner checks actual
import origin and records source/backend hashes.

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 RAYON_NUM_THREADS=1 \
python devtools/scripts/benchmark_chemical_domain_separation.py \
  --source-root . --output .pytest_cache/chemical-domain-inventory.json \
  --scenario inventory --atoms 100000 --states 10 --partition reused
```

Repeat with the baseline source root and a different output path. Supported
scenarios are `inventory`, `structural`, `group_only` and `h5msm`; use
`--structures 1000 --atoms 1000` for the latter coordinate-bearing fixtures.
H5MSM measures the public topology-layer read and a **private** selective structure
codec. This does not advertise a new public lazy/out-of-core query API or change
the separately documented eager public conversion limitations.
