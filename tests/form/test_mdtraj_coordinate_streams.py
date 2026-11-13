"""Check provider coordinate streams against a small known ensemble."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw


@pytest.mark.parametrize("suffix", ["dcd", "xtc"])
@pytest.mark.parametrize("length,time", [("nm", "ps"), ("pm", "fs")])
def test_coordinate_stream_preserves_selected_geometry(
    tmp_path, mdtraj_selection_ensemble, suffix, length, time
):
    import mdtraj as md

    path = tmp_path / ("ensemble." + suffix)
    getattr(mdtraj_selection_ensemble, "save_" + suffix)(str(path))
    units = [
        length if u == "nm" else time if u == "ps" else u
        for u in puw.configure.get_standard_units()
    ]
    with md.open(str(path), mode="r") as reader, puw.context(standard_units=units):
        blocks = [
            dict(block)
            for block in msm.Iterator(
                reader,
                selection=[1, 3],
                structure_indices=[4, 0, 4],
                chunk=2,
                output_type="dictionary",
                coordinates=True,
                box=True,
            )
        ]
        assert [b["coordinates"].shape for b in blocks] == [(2, 2, 3), (1, 2, 3)]
        xyz = np.concatenate(
            [puw.get_value(b["coordinates"], to_unit="nm") for b in blocks]
        )
        box = np.concatenate([puw.get_value(b["box"], to_unit="nm") for b in blocks])
        np.testing.assert_allclose(
            xyz, mdtraj_selection_ensemble.xyz[[4, 0, 4]][:, [1, 3]], rtol=0, atol=1e-5
        )
        np.testing.assert_allclose(
            box,
            mdtraj_selection_ensemble.unitcell_vectors[[4, 0, 4]],
            rtol=0,
            atol=1e-5,
        )
        assert str(puw.get_unit(blocks[0]["coordinates"])) == str(puw.unit(length))
