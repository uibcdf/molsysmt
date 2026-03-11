import molsysmt as msm


def test_edit_returns_a_builder_from_existing_molsys():

    molsys = msm.convert(msm.systems["alanine dipeptide"]["alanine_dipeptide.h5msm"], to_form="molsysmt.MolSys")

    builder = msm.build.edit(molsys)

    assert isinstance(builder, msm.MolSysBuilder)
    assert builder.n_atoms == molsys.topology.n_atoms
    assert builder.n_groups == molsys.topology.n_groups
    assert builder.n_molecules == molsys.topology.n_molecules


def test_edit_accepts_non_native_forms_via_conversion():

    builder = msm.build.edit(msm.systems["alanine dipeptide"]["alanine_dipeptide.h5msm"])
    rebuilt = builder.build()

    assert isinstance(builder, msm.MolSysBuilder)
    assert msm.get_form(rebuilt) == "molsysmt.MolSys"
    assert rebuilt.topology.n_atoms > 0
