# Tests Agents Guide

This guide is for agents and contributors writing or editing tests under `tests/`.
It refines the global testing rules in the repository root `AGENTS.md`.

## Language and framework

- Keep all test module docstrings and comments in English.
- Use `pytest` as the testing framework; rely on its fixtures, parametrization, and markers instead of custom harnesses.

## Layout and naming

- Place tests in the existing directory that mirrors the package area (for example, `tests/pbc` for `molsysmt/pbc`, `tests/form` for `molsysmt/form`).
- Test files should be named `test_*.py`; group related tests in subdirectories where this is already the pattern (for example, `tests/pbc/get_lengths_and_angles_from_box/test_*.py`).
- Use descriptive test function names that reflect the behavior under test (for example, `test_get_lengths_and_angles_from_box_cubic_geometry`).

## Data, fixtures, and determinism

- Prefer bundled systems from `molsysmt.systems` and small synthetic arrays over external or ad hoc data.
- Keep tests deterministic: avoid reliance on network access, random seeds without control, or non-reproducible external state.
- Mark truly slow or optional tests with appropriate pytest markers if needed (for example, `@pytest.mark.slow`), and avoid making the default test suite excessively long.

## Assertions, units, and shapes

- When testing numerical behavior, assert both values and units where relevant.
  - Coordinates and distances: nanometers.
  - Box lengths: nanometers; angles in radians internally (but tests may convert to degrees via `pyunitwizard` when appropriate).
  - Time: picoseconds.
  - Charges: elementary charge units.
- Check array shapes explicitly for key attributes (for example, coordinates `(n_structures, n_atoms, 3)`, box `(n_structures, 3, 3)`).
- For converters and forms, verify integrity of topology (numbers of atoms, bonds, groups, chains, entities) in addition to shapes.

## Scope of tests

- Aim for focused tests that validate one behavior at a time (a single public function or a clearly defined scenario).
- Prefer testing public APIs (for example, `molsysmt.get`, form converters) rather than internal helper functions, unless the helper encapsulates critical logic with no public equivalent.
- When adding new functionality, add or update tests in the closest relevant existing test module rather than creating parallel structures.

## Safety and maintenance

- Avoid tests that depend on external services or write outside the repository (no network, no user directories).
- Keep test code clear and idiomatic; do not introduce unnecessary indirection or metaprogramming.
- When changing behavior, update tests to reflect the intended semantics rather than weakening assertions, unless the previous expectations were clearly incorrect.
