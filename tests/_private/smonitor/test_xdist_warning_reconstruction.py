"""The contract around xdist rebuilding catalog warnings on the controller.

Two things are held here, and they retire in opposite directions.

`test_catalog_warnings_are_not_re_rendered` is the guard for
`uibcdf/molsysmt#158`: it fails if the doubled text ever comes back, whether the
workaround in `conftest.py` is removed too early or a new warning class is
written in a shape that defeats it.

`test_the_xdist_workaround_is_still_needed` is the opposite, and deliberately so.
It fails the day pytest-xdist stops re-rendering, because that is the day the
workaround becomes dead code. A warning would be scrolled past — the suite already
reports around 130 of them — and nobody polls a pull request for months. A red
test with the removal steps in its message is the one reminder that cannot be
missed, and the failure is good news.
"""

import warnings

import pytest

from molsysmt._private.smonitor import UnknownAtomNameWarning

xdist_remote = pytest.importorskip("xdist.remote")
xdist_workermanage = pytest.importorskip("xdist.workermanage")


def _round_trip(instance):
    """Marshal a warning the way xdist does between worker and controller."""
    carrier = warnings.WarningMessage(
        message=instance, category=type(instance), filename=__file__, lineno=0
    )
    data = xdist_remote.serialize_warning_message(carrier)
    return xdist_workermanage.unserialize_warning_message(data).message


def test_catalog_warnings_are_not_re_rendered():
    """A catalog warning crossing to the controller must not render twice.

    `UnknownAtomNameWarning.__init__` takes `atom_name`, and `.args` carries the
    rendered sentence, so a naive `cls(*args)` puts the sentence into `atom_name`
    and the template wraps it again.
    """
    probe = UnknownAtomNameWarning(atom_name="Ar")
    original = str(probe)
    assert original.count("is not recognized") == 1

    rebuilt = str(_round_trip(probe))

    assert "Ar" in rebuilt
    assert rebuilt.count("is not recognized") == 1, rebuilt


def test_the_xdist_workaround_is_still_needed(xdist_re_renders_warnings_verdict):
    """Fails when pytest-xdist no longer needs the guard. That is the point.

    The verdict is taken in `pytest_configure`, before the guard patches
    `unserialize_warning_message`; asking here would measure the workaround.
    """
    if xdist_re_renders_warnings_verdict is None:
        pytest.skip("could not determine how this pytest-xdist rebuilds warnings")

    assert xdist_re_renders_warnings_verdict, (
        "pytest-xdist no longer re-renders warnings on the controller, so the "
        "workaround is obsolete. Remove `_guard_xdist_warning_reconstruction`, "
        "`xdist_re_renders_warnings` and the `xdist_re_renders_warnings_verdict` "
        "fixture from conftest.py, delete this test, close uibcdf/molsysmt#158, "
        "and archive devguide/pending_bugs/"
        "xdist_re_renders_catalog_warnings_on_the_controller.md.\n"
        "Reported warning text will then carry xdist's 'module.Class: ' prefix. "
        "That is xdist's own choice for a warning it cannot faithfully rebuild, "
        "and correcting it would be a formatting preference, not a defect fix. "
        "`test_catalog_warnings_are_not_re_rendered` stays either way."
    )
