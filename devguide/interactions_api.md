# Interaction Analysis API

`molsysmt.interactions` owns chemically interpreted analyses over molecular
systems. Distance-only proximity remains a geometric primitive in `structure`;
it is not by itself an interaction classification. The first public families
are `interactions.hbonds` and `interactions.disulfides`. Other families need
separate scientific contracts and decisions.

## Hydrogen bonds

`interactions.hbonds` is the canonical path for the existing donor and acceptor
helpers and the named Buch and Luzard–Chandler methods. The implementations and
their return conventions were moved without changing their geometric criteria:

| Method | Current default criterion | Result |
| --- | --- | --- |
| `get_buch_hbonds` | Hydrogen–acceptor separation at most 0.23 nm | Per-structure donor, hydrogen, acceptor triples and aligned distances. |
| `get_luzard_chandler_hbonds` | Donor–acceptor separation at most 0.35 nm and the H–D–A angle below 30 degrees | Per-structure triples, distances, and angles. |

Both methods support one molecular system with one or two atom selections.
Passing `molecular_system_2` raises `NotImplementedMethodError`; cross-system
atom and structure alignment has no defined contract yet. Their current array
layout is a legacy method-specific contract, not a common interaction result
schema. The root `molsysmt.hbonds` namespace and direct historical module paths
remain available for compatibility. There is no deprecation decision for them
in 1.0.

For a single selection with no eligible donor or acceptor, each method returns
an empty result for every requested structure rather than attempting a
covalent-path lookup on an empty atom set.

The migration is guarded by regression tests using bundled systems. Those tests
show continuity of the existing implementation, not independent scientific
validation of either hydrogen-bond definition. Callers must choose and report
the named criterion and parameters used.

## Disulfide candidates

`interactions.disulfides.get_disulfide_candidates` identifies sulfur atoms in
eligible groups (by default `CYS`) and returns candidate pairs when atoms in
different groups lie within the maximum S–S distance (by default 0.205 nm).
The detector accepts an atom selection, an ordered set of structure indices,
and periodic boundary conditions. It returns two aligned lists: one array of
global atom-index pairs and one nanometer distance quantity per requested
structure. An evaluated structure with no candidates has an empty `(0, 2)`
pair array and an empty `(0,)` distance array. The detector does not mutate the
system and reports a geometric candidate even if the pair is already recorded
as a bond.

The topology remains authoritative for recorded covalent bonds.
`build.get_disulfide_bonds` delegates to this detector and retains its
single-structure list-of-pairs result for build workflows;
`build.get_missing_bonds` continues to consume that entry point. The detector
has synthetic tests for geometry, selection, group filters, periodicity, frame
order, and already-recorded bonds. These tests validate the implementation of
the stated threshold rule; they do not independently establish chemical bond
identity. The disulfide API is Experimental in the public stability registry.

## Release boundary

No persistent `Interactions` data domain, generic contact classifier, or other
interaction family is part of this first slice. Client libraries can call the
family-specific APIs and should preserve method identity and units in any
presentation or derived analysis. Any shared result format or cross-system
contract requires a separate design decision.
