---
summary: NGLView copy and whole extraction invoke unsupported widget copying
issue: uibcdf/molsysmt#742
status: resolved
opened: 2026-11-13
closed: 2026-11-13
severity: medium
verification: reproduced
area: [form, extract]
guard: tests/form/nglview_NGLWidget/test_independent_copy.py
normative:
blocked_by: []
supersedes: []
---

# Restoring independent molecular copies of NGL widgets

## What

Public copy, unrestricted extraction and conversion back to nglview.NGLWidget
fail for valid single-component molecular widgets. The retained ipywidgets
provider raises NotImplementedError because its widgets cannot use Python's
ordinary copy protocol. This is a pre-1.0 functional defect in an optional form,
not a new graphical-session-cloning feature or a demonstrated data corruption.

## How

The NGL copy module imports copy.copy but decorates a function incorrectly named
extract. Its package therefore exports the imported standard-library function.
The unrestricted copied branch of the real extract module also calls copy.copy.
Six cases, three public routes under nm/ps and pm/fs policies, all reproduce the
provider refusal before a result can be inspected. The earlier aliasing concern
is not claimed as an observed mutation: copying fails first.

## Why

The common copy contract promises independent molecular data through supported
form operations. A widget needs explicit reconstruction with independent
communication and payload. The existing NGL-to-native and native-to-NGL seams
already provide the supported molecular conversion profile; duplicating a GUI
object or inferring new chemistry is not appropriate.

## Correction in progress — 2026-11-13

The adapter now exports a real validated copy function with an optional-provider
boundary. It materializes native molecular data with get_missing_bonds=False,
then constructs a new widget. Whole extraction delegates to it. Explicit
unrestricted reuse remains separate, and selected extraction retains the native
selected-axis route. No whole source copy is added merely to locate data.

The six independent-copy guards and one executable docstring pass. Guards cover
three structures, independent Comm/trajectory/array/topology storage, source
coordinates and frame preservation, declared bonds and both quantity policies.
Expanded reuse/selection controls, affected-cohort receiving, documentation and
final checks remain due. Camera, representations and browser session state are
not cloned; coordinates are materialized, not streamed or copied on write.

## Acceptance criteria

- All three supported public copied routes return independent molecular widgets.
- Source metadata, geometry, active structure and communication remain intact;
  mutation of copied storage does not affect the source.
- Units and the supported selected axes remain physically correct. Missing bonds
  are not inferred solely because a copy was requested.
- Explicit whole reuse remains opt-in and selected extraction keeps its existing
  canonical native atom order and requested structure order.
- Docstrings and User Guide/course/Cookbook explanations distinguish molecular
  payload copying from graphical session preservation and state memory limits.
- Preserve the failed baseline and the exact optional-provider/source profile;
  this work does not qualify a browser/platform, full native/source or installed
  final-pair gate.

## Evidence

The existing nine-form selected cohort has 243 passing cases with one expected
legacy H5MSM warning. The dedicated baseline has six provider refusals; after
correction the six controls and one executable docstring pass. Bounded service
limits remain one CPU, 1.5 GiB for tests, no own swap and a 6.5 GiB host reserve.
The remaining #727 documentation receiving is the next step after this repair.

The expanded NGL reception passes 28 cases, including the current adapter suite,
the independent molecular-copy guards, explicit whole reuse, selected native
atom/structure axes and the executable copy docstring. Source units, molecular
metadata, communication and active structure remain independent/preserved in
that retained provider composition.


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
