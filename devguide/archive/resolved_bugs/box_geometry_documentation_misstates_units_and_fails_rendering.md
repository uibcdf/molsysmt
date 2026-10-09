---
summary: Box geometry documentation misstates units and fails rendering
issue: uibcdf/molsysmt#358
status: resolved
opened: 2026-10-09
closed: 2026-10-09
severity: low
verification: reproduced
area: [docs, units]
guard: devtools/tests/test_public_api_docs.py::test_box_geometry_docstring_renders_without_rst_errors
normative: docs/content/user/foundations/governance/quantities_and_units.md
blocked_by: []
supersedes: []
---

# Box geometry documentation misstates units and fails rendering

**Reported:** 2026-10-09 during the maintainer-requested audit of deferred issues.
**Status:** Resolved; rendering and return-unit documentation agree with the implementation.

## What

`get_lengths_and_angles_from_box` promises lengths in input units and angles
in radians. Its implementation correctly standardizes both output quantities to
the active PyUnitWizard policy. In addition, unescaped `|v0|`, `|v1|` and `|v2|`
are interpreted as substitutions when rendering the API, producing three errors.

## How

Rendering the actual public NumPy docstring through Sphinx Napoleon and Docutils
on source `e2de5f88c` reports three undefined substitutions and a definition-list
warning. This confirms the bounded public-API rendering defect already listed
in the broader uibcdf/molsysmt#144 warning inventory. The two calls to
`puw.standardize` establish the correct length/angle policy boundary, analogous
to the corrected dihedral contract under uibcdf/molsysmt#357.

## Why

An included geometry API must render its vector/angle definitions accurately
and describe the units returned under an application/user policy. This does
not justify admitting global Sphinx cleanup or changing numerical behavior.

## Scope and exclusions

Correct this function's NumPy docstring and examples, and corresponding
Foundations, Toolbox, Cookbook and unit-safety course explanations. Verify
nondefault-unit output against analytical geometry and build a bounded actual
Sphinx API page. Existing six-decimal rounding, Rust kernels, defaults,
candidate files and publication pause remain unchanged. The broader #144
warning population remains owned by that partial post-1.0 issue.

## Acceptance criteria

- The actual API page renders without warnings or errors.
- Row-vector conventions and alpha/beta/gamma column order are explicit.
- Both returned quantities follow the active unit policy.
- Analytical triclinic geometry agrees under pm/degrees and nm/radians policies.
- Public doctests and existing box geometry controls pass.

## Provenance

Linux, shared development environment, Python 3.14.7, PyUnitWizard
`0.28.1+3.g2ab37a5`, Sphinx 9.1.0; 2026-10-09.

## Resolution and executed evidence — 2026-10-09

Replace the malformed nested return list with two proper NumPy-style return
entries. Vector norms are written as ordinary text with literal vector names.
The unit policy, row-vector conventions, angular ordering and existing six-decimal
rounding are explicit. Add a real executable quantity example; corresponding
User Guide/course changes are narrative only.

The new rendering guard builds an actual one-page Sphinx HTML reference with
Autodoc and Napoleon, warning-as-error enabled. In an isolated process,
substituting only the original public docstring makes this same guard fail:
one definition-list warning and three undefined-substitution errors. This
controlled failure does not modify repository or installed source files.
With the corrected docstring, the page builds without Sphinx warnings/errors.
The guard verifies rendering, not scientific accuracy; two analytical triclinic
controls separately verify units, lengths, angle ordering and policy restoration.

```bash
python -m pytest devtools/tests/test_public_api_docs.py tests/pbc/get_lengths_and_angles_from_box/test_active_unit_policy.py molsysmt/pbc/get_lengths_and_angles_from_box.py --doctest-modules --receptor=llm -n12
python -m pytest tests/interactions/hbonds/test_buch_results.py tests/interactions/hbonds/test_luzard_chandler_results.py devtools/tests/test_nightly_full_gate.py tests/pbc/get_lengths_and_angles_from_box tests/pbc/get_box_from_lengths_and_angles --receptor=llm -n12
```

Results: **5 passed** in the first selection and **57 passed** in the second
(overlapping by the two unit controls). The first includes two reference guards,
two analytical controls and one public doctest. Sphinx emits two upstream
`RemovedInSphinx11Warning` Python deprecations outside page diagnostics; the actual
page warning/error stream is empty. Existing bundled 0.4 fixtures emit four
expected deprecation warnings in the second selection. No full-site rebuild or
new installed-candidate qualification is claimed.

Repository-wide Ruff lint/formatting and all fourteen fast release gates pass.
AST comparison confirms unchanged computation; notebook code and saved outputs
remain unchanged. Normal public argument validation supplies nanometer boxes,
so documented rounding is in nanometers/radians before output standardization.
