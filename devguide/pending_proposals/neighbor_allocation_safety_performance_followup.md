---
summary: Profile allocation-safe neighbor search overhead without weakening resource guards.
issue: uibcdf/molsysmt#692
status: partial
opened: 2026-11-10
closed:
verification: measured
area: [structure, performance]
guard: tests/structure/get_neighbors/test_compatibility_output_memory.py
normative:
blocked_by: []
supersedes: []
---

# Profile allocation-safe neighbor search overhead without weakening resource guards.

## What

Investigate the additional CPU cost of #690 while preserving checked sizing,
population-bounded grids and observed-output admission. This is advisory work,
not a numerical defect or a new release blocker.

## How

The [paired pilot](../../devtools/data/native_neighbor_allocation_receiving_690_20261110.json)
records one controlled CPU, same inputs/runtime, three warmups and fifteen
repetitions on each of three 4 × 1,000-atom workloads. Median new/old ratios are
1.1542 compact vacuum, 1.0786 compact periodic and 1.2149 dilute vacuum.
Offsets/indices agree exactly and distances within 1e-13 nm. The old/new order,
short duration and kernel-only scope do not establish a representative ranking.

## Why

The accepted #567 policy keeps correct implementations available. Investigate
comparable differences above roughly 15% with measurements, rather than
removing a correct tool or weakening its resource/scientific guard.

## Acceptance and exclusions

Repeat interleaved comparable campaigns, profile occupancy/coarsening, atomic
admission and small-query scheduling, then document an optimization or an
accepted safety tradeoff. Preserve independent geometry and budget controls.
No new dependency, API, cutoff floor, schema or release-scope requirement.

## Python projection follow-up from #693 — 2026-11-11

The [compatibility-output receipt](../../devtools/data/compatibility_output_memory_693_20261110.json)
adds separate Python projection measurements. It does not remeasure #690's
native kernel. The bounded output model reduces large neighbor-row peaks and
mapped-contact projection peaks; those paths also improve in the measured
untraced timings. Unmapped self-contact conversion remains an advisory warning:
current/legacy median ratios are approximately 1.48, 1.85 and 1.69 for 16, 128
and 512 atoms, with bounded counting/packing instead of whole-map temporaries.
The 512-atom median is about 36.7 ms versus 21.7 ms. Tiny unmapped cases can
also increase peak allocation as fixed/slab overhead dominates; keep those
samples visible rather than asserting a universal improvement.

These are one controlled CPU, two warmups/five samples, projection-only
observations. Alternating order, broader sparse populations and profiling are
needed before a representative performance conclusion. Evaluate vectorized
bounded counting/packing and reuse of sparse occurrence output without weakening
the memory guard, label ordering, periodic/cutoff semantics or empty results.
This warning remains in the open advisory issue under #567. Correctness passing
and reduced peak allocation justify the bounded route; it is not a release gate.

## Bounded Python packing increment — 2026-11-11

The source increment separates actual output counting from index extraction.
Counting no longer builds positions just to discard them. Packing uses Boolean
2-D views of at most 16,384 entries, retaining row-major order even when a wide
row needs multiple column blocks. Strided/Fortran inputs never require a
whole-map flattening copy. All structures' output is admitted before boxing;
the conservative existing budget and scientific contact criterion are unchanged.

**Contract-tested:** 223 geometry cases and module doctests pass, including 40
new checks for rectangular/wide/empty axes, C/Fortran/reversed layouts,
noncontiguous paired output, exact labels/order and pre-boxing refusal. The
4-MiB empty-map cases require less than 1 MiB of additional traced allocation,
which rejects an implementation that silently flattens the whole input.

`benchmarks/contact_pair_projection.py` provides a separate bounded,
interleaved baseline/current study on eight deterministic maps. It reuses the
existing comparison-context and workload telemetry, checks exact results
before timing, retains raw repetitions and measures additional traced allocation.
The baseline is reviewed source `54c9b79a0751bfc74ec204dbc4c46d6b120338fd`;
only the helper from that Git object is executed. The producer requires the
current implementation to match committed bytes and refuses an existing output.

Numerical/resource receiving is complete for this increment. Record the paired
measurement on the committed implementation before making a performance claim.
The earlier simple contiguous-view prototype left most overhead in place;
no universal speedup or native-kernel improvement is inferred from its pilot.
The original #690 kernel study and all prior slow measurements remain in this
open advisory proposal. No new release gate, API, dependency, unit or cutoff
change is introduced.

