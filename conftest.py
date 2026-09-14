"""Repository-wide pytest collection safeguards."""

import importlib
from pathlib import Path

_ROOT = Path(__file__).parent


def pytest_configure(config):
    """Pre-import first-party source packages collected for ``--doctest-modules``.

    Every public function in packages such as ``molsysmt.basic`` lives in a module
    whose file name equals the function name (``molsysmt/basic/convert.py`` ->
    ``convert``) and is re-exported via ``from .convert import convert``. Under
    pytest's ``--import-mode=importlib``, collecting one of those source files for
    ``--doctest-modules`` *before* anything else imports the package makes pytest
    re-execute the file as a fresh module and unconditionally run
    ``setattr(parent, 'convert', <module>)`` (pytest issue #12194), replacing the
    re-exported callable on the package namespace with the module object. The public
    ``molsysmt.convert`` symbol then resolves to a module and raises
    ``TypeError: 'module' object is not callable`` for the rest of the session.

    Importing each first-party source package here, before collection starts, leaves
    all of its submodules in ``sys.modules`` so pytest's own ``import_path``
    short-circuit (``if module_name in sys.modules: return``) skips the re-execution
    and its shadowing ``setattr``. The re-exports stay callable regardless of doctest
    collection order, so the combined documentation-and-test gate is safe. This is a
    test-tooling fix and touches no library code. The set is derived from ``testpaths``
    so it stays correct automatically if more ``molsysmt/*`` source directories are
    later added. See
    ``devguide/archive/resolved_bugs/doctest_module_collection_can_shadow_public_convert.md``.
    """
    for raw in config.getini("testpaths"):
        parts = Path(raw).parts
        if parts[:1] == ("molsysmt",) and (_ROOT / raw).is_dir():
            importlib.import_module(".".join(parts))


# These developer command-line utilities are executable scripts rather than
# import-safe doctest modules. Their dedicated tests exercise the reusable
# validators without importing argument-parsing entry points.
collect_ignore = [
    "devtools/tests/coverage_by_package.py",
    "devtools/tests/coverage_check.py",
    "devtools/tests/coverage_diff.py",
    "devtools/tests/coverage_history.py",
    "devtools/tests/coverage_hotspots.py",
    "devtools/tests/coverage_map.py",
    "devtools/tests/coverage_markdown.py",
    "devtools/tests/coverage_utils.py",
    "devtools/tests/module_test_map.py",
]
