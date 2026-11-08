---
summary: Define an explicit stored-hydrogen policy composition before strict correspondence.
issue: uibcdf/molsysmt#645
status: open
opened: 2026-11-07
closed:
verification: inspected
area: [api, build]
guard:
normative:
blocked_by: []
supersedes: []
---

# Explicit stored-hydrogen policy before correspondence

## What

DockingMT asks for a supported explicit composition to align stored hydrogen
policies from source conversion and fixed-state H generation before strict
chemical correspondence. Its reported source/generated inputs have matching
indexed atom/bond counts but differ in the `allows_implicit_hydrogens` flags
on indexed H atoms. The strict graph matcher treats those policies as labels
and returns no retained maps. This is not established as a matcher defect.

## Evidence and limits

The executed consumer chain, exact public P59 source/reference inputs, versions,
failed witness and source nonmutation limits are preserved in
uibcdf/molsysmt#645 and uibcdf/dockingmt#79. The reported 39-atom/42-bond
comparison and successful heavy-coordinate preservation are consumer findings,
not newly executed provider acceptance. Other differing identifiers/coverage
metadata also require review; literal record agreement does not certify
chemical equivalence. No local fixture or normalization is implemented here.

## Intended study

- Inspect existing public copy, assignment, state/history and H-representation
  tools before proposing another API. ChemicalStates owns stored assignments;
  build owns H generation. Reuse supported general operations.
- Determine whether detached copy plus public assignment is sufficient, with
  explicit preconditions, affected atoms/fields, source axes, allowed losses
  and a retained transformation record. The consumer must not invent a policy.
- If a provider tool is missing, design the smallest useful general operation
  in its owner; keep unknown, isotopic, charged, radical and truly incompatible
  H states explicit. Preserve original sources, coordinates, H-parent links,
  charge, isotope/stereo and meaningful preparation history.
- Receive both actual producers, nondefault units and detached persistence as
  applicable before claiming that an explicit common policy enables matching.
  Do not coerce flags inside the matcher, weaken labels or turn zero matches
  into zero RMSD.

## Priority and scope

This remains a separately assessed provider-policy proposal after #644's clear
public argument defect. It does not automatically enlarge frozen initial-1.0
gates or authorize a downstream workaround. Existing strict correspondence
and #612/#334 qualification obligations remain unchanged. No new engine,
chemical assignment or public namespace is selected by this intake record.
