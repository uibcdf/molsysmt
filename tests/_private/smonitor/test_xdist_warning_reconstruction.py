"""The contract around xdist rebuilding catalog warnings on the controller.

This is the guard for `uibcdf/molsysmt#158`: it fails if the doubled text ever
comes back, whether because a new warning class is written in a shape that
defeats the round trip, or because the base class starts transforming its
message again.

A second test lived here until the fix landed, whose job was to fail the day the
workaround in `conftest.py` became unnecessary. It did exactly that, and both it
and the workaround are gone.
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
