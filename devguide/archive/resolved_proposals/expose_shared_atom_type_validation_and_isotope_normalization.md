---
summary: Expose shared atom type validation and isotope normalization
issue: uibcdf/molsysmt#296
status: resolved
opened: 2026-10-02
closed: 2026-10-02
verification: reproduced
area: [api, attribute]
guard: tests/element/atom/test_atom_types.py
normative: devguide/api_surface.md
blocked_by: []
supersedes: []
---

# Expose shared atom type validation and isotope normalization

**Reported:** 2026-10-02, maintainer-approved modularity review of native SDF tools.
**Status:** Resolved. The approved public tools are implemented and contract-tested.

## What

Expose `element.atom.is_atom_type` and `element.atom.normalize_atom_types` as
general value tools. Use MolSysMT's established `atom_type` terminology for
chemical element symbols. Atom names and force-field/AutoDock labels have
different semantics and must not be implicitly interpreted as elements.

## How

A lightweight private primitive owns the canonical 118-symbol inventory and
explicit D/T normalization. Public digested wrappers define scalar and batch
contracts, nullable mass-number handling, input alignment and typed errors.
The native SDF reader calls the primitive directly and retains its CTAB-specific
reference-isotope table and format diagnostics.

## Why

The modularity review of uibcdf/molsysmt#215 identified explicit symbol and
isotope handling embedded in CTAB reading. General tools let other parsers,
builders and client workflows use the same behavior without depending on an
SDF implementation or an optional toolkit.

## What is measured and what is assumed

**Implemented:** public exports, private primitive reuse and explicit digestion.
**Contract-tested:** canonical versus noncanonical symbols, all 118 elements,
D/T aliases, isotope conflicts, missing values, scalar/batch shape, invalid
containers and source immutability. SDF fixtures cover the consuming parser.
No performance benchmark or chemical perception claim is made.

## What was refuted

Automatic capitalization would reinterpret alpha-carbon names such as CA as
calcium. Atom-name inference and force-field mappings therefore remain separate.
Reference isotopes in V2000 mass-difference fields are a format convention and
are not promoted to a general atomic-mass or isotope-stability API.

## Scope and exclusions

No global change to accepted stored atom labels, atomic-number API, CIP
assignment, sanitization, PDBQT adapter or force-field atom typing. Dummy labels
can exist in models but do not pass a check for a genuine chemical element.

## Acceptance criteria

Both functions use arg_digest and skip_digestion. The SDF reader shares the
same explicit normalization core. Docstrings, Toolbox, Foundations, Cookbook,
course and the symbol registry describe the exact contracts. Regressions fail
in `tests/element/atom/test_atom_types.py` and the native SDF tests.

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
