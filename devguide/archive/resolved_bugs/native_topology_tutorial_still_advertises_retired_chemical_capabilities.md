---
summary: Native Topology tutorial still advertises retired chemical capabilities
issue: uibcdf/molsysmt#719
status: resolved
opened: 2026-11-11
closed: 2026-11-11
severity: medium
verification: reproduced
area: [docs, form]
guard: tests/documentation/test_native_topology_tutorial.py
normative:
blocked_by: []
supersedes: []
---

# Native Topology tutorial still advertises retired chemical capabilities

## What

The six-cell native Topology tutorial declares chemical charges, state-local
bonds/components and chemical-state axes as if they remained in stable Topology.
It links retired add_bonds/remove_bonds modules and advertises coordinate appends
and streaming. The maintained Foundations page already defines the separate
ChemicalStates/Structures owners; the tutorial and micro-guide contradict it.

## How

Compare its declared 76-attribute portfolio with the actual stable-only adapter
flags and public exports. Attribute names and Sphinx role spelling alone cannot
establish implementation. Verify available inventory operations and selected
conversion limits, preserving six cells, code/output payload and existing anchors.
The review also exposes the separate actual inventory-iterator defect in #720.

## Why

Users and native clients must not infer a restored chemical facade from stale
documentation. Correct inventory-versus-chemistry ownership, actual attribute
counts, operation availability and data-loss/prerequisite descriptions without
adding chemistry to Topology or inventing coordinates.

## Acceptance and scope

A regression compares the actual true declaration set with the displayed table,
resolves every advertised native function target, and exercises documented
unavailable operations before checking their status. Native domain-separation
contracts supply behavioral controls. Preserve seventeen conversion registrations
while explaining their prerequisites and partial/lossy projection limits; a
registered converter is not universal conformance. Check actual HTML, internal
references and code payload preservation. No runtime implementation belongs to
this documentation correction; #720 owns its separate source repair.

## Provenance

2026-11-11, Linux/Python 3.14 source inspection pending bounded baseline receiving.
Use the previously qualified native binary and pinned client/support overlays;
shared-host resource limits and original failures remain recorded. Source tests
do not qualify a full suite, installed artifact or final release pair.

## Bounded source receiving

The corrected baseline has five documentation failures, eight real inventory
iterator failures and six passing controls. The first baseline separately
retains two mistakes in the new test (root class import and an ambiguous row
selector); it is not counted as seventeen product defects. The later complete
377-case cohort passes, including six tutorial guards and the actual Markdown
example, 35 inventory cases, 107 strict-flag cases and existing query/domain/
iteration controls plus the public Iterator doctest.

The form tutorial now lists the actual 38 stable declarations, removes retired
bond adapter references, distinguishes unsupported hooks and preserves seventeen
conversion registrations with explicit prerequisites/limits. Its six cells and
stored executable payload remain. Basic Iterator's 38-cell notebook is actually
forced through the maintained executor: 21 code cells complete and outputs/mark
are regenerated; its code sources are unchanged. Core04's prose is updated and
its actual existing native-query cell 36 executes, without claiming a full course
rerun. All fifteen fast gates and applicable Ruff/index checks pass. Complete
strict HTML on clean b0ae02b22 passes with zero warnings. Three actual articles
and 119 unique internal destinations, including sixteen implementation links,
are inspected; stored notebook execution stays disabled in that build.


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
