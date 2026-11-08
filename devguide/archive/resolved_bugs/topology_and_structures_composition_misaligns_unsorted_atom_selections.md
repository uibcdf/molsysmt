---
summary: Topology and Structures composition misaligns unsorted atom selections
issue: uibcdf/molsysmt#658
status: resolved
opened: 2026-11-08
closed: 2026-11-08
severity: high
verification: reproduced
area: [convert, basic]
guard: tests/basic/convert/mult_to_one/test_topology_structures_copy_policy.py
normative: devguide/forms_and_conversions.md
blocked_by: []
supersedes: []
---

# Two native domains disagree on the selected atom order

## What

Public `msm.convert([topology, structures], selection=[3, 0])` returns topology
atoms in ascending source order `[0, 3]` but coordinates in requested order
`[3, 0]`. The result can attach coordinates to the wrong atoms. Both input orders
and default/explicit copy policies are affected. Structure lists remain ordered
and may repeat; their axis must not be sorted together with atom positions.

## How

The private two-domain shortcut delegates separately to `Topology.extract` and
`Structures.extract`. The inventory extractor canonicalizes an atom subset;
the coordinate extractor preserves its supplied order. The shortcut forwards the
same unsorted request to both instead of first declaring their shared atom axis.
The native `MolSys.extract` path already uses the intended common sorted order.

## Why

This is data-integrity behavior, not merely a shape or copy-policy failure.
It was exposed by #656's adverse public-value test, after admitting that route's
missing `copy_if_all` keyword. The original default path has the same separate
extraction behavior; copy keyword admission changes no selected order.

## Evidence and intended correction

A monitored source counterexample retains six failures / nineteen passes,
including the default policy in both input orders. Topology reports names A/D
but coordinates are D/A (18 mismatched Cartesian values in each selected case).
A preceding directed attempt retained four corresponding failures before the
explicit default-policy controls were added. This is synthetic source evidence,
not a demonstrated corruption of a client's saved molecule.

Normalize the selected atom positions once before both existing domain extractors.
Keep source-index sorting, nonconsecutive/repeated **structure** order, independent
subsets and native single-owner rules. No new chemical, geometry or image algorithm
is introduced. Public permutation remains the operation for a requested atom order.

## Acceptance

Assert actual atom-label/coordinate correspondence with distinguishable atom
positions for unsorted subsets and complete permutations, not only shape/parity.
Exercise both input orders and all copy policies, source nonmutation, no invented
chemical state, empty selections and the existing full-axis conflict rejection.
Retain #656's independent copy-option regression and all failed attempts.


## Implemented correction and first receiving — 2026-11-08

The existing shortcut now sorts the selected source atom positions once before
both native extractors, matching Topology/MolSys subset semantics. It does not
sort structure indices or build an intermediate whole-system snapshot. #656
separately adds the missing copy keyword and passes it to Structures extraction;
Topology remains independent and native owner rules decide safe adoption.

The dirty integrated selection passes **247 tests**, including 37 new value/
identity/ownership controls. Unsorted subsets, complete permutations and empty
selections use both input orders and all three copy-policy choices; actual
coordinates are compared to source-indexed analytic values. Public coordinate
edits prove independence versus explicitly requested unowned-domain adoption.
The existing full-axis and malformed-option rejections stay effective. Clean
receiving and public delivery remain pending.


## Resolution — 2026-11-08

**Contract-tested and bounded Parity-tested.** Clean implementation
`35ad4bc59` passes **247 tests**, including all 37 new selected-value and actual
coordinate-edit/ownership cases, conversion doctests, argument admission, partial
domains and Viewer composition. Fourteen fast gates and Sphinx HTML pass on that
same clean source. Five rendered pages are inspected; existing code cells and
saved outputs in all three affected notebooks remain unchanged. Six inherited
HTML title warnings are retained. The
[portable receipt](../../../devtools/data/native_composition_receiving_656_658_20261108.json)
keeps every failure and source/runtime/resource manifest, not only the passing run.

The two-domain shortcut admits the copy option, keeps Topology independent,
passes the policy to Structures extraction and normalizes the shared atom axis
before both existing extractors. It does not add a whole-system intermediate
snapshot, new scientific algorithm, engine, file schema or native binary.
All 8,598 source and 2,463 Viewer-export input hashes remain unchanged during
final receiving. Peak source-test charged memory is 822,231,040 bytes; the HTML
build peaks at 1,332,137,984 bytes. Host availability stays above 15 GiB decimal,
without cap/OOM/reserve/pressure stops under monitored one-CPU/two-GiB units.

The guard checks labeled atom-to-coordinate values, both item orders, subsets,
complete permutations, typed empties, requested structure order/repetitions,
default/True/False ownership and actual mutation consequences. Plausible shapes
or distinct object identities alone cannot satisfy those assertions.

No original saved result is silently repaired. Recreate composites made with
unsorted atom selections from their original aligned domains. Source-version
identity (#657), mechanics persistence (#256) and frozen release qualification
retain their separate owners and scope. This adds no graphical intent or weight.
