# Cation-pi detector controls

Implementation and persistence are tracked by uibcdf/molsysmt#270; scientific
comparison remains open in uibcdf/molsysmt#271. These controls measure the public
MolSysMT implementations, not the speed of the original ProLIF package or the
physical accuracy of either definition.

## Reproducing the measurements

Run from the repository root, sequentially without concurrent tests/builds:

```bash
python devtools/scripts/benchmark_cation_pi_interactions.py --atoms 10000 --structures 1000 --rings 200 --method prolif --output /tmp/cation_pi_prolif_10000x1000.json
python devtools/scripts/benchmark_cation_pi_interactions.py --atoms 10000 --structures 1000 --rings 200 --method centroid_angle_offset --output /tmp/cation_pi_custom_10000x1000.json
python devtools/scripts/benchmark_cation_pi_interactions.py --atoms 100000 --structures 100 --rings 1000 --repetitions 1 --method prolif --output /tmp/cation_pi_prolif_100000x100.json
```

Each source contains separated benzene/ammonium pairs, explicitly neutral and
nonaromatic padding atoms, variable counts and every fifth structure empty.
There is no box. Chemistry and hydrogen counts are declared. Both methods produce
the same prescribed memberships/distances in this deliberately simple fixture;
this does not establish equivalent recognition on arbitrary molecules.
The 10,000-atom control has 200 relations and 146,600 occurrences. Coordinates
occupy 240,000,000 numeric bytes in either scale control.

Raw records contain CPU/platform, library and thread settings, every sample,
base commit, dirty-worktree flag and source/compiled-extension hashes:

- [ProLIF definition, 10,000 atoms × 1,000 structures](../../benchmarks/baselines/cation_pi_prolif_10000x1000.json)
- [Custom definition, 10,000 atoms × 1,000 structures](../../benchmarks/baselines/cation_pi_custom_10000x1000.json)
- [ProLIF definition, 100,000 atoms × 100 structures](../../benchmarks/baselines/cation_pi_prolif_100000x100.json)

The editable installed version may lag source development; hashes identify the
actual implementation. Workers run separately and sequentially. One tiny call
warms the calculation before measurements. The 10,000-atom controls use medians
of three full detector calls. The larger atom-axis control uses one timed call
per worker and must not be interpreted as a stable timing distribution.
Source creation/native loading is excluded from calculation timing. Chemistry
recognition, projection, geometry, sparse packing and file reads are included.
OS page cache is uncontrolled. Eager execution uses one block; forced execution
uses at most 16 structures per block. The complete output stays resident.

## Calculation on 10,000 atoms × 1,000 structures

| Source / execution | ProLIF definition median | Custom definition median |
| --- | ---: | ---: |
| Native / eager | 2.709 s | 1.091 s |
| Native / blocks | 2.632 s | 2.761 s |
| H5MSM / eager projection | 6.667 s | 5.115 s |
| H5MSM / blocks | 6.596 s | 6.249 s |

Preparation differs: ProLIF uses full declared-graph RDKit conversion/SMARTS;
the custom method uses charge centers, a minimum cycle basis and fitted planes.
The measured custom eager advantage in this regular control does not prove better
chemistry or scientific discrimination. Blocking reduces coordinate working size
but adds dispatch costs and is not universally faster. No new detector-specific
Rust kernel is justified by these measurements alone.

## Larger atom axis: 100,000 atoms × 100 structures

| Source / execution | ProLIF definition, one timed call |
| --- | ---: |
| Native / eager | 16.364 s |
| Native / blocks | 15.970 s |
| H5MSM / eager projection | 17.752 s |
| H5MSM / blocks | 17.762 s |

This control has 1,000 relations and 73,320 occurrences. The numeric result is
7,739,056 bytes before indexes and the standalone layer is 196,246 bytes.
Warmed frame queries take 66–68 µs and warmed atom queries 38–40 µs.
Native VmHWM is approximately 958 MB; file eager/block workers reach 574/570 MB.
Blocks do not remove full-source chemical preparation and make little difference
in these high-water marks. These single samples establish successful execution at
this scale, not a timing uncertainty estimate or a speedup claim. Profiling would
be needed before attributing the cost to a particular converter/kernel.

## Memory, queries and persistence

For the 10,000-atom control:

| Metric | ProLIF definition | Custom definition |
| --- | ---: | ---: |
| Numeric result before inverse indexes | 13,621,616 bytes | 12,448,816 bytes |
| Numeric result after first atom query | 14,887,232 bytes | 13,714,432 bytes |
| Frame query, warmed median across workers | 74–83 µs | 70–78 µs |
| Atom query over structures, warmed median | 119–127 µs | 119–128 µs |
| First atom query, including inverse indexes | 4.3–4.6 ms | 4.3–4.9 ms |
| Standalone H5MSM interaction layer | 183,144 bytes | 169,945 bytes |
| Layer write range | 70–72 ms | 66–73 ms |
| Layer read range | 69–74 ms | 65–71 ms |

ProLIF stores an additional oriented angle column to preserve original reported
geometry. Numeric bytes exclude Python objects, coordinates and transient work.
Fifty warmed query calls are measured per worker. The selected atom belongs to
a repeatedly observed ring; this is not a benchmark of arbitrarily changing
relations. H5MSM writes are independent interaction layers, not complete system
or viewer-session writes. Repeated regular geometry compresses exceptionally
well; disk ratios must not be extrapolated to unrelated geometric observations.

Linux process VmHWM spans imports, source loading, calculation, indexing, writing
and reloading. Native workers reach approximately 946–949 MB for ProLIF and
945–946 MB for the custom method. They already materialize their full source.
H5MSM eager/block workers reach about 647/496 MB and 584/472 MB, respectively.
These are process high-water marks, not allocation deltas or viewer measurements.
Numerical budgets are working estimates, not process-RSS caps.

## Evidence boundaries

Geometry/recognition reproduction is checked separately against the executed,
unmodified original ProLIF 2.2.2 detector in
`tests/scientific_truth/curated/test_cation_pi_interactions.py` and the committed
`devtools/data/cation_pi_validation_systems.json`. Controlled cases cover neutral
resonance matches, heteroaromatics, fused rings, warped geometry and empty results.
Checksum-fixed proteins use an explicit declared model chemical state. Default
cutoffs produce no observations in those bundled structures; broader explicitly
recorded distance/angular windows also test positive protein geometry.
The broader windows are implementation controls, not recommended physical cutoffs.

Future scientific comparison must separate feature membership, geometry, full
detector behavior and physical/reference classification. Force-field energy or
quantum/experimental data are not provided here. Neither output size, baseline
agreement nor execution time establishes superiority. No 100,000-atom ×
10,000-structure coordinate load, incremental writer or jointly measured viewer
session is claimed.
