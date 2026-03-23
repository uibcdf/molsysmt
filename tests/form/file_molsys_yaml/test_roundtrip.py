import molsysmt as msm


def test_molsys_yaml_roundtrip_from_molsys(tmp_path):

    molsys = msm.convert(msm.systems["alanine dipeptide"]["alanine_dipeptide.h5msm"], to_form="molsysmt.MolSys")
    output = tmp_path / "alanine.yaml"

    msm.convert(molsys, to_form="file:molsys_yaml", output_filename=str(output))

    assert output.exists()
    assert msm.get_form(str(output)) == "file:molsys_yaml"

    molsys_dict = msm.convert(str(output), to_form="molsysmt.MolSysDict")
    rebuilt = msm.convert(str(output), to_form="molsysmt.MolSys")

    assert msm.info(str(output)).data.loc[0, "form"] == "file:molsys_yaml"
    assert msm.get(str(output), element="system", n_atoms=True) == molsys.topology.n_atoms
    assert msm.get(molsys_dict, element="system", n_atoms=True) == molsys.topology.n_atoms
    assert msm.get(molsys_dict, element="atom", atom_name=True) == molsys.topology.atoms["atom_name"].tolist()
    assert rebuilt.topology.atoms["atom_name"].tolist() == molsys.topology.atoms["atom_name"].tolist()
    assert rebuilt.topology.groups["group_name"].tolist() == molsys.topology.groups["group_name"].tolist()


def test_molsys_yaml_preserves_declared_builder_truth(builder_pdb_molsys, tmp_path):

    output = tmp_path / "builder_fixture.yaml"
    msm.convert(builder_pdb_molsys, to_form="file:molsys_yaml", output_filename=str(output))

    molsys_dict = msm.convert(str(output), to_form="molsysmt.MolSysDict")
    rebuilt = msm.convert(str(output), to_form="molsysmt.MolSys")

    assert msm.get(molsys_dict, element="atom", atom_name=True) == ["N", "CA", "C", "O"]
    assert msm.get(molsys_dict, element="group", group_name=True) == ["ALA", "HOH"]
    assert msm.get(molsys_dict, element="chain", chain_id=True) == ["A"]
    assert msm.get(molsys_dict, element="molecule", molecule_name=True) == ["protein 0", "water"]
    assert rebuilt.topology.bonds[["atom1_index", "atom2_index"]].values.tolist() == (
        builder_pdb_molsys.topology.bonds[["atom1_index", "atom2_index"]].values.tolist()
    )
