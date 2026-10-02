---
summary: Expose read only conversion preflight reports
issue: uibcdf/molsysmt#297
status: resolved
opened: 2026-10-02
closed: 2026-10-02
verification: reproduced
area: [api, basic, convert]
guard: tests/basic/test_get_conversion_report.py
normative: devguide/api_surface.md
blocked_by: []
supersedes: []
---

# Expose read only conversion preflight reports

**Reported:** 2026-10-02, maintainer-approved modularity review of native SDF tools.
**Status:** Resolved. The approved public tools are implemented and contract-tested.

## What

Expose `basic.get_conversion_report`, with its usual root alias, to inspect
conversion losses without invoking the requested conversion or writing its
destination. Preserve the existing `ConversionReport` result contract.

## How

The public digested function normalizes source forms and validates explicit
structure indices using existing tools. It calls the same private audit core
already used by convert(strict=True) and convert(return_report=True). A flat
list of targets produces ordered reports; filenames also accept pathlib.Path.

## Why

Preflight existed internally but users had to request a real conversion to
obtain it. SDF loss authorization makes the missing standalone operation
particularly visible. The query separates inspection from destination writes
while keeping one audit implementation.

## What is measured and what is assumed

**Implemented:** public query, form-agnostic dispatch and shared audit reuse.
**Parity-tested:** reports equal those returned by actual conversions for native
objects, SDF sources, selections and composed sources. Tests assert no source
mutation or destination creation/overwrite. No new exhaustive coverage is claimed.

## What was refuted

Calling convert and deleting its output would still write files and pay for a
full conversion. A separate auditing implementation would drift from strict
mode. Both are avoided by sharing the existing private preflight core.

## Scope and exclusions

No promise of converter availability, optional dependencies, write feasibility
or exhaustive audit for every pair. Converter-specific options remain owned by
convert; querying SD property loss does not authorize its discard. No PDBQT
adapter or new audit profiles are introduced here.

## Acceptance criteria

The public query supports form/path targets, atom/frame selections and ordered
target lists without destination writes. It uses existing argdigest and index
validation. API examples, Toolbox, Cookbook, course and the stability registry
state the coverage limits. `tests/basic/test_get_conversion_report.py` guards
parity and read-only behavior.

## Resolution — 2026-10-02

Accepted and implemented. The executable guard named above protects the new
public behavior; the normative API surface and symbol registry record ownership
and experimental stability. Docstrings, API catalogs, Toolbox, Foundations,
Cookbook and relevant course modules are synchronized.

Validation checkpoint on Linux / the local Python 3.13 Conda environment:

- The combined SDF, public atom/report tools, report audits, argument contracts
  and doctest-shadowing selection passed 390 tests, including the three new
  public-function doctests.
- The final public-tool and doctest selection passed 59 tests, including an
  additional regression proving that the existing nullable-Series isotope
  setter remains supported. This overlaps the broader selection, not an
  additional 59 independent tests.
- Ruff, dependency validation, public docstring validation (223 functions),
  API registry validation and the maintained course-structure check passed.
- The Foundations attribute notebook executed successfully. Course changes
  are prose-only; their code and saved outputs were preserved.
- The HTML documentation build completed. The final incremental build emitted
  17 existing warnings, with none mentioning the new tools or pages. This is
  not a claim of a warning-free documentation tree.

Commands:

```bash
python -m pytest --receptor=llm --doctest-modules molsysmt/element/atom/is_atom_type.py molsysmt/element/atom/normalize_atom_types.py molsysmt/basic/get_conversion_report.py tests/element/atom/test_atom_types.py tests/basic/test_get_conversion_report.py tests/form/file_sdf tests/_private/test_conversion_report_scopes.py tests/_private/test_conversion_fidelity_audit.py tests/_private/test_doctest_module_shadowing.py tests/test_argument_contract.py
python -m pytest --receptor=llm --doctest-modules molsysmt/element/atom/is_atom_type.py molsysmt/element/atom/normalize_atom_types.py molsysmt/basic/get_conversion_report.py tests/element/atom/test_atom_types.py tests/basic/test_get_conversion_report.py
ruff check molsysmt
python devtools/scripts/validate_dependencies.py
python devtools/scripts/validate_docstrings.py
python devtools/scripts/validate_api_stability.py
python devtools/scripts/validate_course.py
python docs/execute_notebooks.py -q -f docs/content/user/foundations/molecular_system/attributes.ipynb
make -C docs html SPHINXOPTS='-q -j 12'
```

The work leaves uibcdf/molsysmt#215 partial for faithful native stereo support
and does not implement the pending PDBQT forms in uibcdf/molsysmt#214.
