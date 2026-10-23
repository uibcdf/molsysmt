---
summary: compare rejects derived box attribute switches
issue: uibcdf/molsysmt#437
status: resolved
opened: 2026-10-23
closed: 2026-10-23
severity: low
verification: reproduced
area: [basic, argdigest, units]
guard: tests/basic/compare/test_compare_structural.py::test_explicit_derived_box_switches_and_physical_values_are_distinct
normative:
blocked_by: []
supersedes: []
---

# Comparing explicitly selected box attributes

**Reported:** 2026-10-23, through the quantity comparisons added for #435.
**Status:** Resolved; explicit box selectors pass boolean query validation.

## What

`msm.compare(molsys, molsys, box_lengths=True)` rejects the boolean switch before
the comparison kernel. The same caller mismatch affects `box_angles` and
`box_volume`. These are declared comparable attributes; selecting the structural
category reaches them while an explicit query fails.

## How

The three argument digestors recognize `molsysmt.basic.get.get` as a boolean
attribute query but omit `molsysmt.basic.compare.compare`. Length/angle selectors
therefore enter physical-value validation; volume rejects its unrecognized caller.

## Why

Public callers and the bound MolSysViewer comparison tool cannot request these
attributes explicitly. This is an argument-boundary defect, separate from #435's
implicit quantity downcast. No scientific result corruption is established.

## Evidence and correction

Five of the new physical comparison cases initially fail before the kernel on
`box_lengths=True`; the separate real full-category case reproduces #435.
The fix adds the comparison caller only to the boolean query branches. Geometry
and setter callers retain physical-value checks. Three independent selector
cases require successful equality and reject a physical quantity supplied where
a boolean selector belongs.

Guard: `tests/basic/compare/test_compare_structural.py`.
Related provider work: uibcdf/molsysmt#435 and uibcdf/molsysmt#421.

## Resolution — 2026-10-23

The length, angle and volume digestors recognize compare as a boolean query
caller. Physical geometry/setter validation is unchanged. The guard separately
selects each of the three attributes and rejects a physical quantity supplied
as a selector. All 179 comparison/PBC/argument/bound-predicate cases pass with
12 workers and pytest-receptor, including unit conversion and warning guards
owned by #435. Documentation and course examples execute the explicit switches.
No public signature, dependency or format is changed.