### Paired committed-source receiving

The [deduplicated two-campaign receipt](../../devtools/data/contact_projection_692_20261111.json)
retains every raw timing, workload, context and memory observation. Both fresh
processes use implementation `af12cb91f260500ff4a6375ffe90b6067a81472b`
against the same frozen pre-increment helper. The source/producer hashes match
and remain unchanged. The tree retains four human RST edits, explicitly listed;
the measured runtime helper is committed. Native ABI3 remains `4ffb82e4` and
is not executed by the measured projection.

Three warmups precede fifteen one-call samples per route; baseline/current order
reverses each repetition. GC is collected before timing and stays enabled.
Equality checks and result retirement are outside timing. A separate warmed
tracemalloc call measures additional allocations, with inputs/expected output
already resident. Both campaigns run with one CPU, 1 GiB, zero scope swap and
six thread caps set to one; the process has nice 10. Before/after host available
memory stays about 14 GiB and pressure averages remain zero. These observations
are not an exclusive reservation or continuous host-memory guarantee. A brief
API/dependency validation overlaps the later part of A; B has no other own
computation. Unrelated users remain uncontrolled. The same telemetry context
is necessary evidence, not proof of identical contention.

| Case | Current / previous median, A | Ratio, B | Previous / current traced peak, A (bytes) |
| --- | ---: | ---: | ---: |
| dense_16 | 0.8794 | 0.8825 | 19,224 / 17,072 |
| dense_128 | 0.7095 | 0.7618 | 1,125,368 / 993,984 |
| dense_512 | 0.7236 | 0.7222 | 15,102,776 / 14,716,046 |
| dense_mapped_512 | 0.7338 | 0.7453 | 19,329,816 / 18,929,024 |
| sparse_512 | 0.3050 | 0.2948 | 174,441 / 154,770 |
| rectangular_mapped | 0.8009 | 0.7883 | 5,769,816 / 5,572,176 |
| fortran_512 | 0.5068 | 0.5202 | 15,102,776 / 14,716,046 |
| reversed_sparse_512 | 0.0773 | 0.0786 | 218,281 / 198,627 |

The 512-atom dense unmapped projection falls from 34.1–34.8 ms to
24.6–25.2 ms in these campaigns (about 27–28% less time). Sparse 512-atom
projection falls from 4.38–4.51 ms to 1.33–1.34 ms (about 70% less).
All eight examples show lower medians and additional traced peaks in both
campaigns. The result concerns Python representation only; it neither remeasures
the #690 kernel nor establishes parity with the historical whole-map legacy
route. Previous slow observations stay intact. Do not infer these ratios for
other sizes, hardware or an entire molecular workflow.

Reproduce on the pinned implementation with the recorded environment and OS
limits, using two fresh output files:

```bash
python -m benchmarks.contact_pair_projection \
  --baseline 54c9b79a0751bfc74ec204dbc4c46d6b120338fd \
  --repeats 15 --output .pytest_cache/contact-projection-new.json
```

The maintained invocation uses module mode so repository imports resolve from
the root without an implicit PYTHONPATH. `--help` passes that route with
PYTHONPATH unset. Actual receiving used the explicit published PyUnitWizard
0.29.2 overlay. A first direct-script help check without PYTHONPATH failed to
resolve `benchmarks`; that is a command-guidance correction, not a hidden
successful receiving run. Original raw session hashes/custody remain in the
receipt; identical context is stored once and every raw sample is retained.

Ruff, public signature stability, optional-import and developer-guide checks
pass. No scientific formula, units, public signatures, dependencies or native
binary change. **#692 remains partial/open for the native-kernel study**; this
Python increment does not replace that broader acceptance or add plan credit.

## Interleaved native evaluation — 2026-11-11

The [native receiving record](../../devtools/data/native_neighbor_kernel_receiving_692_20261111.json)
adds two fresh, interleaved campaigns on committed producer
`e0a547dd8771e17aec6e0b0000617f1bb4b36437`. They compare the preserved
pre-690 extension `2f1f69f6` with the current `4ffb82e4`, without rebuilding
or replacing either. Eight deterministic workloads cover compact/dilute
populations, one or many small structures, dense output, single-cell PBC
and a skew periodic cell. The three original pilot populations retain their
seed, shape and cutoffs. These measurements do not overwrite that older pilot.

