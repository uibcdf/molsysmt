"""Regression: doctest collection must not shadow re-exported public symbols.

Every public function in ``molsysmt.basic`` lives in a module whose file name equals
the function name (``molsysmt/basic/convert.py`` -> ``convert``) and is re-exported via
``from .convert import convert``. Under pytest's ``--import-mode=importlib`` (the mode
configured in ``pytest.ini``), collecting one of those source files for
``--doctest-modules`` *before* anything else imports the package makes pytest
re-execute the file as a fresh module and unconditionally run
``setattr(parent, 'convert', <module>)`` (pytest issue #12194). That replaces the
callable on the package namespace with the module object, so ``molsysmt.convert`` then
resolves to a module and every subsequent ``msm.convert(...)`` fails with
``TypeError: 'module' object is not callable``.

The fix is a pure test-tooling one: the repository-root ``conftest.py`` pre-imports the
first-party source packages listed in ``testpaths`` in ``pytest_configure``, so all
their submodules are already in ``sys.modules`` and pytest's own ``import_path``
short-circuit skips the shadowing re-execution. These tests pin both the low-level
import sequence and the real combined doctest-plus-tests command in a subprocess.

See ``devguide/archive/resolved_bugs/doctest_module_collection_can_shadow_public_convert.md``.
"""

import subprocess
import sys
import types
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

# Public basic functions whose module file name equals the re-exported symbol.
COLLIDING_BASIC_SYMBOLS = [
    "add",
    "append_structures",
    "are_multiple_molecular_systems",
    "compare",
    "concatenate_structures",
    "contains",
    "convert",
    "copy",
    "extract",
    "get",
    "get_attributes",
    "get_form",
    "get_label",
    "has_attribute",
    "info",
    "is_a_molecular_system",
    "is_composed_of",
    "merge",
    "remove",
    "select",
    "set",
    "view",
    "where_is_attribute",
]


def _simulate_first_collection(module_stem):
    """Reproduce pytest importlib-mode collection of a single basic source file.

    Returns the freshly resolved ``molsysmt.<module_stem>`` public symbol after the
    root-conftest safeguard has run, so the test asserts the symbol stays callable.
    """
    import_path = pytest.importorskip("_pytest.pathlib").import_path
    ImportMode = pytest.importorskip("_pytest.pathlib").ImportMode

    # The root conftest safeguard: pre-import the source package before collection.
    import molsysmt.basic  # noqa: F401

    import_path(
        REPO_ROOT / f"molsysmt/basic/{module_stem}.py",
        mode=ImportMode.importlib,
        root=REPO_ROOT,
        consider_namespace_packages=False,
    )

    import molsysmt as msm

    return getattr(msm, module_stem)


def test_colliding_basic_symbol_inventory_is_complete():
    """Every public callable sharing its module name is in the regression matrix."""
    import molsysmt.basic as basic

    module_stems = {
        path.stem
        for path in (REPO_ROOT / "molsysmt/basic").glob("*.py")
        if not path.stem.startswith("_")
    }
    colliding_symbols = sorted(
        stem for stem in module_stems if callable(getattr(basic, stem, None))
    )

    assert COLLIDING_BASIC_SYMBOLS == colliding_symbols


@pytest.mark.parametrize("module_stem", COLLIDING_BASIC_SYMBOLS)
def test_basic_symbol_survives_doctest_style_collection(module_stem):
    """After importlib-mode collection of its own module, the symbol stays callable."""
    resolved = _simulate_first_collection(module_stem)
    assert not isinstance(resolved, types.ModuleType), (
        f"molsysmt.{module_stem} was shadowed by its module during doctest collection"
    )
    assert callable(resolved)


def test_combined_doctests_and_tests_keep_convert_callable(tmp_path):
    """The real combined command runs green, proving the conftest safeguard works.

    The temporary test file forces ``molsysmt/basic/convert.py`` to be collected first
    (the order that used to install the module object on ``molsysmt.convert``) and then
    exercises the public ``msm.convert`` facade in the same process.
    """
    functional_test = tmp_path / "test_convert_facade_is_callable.py"
    functional_test.write_text(
        "import molsysmt as msm\n"
        "\n"
        "def test_public_convert_is_callable():\n"
        "    assert callable(msm.convert)\n"
        "    from molsysmt.native import Topology\n"
        "    topology = Topology(n_atoms=1)\n"
        "    converted = msm.convert(topology, to_form='molsysmt.TopologyDict')\n"
        "    assert msm.get_form(converted) == 'molsysmt.TopologyDict'\n"
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "--doctest-modules",
            "molsysmt/basic/convert.py",
            str(functional_test),
            "-p",
            "no:cacheprovider",
            "-q",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, (
        "combined doctest + test command failed; public convert was likely shadowed:\n"
        f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    )
    assert "module' object is not callable" not in result.stdout
