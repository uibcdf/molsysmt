"""Keep native and same-form trajectory projections on coherent axes."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw


@pytest.mark.parametrize("target", ["molsysmt.MolSys", "mdtraj.Trajectory"])
@pytest.mark.parametrize("length,time", [("nm", "ps"), ("pm", "fs")])
def test_unique_atom_selection_keeps_inventory_and_coordinate_axes(
    mdtraj_selection_ensemble, target, length, time
):
    source = mdtraj_selection_ensemble
    before = source.xyz.copy()
    with puw.context(standard_units=[length, time, "radians"]):
        result = msm.convert(
            source, to_form=target, selection=[3, 1], structure_indices=[2, 0, 2]
        )
        if target == "molsysmt.MolSys":
            assert result.topology.n_atoms == 2
            xyz = puw.get_value(result.structures.coordinates, to_unit="nm")
            times = puw.get_value(result.structures.time, to_unit="ps")
        else:
            assert result.n_atoms == 2
            xyz, times = result.xyz, result.time
        np.testing.assert_array_equal(xyz, source.xyz[[2, 0, 2]][:, [1, 3]])
        np.testing.assert_allclose(times, [9, 1, 9], rtol=0, atol=1e-12)
    np.testing.assert_array_equal(source.xyz, before)
