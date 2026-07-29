# F4 Documentation Lifecycle Checkpoint

**Date:** 2026-07-29
**Stage:** F4 — User Guide, Cookbook, API, demos, and course lifecycle closure
**Status:** `DONE`

## Scope and decision

F4 closes the documentation obligations created by the pre-1.0 conversion,
chemical-state, PDB, H5MSM, and Rust-only work. It does not redefine F2 notebook
execution, nor does it require pre-existing documentation warnings to disappear
before the source release.

The release distinction is explicit:

- affected public behavior must have synchronized docstrings, User Guide or
  Cookbook coverage, course coverage, and executable evidence;
- broken navigation introduced or exposed by the current work is fixed;
- broader historical warning debt is measured and tracked rather than hidden or
  promoted wholesale into the 1.0 critical path.

## Evidence inherited from F2

F2 executed the complete 40-notebook lifecycle scope from fresh kernels on exact
commit `2f6fd59d1`: all 20 Common Core notebooks plus the five affected notebooks
in each Path. It also executed the changed User Guide notebooks for `extract`,
`merge`, and `set`.

No public behavior changed in F3 or in this F4 cleanup. The only new executable
test in F4 guards an already-shipped internal Rust contract: broadcasting a
size-one dihedral target row on both vacuum and periodic paths.

## Course closure

The two final editorial artifacts from the course renumbering were resolved:

- Common Core 12 no longer promises a nonexistent Sequences module and links to
  `{ref}``course-core-iterating-over-hierarchies``;
- Common Core 17 no longer sends the learner back to Module 17 and links to
  `{ref}``course-core-merging-and-growing-systems`` before Path selection.

`course_module_numbering_overlaps.md` is archived as resolved. The course
validator still reports 156 consistent notebooks, and Sphinx reports no
unreadable course toctree target or unresolved reference to either new semantic
label.

## Rust lifecycle residue

The bounded Numba-to-Rust residue is complete:

- the missing dihedral broadcast regression covers three structures on both
  vacuum and periodic paths;
- Rust and Python comments describe Numba as the replaced implementation;
- live references point to archived migration records;
- `rust/README.md` describes the permanent `rust/` crate, private
  `molsysmt._rust` extension, Rust-only runtime, and current tests.

Focused evidence: seven Python tests pass, all 80 Rust unit tests pass, and Ruff
passes.

## API, User Guide, Cookbook, and demos

The full Sphinx build regenerated ten checked-in native/H5MSM autosummary pages.
They now list the current chemical-state, bond-metadata, structural, and
thermodynamic getter/setter surfaces.

The build exposed and F4 repaired all 11 references to nonexistent documents in
the API, Showcase, and User Guide toctrees. An incremental rebuild confirms zero
remaining `toc.not_readable` warnings.

Demo and fixture integrity remains an executable release gate through
`validate_demo_assets.py`; resource integrity is covered separately by
`validate_resources.py`. No demo payload had to be rebuilt in F4 because the
current manifests and H5MSM fixtures validate.

## Warning debt

The forced Sphinx build succeeds but is not globally warning-clean. Before the
bounded navigation repairs it recorded 1,223 warnings, dominated by historical
heading, title, orphan-page, cross-reference, and stale autosummary debt. The
complete classification and remediation plan are in
`pending_bugs/sphinx_warning_baseline_and_api_reference_debt.md`.

This debt is accepted for the source release because the required course
structure is warning-clean, affected workflows are synchronized and executable,
and the remaining families predate the release work. No warning was suppressed.

## Verification

- `python -m pytest --receptor=llm
  tests/lib/test_dihedral_and_axes_kernels.py
  tests/lib/test_advanced_pbc_and_mic_kernels.py` → 7 passed;
- `cargo test --manifest-path rust/Cargo.toml --no-default-features` → 80 passed;
- `ruff check molsysmt tests/lib/test_dihedral_and_axes_kernels.py` → passed;
- `python devtools/scripts/validate_course.py` → 156 notebooks consistent;
- `python devtools/scripts/validate_devguide.py` → passed;
- forced Sphinx build → exit 0;
- post-repair incremental Sphinx build → exit 0, zero `toc.not_readable`.

## Closure

F4 is complete. F5 is the next active stage: land a clean exact commit and run
the fast gate, Ruff, full Python 3.11–3.13 platform matrix, installed-wheel
checks, and documentation workflow on that candidate. Formal weighted completion
remains 90% until the complete Segment F exit gate closes; stage completion is
not converted into partial segment credit.
