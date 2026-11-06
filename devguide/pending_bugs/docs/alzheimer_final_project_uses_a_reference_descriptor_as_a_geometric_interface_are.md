---
summary: Alzheimer final project uses a reference descriptor as a geometric interface area.
issue: uibcdf/molsysmt#589
status: open
opened: 2026-11-05
closed:
severity: medium
verification: reproduced
area: [api, docs, tests]
guard:
normative:
blocked_by: []
supersedes: []
---

# Final-project interface observable

## What / How / Why

What — Alzheimer Module 54 calls physchem.get_area_buried with selection_2 and labels the result lost geometric interface surface. The API is a tabulated Rose group descriptor and does not accept that keyword.

How — reproduced on main 1b359d441b899d26a06a6d927b809f770a09c462 / Python 3.14.7 using bundled alanine dipeptide structure 0: get_area_buried(molsys, selection='group_index==0', selection_2='group_index==2') raises native UnknownArgumentError. The signature and docstring explicitly define a group-table lookup, not a conformational interface calculation.

Why — removing the unsupported keyword alone would still mislabel the science. Correctly distinguish reference descriptors, a geometric SASA/interface calculation and evidence of binding. Full preparation/parameterization/assembly must be qualified separately.

Acceptance — agree the intended observable and its existing owning public tools; implement a bounded scientifically valid lesson with explicit selections, units, geometry/model assumptions and a regression guard. Preserve useful biological content without inventing a descriptor-to-interface interpretation. Do not infer binding stability from a single descriptor or H-bond count.

Record — devguide/pending_bugs/docs/alzheimer_final_project_uses_a_reference_descriptor_as_a_geometric_interface_are.md

Related — #562 fixes only the minimizer call and result continuation in that project; it does not qualify the later characterization or the complete preparation scenario.

## Reassessment

Resolve before claiming execution or scientific qualification of the complete
project. A source-level minimization guard cannot validate this different
observable. A table lookup and a geometric interface area need separate public
contracts; do not silently replace one with the other or attach an invented
unit/meaning. Keep full-network and molecular-preparation execution out of
ordinary bounded regression guards until their own prerequisites are qualified.
