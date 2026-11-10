---
summary: Native neighbor cell grids can allocate gigabytes for two atoms and a small valid cutoff.
issue: uibcdf/molsysmt#690
status: resolved
opened: 2026-11-10
closed: 2026-11-10
severity: critical
verification: reproduced
area: [structure, rust]
guard: tests/structure/get_neighbors/test_allocation_bounds.py
normative:
blocked_by: []
supersedes: []
---

# Native neighbor cell grids scale with empty volume

## What

The reporter's protected two-atom query with coordinates [0,0,0]/[1,1,1] nm,
disjoint source selections and threshold 0.001 nm attempts an 8,000,000,000-byte
cell-head allocation. An independently imposed 2 GiB address-space limit and
zero core-dump limit produce native abort -6. The independently repeated protected baseline confirms this reported failure;
it is not an unconstrained allocation experiment.

## How

At the original source, inspection confirms `rust/src/neighbors.rs`: vacuum and periodic grids
allocate a dense `head` vector from unchecked nx*ny*nz products, independently
of occupied cells. All structure grids are retained before the query loop.
Sparse CSR output does not bound this intermediate. The Python dispatch does
not supply the configured numerical memory budget to the compiled kernel.
The original kernel matches the reported backend at public 1ba5d8af9.

## Why

A valid tiny query can abort its process or exhaust a shared host. Buch and
other clients call the same native search, so a consumer-only cutoff restriction
would obscure a provider defect. Treat this as priority pre-1.0 correctness and
resource integrity ahead of optional draft #687 work. Existing formal phase
weights remain unchanged; no artificial repair bonus is introduced.

## Accepted implementation

Preserve the exact requested distance predicate and existing reduced-cell MIC.
Bound cell-head cardinality by population and the negotiated working allowance;
coarser cells remain scientifically complete because their widths only increase.
Use checked sizing and clean refusals for unsupported/overflowing requests.
An occupied-cell map is an alternative if its lookup/memory tradeoff is better;
never widen a cutoff or impose a positive scientific floor as a workaround.

Review the retained grid collection, query scratch, CSR counts/output and
controlled Rayon concurrency together. Prefer exact output counting before
large result allocation over a quadratic worst-case refusal of valid sparse
queries. Numerical working estimates remain distinct from process RSS or a
reservation on the shared host. Keep #666's exact cutoff/unit boundary separate.

## Acceptance and safe receiving

- Original pre-fix evidence is reproduced only in a subprocess with restrictive
  address-space/core limits and the existing monitored cgroup envelope.
- Tiny cutoffs, wide sparse extents, ordinary vacuum/orthogonal/triclinic PBC,
  empty populations and documented invalid/zero/nonfinite cases have guards.
- Repeated/nonconsecutive structures, self/disjoint populations, CSR/array and
  unit-policy parity preserve source indices and exact scientific criteria.
- Checked products, configured numerical budget and output/scratch growth fail
  cleanly before unsupported allocations. No unbounded physical allocation test.
- Rust and public get_neighbors/get_contacts plus Buch/Luzard consumers are
  received against independent distances/periodic truth under controlled threads.
- Public documentation and the maintained scalability contract describe actual
  intermediate/output guarantees and limits before closure.

## Provenance

2026-11-10 owner source review, reported compiled SHA-256
2f1f69f6e0539bd31ee419ec3b7a4deaab20f09045ce3e6504369c9130438525.
The initial diagnosis preceded the protected reproduction and canonical rebuild
recorded below; neither is inferred from the earlier model/context receipt.
The independently completed #582/#688/#689 receiving does not cover this defect.

## Protected reproduction and implementation — 2026-11-10

The owning reproduction confirms the exact requested 8,000,000,000-byte
allocation and child exit -6 with a 2 GiB address-space ceiling/core dumps off;
the whole bounded run peaks at about 242 MiB. The same protected query succeeds
with the rebuilt backend. Five added Rust resource guards plus existing
independent geometry pass (87 cases); 31 focused Python cases pass after an
initial fixture assumes an unexported root exception. The existing catalog
exception is now deliberately exposed publicly for callers, with a stability
entry and ordinary budget/error guards; no private-module import is required.

Cell heads are capped linearly and coarsened without changing the exact
predicate. Sizing is checked; Vec reservations are fallible; controlled scratch
and observed output charge share one atomic budget. Sparse queries are not
rejected by quadratic worst-case output. The contact consumer reserves its
Boolean map, defers allocation until native admission and fills using one
occurrence-index vector. Final rebuilt/consumer/scientific/documentation and
performance receiving remain pending; this is not source closure.

## Empty periodic scope control — 2026-11-10

The required empty-structure test exposes a separate public fast-path edge:
its periodic box check indexes row zero of an empty selected box series. The
nonperiodic empty control passes. The check now admits the empty series without
reading row zero; typed CSR offsets remain [0] and no native grid is needed.
This is within the reported empty-scope receiving, without changing geometry.

## Accepted source receiving — 2026-11-10

Clean **573476e70a4607bd42d21e9c7a866388fc3c1e6c**, canonical offline Rust
1.97.1 rebuild, backend SHA-256
**58653b1d477be36017d2bc721dafe6e85a508e2325fa3226ccf26c61d449d6e5**:
**954 affected cases**, **83 legacy/consumer cases**, **87 Rust tests**,
**116 scientific cases / 74 nodes**, **14 fast gates**, the repository-required
Clippy command and eight inspected rendered pages pass. Four notebooks retain
all **37 executable cells**, outputs and execution metadata. The [receiving
record](../../../devtools/data/native_neighbor_allocation_receiving_690_20261110.json)
retains exact inputs, canonical build, original failed controls and resource
observations. The public numerical-budget exception has an explicit root export.
No scientific cutoff, MIC predicate, schema or dependency floor changes.

The selected guard includes the protected original abort, independent lattice
and Euclidean oracles, configured/observed budget refusals, sparse admission,
empty/invalid scopes, source preservation and forced contact-map admission.
This closes the native allocation failure, not every surrounding GUI or
representation cost. The numerical estimate is not total RSS or reserved RAM.

All three actual-Jupyter attempts remain **failed**: a two-CPU late-workflow
deadline, a four-CPU server-startup deadline before a molecular cell, and a
four-CPU PCA-popup deadline after numeric geometry checks. The complete UI
workflow remains under #421; the distinct #615 uncertainty stays open. No
assertion or deadline was relaxed. The supplemental `--all-targets` Clippy
attempt also remains failed on nine inherited test-only statements; the actual
required production-library command passes without suppression.

The short same-host paired kernel pilot preserves exact indices/offsets and
distances within 1e-13 nm, with median additional CPU cost about 8–21%.
[#692](https://github.com/uibcdf/molsysmt/issues/692) owns advisory optimization;
[#693](https://github.com/uibcdf/molsysmt/issues/693) owns separate Python
compatibility-output accounting. Neither withdraws this correct allocation
repair. Scale, complete GUI, installed/platform and final-candidate acceptance
are not inferred. Formal weighted progress remains **75.6386%**.
