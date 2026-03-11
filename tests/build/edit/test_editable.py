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
