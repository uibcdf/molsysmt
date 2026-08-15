"""Cross-repo unit-policy authority tests.

The MolSysSuite libraries share one PyUnitWizard kernel inside a process, and
each configures it from its own ``_pyunitwizard.py``, which runs on first
import. Before the shared-policy rule, the last import won and the four did not
agree: the same call returned ``1.0 radian`` or ``57.3 degree`` depending on
which library was imported first, and a later first-import silently undid a
choice the user had already made.

These run in subprocesses because import order is only observable once per
interpreter: ``sys.modules`` caches the first import, so a single process
cannot exercise a second ordering.

They import ``<library>._pyunitwizard`` rather than the package, because that
submodule is where configuration happens and several suite libraries reach it
lazily -- ``import molsysmt`` alone configures nothing. That laziness is the
reason ordering is hard to reason about in a notebook, and the reason these
tests pin it.
"""

import subprocess
import sys

import pytest


SUITE_LIBRARIES = ["molsysmt", "molsysviewer", "topomt", "pharmacophoremt"]


def _run(body):
    """Execute `body` in a fresh interpreter and return its stripped stdout."""
    result = subprocess.run(
        [sys.executable, "-c", body],
        capture_output=True,
        text=True,
        timeout=600,
    )
    assert result.returncode == 0, result.stderr[-2000:]
    return result.stdout.strip()


def _importable(library):
    return (
        subprocess.run(
            [sys.executable, "-c", f"import {library}._pyunitwizard"],
            capture_output=True,
        ).returncode
        == 0
    )


AVAILABLE = [library for library in SUITE_LIBRARIES if _importable(library)]


PROBE = """
import warnings; warnings.filterwarnings('ignore')
{imports}
import pyunitwizard as puw
print(puw.to_string(puw.standardize(puw.quantity(1.0, 'radian'))))
print(puw.to_string(puw.standardize(puw.quantity(1.0, 'kJ/mol'))))
print(puw.to_string(puw.standardize(puw.quantity(1.0, 'dalton'))))
"""


# The shared policy, stated absolutely. Comparing orderings against each other
# is not enough: a library that imposes its own policy in *every* ordering makes
# them all agree with one another and disagree with the suite.
SHARED_POLICY_RESULTS = ["1.0 radian", "1.0 kilojoule / mole", "1.0 dalton"]


@pytest.mark.skipif(len(AVAILABLE) < 2, reason="Needs two suite libraries installed")
@pytest.mark.parametrize("first", AVAILABLE)
def test_any_import_order_yields_the_shared_policy(first):
    """Whichever suite library is imported first, the shared policy is what applies."""
    others = [library for library in AVAILABLE if library != first]
    ordering = [first] + others

    results = _run(
        PROBE.format(imports="\n".join(f"import {lib}._pyunitwizard" for lib in ordering))
    ).splitlines()

    assert results == SHARED_POLICY_RESULTS, (
        f"importing {' then '.join(ordering)} did not produce the shared policy:\n"
        f"{results}\nagainst\n{SHARED_POLICY_RESULTS}"
    )


@pytest.mark.skipif(not AVAILABLE, reason="No suite library installed")
def test_a_suite_library_declares_the_shared_policy():
    """The declared policy is the shared one, whoever declares it."""
    report = _run(
        f"""
import warnings; warnings.filterwarnings('ignore')
import {AVAILABLE[0]}._pyunitwizard
import pyunitwizard as puw
report = puw.configure.report()
print(report['default_form'])
print(report['provenance'])
print(','.join(report['standard_units']))
"""
    ).splitlines()

    assert report[0] == "pint"
    assert report[1] in AVAILABLE
    standard_units = report[2].split(",")
    assert "nm" in standard_units
    assert "radians" in standard_units
    assert "dalton" in standard_units


@pytest.mark.skipif(len(AVAILABLE) < 2, reason="Needs two suite libraries installed")
def test_a_later_import_does_not_undo_the_user_choice():
    """A user's policy outranks any library imported afterwards.

    This is the failure mode a shared policy alone does not fix: the libraries
    agreeing with each other says nothing about them agreeing with the user.
    """
    first, second = AVAILABLE[0], AVAILABLE[1]

    output = _run(
        f"""
import warnings; warnings.filterwarnings('ignore')
import {first}._pyunitwizard
import pyunitwizard as puw

puw.configure.add_standard_units(['angstrom'])
chosen = puw.to_string(puw.standardize(puw.quantity(1.0, 'meter')))

import {second}._pyunitwizard
after = puw.to_string(puw.standardize(puw.quantity(1.0, 'meter')))

print(chosen)
print(after)
"""
    ).splitlines()

    assert "angstrom" in output[0]
    assert output[1] == output[0], (
        f"importing {second} undid the user's choice: {output[1]} instead of {output[0]}"
    )
