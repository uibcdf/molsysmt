"""Repository-wide pytest collection safeguards."""

import importlib
from pathlib import Path

_ROOT = Path(__file__).parent


def _guard_xdist_warning_reconstruction():
    """Stop xdist re-rendering a catalog warning when it crosses to the controller.

    ``pytest_warning_recorded`` fires on the worker; xdist serializes the warning
    and the controller rebuilds it as ``cls(*message_args)``, where
    ``message_args`` is the original's ``.args``. ``CatalogWarning.__init__`` ends
    in ``super().__init__(full_message)``, so that tuple is the *rendered* text —
    and our subclasses take a domain field first positionally. The controller
    therefore calls ``UnknownAtomNameWarning("Atom name 'Ar' is not ...")``, the
    text lands in ``atom_name``, and the catalog template wraps its own output a
    second time. Subclasses that reject the call fall back to a generic
    ``Warning("module.Class: msg")``, and subclasses whose parameters all have
    defaults rebuild quietly with the *default* message, which is wrong without
    looking wrong.

    Keep the reconstruction only when it round-trips. The worker already computed
    the correct text, and ``category`` is rebuilt upstream from its own fields, so
    the real class survives regardless. With this in place a ``-n 12`` run reports
    exactly what a serial run reports.

    Reporting only: the emitted diagnostics are correct either way. Remove once a
    released pytest-xdist no longer rebuilds warnings this way. See
    ``devguide/pending_bugs/xdist_re_renders_catalog_warnings_on_the_controller.md``.
    """
    try:
        import xdist.workermanage as workermanage
    except ImportError:  # running without xdist
        return
    if getattr(workermanage, "_molsysmt_warning_roundtrip_guard", False):
        return

    original = workermanage.unserialize_warning_message

    def guarded(data):
        message = original(data)
        expected = data.get("message_str")
        if expected is not None and str(message.message) != expected:
            message.message = Warning(expected)
        return message

    workermanage.unserialize_warning_message = guarded
    workermanage._molsysmt_warning_roundtrip_guard = True


_guard_xdist_warning_reconstruction()


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
