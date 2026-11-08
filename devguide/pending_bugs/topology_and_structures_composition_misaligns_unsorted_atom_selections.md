---
summary: Topology and Structures composition misaligns unsorted atom selections
issue: uibcdf/molsysmt#658
status: active
opened: 2026-11-08
closed:
severity: high
verification: reproduced
area: [convert, basic]
guard:
normative:
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
