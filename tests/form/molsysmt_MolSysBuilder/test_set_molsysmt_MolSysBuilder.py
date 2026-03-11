import numpy as np

import molsysmt as msm
from molsysmt import pyunitwizard as puw


def test_set_declared_topological_and_structural_attributes(molsys_builder_complete):

    msm.set(molsys_builder_complete, element="atom", selection=[0], atom_name="X")
    msm.set(molsys_builder_complete, element="group", selection=[0], group_name="GLY")
    msm.set(molsys_builder_complete, element="chain", selection=[0], chain_name="B")
    msm.set(
        molsys_builder_complete,
        coordinates=puw.quantity(
            np.array(
                [
                    [[1.0, 0.0, 0.0], [1.1, 0.0, 0.0], [1.2, 0.0, 0.0]],
                ]
            ),
            "nm",
        ),
        box=puw.quantity(np.ones((1, 3, 3)), "nm"),
        time=puw.quantity(np.array([2.0]), "ps"),
        structure_id=[7],
    )

    output = msm.get(
        molsys_builder_complete,
        element="atom",
        atom_name=True,
        output_type="dictionary",
    )

    assert output["atom_name"] == ["X", "CA", "O"]
    assert msm.get(molsys_builder_complete, element="group", group_name=True) == ["GLY", "HOH"]
    assert msm.get(molsys_builder_complete, element="chain", chain_name=True) == ["B"]
    assert np.allclose(
        puw.get_value(msm.get(molsys_builder_complete, element="system", coordinates=True), to_unit="nm"),
        np.array([[[1.0, 0.0, 0.0], [1.1, 0.0, 0.0], [1.2, 0.0, 0.0]]]),
    )
    assert puw.get_value(msm.get(molsys_builder_complete, element="system", time=True), to_unit="ps").tolist() == [2.0]
    assert msm.get(molsys_builder_complete, element="system", structure_id=True) == ["7"]
