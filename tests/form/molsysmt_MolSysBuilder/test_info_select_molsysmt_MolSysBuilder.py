import molsysmt as msm


def test_info_reports_declared_builder_state(molsys_builder_complete):

    output = msm.info(molsys_builder_complete).data

    assert output.loc[0, "form"] == "molsysmt.MolSysBuilder"
    assert output.loc[0, "n_atoms"] == 3
    assert output.loc[0, "n_groups"] == 2
    assert output.loc[0, "n_molecules"] == 2
    assert output.loc[0, "n_entities"] == 2
    assert output.loc[0, "n_structures"] == 1


def test_select_operates_on_declared_builder_state(molsys_builder_complete, molsys_builder_partial):

    assert msm.select(molsys_builder_complete, selection='group_name=="ALA"') == [0, 1]
    assert msm.select(molsys_builder_complete, element="group", selection='group_name=="ALA"') == [0]
    assert msm.select(molsys_builder_complete, element="molecule", selection='molecule_type=="water"') == [1]
    assert msm.select(molsys_builder_partial, selection='group_index==0') == [0, 1]
