---
summary: Unrestricted NetworkX extraction returns an empty graph when reuse is requested
issue: uibcdf/molsysmt#743
status: resolved
opened: 2026-11-13
closed: 2026-11-13
severity: high
verification: reproduced
area: [form, extract]
guard: tests/form/networkx_Graph/test_unrestricted_extraction.py
normative:
blocked_by: []
supersedes: []
---

# Preserving unrestricted NetworkX molecular graphs

## What

Public extraction and conversion back to networkx.Graph return an empty result
when an unrestricted caller requests copy_if_all=False. A four-atom/two-bond
source becomes a zero-node graph; the source is unchanged. Two independent public
route controls reproduce the incorrect result. This is pre-1.0 correctness work.

## How

The adapter's unrestricted reuse branch calls item.subgraph(atom_indices).copy()
with the literal 'all' sentinel. NetworkX interprets it as node labels, not an
axis selector. The separate selected branches call nonexistent atom_slice/slice
methods. These are not valid NetworkX molecular-selection implementations.

## Why

A successful full extraction must preserve all molecular data. It must not
interpret the selection sentinel as chemical/index labels. Selected graph axes
also need an explicit mapping of atom positions, graph keys and chemical edge
references; replacing the broken methods with a guessed subgraph remap could
silently corrupt those references.

## Correction in progress — 2026-11-13

Unrestricted extraction now returns item.copy() or the original graph according
to the copy flag. Node keys, edges and supported scalar metadata stay intact.
Explicit atom/structure subsets raise catalogued NotImplementedMethodError before
constructing a result; they were previously unusable AttributeError branches.
No selected-graph capability is introduced. Broader conversion/profile coverage
remains under #181; a future graph-selection implementation needs its own mapping
contract rather than becoming a new release requirement through this fix.

The guard compares independent expected four-node/two-edge inventories and exact
node/edge metadata for both public routes, before and after calls. Additional
controls check source preservation on refusal and ownership of copied scalar
attribute dictionaries. Arbitrary nested extension values retain NetworkX's own
shallow-copy semantics and are not certified as a deep scientific payload.

## Acceptance criteria

- Full public extraction and same-form conversion retain four nodes/two edges and
  source metadata under explicit reuse; whole copied results remain independent
  for the supported scalar graph contract.
- Unsupported subsets refuse clearly without changing the source. Do not invent
  atom-index/node-label correspondence or chemical edge-reference remapping.
- Update the adapter docstring, form guide and applicable basic/course/Cookbook
  limits. Retain both original wrong-result controls and actual native exits.
- Receive the affected graph cohort and all relevant documentation. This does
  not qualify a complete-source/scientific, installed or final-pair gate.

## Runtime receiving in progress — 2026-11-13

The affected graph suite and executable docstring pass 22 cases. The two failed
wrong-inventory baselines remain retained. One earlier launch fails before pytest
because the inherited harness expects a documentation page-list file; no tests
are executed in that attempt. Its supervisor state/log are preserved separately
and the runtime phase is corrected rather than calling that a product failure.
Documentation and final affected-cohort receiving remain due.


## Completed receiving — 2026-11-13

Published b16c43a0d and the immutable owning implementation 6dd779adc have
independent public-tree verification. The final joint selection passes 340
cases; all 95 form notebooks have explicit receiving ownership and actual HTML
link checks. Twenty-three selected pages build without warnings, preserving
code/output/metadata, headings and anchors. The affected runtime cohorts and
original failed witnesses remain separately recorded.

See the [receiving receipt](../../../devtools/data/remaining_form_reference_receiving_727_20261113.json)
and [current form contract](../../forms_and_conversions.md). This closes the
reported mechanism, not every conversion/scientific/performance capability.
CuPy, complete-source/scientific gates, installed final-pair acceptance and
publication remain outside this scope.
