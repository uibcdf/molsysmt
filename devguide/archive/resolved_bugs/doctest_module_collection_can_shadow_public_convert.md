# Bug: doctest module collection can shadow the public `convert` symbol

> Archived resolution record. This document describes the defect as originally
> diagnosed and how it was resolved; current behavior is defined by code, the
> repository-root `conftest.py`, and the regression test.

**Status:** resolved 2026-07-21
**Severity:** low — test-collection artifact only; no production code path and no
end-user import is affected. The default `pytest` gate was already green.
**Fix:** repository-root `conftest.py` (`pytest_configure`), no library change.
**Regression tests:** `tests/_private/test_doctest_module_shadowing.py`
**Normative doc:** `devguide/testing_strategy.md` ("Source-doctest collection order is a hard contract")

## Symptom

Combining direct module doctest collection with ordinary tests in one pytest
process could replace the public `molsysmt.convert` function with a module object:

```text
pytest --doctest-modules molsysmt/basic/convert.py tests/conversion_truth
```

The doctest itself passed, but ordinary tests subsequently failed at
`msm.convert(...)` with `TypeError: 'module' object is not callable`. A normal
Python import sequence and separate pytest processes retained `molsysmt.convert`
as a function.

## Root cause — the exact import sequence

`pytest.ini` sets `addopts = --doctest-modules ... --import-mode=importlib` and
`testpaths = tests molsysmt/basic`, so a plain `pytest` run collects the doctests of
`molsysmt/basic/*.py` in the same process as the functional suite.

Every public function in `molsysmt.basic` lives in a module whose file name equals
the function name and is re-exported through the package namespace:

```python
# molsysmt/basic/__init__.py
from .convert import convert          # binds molsysmt.basic.convert = <function>
```

`molsysmt.convert` is then a lazy top-level alias (`molsysmt/__init__.py`,
`_LAZY_ATTRIBUTES['convert'] = ('.basic', 'convert')`) that reads
`getattr(molsysmt.basic, 'convert')`.

When pytest collects `molsysmt/basic/convert.py` for doctests **before** anything
else imports `molsysmt.basic`, `_pytest.pathlib.import_path` (importlib mode) runs
`_import_module_using_spec('molsysmt.basic.convert', ...)`, which:

1. imports the parent package first — `molsysmt/basic/__init__.py` runs
   `from .convert import convert`, binding the **function** onto `molsysmt.basic`;
2. builds a fresh spec for `convert.py`, creates a **new** module object, overwrites
   `sys.modules['molsysmt.basic.convert']` with it, and executes it;
3. runs, **unconditionally**, `setattr(parent_module, 'convert', mod)` (pytest issue
   #12194) — replacing the re-exported function on `molsysmt.basic` with the module.

The lazy `molsysmt.__getattr__('convert')` then reads that module and caches it, so
`molsysmt.convert` is a module for the rest of the session.

`insert_missing_modules` (which has a `hasattr` guard) is **not** the culprit; the
unconditional `setattr` in `_import_module_using_spec` is.

### Why the default suite stayed green, and why it is narrow

`testpaths` lists `tests` before `molsysmt/basic`, so a normal run imports
`molsysmt` (and therefore `molsysmt.basic`) while collecting `tests/` first. By the
time the basic doctests are collected, `molsysmt.basic.convert` is already in
`sys.modules`, and `import_path` short-circuits (`if module_name in sys.modules:
return sys.modules[module_name]`) — no re-execution, no shadow. The bug only bit a
*targeted* invocation that put a basic source file first (before the suite imported
the package), and at most one symbol per run (the first-collected colliding module).

## Inventory of potentially affected symbols

The pattern is general to any `from .X import X` re-export whose source file gets
collected by `--doctest-modules` under importlib mode before the package is imported.

- **Collected today (`testpaths` includes `molsysmt/basic`):** all 23 public basic
  functions re-exported by name — `add`, `append_structures`,
  `are_multiple_molecular_systems`, `compare`, `concatenate_structures`, `contains`,
  `convert`, `copy`, `extract`, `get`, `get_attributes`, `get_form`, `get_label`,
  `has_attribute`, `info`, `is_a_molecular_system`, `is_composed_of`, `merge`,
  `remove`, `select`, `set`, `view`, `where_is_attribute`.
- **Latent, not collected today:** the same shape exists elsewhere, e.g.
  `molsysmt/build/solve_atoms_with_alternate_location.py` and
  `molsysmt/form/file_pdb/has_atoms_with_alternate_locations.py`. Those directories are
  not in `testpaths`, so `--doctest-modules` never collects them and they cannot be
  shadowed in a normal run. If they are ever added to `testpaths`, the safeguard below
  covers them automatically.

## Decision and fix

A structural library-side guarantee for *every* symbol under *every* import order is
not reasonable given Python + pytest's import model: pytest's `setattr` is
unconditional and cannot be intercepted at the subpackage namespace (the shadow lands
in the package `__dict__`, so a package-level `__getattr__` never fires). Eliminating
the collision by renaming every `basic/` module would be a large, invasive change to a
public-ish module layout used by doctests and downstream libraries, and it is
disproportionate to a test-only, non-default-invocation artifact.

Because the trigger is purely a *collection-order* property of the test harness, the
fix belongs in the test harness, not in the shipped library. The repository-root
`conftest.py` now pre-imports, in `pytest_configure` (which runs before collection),
every first-party source package listed in `testpaths`:

```python
def pytest_configure(config):
    for raw in config.getini("testpaths"):
        parts = Path(raw).parts
        if parts[:1] == ("molsysmt",) and (_ROOT / raw).is_dir():
            importlib.import_module(".".join(parts))
```

This leaves all submodules in `sys.modules` before collection, so `import_path`
short-circuits and never runs the shadowing `setattr`, regardless of collection order.
It is derived from `testpaths`, so it stays correct if more `molsysmt/*` source
directories are added. No library code changed.

## Verification

- `tests/_private/test_doctest_module_shadowing.py`:
  - an inventory assertion derived from the source modules and package exports, so a
    newly added same-name public callable cannot silently escape the regression matrix;
  - parametrized reproduction of importlib-mode collection for the colliding basic
    symbols, asserting each stays callable;
  - a subprocess running the real combined command
    (`--doctest-modules molsysmt/basic/convert.py` + a functional test that calls
    `msm.convert`), asserting exit code 0 and no `'module' object is not callable`.
- Before the fix the combined command failed with `TypeError: 'module' object is not
  callable`; after it, `78 passed`.

## Residual risk

- The safeguard depends on `testpaths` naming the source directory. A future doctest
  run that points `--doctest-modules` at a `molsysmt/*` source file **outside**
  `testpaths`, in a process that has not imported that package, could re-expose the
  shadow for that one symbol. Mitigation: keep source-doctest directories in
  `testpaths` (documented in `devguide/testing_strategy.md`).
- No production import path is affected; a normal `import molsysmt.basic.convert`
  never triggered the shadow.
