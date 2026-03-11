import molsysmt as msm


def test_molsys_to_molsysdict_roundtrip_and_queries():

    molsys = msm.convert(msm.systems["alanine dipeptide"]["alanine_dipeptide.h5msm"], to_form="molsysmt.MolSys")
    molsys_dict = msm.convert(molsys, to_form="molsysmt.MolSysDict")

    assert msm.get(molsys_dict, element="system", n_atoms=True) == molsys.topology.n_atoms
    assert msm.get(molsys_dict, element="atom", atom_name=True) == molsys.topology.atoms["atom_name"].tolist()
    assert msm.get(molsys_dict, element="group", group_name=True) == molsys.topology.groups["group_name"].tolist()
    assert msm.get(molsys_dict, element="chain", chain_id=True) == molsys.topology.chains["chain_id"].tolist()
    assert msm.info(molsys_dict).data.loc[0, "form"] == "molsysmt.MolSysDict"

    rebuilt = msm.convert(molsys_dict, to_form="molsysmt.MolSys")

    assert rebuilt.topology.atoms["atom_name"].tolist() == molsys.topology.atoms["atom_name"].tolist()
    assert rebuilt.topology.groups["group_name"].tolist() == molsys.topology.groups["group_name"].tolist()
    assert rebuilt.topology.chains["chain_id"].tolist() == molsys.topology.chains["chain_id"].tolist()


def test_molsysdict_converts_to_molsysbuilder_without_building_fallbacks():

    builder = msm.MolSysBuilder()
    atom_index_0 = builder.add_atom(atom_name="Ar")
    atom_index_1 = builder.add_atom(atom_name="Ar")
    builder.add_group([atom_index_0], group_name="GAS")

    molsys_dict = msm.convert(builder, to_form="molsysmt.MolSysDict")
    rebuilt_builder = msm.convert(molsys_dict, to_form="molsysmt.MolSysBuilder")

    output = msm.get(
        rebuilt_builder,
        element="atom",
        atom_index=True,
        atom_name=True,
        group_index=True,
        output_type="dictionary",
    )

    assert output["atom_index"] == [0, 1]
    assert output["atom_name"] == ["Ar", "Ar"]
    assert output["group_index"] == [0, None]
    assert msm.get(rebuilt_builder, element="system", n_groups=True) == 1
    assert msm.get(rebuilt_builder, element="system", n_molecules=True) == 0


def test_molsysdict_preserves_declared_builder_truth(builder_pdb_molsys):

    molsys_dict = msm.convert(builder_pdb_molsys, to_form="molsysmt.MolSysDict")
    rebuilt = msm.convert(molsys_dict, to_form="molsysmt.MolSys")

    assert msm.get(molsys_dict, element="atom", atom_name=True) == ["N", "CA", "C", "O"]
    assert msm.get(molsys_dict, element="group", group_id=True) == ["10", "11"]
    assert msm.get(molsys_dict, element="group", group_name=True) == ["ALA", "HOH"]
    assert msm.get(molsys_dict, element="chain", chain_id=True) == ["A"]
    assert msm.get(molsys_dict, element="molecule", molecule_id=True) == ["20", "21"]
    assert msm.get(molsys_dict, element="entity", entity_id=True) == ["30", "31"]
    assert rebuilt.topology.atoms["atom_name"].tolist() == builder_pdb_molsys.topology.atoms["atom_name"].tolist()
    assert rebuilt.topology.groups["group_id"].tolist() == builder_pdb_molsys.topology.groups["group_id"].tolist()
    assert rebuilt.topology.molecules["molecule_id"].tolist() == builder_pdb_molsys.topology.molecules["molecule_id"].tolist()
