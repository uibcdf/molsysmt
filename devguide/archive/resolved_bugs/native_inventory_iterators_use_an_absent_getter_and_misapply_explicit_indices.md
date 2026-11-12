---
summary: Native inventory iterators use an absent getter and misapply explicit indices
issue: uibcdf/molsysmt#720
status: resolved
opened: 2026-11-11
closed: 2026-11-11
severity: medium
verification: reproduced
area: [form, tests]
guard: tests/form/molsysmt_Topology/test_inventory_iterator.py
normative:
blocked_by: []
supersedes: []
---

# Native inventory iterators use an absent getter and misapply explicit indices

## What

The real native TopologyIterator imports get_n_atoms_from_system from a module
that does not define it. Explicit source indices are placed into a query Boolean
flag, then a range of their length replaces their actual positions. MolSys uses
this same inventory adapter. This is separate from #717's unavailable stubs.

## How

Reproduce default and explicit/nonconsecutive/repeated/empty atom and group
positions, direct adapters and public native Iterator composition. The current
constructor uses a hard-coded atom count even for other element axes. The test
fixture has four atoms and two groups, deliberately distinguishing these counts.

## Why

Inventory iteration must preserve source correspondence and requested traversal,
without coordinates, chemical reconstruction or expensive molecular-system
conversion. Fix the existing adapter using public validated queries and the
existing indices_iterator helper; preserve its public contract while choosing its existing inventory route when no structure axis is declared.

## Acceptance and scope

Normalize/validate at the existing public boundary and query actual selected
inventory once. Keep requested source positions, order/repeats and start/stop/
step/chunk semantics; exhaust normally and preserve independent input tables.
Retain value/dictionary output conventions and native MolSys delegation. Add
negative validation controls and existing stable-domain/public-iterator receiving.
Document the actual behavior and changes. No new structural streaming, chemical
facade, optional dependency or new generic public utility is introduced.

## Provenance

2026-11-11, Linux/Python 3.14 source inspection pending bounded baseline receiving.
Use the previously qualified native binary and pinned client/support overlays;
shared-host resource limits and original failures remain recorded. Source tests
do not qualify a full suite, installed artifact or final release pair.

## Bounded source receiving

The corrected 19-case baseline has thirteen failures and six positive controls.
Eight failures reach the old inventory implementation (missing getter, wrong
selected values or group indexing); the other five are #719 documentation checks.
Failed drafts remain retained: one omitted output-mode field, an inherited
flag-digester defect (#722), and reused result dictionaries discovered when
retaining chunks. The repair now queries selected row values once through the
existing native get boundary, uses the existing range/indices helper, validates
query kwargs through a scoped ArgDigest registry and yields fresh form mappings.

A separate narrow dispatcher correction routes shared index/count requests
through the existing inventory path when source forms declare no structure
axis. It adds no public parameter or structural-streaming route. Forms declaring
both axes retain their existing index-only interpretation; explicit inventory
attributes or the topology domain disambiguate it. The principal public contract
and coordinate-bearing iteration stay unchanged. The previous complete cohort
with that missing case fails one/373; its original failure is preserved.

The final 377-case cohort passes: 35 direct/public inventory cases, six tutorial
checks, 39 domain-separation cases, 17 existing public iteration controls,
107 strict-flag cases, 27 name/type and 81 core digester controls, 64 native-query
cases and one public Iterator doctest. Order/repeats, empty selections, distinct
atom/group sizes, aliases, traversal windows, typed errors, retained mappings
and nonmutation are covered. A later comment-only clarification preserves the
entire executable/docstring AST. The actual Basic Iterator notebook executes
21 cells successfully, and Core04's existing native-query cell runs separately.
Fifteen fast gates and applicable Ruff/index checks pass. Complete strict HTML
on clean b0ae02b22 has zero warnings; actual article/reference receiving passes.


## Resolution

The implementation and maintained examples are received at b0ae02b22, with
Boolean-context corrections at 4280a8d42. The [shared receipt](../../../devtools/data/native_inventory_receiving_719_720_722_20261111.json)
owns exact inputs, overlapping counts, failed probes, runtime/native identity,
resource limits and documentation scope. The addressable guard above checks
actual behavior: declared capability and live example execution (#719), source
positions/traversal and retained chunks (#720), or accepted/rejected flag values
plus public query results (#722). It cannot pass merely by matching a table's
format or silently skipping an unavailable path.

This closes these bounded defects, not the wider #378 review, #615/#713
causality, client memory campaign or installed/final-candidate acceptance. No
release/publication action or extra formal scorecard credit is implied.
