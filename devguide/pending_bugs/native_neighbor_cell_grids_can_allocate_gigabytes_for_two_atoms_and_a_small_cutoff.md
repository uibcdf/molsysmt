---
summary: Native neighbor cell grids can allocate gigabytes for two atoms and a small valid cutoff.
issue: uibcdf/molsysmt#690
status: active
opened: 2026-11-10
closed:
severity: critical
verification: inspected
area: [structure, rust]
guard:
normative:
blocked_by: []
supersedes: []
---

# Native neighbor cell grids scale with empty volume

## What

The reporter's protected two-atom query with coordinates [0,0,0]/[1,1,1] nm,
disjoint source selections and threshold 0.001 nm attempts an 8,000,000,000-byte
cell-head allocation. An independently imposed 2 GiB address-space limit and
zero core-dump limit produce native abort -6. This is reported evidence, not a
passing scientific test or an unconstrained reproduction by this agent.

## How

Source inspection confirms `rust/src/neighbors.rs`: vacuum and periodic grids
allocate a dense `head` vector from unchecked nx*ny*nz products, independently
of occupied cells. All structure grids are retained before the query loop.
Sparse CSR output does not bound this intermediate. The Python dispatch does
not supply the configured numerical memory budget to the compiled kernel.
The source is unchanged from the reported backend at public 1ba5d8af9.

## Why

A valid tiny query can abort its process or exhaust a shared host. Buch and
other clients call the same native search, so a consumer-only cutoff restriction
would obscure a provider defect. Treat this as priority pre-1.0 correctness and
resource integrity ahead of optional draft #687 work. Existing formal phase
weights remain unchanged; no artificial repair bonus is introduced.

## Implementation strategy under review

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
No Rust rebuild or native reproduction has yet been executed for this issue.
The independently completed #582/#688/#689 receiving does not cover this defect.