Before timing, both routes agree with an independent all-pairs oracle: exact
CSR offsets/indices and distances within 1e-13 nm. Orthogonal cells use direct
minimum images; the bounded skew fixture uses explicit `[-2,2]^3` lattice
images. Every timed result is checked outside timing. All-pairs enumeration is
a small-fixture oracle, not a proposed production replacement.

Three warmups precede fifteen repeat-block means of five individually timed
calls per route. Order reverses each repetition; campaign B reverses the
initial route in a fresh process. GC stays enabled and is collected before
each block. Imports, preparation, checking, retirement and modeled grid
statistics are outside timing. The receipt preserves all **480 raw block
means**, actual input identities, dependency/build environment, unit policy,
source and binary hashes, and separate host/resource observations.

| Case | Current / baseline median, A | Ratio, B | Interpretation |
| --- | ---: | ---: | --- |
| compact | 1.1173 | 1.0527 | No repeated >15% warning in this study. |
| compact PBC | 1.1104 | 0.9800 | Direction varies; no attributed speedup. |
| dilute | 1.8899 | 1.8703 | Repeated advisory warning. |
| one small structure | 1.0992 | 0.8396 | Short/noisy case; direction varies. |
| many small structures | 1.2338 | 1.2448 | Repeated advisory warning. |
| dense | 1.2321 | 1.0682 | Only A exceeds the threshold; retain both. |
| one-cell PBC | 1.1194 | 1.1267 | No repeated >15% warning in this study. |
| skew PBC | 1.0235 | 1.0201 | No repeated >15% warning in this study. |

For dilute input, medians are about **2.00/3.77 ms** (baseline/current) in A
and **2.02/3.77 ms** in B. For many small structures, they are **1.38/1.70 ms**
and **1.36/1.69 ms**. These are kernel calls on this shared host, not public
get_neighbors/get_contacts pipeline times, general slowdowns, confidence
intervals or a reason to withhold correct results. Absolute times and ratios
need not reproduce the earlier differently scheduled pilot.

### Grid evidence and remaining experiment

A separate source-derived model calculates head counts and candidate visits;
these are **not instrumented native counters**. On the four dilute structures,
head tables fall from **143,748 to 8,192 entries** (about 94.3% fewer head-table
bytes), while predicted candidate visits rise from **2,798 to 44,816**.
This models a real tradeoff: limiting empty spatial storage can require more
distance checks. It does not measure total allocation reduction or establish
the timing contribution of coarsening versus checked growth, atomic output
admission, scheduling, sorting or flattening. Skew-basis grid counts are not
modeled. The host's `perf_event_paranoid=4` was inspected; no system setting
was changed or privileged profiler launched.

The next bounded experiment should evaluate more balanced coarsening **within
the same four-heads-per-reference bound**. For the 1,000-atom example, the
current `[16,16,8]` table uses 2,048 heads; `[15,16,16]` would use 3,840,
still below 4,000. That is a testable occupancy hypothesis, not an implemented
optimization or a speed claim. Preserve complete candidate coverage, cutoff,
MIC geometry, checked storage and admission before retained output allocation.
Measure the private prototype before changing the client reference binary.

### Receiving and disposition

Six new analytical-oracle/custody/model controls and nine existing telemetry
controls pass (**15 total, no skips**); they reject wrong pair identities and
unreviewed executable bytes. Both campaigns exit zero, with one CPU, 1.5-GiB
memory cap, no swap and an active 6.5-GiB host-reserve watchdog. Scope peaks
are about 242 and 178 MiB; observed host available memory stays above 13.96 GiB,
with zero recorded full-pressure averages, OOM or reserve stops. The different
peaks are whole-scope observations, not a baseline/current allocation comparison.
One failed scope setup is retained: this systemd rejects `MemoryOOMGroup`;
the corrected launch records its actual value while enforcing the supported
CPU/memory/swap/task limits.

The benchmark is runnable from the repository root with
`python -m benchmarks.neighbor_kernel_profile --help`. Supply the preserved
extension matching the fixed digest through `--baseline-extension`, a fresh
`--output`, six explicit thread caps and an OS resource limit. The executable
is not automatically downloaded or rebuilt. Two fresh invocations use
`--first baseline` and `--first current` respectively.

**#692 remains partial/open for optimization or an explicitly accepted safety
tradeoff.** Native runtime, current client binary, public APIs, dependencies and
scientific classifications are unchanged. This advisory evaluation earns no
additional original-plan credit or new release gate.
