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
