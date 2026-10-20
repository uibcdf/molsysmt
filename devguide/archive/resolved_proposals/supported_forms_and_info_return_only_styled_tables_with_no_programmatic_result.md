---
summary: Offer programmatic results for supported capability reports.
issue: uibcdf/molsysmt#188
status: resolved
opened: 2026-08-19
closed: 2026-10-20
verification: measured
area: [api, basic]
guard: tests/supported/test_programmatic_reports.py
normative:
blocked_by: []
supersedes: []
---

# Programmatic capability reports

**Reported:** 2026-08-19 external audit; selected by the maintainer on 2026-10-20.
**Status:** Resolved with preserved visual defaults and documented programmatic outputs.

## What

Add keyword-only output_type and skip_digestion to supported.forms, conversions,
syntaxes and dependencies. Retain their styled default and all existing positional
filters. Forms additionally returns a name list. DataFrame/dictionary outputs
expose the data without constructing a Styler.

The original report also named info. At the 2026-10-20 source checkpoint, info
already supports dataframe and dictionary output (the latter is a list of records).
It requires no new return path and retains that distinct existing contract.
The historical 89-form count described the August audit, not the current registry.

## How

Public boundaries use ArgDigest with caller-specific output/filter contracts.
Each report builds its existing table once, then returns it, a detached
index/columns/data dictionary, or its visual wrapper. Forms lists retain table
order. Raw Info values are detached from adapter metadata; HTML link formatting
belongs only to rendering. Dictionary axes reconstruct the table with
pandas.DataFrame(**record), including nonconsecutive row labels.

Conversion matrices retain Boolean type, declared edges, sorted axes, orientation
and filter precedence. Empty filters retain the opposite requested axis and
repeated names are deduplicated, as with the former dict-based construction.
Unknown explicit form filters retain false entries rather than certifying a route.
The compatibility syntax-registry module forwards the new keyword arguments.

## Why

Public enumeration must work in scripts and downstream libraries without reaching
into Styler.data or private tier registries. Capability declarations are distinct
from optional-provider availability, input admission and conversion fidelity.
This adds a useful return path, not a new capability classifier or loader.

## What is measured and what is assumed

The original August audit reproduced TypeError from len(supported.forms()). The
new public list is compared against the complete authoritative FORM_TIERS roster,
without preserving a historical count in a second registry. Programmatic frames
and dictionaries are compared with visual data and literal native conversion
edges; returned metadata is actually mutated to test isolation.

There is no performance benchmark claim. A guard prevents Styler construction
on every programmatic route. No molecular coordinates or provider calculations
are needed for these reports. Existing metadata/conversion registry discovery
remains the owner; cache/performance redesign is excluded.

## What was refuted

- Changing info again would duplicate a delivered feature.
- Styler.data is not needed as a public enumeration route.
- Returning a matrix as unlabelled nested lists would lose its axes.
- A true conversion entry is not a guarantee that every input/provider can run it.
- Fixed adapter counts would become another stale source of truth.

## Scope and exclusions

Four capability reports, validation, dictionary shape, metadata isolation,
defined empty matrices and preserved visual defaults. No new dependencies,
scientific methods, form visibility policy, eager-loading redesign or tier changes.
Native copy protocols and fast-path redesign remain deferred for prior study.

## Acceptance criteria

Public enumeration equals the registry; all four output tables preserve data,
axes and filters; invalid inputs have actionable errors; syntax compatibility
imports retain the callable report; no Styler is constructed for data output;
examples/docstrings, Foundations, Toolbox, Cookbook and Common Core 01 are updated.

## Provenance

Original audit: Linux/Python 3.13.14, pandas 2.3.3, 2026-08-19.
Implementation checks: Linux, existing development Python 3.14.7, 2026-10-20.

## Resolution and validation

**Contract-tested:** 80 tests pass with
`python -m pytest tests/supported tests/test_argument_contract.py
 tests/test_form_plugin_conventions.py tests/_private/test_form_tier.py
 tests/basic/select/test_syntax_capabilities.py -n 12 --receptor=llm`.
The four new public doctests pass. A targeted guard forbids DataFrame.style
access on programmatic calls. Other controls assert actual declared edges,
registry equality, metadata isolation after mutation, orientation, empty axes,
filter behavior and compatibility after importing the old syntax module.

All fourteen fast release checks, docstring fidelity, whole-repository Ruff
lint/format and the signature guard pass (four accepted extensions). The new
Toolbox page's Python blocks are executed. Foundations, Cookbook and Common
Core 01 include executed sections reporting the public roster (96 forms at this
checkpoint) and the declared MolSys-to-Topology edge. Older cells, outputs and
metadata are unchanged; missing IDs in the older course notebook are assigned
in the 4.5 notebook schema. The complete new Toolbox/API pages and added notebook
sections render without Sphinx diagnostics. Paired contracts and manifest agree.

No form count is frozen into runtime logic or an authoritative second table.
These source checks do not qualify replacement release artifacts. The supported
module remains experimental, and existing info output semantics are unchanged.
