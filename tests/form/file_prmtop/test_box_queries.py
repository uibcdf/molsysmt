"""Checking topology box delivery against OpenMM and general periodic tools."""

import numpy as np
import pytest

import molsysmt as msm

pytest.importorskip("openmm")
puw = msm.pyunitwizard


@pytest.fixture
def prmtop():
    return msm.systems["pentalanine"]["pentalanine.prmtop"]


def test_five_box_queries_use_existing_general_geometry(prmtop):
    from openmm.app import AmberPrmtopFile

    reference = np.array(
        puw.get_value(
            AmberPrmtopFile(prmtop).topology.getPeriodicBoxVectors(), to_unit="nm"
        )
    )[None]
    box = msm.get(prmtop, box=True)
    np.testing.assert_allclose(puw.get_value(box, to_unit="nm"), reference)
    for attribute in ["box_lengths", "box_angles", "box_volume", "box_shape"]:
        actual = msm.get(prmtop, **{attribute: True})
        expected = msm.get({"box": puw.quantity(reference, "nm")}, **{attribute: True})
        if puw.is_quantity(actual):
            assert puw.get_unit(actual) == puw.get_unit(expected)
            np.testing.assert_allclose(puw.get_value(actual), puw.get_value(expected))
        else:
            np.testing.assert_equal(actual, expected)
    result = msm.get(
        prmtop,
        box=True,
        box_lengths=True,
        box_angles=True,
        box_volume=True,
        box_shape=True,
    )
    assert len(result) == 5
    assert (
        msm.get(msm.convert(prmtop, to_form="molsysmt.MolSys"), n_structures=True) == 0
    )


def test_box_selection_and_nondefault_units(prmtop):
    assert msm.get(prmtop, structure_indices=None, box=True) is None
    assert msm.get(prmtop, structure_indices=[], box=True).shape == (0, 3, 3)
    with puw.context(standard_units=["angstrom", "fs", "degree"]):
        box = msm.get(prmtop, box=True)
        assert puw.get_unit(box) == puw.get_unit(puw.quantity(1.0, "angstrom"))
        assert puw.get_value(box, to_unit="nm")[0, 0, 0] == pytest.approx(4.29511093)


def test_nonperiodic_topology_returns_no_box(prmtop, tmp_path):
    import re
    from pathlib import Path

    text = Path(prmtop).read_text()
    before, after = re.split(r"%FLAG POINTERS[^\n]*\n", text, maxsplit=1)
    pointers, tail = after.split("%FLAG", 1)
    lines = pointers.splitlines()
    values = [int(value) for line in lines[1:] for value in line.split()]
    values[27] = 0  # AMBER's documented IFBOX pointer.
    rows = [
        "".join(f"{value:8d}" for value in values[start : start + 10])
        for start in range(0, len(values), 10)
    ]
    filename = tmp_path / "nonperiodic.prmtop"
    filename.write_text(
        before
        + "%FLAG POINTERS\n"
        + lines[0]
        + "\n"
        + "\n".join(rows)
        + "\n%FLAG"
        + tail
    )
    for attribute in ["box", "box_lengths", "box_angles", "box_volume", "box_shape"]:
        assert msm.get(str(filename), **{attribute: True}) is None
