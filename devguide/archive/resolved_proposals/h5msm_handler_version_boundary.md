---
summary: Clarify H5MSM 0.5 file-handler capability and rejection diagnostics.
issue: uibcdf/molsysmt#411
status: resolved
opened: 2026-10-22
closed: 2026-10-22
verification: reproduced
area: [form, convert]
guard: tests/basic/convert/one_to_one/test_h5msm_handler_version_boundary.py::test_modular_handler_rejected_before_domain_loading
normative:
blocked_by: []
supersedes: []
---

# H5MSM file-handler version boundary

**Reported:** 2026-10-22, while qualifying removal ownership (#406).
**Status:** Resolved and locally contract-tested.

## What

Requesting `msm.convert(path, to_form="molsysmt.H5MSMFileHandler")` for
H5MSM 0.5 previously materialized the file as MolSys and then reported an
unsupported conversion from MolSys. Preserve the supported version boundary
and report the actual unsupported file-version/handler combination instead.

## How

A private conversion-boundary check inspects only the root version attribute
when a legacy handler is requested. It checks complementary input lists and
multiple-output requests before any modular domain reader is invoked. It
raises the existing catalogued `FormatError`, explaining that the handler
supports 0.3/0.4 and naming resident `convert` and selected-domain `read_layers`
alternatives. The direct constructor uses the same recovery message for 0.5
and closes the rejected file. Other unsupported-version diagnostics remain
unchanged. Ordinary resident conversions do not perform this extra check.

## Why

Users should not interpret a generic MolSys conversion failure as a defect
in resident 0.5 loading. A new file-backed reader is a separate capability,
not a prerequisite for this diagnostic improvement or for 1.0.

## What is measured and what is assumed

The focused command is:

```bash
python -m pytest tests/basic/convert/one_to_one/test_h5msm_handler_version_boundary.py tests/basic/convert/one_to_one/test_h5msm05_load_ownership.py tests/native/test_h5msm_file_handler.py --receptor=llm -n 12
```

It passes 45 cases. The new guards use valid synthetic 0.5 files and forbid
the materializing reader; an attribute-only HDF5 file is not a valid public
molecular-system input and is rejected by argument validation first. Root
versions stored as text and bytes, string/Path inputs, single/composite
inputs and multiple targets are covered. Legacy 0.3/0.4 conversion still
opens its handler, and direct 0.5 rejection leaves its file handle closed.
Existing resident-load guards retain all supported partial domain combinations.

The convert doctest passes and docstring validation passes all 247 public
functions. The 14 fast release gates and package-wide Ruff checks pass.
Both updated notebooks execute in temporary copies with unchanged code cells.
The first convert notebook execution failed because the isolated documentation
fixture lacked the existing static views; linking those assets allows the
unchanged notebook to complete. A focused five-page plus API Sphinx build
succeeds with 60 warnings from missing global context and inherited markup;
this does not claim a warning-free full documentation build. All six HTML
pages contain the supported-version and rejection statements.
This is contract evidence, not a streaming benchmark.

The combined affected command passes 138 cases:

```bash
python -m pytest tests/physchem/test_chemical_template_context.py tests/physchem/test_normalize_aromatic_bond_orders.py tests/physchem/test_chemical_preparation_evidence.py tests/heavy/test_native_modular_sources.py tests/test_argument_contract.py tests/test_form_plugin_conventions.py tests/interactions/test_h5msm05.py tests/basic/convert/one_to_one/test_h5msm_handler_version_boundary.py tests/native/test_chemical_states.py --receptor=llm -n 12
```

The final complete command `python -m pytest --receptor=llm -n 12` passes
**15,066 cases with two skips**, exit 0, in 416.96 seconds (1,726 warnings,
52 warning groups). The skips are the CuPy path without CuPy and the
without-RDKit SMILES fallback when RDKit is present. This is a local
Linux/Python 3.14 development result, not a platform matrix or installed-pair
qualification. Source includes the combined #411/#414–#417 repairs.

## What was refuted

The initial report claimed the direct handler could open 0.5. Inspection and
reproduction refute that claim: it already rejects 0.5 and supports only
0.3/0.4. Its rejection now explains the recovery path consistently.
Implementing a new 0.5 streaming handler would exceed the requested scope.

## Scope and exclusions

No new file schema, handler capability, dependency, public argument or
exception class. Selected-layer reads still materialize their requested
payloads. No public lazy 0.5 trajectory reader is claimed. Standalone
conversion-report planning remains a separate route; this change concerns
executed conversion rejection. Missing files, invalid molecular-system inputs
and other errors retain their own validation paths.

## Acceptance criteria

The public conversion names the 0.5/legacy-handler incompatibility without
reading domains; the constructor closes rejected files; supported legacy
handlers and resident modular loads remain operational. User Guide,
Cookbook, convert tutorial, docstring and shared native-forms course module
explain the same boundary.

## Provenance

Linux, Python 3.14.7, current development environment, 2026-10-22. Source
baseline `70103677841fba359c7e1ca9b092d04d41e5807e` plus this recorded change.
