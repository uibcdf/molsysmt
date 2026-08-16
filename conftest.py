"""Repository-wide pytest collection safeguards."""

import importlib
import warnings
from pathlib import Path

import pytest

_ROOT = Path(__file__).parent

#: Verdict of the xdist probe, taken once per process before the guard
#: patches anything. `None` until `pytest_configure` has run.
_XDIST_RE_RENDERS = None


def xdist_re_renders_warnings():
    """Ask the installed xdist whether it still rebuilds warnings by re-rendering.

    Returns ``True`` when it does, ``False`` when it does not, and ``None`` when
    the question could not be put — xdist absent, or its internals moved.

    The question is asked of the behaviour, not of the output, because the output
    does not answer it. Our guard normalises the text either way, so a fixed xdist
    and a broken one look identical downstream; watching the report would never
    reveal that the workaround had outlived its cause.

    A real catalog warning is used as the probe rather than a synthetic one: it is
    importable by the module path xdist marshals, and it has exactly the shape that
    breaks — a domain field where the message is expected. Re-rendering is then
    distinguishable from every other outcome by the *type* that comes back:

    ==========================================  ===========================
    ``cls(*args)`` rebuilds and the text grows  the defect — returns True
    the rebuild is refused, generic ``Warning``  fixed, or never applied
    the text survives unchanged                  fixed
    ==========================================  ===========================
    """
    try:
        from xdist.remote import serialize_warning_message
        from xdist.workermanage import unserialize_warning_message
    except ImportError:  # no xdist, or the entry points moved
        return None

    try:
        from molsysmt._private.smonitor import UnknownAtomNameWarning

        probe = UnknownAtomNameWarning(atom_name="Ar")
        original_text = str(probe)
        carrier = warnings.WarningMessage(
            message=probe, category=type(probe), filename=__file__, lineno=0
        )
        rebuilt = unserialize_warning_message(serialize_warning_message(carrier)).message
    except Exception:
        return None

    return isinstance(rebuilt, UnknownAtomNameWarning) and str(rebuilt) != original_text


def _guard_xdist_warning_reconstruction():
    """Stop xdist re-rendering a catalog warning when it crosses to the controller.

    ``pytest_warning_recorded`` fires on the worker; xdist serializes the warning
    and the controller rebuilds it as ``cls(*message_args)``, where ``message_args``
    is the original's ``.args``. ``CatalogWarning.__init__`` ends in
    ``super().__init__(full_message)``, so that tuple is the *rendered* text — and
    our subclasses take a domain field first positionally. The controller therefore
    calls ``UnknownAtomNameWarning("Atom name 'Ar' is not ...")``, the text lands in
    ``atom_name``, and the catalog template wraps its own output a second time.

    Keep the reconstruction only when it round-trips. The worker already computed
    the correct text, and ``category`` is rebuilt upstream from its own fields, so
    the real class survives regardless. With this in place a ``-n 12`` run reports
    exactly what a serial run reports.

    The guard installs itself only while the defect is present.
    ``test_the_xdist_workaround_is_still_needed`` fails the day it stops being, which
    is the only reminder that cannot be scrolled past. A fix is proposed as
    ``pytest-dev/pytest-xdist#1372``, but this waits on the behaviour rather than on
    that pull request: any fix, backport or replacement retires it. See
    ``devguide/pending_bugs/xdist_re_renders_catalog_warnings_on_the_controller.md``.
    """
    try:
        import xdist.workermanage as workermanage
    except ImportError:  # running without xdist
        return
    if getattr(workermanage, "_molsysmt_warning_roundtrip_guard", False):
        return

    global _XDIST_RE_RENDERS
    _XDIST_RE_RENDERS = xdist_re_renders_warnings()
    if _XDIST_RE_RENDERS is False:
        # Retirement is announced by `test_the_xdist_workaround_is_still_needed`,
        # not from here: a warning raised during `pytest_configure` is emitted
        # before pytest installs its capture and never reaches the report.
        return
    # `None` keeps the guard: unable to tell is not the same as known to be fixed,
    # and the guard costs nothing when it turns out to be unnecessary.

    original = workermanage.unserialize_warning_message

    def guarded(data):
        message = original(data)
        expected = data.get("message_str")
        if expected is not None and str(message.message) != expected:
            message.message = Warning(expected)
        return message

    workermanage.unserialize_warning_message = guarded
    workermanage._molsysmt_warning_roundtrip_guard = True


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

    # After the pre-imports: the probe builds a real catalog warning, so it needs
    # the package. Still long before any warning can cross to the controller.
    _guard_xdist_warning_reconstruction()


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


@pytest.fixture(scope="session")
def xdist_re_renders_warnings_verdict():
    """Whether the installed xdist re-rendered warnings, measured before patching.

    Taken in `pytest_configure`, because by the time a test runs the guard has
    replaced `unserialize_warning_message` and asking again would measure the
    workaround instead of the defect.
    """
    return _XDIST_RE_RENDERS
