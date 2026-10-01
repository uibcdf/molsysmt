"""Protecting periodic initialization through native and form-agnostic setters."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import StructuralInconsistencyError
from molsysmt.native import MolSys, Structures


@pytest.mark.parametrize("native", [True, False])
@pytest.mark.parametrize("domain", ["structures", "molsys"])
def test_full_box_assignment_initializes_missing_series_with_units(native, domain):
    structures = Structures(coordinates=puw.quantity(np.zeros((2, 1, 3)), "nm"))
    source = structures if domain == "structures" else MolSys._from_partial_domains(structures=structures)
    matrices = np.stack((np.eye(3) * 20, np.eye(3) * 30))
    if native:
        structures.set_box(value=puw.quantity(matrices, "angstrom"))
    else:
        msm.set(source, box=puw.quantity(matrices, "angstrom"))
    assert structures.box is not None
    np.testing.assert_allclose(puw.get_value(msm.get(source, box=True), to_unit="nm"), matrices / 10)
    assert not structures._box.flags.writeable
    assert structures.n_structures == 2


def test_partial_missing_box_assignment_fails_without_claiming_success():
    structures = Structures(coordinates=puw.quantity(np.zeros((2, 1, 3)), "nm"))
    with pytest.raises(StructuralInconsistencyError, match="full box series"):
        msm.set(structures, structure_indices=[1], box=puw.quantity([np.eye(3)], "nm"))
    assert structures.box is None
    msm.set(structures, box=puw.quantity(np.repeat(np.eye(3)[None], 2, axis=0), "nm"))
    msm.set(structures, structure_indices=[1], box=puw.quantity([np.eye(3) * 3], "nm"))
    np.testing.assert_allclose(puw.get_value(structures.box, to_unit="nm"), [np.eye(3), np.eye(3) * 3])
