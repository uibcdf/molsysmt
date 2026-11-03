"""Keep coordinate-free chemical matching independent of structural-series reads."""

import numpy as np
import pytest
from rdkit import Chem

import molsysmt as msm


@pytest.mark.parametrize("selection", ["all", [2]])
def test_numeric_smarts_matching_does_not_read_coordinates(
    selection, tmp_path, monkeypatch
):
    from molsysmt.form import _h5msm05_modular

    source = msm.convert(Chem.MolFromSmiles("CCO"), to_form="molsysmt.MolSys")
    source.structures.append(
        coordinates=msm.pyunitwizard.quantity(np.zeros((3, 3, 3)), "nm")
    )
    path = str(tmp_path / "chemistry.h5msm")
    msm.convert(source, to_form=path)

    def reject(*args, **kwargs):
        pytest.fail(
            "Numeric SMARTS matching must not read structural arrays or analyses."
        )

    for name in (
        "read_independent_structures",
        "read_molsys_file",
        "read_named_analyses",
    ):
        monkeypatch.setattr(_h5msm05_modular, name, reject)
    result = msm.chemical_states.get_substructure_matches(
        path, "[O]", selection=selection, structure_indices=[2, 0, 2]
    )
    assert result["matches"][0].tolist() == [[2]]
    assert result["source_atom_indices"].tolist() == [0, 1, 2]
