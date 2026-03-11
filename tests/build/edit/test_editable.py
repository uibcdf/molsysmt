import molsysmt as msm


def test_editable_returns_a_builder_from_existing_molsys():

    molsys = msm.convert(msm.systems["alanine dipeptide"]["alanine_dipeptide.h5msm"], to_form="molsysmt.MolSys")

    builder = msm.build.editable(molsys)

    assert isinstance(builder, msm.MolSysBuilder)
    assert builder.n_atoms == molsys.topology.n_atoms
    assert builder.n_groups == molsys.topology.n_groups
    assert builder.n_molecules == molsys.topology.n_molecules


def test_editable_accepts_non_native_forms_via_conversion():

    builder = msm.build.editable(msm.systems["alanine dipeptide"]["alanine_dipeptide.h5msm"])
    rebuilt = builder.build()

    assert isinstance(builder, msm.MolSysBuilder)
    assert msm.get_form(rebuilt) == "molsysmt.MolSys"
    assert rebuilt.topology.n_atoms > 0


def test_editable_without_input_returns_an_empty_builder():

    builder = msm.build.editable()

    assert isinstance(builder, msm.MolSysBuilder)
    assert builder.n_atoms == 0
    assert builder.n_groups == 0
    assert builder.n_molecules == 0


def test_editable_supports_declared_topology_edits_before_build():

    builder = msm.build.editable(msm.systems["T4 lysozyme L99A"]["181l.h5msm"])
    original_n_bonds = builder.n_bonds

    builder.remove_bonds([0])
    water_group_indices = msm.select(
        builder,
        element="group",
        selection='group_type=="water"',
        syntax="MolSysMT",
    )
    builder.assign_groups_to_new_chain(water_group_indices, chain_id="W", chain_name="waters", chain_type="water")
    rebuilt = builder.build()

    assert builder.n_bonds == original_n_bonds - 1
    assert "W" in rebuilt.topology.chains["chain_id"].tolist()
    assert rebuilt.topology.n_bonds == original_n_bonds - 1
