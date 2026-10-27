---
summary: Expose unit-aware Zimmerman bulkiness reference lookup
issue: uibcdf/molsysmt#487
status: resolved
opened: 2026-10-26
closed: 2026-10-26
verification: measured
area: [physchem, api, units]
guard: tests/physchem/test_get_bulkiness.py::test_bulkiness_curation_and_configured_area_units
normative:
blocked_by: []
supersedes: []
---

# Exposing unit-aware Zimmerman bulkiness reference lookup

## What

Implement the maintainer-approved first candidate from uibcdf/molsysmt#485 as
`physchem.get_bulkiness`. Reuse the unchanged twenty-entry Zimmerman table and
return PyUnitWizard-standardized area quantities. The descriptor is a name-based
reference lookup, not a conformational surface measurement or chemical validator.

## How

The form-agnostic reader obtains selected group names through basic.get and
uses the existing shared table helper. Its new private allow_placeholders=False
mode rejects unlisted DUM/X values without changing legacy readers' default
neutral-dummy behavior. Numeric selections retain order/repetitions; unsupported
populations fail before selection. Empty results retain a floating quantity axis.

The reader has ArgDigest/skip_digestion and definition validation. Units start
from angstrom² and standardize through the active PyUnitWizard policy. Offline
bibliographic records identify Zimmerman (1968) as reference-scale source and
Proust et al. (2019), Table 1, as the explicit later area interpretation. Existing
lazy optional Ackredit boundaries track once per successful/empty call; failures
and absent providers preserve completed science and unsupported groups do not
credit a completed lookup. No provider software execution is claimed.

## Why and scientific boundary

The existing table matches all twenty AAindex1 ZIMJ680102 and official ProtScale
entries. The original 1968 full-text derivation/normalization has not been
re-audited. Later original research explicitly uses the descriptor as an area.
The supported contract is that bounded reference lookup, not reconstructed
geometry or arbitrary group chemistry. Experimental API classification and
partial scientific evidence retain that limitation.

Source identities and reviewed values/units are in
[the candidate review](../../../devtools/data/zimmerman_bulkiness_review_20261026.json).

## Acceptance criteria

Independent reference values, squared-unit conversions under nm/angstrom/pm,
four input forms, repeated/empty/string selections, strict unsupported-name
errors, detached values and unchanged domains must pass. Protect existing helper
callers with a regression selection, and qualify optional attribution absence,
provider failure and real enclosing-session reuse. Update the User Guide,
Cookbook, shared/four-path course, docstring and both maintained registries.

## Scope and exclusions

No new data table or scientific dependency, coordinate read, native storage,
force-field calculation, automatic molecular aggregation, Rust kernel, Viewer
addon contract or release publication. Wider observable exploration and remaining
original-source review stay in uibcdf/molsysmt#485. This change does not close
Collantes ISA/ECI reviews under uibcdf/molsysmt#473/#475.

## Resolution and local qualification

The reader and its lifecycle are complete as an experimental public capability.
The new reference tutorial, explicit-unit export recipe, Foundations, API page,
shared Module 20 and four path-specific Module 39 pages document strict group
scope, quantities, attribution and the partial scientific boundary. The twenty
table entries remain unchanged by AST comparison; helper defaults remain covered.

The final broad physchem/reference/Viewer-table regression and new doctest pass
**1,407 tests in 75.33 seconds**, using twelve workers and pytest-receptor. There
are 171 expected legacy-H5MSM warnings, 31 existing object-downcasting warnings
and six deliberate unsupported-GPU diagnostics. New missing-name/coordinates-only
and single-index controls are included. The new tutorial executes cleanly in
9.0 seconds; the standalone Cookbook block also executes. All five course updates
retain executable cells, outputs and metadata.

All 492 raw notebook-schema cases pass (7.50 seconds); 252 public docstrings,
signature checks, selected Ruff and dependency audits pass, as do fourteen fast
release gates. The final incremental HTML build has zero errors and seventeen
existing warnings under uibcdf/molsysmt#144, with no diagnostic on either new
page. Incremental counts are not compared as a warning-debt benchmark.

An initial test-authoring assertion caught ArgumentError instead of the existing
separate ArgumentChoiceError; it was corrected without weakening the actual
element/error semantics. A doctest now rounds its displayed values because the
Å²/nm² round trip exposes ordinary floating-point precision; numerical tests
retain strict 1e-12 absolute tolerances. Neither is scientific defect evidence.

The guard compares actual selected quantities to independently transcribed
curation values, units, shapes and ordering across four input forms and three
unit policies. The governed scientific test separately protects bounded
ALA/GLY/TRP reference values; partial evidence does not claim the original
geometric derivation was reproduced.

Exact source/environment/checks are in
[the implementation receipt](../../../devtools/data/zimmerman_bulkiness_implementation_20261026.json).
This is local Linux/Python 3.14.7 source qualification, not cross-platform, full
scientific-suite, installed-pair or publication evidence. Wider candidates and
remaining original-source questions stay in uibcdf/molsysmt#485.
