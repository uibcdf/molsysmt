import molsysmt as msm


def test_builder_add_bond_accepts_and_normalizes_declared_metadata():
    builder = msm.MolSysBuilder()
    atom_0 = builder.add_atom(atom_name="C")
    atom_1 = builder.add_atom(atom_name="O")

    builder.add_bond(atom_0, atom_1, bond_order=2, bond_type="double")

    assert builder.topology.bonds["bond_order"].tolist() == [2]
    assert "bond_type" not in builder.topology.bonds
