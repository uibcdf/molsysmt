"""Check coupled atom axes against literal coordinates, not converter parity."""

import numpy as np
import pytest

import molsysmt as msm


@pytest.mark.parametrize("form", ["rdkit", "mdtraj"])
def test_nonconsecutive_native_subset_keeps_labels_chemistry_and_geometry_aligned(form):
    if form == "rdkit":
        Chem = pytest.importorskip("rdkit.Chem")
        source = Chem.MolFromSmiles("OCN")
        conformer = Chem.Conformer(3)
        for index, x in enumerate([10.0, 20.0, 30.0]):
            conformer.SetAtomPosition(index, (x, 0.0, 0.0))
        source.AddConformer(conformer)
    else:
        md = pytest.importorskip("mdtraj")
        topology = md.Topology()
        chain = topology.add_chain()
        group = topology.add_residue("LIG", chain)
        atoms = [
            topology.add_atom(symbol, md.element.get_by_symbol(symbol), group)
            for symbol in ["O", "C", "N"]
        ]
        topology.add_bond(atoms[0], atoms[1])
        topology.add_bond(atoms[1], atoms[2])
        source = md.Trajectory(
            np.asarray([[[1.0, 0.0, 0.0], [2.0, 0.0, 0.0], [3.0, 0.0, 0.0]]]), topology
        )
    result = msm.convert(source, to_form="molsysmt.MolSys", selection=[2, 0])
    assert result.get(element="atom", atom_type=True) == ["O", "N"]
    assert result.get(bonded_atom_pairs=True) == []
    assert result.chemical_states.n_atoms == 2
    coordinates = msm.pyunitwizard.get_value(
        result.structures.coordinates, to_unit="nm"
    )
    np.testing.assert_allclose(coordinates, [[[1.0, 0.0, 0.0], [3.0, 0.0, 0.0]]])
